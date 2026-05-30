# -*- coding: utf-8 -*-
"""

░▒▓█▓▒░▒▓██████████████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░                          
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                 
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                                 
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░                            
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                 
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░                                 
░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░                          
                                                                                            
                                                                                            
░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░ ░▒▓██████▓▒░    ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓████████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                            

Created on Thu Aug 13 15:47:34 2025

@author: LNC Miguel Velasco Orozco 

Este programa sirve para obtener los IDs de imagen para las descargas desde el PPMI según la modalidad y si
son de una sola adquisición o longitudinales.

Además puede omitir los sujetos que ya se hayan analizado desde corridas previas

Utiliza los Archivos SUBJECTS_LIST_## e INTERNAL_# provenientes del Metadata Refiner 
Para omitir sujetos ya previamente analizados se utiliza un archivo con la misma estructura a SUBJECTS_LIST_ pero
que contenga los IDs de los sujetos ya analizados. 

Genera el archivo DOWNLOAD_IDS_##.txt con los IDs de las imágenes separados por comas para introducir en el panel de 
descarga del PPMI
Genera el archivo ANALYZED_SUBJECTS_LIST_##.csv con la misma estructura que SUBJECTS_LIST para dejar listo los datos de 
los sujetos que ya fueron analizados*. En caso de haber tenido sujetos ya analizados, sus ID's se incluyen en este
archivo.

*O al menos descargados.

/////UPDATE Ver 1.1

Por alguna razón en algunos sujetos el ID de imagen está cambiada la primera 'I' por una 'D', lo cual hace
que el buscador en PPMI lance un mensaje de caracter incorrecto. Al revisar esas imágenes buscando por sujeto
en vez del ID aparece la misma cadena numérica solo que con una 'I' en vez de la 'D', por lo que en el módulo 
de creación del archivo de texto puse una línea que intercambia todas las 'D' por una 'I'.


"""
VER='1.1'

import easygui as eg
import os                #Sirve para el Manejo de archivos
import pandas as pd
import numpy as np
from datetime import datetime 

#Functions
def flatten(xss):
    return [x for xs in xss for x in xs]

#%%----PATH MANAGER----

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Image Fetcher "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Image Type
message = 'Please select Image Type'
title = "Image Fetcher "+VER+" - Start"
choices = ['T13D','DTI','fMRI', 'NM']
itype = eg.multchoicebox(message, title, choices) 

#Omit Aalyzed Subjects
message = 'Do you want to omit previously analyzed subjects?\n\nRequires extra SUBJECTS_LIST file'
title = "Image Fetcher "+VER+" - Start"
analyzed = eg.ynbox(message, title) 

#Session Save path
message = 'Please input Session Save Folder'
title = "Image Fetcher "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Internal File path
message = 'Please Select Metadata Internal Refined File'
title = "Image Fetcher "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
fl_path = temp_path.replace(os.path.sep ,"/")

#Subjects list File path
message = 'Please Select current Subjects List File'
title = "Image Fetcher "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
sl_path = temp_path.replace(os.path.sep ,"/")

#Omit subjects
if analyzed:
    message = 'Please Select previous Subjects List File'
    title = "Image Fetcher "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
    omit_path = temp_path.replace(os.path.sep ,"/")


#-------Change working directory to save path 
os.chdir(sv_path)

#%%----DATA LOAD----

#Read Internal Refined File
intfile = pd.read_csv(fl_path)  

#Read current subjects file path 
slfile = pd.read_csv(sl_path)

if analyzed:
    omitfile = pd.read_csv(omit_path)

#%%----ID retrival by image and subject type----

#If there are already analyzed subjects extract all the omit data

if analyzed:
    #T13D
    t1_s_omit = np.array(omitfile['Single Aqc T13D Subjects'].dropna().astype(int)) #Select T13d single Acq subject IDs
    t1_l_omit = np.array(omitfile['Longitudinal T13D Subjects'].dropna().astype(int)) #Select T13d longitudinal subject IDs 
    
    #fMRI
    fmri_s_omit = np.array(omitfile['Single Aqc fMRI Subjects'].dropna().astype(int)) #Select fMRI single Acq subject IDs
    fmri_l_omit = np.array(omitfile['Longitudinal fMRI Subjects'].dropna().astype(int)) #Select fMRI longitudinal subject IDs

    #DTI
    dti_s_omit = np.array(omitfile['Single Aqc DTI Subjects'].dropna().astype(int)) #Select DTI single Acq subject IDs
    dti_l_omit = np.array(omitfile['Longitudinal DTI Subjects'].dropna().astype(int)) #Select T13d longitudinal subject IDs 
    
    #NM
    nm_s_omit = np.array(omitfile['Single Aqc NM Subjects'].dropna().astype(int)) #Select NM single Acq subject IDs
    nm_l_omit = np.array(omitfile['Longitudinal NM Subjects'].dropna().astype(int)) #Select NM longitudinal subject IDs 


