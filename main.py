# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:55:04 2024

@author: Marianne
"""

import sys
sys.path.append('./_internal/')

from library import list_all_watch, export_data
import tkinter as tk
from tkinter import filedialog as fd
import tkinter.scrolledtext as st
import time
from tkcalendar import Calendar,DateEntry
import os

basedir = os.path.dirname(__file__)

# Create the window
window = tk.Tk()
window.title("Fitbit Data Wizard")
window.geometry("800x600")
window.iconbitmap(os.path.join(basedir, "wizard_emoji.ico"))

r=0

# Add title and instructions
title = tk.Label(window,text = "Bienvenue sur Fitbit Data Wizard ! 🪄",
                 font=("Helvetica", 16))
title.grid(column=0,row=r,columnspan=10,padx=225)

r+=1

inst1 = tk.Label(window,
                 text = "Entrez le répertoire de votre dossier avec toutes vos montres,\nchoisissez la date de début et de fin et sélectionnez les métriques à exporter.",
                 font = ("Helvetica", 10))
inst1.grid(column=0,row=r,columnspan=10)

r+=1

# Enter the root path
path = tk.Label(window,text="Votre dossier : ",font=("Helvetica", 10))
path.grid(column=0,row=r, pady=50, padx=30, sticky='w',columnspan=3)

pathEntry = tk.Entry(window, width=90)
pathEntry.grid(column=0, row=r, pady=50, padx=125, columnspan=6, sticky='w')

def browse():
    directory=fd.askdirectory()
    pathEntry.delete(0,tk.END)
    pathEntry.insert(0,directory)

browseButton = tk.Button(window,text='Mes dossiers',command=browse,bg='lightblue')
browseButton.grid(column=4,columnspan=6,padx=50,row=r,pady=50, sticky='w')
r+=1

# Enter the start and end 
option = tk.Label(window, text='Options :',font=("Helvetica", 10))
option.grid(column=0, row=r, pady=5, padx=30, sticky='w')
r+=1

date=tk.Label(window,text='Dates :')
date.grid(column=0, row=r, pady=5, padx=35, sticky='w')

r+=1

useDate = tk.BooleanVar()
date1 = tk.Label(window,text='Date de début : ')
startcal = DateEntry(window, width=12, year=2024)
date2 = tk.Label(window,text='Date de fin : ')
endcal = DateEntry(window, width=12, year=2024)

def showCalendar() :
    
    if useDate.get() : 
        date1.grid(column=0,row=8,pady=5,sticky='w',padx=53,columnspan=2)
        startcal.grid(column=1, row=8, pady=5, sticky='w')
        date2.grid(column=2,row=8,pady=5, padx=5,sticky='w')
        endcal.grid(column=2, columnspan=2, padx=115, row=8, pady=5,sticky='w')
    
    else :
        date1.grid_forget()
        startcal.grid_forget()
        date2.grid_forget()
        endcal.grid_forget()


check1 = tk.Checkbutton(window, text='Exporter toutes les dates des fichiers',
                        variable=useDate, onvalue=False, offvalue=True, command=showCalendar)
check1.select()
check1.grid(column=0, row=r, pady=5, columnspan=6,sticky='w',padx=32)

r+=4

# Les métriques

useSed = tk.BooleanVar() 
useLight = tk.BooleanVar() 
useMod = tk.BooleanVar()
useVery = tk.BooleanVar()

useStepsD = tk.BooleanVar()
useStepsM = tk.BooleanVar()
useCalD = tk.BooleanVar()
useCalM = tk.BooleanVar()
useBpm = tk.BooleanVar()
useRest = tk.BooleanVar()

metrics = tk.Label(window, text='Métriques :')
metrics.grid(column=0, row=r, pady=5,padx=35, sticky='w')
r+=1

sedentary = tk.Checkbutton(window, text='Min. sédendaires',
                           variable=useSed, onvalue=True, offvalue=False)
sedentary.select()
sedentary.grid(column=0, row=r, pady=5, padx=35,sticky='w')

lightly = tk.Checkbutton(window, text='Min. peu actives',
                         variable=useLight, onvalue=True, offvalue=False)
lightly.select()
lightly.grid(column=1, row=r, pady=5, sticky='w')

moderately = tk.Checkbutton(window, text='Min. actives',
                            variable=useMod, onvalue=True, offvalue=False)
moderately.select()
moderately.grid(column=2, row=r, pady=5,sticky='w')

very = tk.Checkbutton(window, text='Min. très actives',
                      variable=useVery, onvalue=True, offvalue=False)
very.select()
very.grid(column=3, row=r, pady=5,sticky='w')

r+=1

stepsD = tk.Checkbutton(window, text='Pas par jour',
                       variable=useStepsD, onvalue=True, offvalue=False)
stepsD.select()
stepsD.grid(column=0, row=r, pady=5,padx=35,sticky='w')

stepsM = tk.Checkbutton(window, text='Pas par minute',
                       variable=useStepsM, onvalue=True, offvalue=False)
stepsM.select()
stepsM.grid(column=1, row=r, pady=5, sticky='w')


caloriesD = tk.Checkbutton(window, text='Calories par jour',
                          variable=useCalD, onvalue=True, offvalue=False)
caloriesD.grid(column=2, row=r, pady=5,sticky='w')

caloriesM = tk.Checkbutton(window, text='Calories par minute',
                          variable=useCalM, onvalue=True, offvalue=False)
caloriesM.grid(column=3, row=r, pady=5,sticky='w')

r+=1

heart = tk.Checkbutton(window, text='BPM moyen, min et max',
                       variable=useBpm, onvalue=True, offvalue=False)
heart.grid(column=0, row=r, pady=5,padx=35,sticky='w')

resting = tk.Checkbutton(window, text='BPM au repos',
                         variable=useRest, onvalue=True, offvalue=False)
resting.grid(column=1, row=r, pady=5,sticky='w')

r+=1

autre = tk.Label(window,text='Autre :')
autre.grid(column=0,row=r, pady=5, padx=35, sticky='w')

r+=1

cutDays=tk.BooleanVar()

watchWorn = tk.Checkbutton(window,text="Retirer les jours où la montre n'est pas portée",
                           variable=cutDays, onvalue=True, offvalue=False)
watchWorn.grid(column=0,row=r, pady=5, padx=35, sticky='w', columnspan=6)

r+=1

def openNewWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Fitbit Data Wizard")
    newWindow.geometry("500x250")
    newWindow.iconbitmap(os.path.join(basedir, "wizard_emoji.ico"))
    
    label = tk.Label(newWindow, 
                     text="Progression :", 
                     font = ("Helvetica", 10))
    label.pack(anchor='w',padx=25)
    
    return(newWindow)

def defineKeywords():
    
    keywords = {}
    
    if useSed.get():
        keywords['sedentary'] = 'D'
    if useLight.get():
        keywords['lightly'] = 'D'
    if useMod.get():
        keywords['moderately'] = 'D'
    if useVery.get():
        keywords['very'] = 'D'    
    if useStepsD.get():
        keywords['steps'] = 'D'
    if useStepsM.get():
        keywords['steps'] = 'M'
    if useCalD.get():
        keywords['calories'] = 'D'
    if useCalM.get():
        keywords['calories'] = 'M'
    if useBpm.get():
        keywords.append('heart_rate')
    if useRest.get():
        keywords.append('resting')      
        
    return(keywords)
    

def useInput():
    
    newWindow = openNewWindow()
    
    start = time.time()
    
    root_path = pathEntry.get()
    watch_list = list_all_watch(root_path)
    
    progress = st.ScrolledText(newWindow,    
                                      width = 60,  
                                      height = 10,  
                                      font = ("Helvetica", 10)) 
    progress.pack(padx=10,pady=10)
    
    startDate = startcal.get()
    endDate = endcal.get()
    
    keywords = defineKeywords()
    
    # Afficher les options dans la boite de texte
    
    for w in watch_list:
        if useDate.get() :
            verif = export_data(root_path,w,startDate=startDate,endDate=endDate,keyword=keywords,cut=cutDays.get())
        else : verif = export_data(root_path,w,keyword=keywords,cut=cutDays.get())
        
        
        if len(verif) == 2:
            break
        else:
            message = "---------------------------------------------------------\n" + "L'extraction de {w} est terminée.\n".format(w=w) + "---------------------------------------------------------\n"
            progress.insert(tk.END, message)
            progress.see("end")
            progress.update()
    
    end = time.time()
    
    if len(verif) == 2:
        progress.insert(tk.END,"\nERREUR!",'error')
        progress.tag_config('error', foreground='red')
        message = "\nUne erreur est survenue. Assurez-vous d'avoir bien entré vos paramètres avant de relancer le programme et de regarder la vidéo explicative.\nSi l'erreur persiste, veuillez envoyer à Marianne Fortier vos fichiers,\nles paramètres entrés et copier-coller le texte d'erreur plus bas au\nmarianne.fortier@gmail.com."
        progress.insert(tk.END,message)
        message = "\n\nL'erreur est "+str(verif[1])
        progress.insert(tk.END,message)
    else:
        progress.insert(tk.END,"\nSUCCÈS!",'success')
        progress.tag_config('success', foreground='green')
        message = "\nL'extraction s'est terminée en "+ time.strftime("%H h %M min %S sec.", time.gmtime(end-start))
        progress.insert(tk.END,message)
        progress.insert(tk.END,"\nVos fichiers se trouvent dans " + root_path)
        progress.see("end")

    progress.configure(state ='disabled')
    
    finishButton = tk.Button(newWindow,
                       text="OK",
                       command=newWindow.destroy,
                       bg="lightblue",
                       padx=15,
                       font=("Helvetica", 8))
    finishButton.pack(pady=5,anchor='n')
    
    
button = tk.Button(window,text="Commencer la magie ✨",command=useInput,bg="lightblue")
button.grid(column=0,row=r,columnspan=6,pady=20)

r+=1

credit = tk.Label(window,text='Application développée par Marianne Fortier',font=("Helvetica", 8, "italic"))
credit.grid(column=3,row=r,columnspan=5, pady=15, padx=10, sticky='e')

window.mainloop()
