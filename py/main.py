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

import warnings
warnings.filterwarnings('ignore') 

basedir = os.path.dirname(__file__)

# Create the window
window = tk.Tk()
window.title("Fitbit Data Wizard")
window.geometry("800x500")
window.iconbitmap(os.path.join(basedir, "../other/wizard_emoji.ico"))

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
path.grid(column=0,row=r, pady=40, padx=30, sticky='w',columnspan=3)

pathEntry = tk.Entry(window, width=70)
pathEntry.grid(column=0, row=r, pady=40, padx=125, columnspan=6, sticky='w')

def browse():
    directory=fd.askdirectory()
    pathEntry.delete(0,tk.END)
    pathEntry.insert(0,directory)

browseButton = tk.Button(window,text='Mes dossiers',command=browse,bg='lightblue')
browseButton.grid(column=4,columnspan=6,padx=40,row=r,pady=40, sticky='w')
r+=1

# Enter the start and end 
option = tk.Label(window, text='Options :',font=("Helvetica", 10))
option.grid(column=0, row=r, pady=5, padx=30, sticky='w')
r+=1

date1 = tk.Label(window,text='Date de début : ')
startcal = DateEntry(window, width=12, year=2024)
timetxt1 = tk.Label(window,text="HH:MM")
hourstart = tk.Entry(window,width=3)
twodots1 = tk.Label(window,text=':')
minstart = tk.Entry(window,width=3)

date2 = tk.Label(window,text='Date de fin : ')
endcal = DateEntry(window, width=12, year=2024)
timetxt2 = tk.Label(window,text="HH:MM")
hourend = tk.Entry(window,width=3)
twodots2 = tk.Label(window,text=':')
minend = tk.Entry(window,width=3)

def showCalendar(r) :
    
    date1.grid(column=0,row=r,pady=5,sticky='w',padx=35,columnspan=3)
    startcal.grid(column=0, row=r, pady=5, columnspan=3, padx=122, sticky='w')
    timetxt1.grid(column=1,row=r,pady=5,columnspan=2,sticky='w')
    hourstart.grid(column=1,row=r,padx=55,columnspan=3,sticky='w')
    twodots1.grid(column=1,row=r,padx=80,columnspan=2,sticky='w')
    minstart.grid(column=1,row=r,padx=93,columnspan=3,sticky='w')
        
    date2.grid(column=0,row=r+1,pady=5,padx=35,sticky='w',columnspan=3)
    endcal.grid(column=0, columnspan=3, padx=122, row=r+1, pady=5,sticky='w')
    timetxt2.grid(column=1,row=r+1,pady=5,columnspan=2,sticky='w')
    hourend.grid(column=1,row=r+1,padx=55,columnspan=3,sticky='w')
    twodots2.grid(column=1,row=r+1,padx=80,columnspan=2,sticky='w')
    minend.grid(column=1,row=r+1,padx=93,columnspan=3,sticky='w')

showCalendar(r)
r+=5

# Les métriques
useSteps = tk.BooleanVar()
useActive = tk.BooleanVar()

metrics = tk.Label(window, text='Métriques :')
metrics.grid(column=0, row=r, pady=5,padx=35, sticky='w')
r+=1

active = tk.Checkbutton(window, text='Zones actives',
                      variable=useActive, onvalue=True, offvalue=False)
active.select()
active.grid(column=0, row=r, pady=5,padx=35,sticky='w')

steps = tk.Checkbutton(window, text='Pas',
                       variable=useSteps, onvalue=True, offvalue=False)
steps.select()
steps.grid(column=1, row=r, pady=5, sticky='w')

r+=1

birth = tk.Label(window,text='Année de naissance :')
birth.grid(column=0,row=r, pady=5, padx=35, sticky='w',columnspan=3)
yr_birth = tk.Entry(window,width=10)
yr_birth.grid(column=0,row=r,pady=5,padx=152,sticky='w',columnspan=3)

r+=1

def openNewWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Fitbit Data Wizard")
    newWindow.geometry("500x250")
    newWindow.iconbitmap(os.path.join(basedir, "../other/wizard_emoji.ico"))
    
    label = tk.Label(newWindow, 
                     text="Progression :", 
                     font = ("Helvetica", 10))
    label.pack(anchor='w',padx=25)
    
    return(newWindow)

def defineKeywords():
    
    keywords = []
    
    if useActive.get():
        keywords.append('heart_rate')
    if useSteps.get():
        keywords.append('steps')     
        
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

    startTime = str(hourstart.get())+':'+str(minstart.get())
    endTime = str(hourend.get())+':'+str(minend.get())
    
    birth_year = yr_birth.get()
    
    keywords = defineKeywords()
    
    # Afficher les options dans la boite de texte
    for w in watch_list:
        print(w)
        verif = export_data(root_path,w,startDate+' '+startTime,endDate+' '+endTime,birth_year,keyword=keywords)        
        print(verif)
        if verif[0] == 'Error':
            break
        elif verif[0] == 'No data':
            message = "-------------------------------------------------------------------\n" + "{w} n'a aucune donnée pour les dates entrées.\n".format(w=w) + "-------------------------------------------------------------------\n"
            progress.insert(tk.END, message)
            progress.see("end")
            progress.update()
        else:
            message = "-------------------------------------------------------------------\n" + "L'extraction de {w} est terminée.\n".format(w=w) + "-------------------------------------------------------------------\n"
            progress.insert(tk.END, message)
            progress.see("end")
            progress.update()
    
    end = time.time()
    
    if verif[0] == 'Error':
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
button.grid(column=0,row=r,columnspan=6,pady=30)