if 'T13D' in itype:   #Select T13D image IDs
    print('\nStarting T13D...')
    t1_s= np.array(slfile['Single Aqc T13D Subjects'].dropna().astype(int)) #Select T13d single Acq subject IDs 
    t1_l= np.array(slfile['Longitudinal T13D Subjects'].dropna().astype(int)) #Select T13d longitudinal subject IDs 

    if analyzed: #Omit analyzed subjects  
        print('Removing previously analyzed T13D subjects...')
        print('Number of T13D single acquisition subjects to omit: '+str(len(t1_s_omit)))
        print('Number of T13D longitudinal acquisition subjects to omit: '+str(len(t1_l_omit)))
        
        #Subjects filter
        t1_s_subs = np.array([i for i in t1_s if i not in t1_s_omit])
        t1_l_subs = np.array([i for i in t1_l if i not in t1_l_omit])
        print('Number of T13D single acquisition subject IDs to download: '+str(len(t1_s_subs)))
        print('Number of T13D longitudinal acquisition subject IDs to download: '+str(len(t1_l_subs)))
    
    else: #If none to omit 
        
        t1_s_subs = t1_s
        t1_l_subs = t1_l
        print('Number of T13D single acquisition subject IDs to download: '+str(len(t1_s_subs)))
        print('Number of T13D longitudinal acquisition subject IDs to download: '+str(len(t1_l_subs)))
    
        
        
    #Single Acq IDs dictionary 
    t1_s_ids={}
    temp_ids=[]
    
    for i in t1_s_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='T13D')]['Image Data ID'])
        t1_s_ids.update({i:temp_ids})
     
    #Longitudinals IDs dictionary 
    t1_l_ids={}
    temp_ids=[]
    
    for i in t1_l_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='T13D')]['Image Data ID'])
        t1_l_ids.update({i:temp_ids})
    
      
if 'fMRI' in itype:   #Select fMRI image IDs

    print('\nStarting fMRI...')
    fmri_s= np.array(slfile['Single Aqc fMRI Subjects'].dropna().astype(int)) #Select fMRI single Acq subject IDs 
    fmri_l= np.array(slfile['Longitudinal fMRI Subjects'].dropna().astype(int)) #Select fMRI longitudinal subject IDs 

    if analyzed: #Omit analyzed subjects  
        print('Removing previously analyzed fMRI subjects...')
        print('Number of fMRI single acquisition subjects to omit: '+str(len(fmri_s_omit)))
        print('Number of fMRI longitudinal acquisition subjects to omit: '+str(len(fmri_l_omit)))
        
        #Subjects filter
        fmri_s_subs = np.array([i for i in fmri_s if i not in fmri_s_omit])
        fmri_l_subs = np.array([i for i in fmri_l if i not in fmri_l_omit])
        print('Number of fMRI single acquisition subject IDs to download: '+str(len(fmri_s_subs)))
        print('Number of fMRI longitudinal acquisition subject IDs to download: '+str(len(fmri_l_subs)))
    
    
    else: #If none to omit 
        fmri_s_subs = fmri_s
        fmri_l_subs = fmri_l
        print('Number of fMRI single acquisition subject IDs to download: '+str(len(fmri_s_subs)))
        print('Number of fMRI longitudinal acquisition subject IDs to download: '+str(len(fmri_l_subs)))
        
    #Single Acq IDs dictionary 
    fmri_s_ids={}
    temp_ids=[]
    
    for i in fmri_s_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='fMRI')]['Image Data ID'])
        fmri_s_ids.update({i:temp_ids})
     
    #Longitudinals IDs dictionary 
    fmri_l_ids={}
    temp_ids=[]
    
    for i in fmri_l_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='fMRI')]['Image Data ID'])
        fmri_l_ids.update({i:temp_ids})
      

