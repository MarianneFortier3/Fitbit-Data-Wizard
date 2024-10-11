# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:06:35 2023

@author: Marianne
"""

# Fonctions pour extraire les données des montres

import pandas as pd
import numpy as np
import os
import sys


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def find_json_files(file_list, keyword):
    
    if keyword in ['stepsD','stepsM','caloriesD','caloriesM']:
        keyword = keyword[:-1]
    
    matched_files = [f for f in file_list if f.startswith(keyword)]
        
    return(matched_files)

def open_and_concat_minutes_resting(data_path,file_list,keyword,cut=False):
    
    to_concat=[]
    
    for f in file_list:
        df = pd.read_json(data_path+f)
        
        if keyword=='resting':
            values = pd.DataFrame.from_records(df['value'].values)
            df.drop(labels='value',axis=1,inplace=True)
            df['resting_bpm']=values['value']
        else:
            df.rename(columns={'value':keyword},inplace=True)
            
        df.set_index('dateTime',inplace=True)
        
        if cut :
            if keyword in ['lightly', 'moderately', 'very']:
                df.drop(df.loc[df[keyword]==0].index,inplace=True)
            elif keyword=='resting':
                df.drop(df.loc[df[keyword+'_bpm']==0].index,inplace=True)
            else:
                df.drop(df.loc[df[keyword]==1440].index,inplace=True)
        
        to_concat.append(df)
    
    result = pd.concat(to_concat)
    
    return(result)
        
def open_and_concat_steps_cal(data_path,file_list,keyword,cut=False):
    
    to_concat = []  
    freq = keyword[-1]
    keyword = keyword[:-1]
    
    
    for f in file_list :
        df = pd.read_json(data_path+f)
        df.set_index('dateTime',inplace=True)
        df.rename(columns={'value':keyword},inplace=True)
        df_daily = df.groupby(df.index.date).sum()
        df_daily.index = pd.to_datetime(df_daily.index)
        
        if freq=='D':
            df = df_daily
        
        if cut :
            if keyword=='steps':
                dates_not_worn = df_daily.loc[df_daily[keyword]==0].index.date
            else:
                dates_not_worn = df_daily.loc[round(df_daily[keyword]).isin([979,980])].index.date 
            not_worn = df.loc[np.isin(df.index.date,dates_not_worn)].index
            df.drop(not_worn,inplace=True)
        
        to_concat.append(df)
    
    result = pd.concat(to_concat)
    result = result.groupby(result.index).sum()
    result.index.name = 'datetime'
    
    return(result)

def open_and_concat_heart(data_path,file_list,keyword,cut=False):
    
    to_concat = []  
    
    for f in file_list :
        df = pd.read_json(data_path+f)
        values = pd.DataFrame.from_records(df['value'].values)
        df.drop(labels='value',axis=1,inplace=True)
        df['bpm']=values['bpm']
        
        df.set_index('dateTime',inplace=True)
        df.rename(columns={'value':keyword},inplace=True)
        
        to_concat.append(df)
    
    result = pd.concat(to_concat)
    
    result = result.groupby(result.index.date).bpm.agg(['mean','min','max'])
    result.rename(columns={'mean':'mean_bpm','min':'min_bpm','max':'max_bpm'},inplace=True)
        
    if cut :
        result.drop(result.loc[result['mean_bpm']==0].index,inplace=True)
        result.drop(result.loc[result['mean_bpm']==70].index,inplace=True)
        
    return(result)

def list_all_watch(root_path):
    
    watch_list = []
    
    for watch in next(os.walk(root_path))[1]:
        watch_list.append(watch)
    
    return(watch_list)

def export_data(root_path, w, 
                keyword = ['sedentary','lightly','moderately','very','stepsD'],
                startDate = None, endDate = None, cut=False):  
    try:
        data_path = root_path + '/' + w + '/Fitbit/Global Export Data/'  
        all_files_list = os.listdir(data_path)
            
        to_extract_files = pd.Series(data=None,index=keyword)
            
        for k in keyword :
            to_extract_files[k] = find_json_files(all_files_list,k)
            
        concatenated_json_D = []
        concatenated_json_M = []

        date_list = []
            
        for k in keyword:
            
            if k in ['sedentary', 'lightly', 'moderately', 'very', 'resting']:
                concatenated_file = open_and_concat_minutes_resting(data_path, to_extract_files[k], k, cut=cut)
            
            elif k in ['stepsD','stepsM','caloriesD','caloriesM']:
                concatenated_file = open_and_concat_steps_cal(data_path, to_extract_files[k], k,cut=cut)
            elif k in ['heart_rate']:
                concatenated_file = open_and_concat_heart(data_path, to_extract_files[k], k, cut=cut)
            
            concatenated_file.set_index(pd.to_datetime(concatenated_file.index),inplace=True)
            
            if k in ['stepsM','caloriesM']:
                concatenated_json_M.append(concatenated_file)
            else :
                concatenated_json_D.append(concatenated_file)
            date_list.extend(concatenated_file.index)
            
        dateList = np.unique(date_list)
        dateList.sort()
        pretty_w = w.replace(' ','_')
        excel_file = root_path + '/' + pretty_w +'_final_data.xlsx'
        excel_mode = 'w'
        
        if len(concatenated_json_D)!=0: 
            result_file = pd.DataFrame()     
            min_date = min(dateList)
            max_date = max(dateList)
            result_file['Date'] = pd.date_range(min_date,max_date)
        
            result_file = pd.concat(concatenated_json_D,axis=1)
            result_file.fillna('0',inplace=True)
        
            if (startDate != None) & (endDate != None) :
                startDate = pd.to_datetime(startDate)
                endDate = pd.to_datetime(endDate)
    
                result_file = result_file.loc[startDate:endDate]
            
            excel_writer = pd.ExcelWriter(excel_file,date_format='YYYY-MM-DD',
                                          mode=excel_mode,
                                          datetime_format='YYYY-MM-DD HH:MM:SS',
                                          engine="openpyxl")

            with excel_writer as writer:  
                result_file.to_excel(writer, sheet_name='métriques journalières',
                                     index_label='Dates') 
            excel_mode = 'a'
            
        if len(concatenated_json_M)!=0: 
            result_file = pd.DataFrame()     
            min_date = min(dateList)
            max_date = max(dateList)
            result_file['Date'] = pd.date_range(min_date,max_date,freq='min')
        
            result_file = pd.concat(concatenated_json_M,axis=1)
            result_file.fillna('0',inplace=True)
        
            if (startDate != None) & (endDate != None) :
                startDate = pd.to_datetime(startDate)
                endDate = pd.to_datetime(endDate)
    
                result_file = result_file.loc[startDate:endDate]
    
            excel_writer = pd.ExcelWriter(excel_file,date_format='YYYY-MM-DD',
                                          mode=excel_mode,
                                          datetime_format='YYYY-MM-DD HH:MM:SS',
                                          engine="openpyxl")
            with excel_writer as writer:  
                result_file.to_excel(writer, sheet_name='métriques originales',
                                     index_label='Dates')           
        return('Success')
    except Exception as error:
        return(['Error',error])
    