r+=1

credit = tk.Label(window,text='Application développée par Marianne Fortier',font=("Helvetica", 8, "italic"))
credit.grid(column=3,row=r,columnspan=5, padx=10, pady=25, sticky='e')

window.mainloop()
=======
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

import warnings
warnings.filterwarnings('ignore') 

basedir = os.path.dirname(__file__)

# Create the window
window = tk.Tk()
window.title("Fitbit Data Wizard")
window.geometry("800x500")
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
path.grid(column=0,row=r, pady=40, padx=30, sticky='w',columnspan=3)

pathEntry = tk.Entry(window, width=70)
pathEntry.grid(column=0, row=r, pady=40, padx=125, columnspan=6, sticky='w')

def browse():
    directory=fd.askdirectory()
    pathEntry.delete(0,tk.END)
    pathEntry.insert(0,directory)

browseButton = tk.Button(window,text='Mes dossiers',command=browse,bg='lightblue')
browseButton.grid(column=4,columnspan=6,padx=40,row=r,pady=40, sticky='w')
r+=1

# Enter the start and end 
option = tk.Label(window, text='Options :',font=("Helvetica", 10))
option.grid(column=0, row=r, pady=5, padx=30, sticky='w')
r+=1

date1 = tk.Label(window,text='Date de début : ')
startcal = DateEntry(window, width=12, year=2024)
timetxt1 = tk.Label(window,text="HH:MM")
hourstart = tk.Entry(window,width=3)
twodots1 = tk.Label(window,text=':')
minstart = tk.Entry(window,width=3)

date2 = tk.Label(window,text='Date de fin : ')
endcal = DateEntry(window, width=12, year=2024)
timetxt2 = tk.Label(window,text="HH:MM")
hourend = tk.Entry(window,width=3)
twodots2 = tk.Label(window,text=':')
minend = tk.Entry(window,width=3)

def showCalendar(r) :
    
    date1.grid(column=0,row=r,pady=5,sticky='w',padx=35,columnspan=3)
    startcal.grid(column=0, row=r, pady=5, columnspan=3, padx=122, sticky='w')
    timetxt1.grid(column=1,row=r,pady=5,columnspan=2,sticky='w')
    hourstart.grid(column=1,row=r,padx=55,columnspan=3,sticky='w')
    twodots1.grid(column=1,row=r,padx=80,columnspan=2,sticky='w')
    minstart.grid(column=1,row=r,padx=93,columnspan=3,sticky='w')
        
    date2.grid(column=0,row=r+1,pady=5,padx=35,sticky='w',columnspan=3)
    endcal.grid(column=0, columnspan=3, padx=122, row=r+1, pady=5,sticky='w')
    timetxt2.grid(column=1,row=r+1,pady=5,columnspan=2,sticky='w')
    hourend.grid(column=1,row=r+1,padx=55,columnspan=3,sticky='w')
    twodots2.grid(column=1,row=r+1,padx=80,columnspan=2,sticky='w')
    minend.grid(column=1,row=r+1,padx=93,columnspan=3,sticky='w')

showCalendar(r)
r+=5

# Les métriques
useSteps = tk.BooleanVar()
useActive = tk.BooleanVar()

metrics = tk.Label(window, text='Métriques :')
metrics.grid(column=0, row=r, pady=5,padx=35, sticky='w')
r+=1

active = tk.Checkbutton(window, text='Zones actives',
                      variable=useActive, onvalue=True, offvalue=False)
active.select()
active.grid(column=0, row=r, pady=5,padx=35,sticky='w')

steps = tk.Checkbutton(window, text='Pas',
                       variable=useSteps, onvalue=True, offvalue=False)
steps.select()
steps.grid(column=1, row=r, pady=5, sticky='w')

r+=1

birth = tk.Label(window,text='Année de naissance :')
birth.grid(column=0,row=r, pady=5, padx=35, sticky='w',columnspan=3)
yr_birth = tk.Entry(window,width=10)
yr_birth.grid(column=0,row=r,pady=5,padx=152,sticky='w',columnspan=3)

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
    
    keywords = []
    
    if useActive.get():
        keywords.append('heart_rate')
    if useSteps.get():
        keywords.append('steps')     
        
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

    startTime = str(hourstart.get())+':'+str(minstart.get())
    endTime = str(hourend.get())+':'+str(minend.get())
    
    birth_year = yr_birth.get()
    
    keywords = defineKeywords()
    
    # Afficher les options dans la boite de texte
    for w in watch_list:
        print(w)
        verif = export_data(root_path,w,startDate+' '+startTime,endDate+' '+endTime,birth_year,keywords=keywords)        
        print(verif)
        if verif[0] == 'Error':
            break
        elif verif[0] == 'No data':
            message = "-------------------------------------------------------------------\n" + "{w} n'a aucune donnée pour les dates entrées.\n".format(w=w) + "-------------------------------------------------------------------\n"
            progress.insert(tk.END, message)
            progress.see("end")
            progress.update()
        else:
            message = "-------------------------------------------------------------------\n" + "L'extraction de {w} est terminée.\n".format(w=w) + "-------------------------------------------------------------------\n"
            progress.insert(tk.END, message)
            progress.see("end")
            progress.update()
    
    end = time.time()
    
    if verif[0] == 'Error':
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
button.grid(column=0,row=r,columnspan=6,pady=30)

r+=1

credit = tk.Label(window,text='Application développée par Marianne Fortier',font=("Helvetica", 8, "italic"))
credit.grid(column=3,row=r,columnspan=5, padx=10, pady=25, sticky='e')

window.mainloop()
>>>>>>> Stashed changes