if 'DTI' in itype:   #Select fMRI image IDs
    print('\nStarting DTI...')
    dti_s= np.array(slfile['Single Aqc DTI Subjects'].dropna().astype(int)) #Select DTI single Acq subject IDs 
    dti_l= np.array(slfile['Longitudinal DTI Subjects'].dropna().astype(int)) #Select DTI longitudinal subject IDs 

    if analyzed: #Omit analyzed subjects  
        print('Removing previously analyzed DTI subjects...')
        print('Number of DTI single acquisition subjects to omit: '+str(len(dti_s_omit)))
        print('Number of DTI longitudinal acquisition subjects to omit: '+str(len(dti_l_omit)))
        
        #Subjects filter
        dti_s_subs = np.array([i for i in dti_s if i not in dti_s_omit])
        dti_l_subs = np.array([i for i in dti_l if i not in dti_l_omit])
        print('Number of DTI single acquisition subject IDs to download: '+str(len(dti_s_subs)))
        print('Number of DTI longitudinal acquisition subject IDs to download: '+str(len(dti_l_subs)))
        
    else: #If none to omit 
        dti_s_subs = dti_s
        dti_l_subs = dti_l
        print('Number of DTI single acquisition subject IDs to download: '+str(len(dti_s_subs)))
        print('Number of DTI longitudinal acquisition subject IDs to download: '+str(len(dti_l_subs)))
        
    #Single Acq IDs dictionary 
    dti_s_ids={}
    temp_ids=[]
    
    for i in dti_s_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='DTI')]['Image Data ID'])
        dti_s_ids.update({i:temp_ids})
     
    #Longitudinals IDs dictionary 
    dti_l_ids={}
    temp_ids=[]
    
    for i in dti_l_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='DTI')]['Image Data ID'])
        dti_l_ids.update({i:temp_ids})
      


if 'NM' in itype:   #Select fMRI image IDs
    print('\nStarting NM...')
    nm_s= np.array(slfile['Single Aqc NM Subjects'].dropna().astype(int)) #Select NM single Acq subject IDs 
    nm_l= np.array(slfile['Longitudinal NM Subjects'].dropna().astype(int)) #Select NM longitudinal subject IDs 

    if analyzed: #Omit analyzed subjects  
        print('Removing previously analyzed NM subjects...')
        print('Number of NM single acquisition subjects to omit: '+str(len(nm_s_omit)))
        print('Number of NM longitudinal acquisition subjects to omit: '+str(len(nm_l_omit)))
        
        #Subjects filter
        nm_s_subs = np.array([i for i in nm_s if i not in nm_s_omit])
        nm_l_subs = np.array([i for i in nm_l if i not in nm_l_omit])
        print('Number of NM single acquisition subject IDs to download: '+str(len(nm_s_subs)))
        print('Number of NM longitudinal acquisition subject IDs to download: '+str(len(nm_l_subs)))
    
    else: #If none to omit 
        nm_s_subs = nm_s
        nm_l_subs = nm_l
        print('Number of NM single acquisition subject IDs to download: '+str(len(nm_s_subs)))
        print('Number of NM longitudinal acquisition subject IDs to download: '+str(len(nm_l_subs)))
        
    #Single Acq IDs dictionary 
    nm_s_ids={}
    temp_ids=[]
    
    for i in nm_s_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='NM')]['Image Data ID'])
        nm_s_ids.update({i:temp_ids})
     
    #Longitudinals IDs dictionary 
    nm_l_ids={}
    temp_ids=[]
    
    for i in nm_l_subs: #iterate through single acq subs
        temp_ids = list(intfile[(intfile['Subject']==i) & (intfile['Modality']=='NM')]['Image Data ID'])
        nm_l_ids.update({i:temp_ids})

#%%----DOWNLOAD_IDS File creation----


