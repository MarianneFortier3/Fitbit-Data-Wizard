# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:06:35 2023

@author: Marianne
"""

# Fonctions pour extraire les données des montres

import pandas as pd
from pandas.tseries.offsets import DateOffset
import numpy as np
import os
import sys
from datetime import datetime, timedelta

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Find the files starting with the keyword
def find_json_files(file_list, keyword, dates):
    matched_files = []
    for d in dates:
        try:
            for f in file_list:
                if f.startswith(keyword+'-'+d):
                    matched_files.append(f)
        except:
            pass
    matched_files = np.array(matched_files).flatten()
    
    return(matched_files)

# Extract active zones
def open_and_concat_active(data_path,file_list,keyword,birth_year,startDate,endDate):
    
    to_concat = []
    
    if len(file_list) != 0:
    
        for f in file_list:
            df = pd.read_json(data_path+f)
            values = pd.DataFrame.from_records(df['value'].values)
            df.drop(labels='value',axis=1,inplace=True)
            df['bpm']=values['bpm']
            
            df.set_index('dateTime',inplace=True)
            df.rename(columns={'value':keyword},inplace=True)
            
            to_concat.append(df)
            
        original = pd.concat(to_concat)
        original = original.loc[startDate:endDate-timedelta(seconds=1)]
        result = original.resample('1min').mean()
        result['écart-type'] = original.resample('1min').std(ddof=0)

        fcm = 220 - (datetime.now().year - int(birth_year))
        result['zone'] = None
        result['zone'].loc[result['bpm']<0.5*fcm] = 'sédentaire'
        result['zone'].loc[(result['bpm']>=0.5*fcm) & (result['bpm']<0.7*fcm)] = 'légère'
        result['zone'].loc[(result['bpm']>=0.7*fcm) & (result['bpm']<0.85*fcm)] = 'modérée'
        result['zone'].loc[(result['bpm']>=0.85*fcm)] = 'intense'
        result.index.name = 'datetime'
        result.dropna(inplace=True)
    else:
        result=pd.DataFrame()

    return(result.round(2))
 
# Extract steps    
def open_and_concat_steps(data_path,file_list,keyword,startDate,endDate):
    
    to_concat = []  
    
    if len(file_list) != 0:
    
        for f in file_list :
            df = pd.read_json(data_path+f)
            df.set_index('dateTime',inplace=True)
            df.rename(columns={'value':keyword},inplace=True)
            
            to_concat.append(df)
        
        result = pd.concat(to_concat)
        result = result.loc[startDate:endDate-timedelta(seconds=1)]
        result = result.resample('1min').sum()
        result.index.name = 'datetime'
        result.dropna(inplace=True)
        
        result = result.loc[result[keyword]!=0]
    else:
        result=pd.DataFrame()
    
    return(result)

# Extract daily stats
def daily_stats(result_min,startDate,endDate,keyword=['steps','heart_rate']):
    
    df = []

    if 'steps' in keyword:
        # Compute steps
        steps = result_min['steps'].resample('D').sum()
        df.append(steps)
    if 'heart_rate' in keyword:
        # Compute zones
        result_min['day'] = result_min.index.normalize()
        zone = result_min.groupby(['day','zone'])['bpm'].count().unstack(level=1)
        df.append(zone)
        # Compute bpm stats
        bpm_gb = result_min.groupby('day')['bpm'].agg(['max','min','mean','std'])
        bpm_gb.rename(columns = {'max':'bpm_max','min':'bpm_min','mean':'bpm_moyen','std':'bpm_et'},inplace=True)
        df.append(bpm_gb)
    
    result_day = pd.concat(df,axis=1)
    print(result_day)
    day_list = pd.date_range(startDate.normalize(),endDate-timedelta(seconds=1),freq='D')
    print(day_list)
    for d in day_list:
        if d not in result_day.index:
            result_day.loc[d] = None
    if endDate.hour == 0:
        endDate = endDate - timedelta(minutes=1)
        
    start_date_index = pd.date_range(startDate.normalize(),endDate,freq='D')
    if startDate not in start_date_index:
        start_date_index = start_date_index.delete(0)
        start_date_index = start_date_index.insert(0,startDate)
        
    end_date_index = pd.date_range(startDate.strftime('%Y%m%d 23:59:00'),endDate.strftime('%Y%m%d 23:59:00'),freq='D')
    if endDate not in end_date_index:
        end_date_index = end_date_index.delete(len(end_date_index)-1)
        end_date_index = end_date_index.insert(len(end_date_index),endDate)
    
    print(start_date_index)
    print(end_date_index)
    
    result_day.insert(0,'endDate',end_date_index)
    result_day.insert(0,'startDate',start_date_index) 
        
    return(result_day.reset_index(drop=True))

# Make a liste with all the watches in the directory
def list_all_watch(root_path):
    
    watch_list = []
    
    for watch in next(os.walk(root_path))[1]:
        watch_list.append(watch)
    
    return(watch_list)

# Extract what the client wants for one watch
def export_data(root_path, w, startDate, endDate, birth_year, keyword = ['steps','heart_rate']):  
    try:
        startDate = pd.to_datetime(startDate,format='%m/%d/%y %H:%M')
        endDate = pd.to_datetime(endDate,format='%m/%d/%y %H:%M')
        
        data_path = root_path + '/' + w + '/Fitbit/Global Export Data/'  
        all_files_list = os.listdir(data_path)
            
        to_extract_files = {}
            
        for k in keyword :
            if k == 'heart_rate':
                dates = pd.date_range(startDate.normalize()-timedelta(days=1),endDate.normalize()+timedelta(days=1),freq='D')
                dates = dates.strftime('%Y-%m-%d')
                to_extract_files[k] = find_json_files(all_files_list,k,dates)
            elif k == 'steps':
                dates = pd.date_range(startDate.normalize()-DateOffset(months=1),endDate.normalize()+DateOffset(months=1),freq='D')
                dates = dates.strftime('%Y-%m')
                to_extract_files[k] = find_json_files(all_files_list,k,np.unique(dates))    
        concatenated_json = []
        date_list = []
        no_data=True
            
        for k in keyword :
            if k == 'steps':
                concatenated_file = open_and_concat_steps(data_path, to_extract_files[k], k, startDate, endDate)
            elif k == 'heart_rate':
                concatenated_file = open_and_concat_active(data_path, to_extract_files[k], k, birth_year, startDate, endDate)
            
            concatenated_file.set_index(pd.to_datetime(concatenated_file.index),inplace=True)
            
            concatenated_json.append(concatenated_file)
            date_list.extend(concatenated_file.index)
            if len(concatenated_file)==0:
                keyword.remove(k)
            else:
                no_data=False

        if no_data :
            return(['No data'])
            
        dateList = np.unique(date_list)
        dateList.sort()
            
        result_file = pd.DataFrame(data=None)     
        min_date = min(dateList)
        max_date = max(dateList)
        result_file['Date'] = pd.date_range(min_date,max_date)
        
        result_file = pd.concat(concatenated_json,axis=1)
    
        result_file = result_file.loc[startDate:endDate]
        result_file.dropna(inplace=True,how='all')
        result_file = result_file.round(4)
            
        pretty_w = w.replace(' ','_')
        
        excel_file = root_path + '/' + pretty_w +'_'+startDate.strftime('%Y%m%d_%H%M')+'_'+endDate.strftime('%Y%m%d_%H%M')+'.xlsx'
    
        excel_writer = pd.ExcelWriter(excel_file,mode='w',
                                      datetime_format='YYYY-MM-DD HH:MM:SS',
                                      engine="openpyxl")

        with excel_writer as writer:  
            result_file.to_excel(writer, sheet_name='Par minute',
                                 index_label='Dates') 
        
        # Add daily results
        result_daily = daily_stats(result_file,startDate,endDate,keyword)
        result_daily = result_daily.round(4)
        excel_writer = pd.ExcelWriter(excel_file,mode='a',
                                      datetime_format='YYYY-MM-DD HH:MM:SS',
                                      engine="openpyxl")
        with excel_writer as writer:  
            result_daily.to_excel(writer, sheet_name='Total',index=False)         

        return(['Success'])
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb.tb_lineno)
        return(['Error',error])
    