#Initialyze .txt file 
with open ('DOWNLOAD_IDs_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.txt', 'w') as savefile:
    savefile.write('░▒▓█▓▒░▒▓██████████████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░   \n')        
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  \n')        
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░    \n')  
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░ \n') 
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░   \n') 
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░   \n') 
    savefile.write('░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░  \n') 
    savefile.write('\n') 
    savefile.write('░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░ \n')
    savefile.write('░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n')
    savefile.write('░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n')
    savefile.write('░▒▓██████▓▒░ ░▒▓██████▓▒░    ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓███████▓▒░  \n')
    savefile.write('░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n')
    savefile.write('░▒▓█▓▒░      ░▒▓█▓▒░         ░▒▓█▓▒░  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ \n')
    savefile.write('░▒▓█▓▒░      ░▒▓████████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ \n') 
    savefile.write('\n') 
    savefile.write('------------------------------Session Values------------------------------------------------\n\n') 
    savefile.write('Created By: NeuroSc Miguel Velasco-Orozco \u00A9 2025\nVersion Control: '+VER+'\n\n\n')
    savefile.write('Session Name: '+sname+'\n\n')
    savefile.write('Internal File Route: \n'+fl_path+'\n\n')
    savefile.write('Current Subjects List File Route: \n'+sl_path+'\n\n')
    if analyzed:
        savefile.write('Omitted Subjects List File Route: \n'+omit_path+'\n\n')        
    savefile.write('Save Folder Route: \n'+sv_path+'\n\n\n')
    savefile.write('Start Timestamp: '+str(datetime.now())+'\n')
    savefile.write('--------------------------------------------------------------------------------------------\n') 
    
    savefile.write('\n\n\n')
    #T13D
    if 'T13D' in itype:
        savefile.write('--------------------------T1 3D-----------------------------')
        if analyzed:
            savefile.write('\nNumber of T13D single acquisition subjects to omit: '+str(len(t1_s_omit)))
            savefile.write('\nNumber of T13D longitudinal acquisition subjects to omit: '+str(len(t1_l_omit)))
        savefile.write('\nNumber of T13D single acquisition subject IDs to download: '+str(len(t1_s_subs)))
        savefile.write('\nNumber of T13D longitudinal acquisition subject IDs to download: '+str(len(t1_l_subs)))
        savefile.write('\n\n>Single acquisition IDs\n')
        tmplist=str(flatten(list(t1_s_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n\n>Longitudinal acquisition IDs\n')
        tmplist=str(flatten(list(t1_l_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        
    #DTI
    if 'DTI' in itype:
        savefile.write('--------------------------DTI-----------------------------')
        if analyzed:
            savefile.write('\nNumber of DTI single acquisition subjects to omit: '+str(len(dti_s_omit)))
            savefile.write('\nNumber of DTI longitudinal acquisition subjects to omit: '+str(len(dti_l_omit)))
        savefile.write('\nNumber of DTI single acquisition subject IDs to download: '+str(len(dti_s_subs)))
        savefile.write('\nNumber of DTI longitudinal acquisition subject IDs to download: '+str(len(dti_l_subs)))
        savefile.write('\n\n>Single acquisition IDs\n')
        tmplist=str(flatten(list(dti_s_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n\n>Longitudinal acquisition IDs\n')
        tmplist=str(flatten(list(dti_l_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        
    #fMRI
    if 'fMRI' in itype:
        savefile.write('--------------------------fMRI-----------------------------')
        if analyzed:
            savefile.write('\nNumber of fMRI single acquisition subjects to omit: '+str(len(fmri_s_omit)))
            savefile.write('\nNumber of fMRI longitudinal acquisition subjects to omit: '+str(len(fmri_l_omit)))
        savefile.write('\nNumber of fMRI single acquisition subject IDs to download: '+str(len(fmri_s_subs)))
        savefile.write('\nNumber of fMRI longitudinal acquisition subject IDs to download: '+str(len(fmri_l_subs)))
        savefile.write('\n\n>Single acquisition IDs\n')
        tmplist=str(flatten(list(fmri_s_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n\n>Longitudinal acquisition IDs\n')
        tmplist=str(flatten(list(fmri_l_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')

    #NM
    if 'NM' in itype:
        savefile.write('--------------------------NM-----------------------------')
        if analyzed:
            savefile.write('\nNumber of NM single acquisition subjects to omit: '+str(len(nm_s_omit)))
            savefile.write('\nNumber of NM longitudinal acquisition subjects to omit: '+str(len(nm_l_omit)))
        savefile.write('\nNumber of NM single acquisition subject IDs to download: '+str(len(nm_s_subs)))
        savefile.write('\nNumber of NM longitudinal acquisition subject IDs to download: '+str(len(nm_l_subs)))
        savefile.write('\n\n>Single acquisition IDs\n')
        tmplist=str(flatten(list(nm_s_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n\n>Longitudinal acquisition IDs\n')
        tmplist=str(flatten(list(nm_l_ids.values()))) #Takes all the values and puts them in list, then converts list to string
        tmplist=tmplist.replace("'","") #Removes ' character from numbers 
        tmplist=tmplist.replace("[","") #Removes [ character from numbers 
        tmplist=tmplist.replace("]","") #Removes ] character from numbers 
        tmplist=tmplist.replace("D","I") #Replaces D for I (read documentation)
        savefile.write('\n')
        savefile.write(tmplist)
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')
        savefile.write('\n')

#%%----ANALYZED_SUBJECTS file generation ----
    
if analyzed: 
    if 'T13D' not in itype: #if this kind of image was not selected but previously analyzed
        t1_s_analyzed=list(t1_s_omit) #only include the previously analyzed
        t1_l_analyzed=list(t1_l_omit)
    elif 'T13D' in itype:#if this kind of image was selected and previously analyzed
        t1_s_analyzed=list(t1_s_omit)+list(t1_s_subs) #list of the currently analyzed plus the previously analyzed
        t1_l_analyzed=list(t1_l_omit)+list(t1_l_subs)
    
        
    if 'DTI' not in itype:
        dti_s_analyzed=list(dti_s_omit)
        dti_l_analyzed=list(dti_l_omit)
    elif 'DTI' in itype:
        dti_s_analyzed=list(dti_s_omit)+list(dti_s_subs)
        dti_l_analyzed=list(dti_l_omit)+list(dti_l_subs)
    
    
    if 'fMRI' not in itype:
        fmri_s_analyzed=list(fmri_s_omit)
        fmri_l_analyzed=list(fmri_l_omit)
    elif 'fMRI' in itype:
        fmri_s_analyzed=list(fmri_s_omit)+list(fmri_s_subs)
        fmri_l_analyzed=list(fmri_l_omit)+list(fmri_l_subs)
        
        
    if 'NM' not in itype:
        nm_s_analyzed=list(nm_s_omit)
        nm_l_analyzed=list(nm_l_omit)
    elif 'NM' in itype:
        nm_s_analyzed=list(nm_s_omit)+list(nm_s_subs)
        nm_l_analyzed=list(nm_l_omit)+list(nm_l_subs)
    
    subs_ls=pd.DataFrame([fmri_l_analyzed, fmri_s_analyzed, 
                          t1_l_analyzed, t1_s_analyzed, 
                          dti_l_analyzed, dti_s_analyzed,
                          nm_l_analyzed, nm_s_analyzed])
    subs_ls=subs_ls.transpose()
    subs_ls.columns=['Longitudinal fMRI Subjects','Single Aqc fMRI Subjects','Longitudinal T13D Subjects','Single Aqc T13D Subjects','Longitudinal DTI Subjects','Single Aqc DTI Subjects','Longitudinal NM Subjects','Single Aqc NM Subjects']
    
    subs_ls.to_csv('ANALYZED_SUBJECTS_LIST_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)
    
    print('Image Fetcher completed succesfully')
    
    
if not analyzed:
    
    if 'T13D' not in itype:
        t1_s_subs=[]
        t1_l_subs=[]
        
    if 'DTI' not in itype:
        dti_s_subs=[]
        dti_l_subs=[]
    
    if 'fMRI' not in itype:
        fmri_s_subs=[]
        fmri_l_subs=[]
        
    if 'NM' not in itype:
        nm_s_subs=[]
        nm_l_subs=[]
    
    subs_ls=pd.DataFrame([fmri_l_subs, fmri_s_subs, t1_l_subs, t1_s_subs, dti_l_subs, dti_s_subs ,nm_l_subs, nm_s_subs])
    subs_ls=subs_ls.transpose()
    subs_ls.columns=['Longitudinal fMRI Subjects','Single Aqc fMRI Subjects','Longitudinal T13D Subjects','Single Aqc T13D Subjects','Longitudinal DTI Subjects','Single Aqc DTI Subjects','Longitudinal NM Subjects','Single Aqc NM Subjects']
    
    subs_ls.to_csv('ANALYZED_SUBJECTS_LIST_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)
    
    print('Image Fetcher completed succesfully')