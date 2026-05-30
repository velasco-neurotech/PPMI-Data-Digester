# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 15:27:43 2024
  __  __      _            _       _              _                ___       _.--. 
 |  \/  |    | |          | |     | |             \`.|\..----...-'`   `-._.-'_.-'` 
 | \  / | ___| |_ __ _  __| | __ _| |_ __ _       /  ' `         ,       __.--'               
 | |\/| |/ _ \ __/ _` |/ _` |/ _` | __/ _` |      )/' _/     \   `-_,   /         
 | |  | |  __/ || (_| | (_| | (_| | || (_| |      `-'" `"\_  ,_.-;_.-\_ ',  
 |_|  |_|\___|\__\__,_|\__,_|\__,_|\__\__,_|         _.-'_./   {_.'   ; /
  _____       __ _                                  {_.-``-'         {_/   
 |  __ \     / _(_)                
 | |__) |___| |_ _ _ __   ___ _ __ 
 |  _  // _ \  _| | '_ \ / _ \ '__|
 | | \ \  __/ | | | | | |  __/ |   
 |_|  \_\___|_| |_|_| |_|\___|_| 
 


@author: Miguel Velasco

>------Version Control 1.0:
    
Este programa intenta organizar la base de datos para hacer una comparación entre los pacientes con datos
de fMRI y el número de sesiones que tienen fMRI. Este programa trabaja con el csv de metadatos proveniente 
de las descargas de la base de datos del PPMI. Es indiferente si son casos o controles, funciona para ambas.

Primero abre el archivo de metadatos directamente como fue descargado desde el PPMI, ignora los elementos 
que estén clasificados como PET, SPECT y CT. Considera los datos de las imágenes que sean provenientes 
de resonancia magnética como las DTI, fMRI y las estructurales 3D.

Después genera el archivo Log de la sesión llamado 'Session Log File' que incluye el nombre de la sesión 
especificado al inicio del programa y también el nombre del operador. 

El siguiente bloque de código consta de correccciones en la modalidad, ya que en la base de datos hay varias
imágenes mal catalogadas en la modalidad de acuerdo al nombre de la secuencia que se hizo. Primero hay que 
seleccionar todas la secuencias que estaban catalogadas como 'fMRI' para moverlas a la modalidad 'MRI'. Luego 
el paso inverso, mover la que están catalogadas como MRI pero pertenecen a  fMRI. Después las secuencias que se
encuentran nombradas como DTI pero no corresponden a DTI. Y las que están en MRI pero en realidad son secuecias DTI.

Después de haber hecho las correcciones manuales se genera una lista de cuáles fueron las secuencias 
corregidas por categoría. También se inlcuye en el log la nueva lista de secuencias que fueron incluidas por categoría.

El paso que sigue es seleccionar todas las secuencias que se encutran en la modalidad estructural (MRI) pero 
son de neuromelanina (NM), se crea una sub-base interna donde se renombra la categoría de estas secuencias a 'NM', 
esta base interna también se exporta como 'INTERNAL_[NAME]' y también graba en el Session Log File los nombres de 
las secuencias que se consideraron como Neuromelanina.

Luego se tienen que seleccionar las secuencias estructurales que corresponden a T1 3D (MP-RAGE, BRAVO)

>--------------------- 2.0

Se remueven funciones de plot y se pasan al archivo Metadata Plotter para no tener que volver a correr 
el refinador cuando se quiere hacer únicamente el plot.

Se añade en el log poner los ids de sujeto según la modalidad para los longitudinales y singles

"""
#%%Imports

VER='2.0'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import easygui as eg
import os                #Sirve para el Manejo de archivos
from datetime import datetime 
import pandas as pd
#import time
os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]


#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Metadata Refiner "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Operator Name
message = 'Please input Operator Name or ID'
title = "Metadata Refiner "+VER+" - Start"
oname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Metadata Refiner "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Metadata File'
title = "Metadata Refiner "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
fl_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)

#%%Session Log File 

#Further Notes: Probablemente agregar un check si ya existe una sesión con ese nombre y pedir si 
#se reemplaza el archivo o si solamente se actualiza como la parte 2 del análisis, aunque técnicamente
#podría ser innecesario.

with open (sname+' - Session Log File.txt', 'w') as savefile:
    savefile.write(' __  __      _            _       _ \n')        
    savefile.write('|  \/  |    | |          | |     | |\n')        
    savefile.write('| \  / | ___| |_ __ _  __| | __ _| |_ __ _\n')  
    savefile.write('| |\/| |/ _ \ __/ _` |/ _` |/ _` | __/ _` |\n') 
    savefile.write('| |  | |  __/ || (_| | (_| | (_| | || (_| |\n') 
    savefile.write('|_|  |_|\___|\__\__,_|\__,_|\__,_|\__\__,_|\n') 
    savefile.write(' _____       __ _                 \n')
    savefile.write('|  __ \     / _(_)                \n')
    savefile.write('| |__) |___| |_ _ _ __   ___ _ __ \n')
    savefile.write('|  _  // _ \  _| | ´_ \ / _ \ ´__|\n')
    savefile.write('| | \ \  __/ | | | | | |  __/ |   \n')
    savefile.write('|_|  \_\___|_| |_|_| |_|\___|_| \n')
    savefile.write('Created By: NeuroSc Miguel Velasco-Orozco \u00A9 2024\nVersion Control: '+VER+'\n\n\n')
    savefile.write('Session Name: '+sname+'\n\n')
    savefile.write('Operator Name: '+oname+'\n\n')
    savefile.write('Working File Route: \n'+fl_path+'\n\n')
    savefile.write('Save Folder Route: \n'+sv_path+'\n\n\n')
    savefile.write('Start Timestamp: '+str(datetime.now())+'\n')
    
#%%File open 

#--------Read File and ignore irrelevant columns
csvfile = pd.read_csv(fl_path)  
or_data=csvfile.iloc[:,0:11] 

#%% Data filter & Log 

removal_counter=or_data['Modality'].value_counts()

#Remove PET data 
if any(or_data['Modality']=='PET'):
    filt_data=or_data[or_data['Modality']!='PET']  #Filtered dataframe ignoring non-MR images
else:
    filt_data = or_data

#Remove SPECT data 
if any(or_data['Modality']=='SPECT'):
    filt_data=filt_data[filt_data['Modality']!='SPECT']

#Remove CT data 
if any(or_data['Modality']=='CT'):
    filt_data=filt_data[filt_data['Modality']!='CT']
    
#Remove DTI data 
#filt_data=filt_data[filt_data['Modality']!='DTI']


#----------Data change log file

with open (sname+' - Session Log File.txt', 'a') as dcfile:
    dcfile.write('\n\n\n---------DATA CHANGE LOG--------\n\n')
    dcfile.write('>Number of Original Images: '+str(len(or_data))+'\n\nEXCLUSIONS:\n')
    
    if any(or_data['Modality']=='PET'):
        dcfile.write('Number of PET images excluded: '+str(removal_counter['PET'])+'\n')
    
    if any(or_data['Modality']=='SPECT'):
        dcfile.write('Number of SPECT images excluded: '+str(removal_counter['SPECT'])+'\n')
    
    if any(or_data['Modality']=='CT'):
        dcfile.write('Number of CT images excluded: '+str(removal_counter['CT'])+'\n')
    
    #dcfile.write('Number of DTI images excluded: '+str(removal_counter['DTI'])+'\n\n')
    if any(or_data['Modality']=='CT') & any(or_data['Modality']=='PET') & any(or_data['Modality']=='SPECT'):
        dcfile.write('>Number of Excluded Images: '+str(removal_counter['PET']+removal_counter['SPECT']+
                                                        removal_counter['CT'])+'\n\nINCLUSIONS:\n')
                                                   #removal_counter['DTI'])+'\n\nINCLUSIONS:\n')
    dcfile.write('Number of fMRI (Pre Revised) images included: '+str(removal_counter['fMRI'])+'\n')
    dcfile.write('Number of MRI (Pre Revision) images included: '+str(removal_counter['MRI'])+'\n')
    dcfile.write('Number of DTI (Pre Revision) images included: '+str(removal_counter['DTI'])+'\n\n')
    dcfile.write('>Number of Included Images: '+str(len(filt_data))+'\n')

#%%Unique Sequence Extraction 

#Obtain all descriptions conditional to modality
fmri_seq=filt_data[filt_data['Modality']=='fMRI']['Description'].value_counts()
mri_seq=filt_data[filt_data['Modality']=='MRI']['Description'].value_counts()
dti_seq=filt_data[filt_data['Modality']=='DTI']['Description'].value_counts()

#Choices List to move from one modality to other 
fmri_choices = ['None to move']
mri_choices = ['None to move']
dti_choices = ['None to move']

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n\n---------UNIQUE SEQUENCE LOG--------\n')
    seqfile.write('(Sequences pre fMRI/DTI revision)\n\n\n')
    seqfile.write('>fMRI Unique Sequences \n\n')
    for i in range(len(fmri_seq.index)): #Write names of unique fMRI sequences
        seqfile.write(str(fmri_seq.index[i])+' ............ '+str(fmri_seq[i])+'\n')
        fmri_choices.append(str(fmri_seq.index[i]))

    seqfile.write('\n\n>MRI Unique Sequences \n\n')
    for i in range(len(mri_seq.index)): #Write names of unique MRI sequences
        seqfile.write(str(mri_seq.index[i])+' ............ '+str(mri_seq[i])+'\n')
        mri_choices.append(str(mri_seq.index[i]))
    
    seqfile.write('\n\n>DTI Unique Sequences \n\n')
    for i in range(len(dti_seq.index)): #Write names of unique DTI sequences
        seqfile.write(str(dti_seq.index[i])+' ............ '+str(dti_seq[i])+'\n')
        dti_choices.append(str(dti_seq.index[i]))

#%%fMRI to MRI correction 

text = 'Please select sequences to change from Modality fMRI to MRI \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - fMRI to MRI Revision"
fmri_to_mri = eg.multchoicebox(text, title, fmri_choices)

if 'None to move' in fmri_to_mri:
    
    fmri_to_mri = ['None to move']
    title = "Metadata Refiner "+VER+" - fMRI to MRI Confirmation"
    message = "NO sequences will be renamed from fMRI to MRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
    
else:

    title = "Metadata Refiner "+VER+" - fMRI to MRI Confirmation"
    message = "Sequences selected  : " + str(fmri_to_mri)+"\n\n\nSelected sequences will be renamed from fMRI to MRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

#%%MRI to fMRI correction

text = 'Please select sequences to change from Modality MRI to fMRI \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - MRI to fMRI Revision"
mri_to_fmri = eg.multchoicebox(text, title, mri_choices)

if 'None to move' in mri_to_fmri:
    
    mri_to_fmri = ['None to move']
    title = "Metadata Refiner "+VER+" - MRI to fMRI Confirmation"
    message = "NO sequences will be renamed from MRI to fMRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
    
else:
    
    title = "Metadata Refiner "+VER+" - MRI to fMRI Confirmation"
    message = "Sequences selected  : " + str(mri_to_fmri)+"\n\n\nSelected sequences will be renamed from MRI to fMRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

#%%DTI to MRI correction

text = 'Please select sequences to change from Modality DTI to MRI \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - MRI to DTI Revision"
dti_to_mri = eg.multchoicebox(text, title, dti_choices)

if 'None to move' in dti_to_mri:
    
    dti_to_mri = ['None to move']
    title = "Metadata Refiner "+VER+" - DTI to MRI Confirmation"
    message = "NO sequences will be renamed from DTI to MRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
    
else:
    
    title = "Metadata Refiner "+VER+" - DTI to MRI Confirmation"
    message = "Sequences selected  : " + str(dti_to_mri)+"\n\n\nSelected sequences will be renamed from DTI to MRI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

#%%MRI to DTI correction

text = 'Please select sequences to change from Modality MRI to DTI \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - MRI to DTI Revision"
mri_to_dti = eg.multchoicebox(text, title, [x for x in mri_choices if x not in mri_to_fmri])

if 'None to move' in mri_to_dti:
    
    mri_to_dti = ['None to move']
    title = "Metadata Refiner "+VER+" - MRI to DTI Confirmation"
    message = "NO sequences will be renamed from MRI to DTI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
    
else:
    
    title = "Metadata Refiner "+VER+" - MRI to DTI Confirmation"
    message = "Sequences selected  : " + str(mri_to_dti)+"\n\n\nSelected sequences will be renamed from MRI to DTI.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
#%%Log File Sequence Update

with open (sname+' - Session Log File.txt', 'a') as chngfile:
    chngfile.write('\n\n\n---------SEQUENCE REVISION AND CHANGE LOG--------\n\n')
    chngfile.write('>Sequences Changed from fMRI to MRI modality\n\n')
    
    if 'None to move' in fmri_to_mri:  #Revised fMRI to MRI images
        chngfile.write('No fMRI to MRI sequences changed\n')
    else:
        c = 0 
        for i in fmri_to_mri:
            chngfile.write(i+' ............ '+str(fmri_seq[i])+'\n')
            c += fmri_seq[i]
        chngfile.write('\nTotal fMRI to MRI image indexes changed: '+str(c))
    
    
    if 'None to move' in mri_to_fmri: #Revised MRI to fMRI images
        chngfile.write('No MRI to fMRI sequences changed\n') 
    else:
        c = 0 
        chngfile.write('\n\n>Sequences Changed from MRI to fMRI modality\n\n')
        for i in mri_to_fmri:
            chngfile.write(i+' ............ '+str(mri_seq[i])+'\n')
            c += mri_seq[i]
        chngfile.write('\nTotal MRI to fMRI image indexes changed: '+str(c))
        
    
    if 'None to move' in dti_to_mri: #Revised DTI to MRI images
        chngfile.write('No DTI to MRI sequences changed\n')   
    else:
        c = 0 
        chngfile.write('\n\n>Sequences Changed from DTI to MRI modality\n\n')
        for i in dti_to_mri:
            chngfile.write(i+' ............ '+str(dti_seq[i])+'\n')
            c += dti_seq[i]
        chngfile.write('\nTotal DTI to MRI image indexes changed: '+str(c))
    
    
    if 'None to move' in mri_to_dti: #Revised MRI to DTI images
        chngfile.write('No MRI to DTI sequences changed\n')   
    else:
        c = 0 
        chngfile.write('\n\n>Sequences Changed from MRI to DTI modality\n\n')
        for i in mri_to_dti:
            chngfile.write(i+' ............ '+str(mri_seq[i])+'\n')
            c += mri_seq[i]
        chngfile.write('\nTotal MRI to fMRI image indexes changed: '+str(c))

#%%Modality renaming

#New dataframe with corrected modality
revised_data = filt_data


if 'None to move' not in fmri_to_mri:
    for i in fmri_to_mri:
        revised_data.loc[filt_data['Description']==i,'Modality']='MRI' #Find sequence by description but change in row modality

if 'None to move' not in mri_to_fmri:
    for i in mri_to_fmri:
        revised_data.loc[filt_data['Description']==i,'Modality']='fMRI' #Find sequence by description but change in row modality
        
if 'None to move' not in mri_to_dti:
    for i in mri_to_dti:
        revised_data.loc[filt_data['Description']==i,'Modality']='DTI' #Find sequence by description but change in row modality
        
if 'None to move' not in dti_to_mri:
    for i in dti_to_mri:
        revised_data.loc[filt_data['Description']==i,'Modality']='MRI' #Find sequence by description but change in row modality
    

#%% New Unique sequences report card

#Extract new unique sequences by modality 
rev_fmri_seq=revised_data[revised_data['Modality']=='fMRI']['Description'].value_counts()
rev_mri_seq=revised_data[revised_data['Modality']=='MRI']['Description'].value_counts()
rev_dti_seq=revised_data[revised_data['Modality']=='DTI']['Description'].value_counts()

rev_mri_choices = ['No Neuromelanin sequences']  #Choices to select neuromelanin

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n\n---------REVISED UNIQUE SEQUENCE LOG--------\n')
    seqfile.write('>fMRI Unique Sequences (Revised) \n\n')
    for i in range(len(rev_fmri_seq.index)):
        seqfile.write(str(rev_fmri_seq.index[i])+' ............ '+str(rev_fmri_seq[i])+'\n')
        
    
    seqfile.write('\n\n>MRI Unique Sequences (Revised)\n\n')
    for i in range(len(rev_mri_seq.index)):
        seqfile.write(str(rev_mri_seq.index[i])+' ............ '+str(rev_mri_seq[i])+'\n')
        rev_mri_choices.append(str(rev_mri_seq.index[i])) #Neuromelanin sequences are in MRI category
    
    
    seqfile.write('\n\n>DTI Unique Sequences (Revised)\n\n')
    for i in range(len(rev_dti_seq.index)):
        seqfile.write(str(rev_dti_seq.index[i])+' ............ '+str(rev_dti_seq[i])+'\n')
        
    seqfile.write('\n\nNumber of fMRI (Revised) images included: '+str(revised_data['Modality'].value_counts()['fMRI'])+'\n')
    seqfile.write('Number of MRI (Revised) images included: '+str(revised_data['Modality'].value_counts()['MRI'])+'\n')
    seqfile.write('Number of DTI (Revised) images included: '+str(revised_data['Modality'].value_counts()['DTI'])+'\n\n')
    seqfile.write('>Number of Included Images: '+str(len(revised_data))+'\n')

#%%Neuromelanin Selection

text = 'Please select sequences corresponding to Neuromelanin \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - NM Selection"
nm_seq = eg.multchoicebox(text, title, rev_mri_choices)

if 'No Neuromelanin sequences' in nm_seq:
    
    nm_seq = ['No Neuromelanin sequences']
    title = "Metadata Refiner "+VER+" - NM Seq Confirmation"
    message = "NO Neuromelanin sequences will be selected.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

else:
    title = "Metadata Refiner "+VER+" - NM Seq Confirmation"
    message = "Sequences selected  : " + str(nm_seq)+"\n\n\nSelected sequences are Neuromelanin sequences.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)
    
#%%Neuromelanin & internal dataframe

#Create an internal dataframe to add Neuromelanin (NM) as a modality value. Does not export to main CSV but in Internal
revised_data_internal = revised_data

if 'No Neuromelanin sequences' not in nm_seq:
    for i in nm_seq:
        revised_data_internal.loc[revised_data['Description']==i,'Modality']='NM' #Find sequence by description but change in row modality

 
#%% Neuromelanin sequences report card 


with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n\n----------NEUROMELANIN SEQUENCE LOG----------\n')
    seqfile.write('\n>Neuromelanin sequences extracted from revised MRI Modality Sequences\n\n')
    c=0
    for i in nm_seq:
        seqfile.write(i+' ............ '+str(rev_mri_seq[rev_mri_seq.index==i][0])+'\n')
        c+=rev_mri_seq[rev_mri_seq.index==i][0]
    
    seqfile.write('\n\nNumber of Neuromelanin Images: '+str(c))
    
#%% T1 3D Structural selection 

rev_mri_seq_2=revised_data_internal[revised_data_internal['Modality']=='MRI']['Description'].value_counts()
rev_mri_choices_2 =['No T1 3D Sequences']

for i in range(len(rev_mri_seq_2.index)):
    rev_mri_choices_2.append(rev_mri_seq_2.index[i])

text = 'Please select sequences corresponding to T1 3D \n\nREMEMBER FIRST CHOICE IS SELECTED BY DEFAULT; DESELECT MANUALLY'
title = "Metadata Refiner "+VER+" - T1 3D Selection"
t1_seq = eg.multchoicebox(text, title, rev_mri_choices_2)

if 'No T1 3D Sequences' in t1_seq:
    
    t1_seq = ['No T1 3D Sequences']
    title = "Metadata Refiner "+VER+" - T1 3D Seq Confirmation"
    message = "NO T1 3D sequences will be selected.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

else:
    title = "Metadata Refiner "+VER+" - T1 3D Seq Confirmation"
    message = "Sequences selected  : " + str(t1_seq)+"\n\n\nSelected sequences are T1 3D sequences.\n\nDo you wish to continue?"
    continuar = eg.ccbox(message, title)

#%% T1 3D internal dataframe naming 

if 'No T1 3D Sequences' not in t1_seq:
    for i in t1_seq:
        revised_data_internal.loc[revised_data['Description']==i,'Modality']='T13D' #Find sequence by description but change in row modality

#%% T1 3D sequences report card 


with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n\n----------T1 3D SEQUENCE LOG----------\n')
    seqfile.write('\n>T1 3D sequences extracted from revised MRI Modality Sequences\n\n')
    c=0
    for i in t1_seq:
        seqfile.write(i+' ............ '+str(rev_mri_seq_2[rev_mri_seq_2.index==i][0])+'\n')
        c+=rev_mri_seq_2[rev_mri_seq_2.index==i][0]
    
    seqfile.write('\n\nNumber of T1 3D Images: '+str(c))
    
#%%CSV file generation 

revised_data.to_csv('REVISED_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)

#%% Internal CSV file generation 

revised_data_internal.to_csv('INTERNAL_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)

#%%------------------------------PART 2: Subject Extraction------------------------------
#%% Number of subjects with fMRI 


subj_fmri= revised_data_internal[revised_data_internal['Modality']=='fMRI']['Subject'].value_counts()
long_fmri=[] #list of longitudinal subjects
singles_fmri=[] #list of singles subjects

plt.figure()
plt.title(sname+' fMRI subject dates')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=200))

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0
m = 0 #Max number of acquisitions counter
M=0  #Male-Female Counters
F=0
M2=0
F2=0
tba=[] #time between appointments
aqnum=[] #Number of acquisitions per subject

for j,i in enumerate(subj_fmri.index):
    aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Acq Date'].value_counts()
    
    if len(aqdate.index) >1:
        long_fmri.append(i)
        aqnum.append(len(aqdate.index))
        c+=1
        #Max number of acquisitions
        if len(aqdate.index)>m:
            m = len(aqdate.index)
            
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='o', color='Steelblue')
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='o', color='Violet')
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        singles_fmri.append(i)
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Midnightblue', marker='o')
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Darkviolet', marker='o')
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
#plt.savefig('fMRI Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Longitudinal Subjects: '+str(c))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure()
plt.title(sname+' Days Between Appointments: fMRI Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.legend()
#plt.savefig('fMRI TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n\n----------SUBJECT DATA PER SEQUENCE LOG----------\n')
    seqfile.write('\n>fMRI Modality:')
    seqfile.write('\nTotal Longitudinal Subjects: '+str(c))
    seqfile.write('\nMale Longitudinal Subjects: '+str(M))
    seqfile.write('\nFemale Longitudinal Subjects: '+str(F))
    seqfile.write('\nTotal Single Acquisition Subjects: '+str(c2))
    seqfile.write('\nMale Single Subjects: '+str(M2))
    seqfile.write('\nFemale Single Subjects: '+str(F2))
    seqfile.write('\nMax Acquisition Times : '+str(m))
    seqfile.write('\nMean Acquisition Times: %.2f'%(np.mean(aqnum)))
    seqfile.write('\nStandard deviation Acquisition Times: %.2f'%(np.std(aqnum)))
    seqfile.write('\nMean Days Between Appointments: %.2f'%(np.mean(tba)))
    seqfile.write('\nStandard deviation Days Between Appointments: %.2f'%(np.std(tba)))
    

#%% Number of subjects with NM

subj_nm= revised_data_internal[revised_data_internal['Modality']=='NM']['Subject'].value_counts()
long_nm=[] #list of longitudinal subjects
singles_nm=[] #list of singles subjects

plt.figure()
plt.title(sname+' NM subject dates')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=200))

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0
m = 0
M=0  #Male-Female Countera
F=0
M2=0
F2=0
tba=[] #Time between appointments
aqnum=[] #Number of acquisitions per subject

for j,i in enumerate(subj_nm.index):
    aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Acq Date'].value_counts()
    if len(aqdate.index) >1:
        long_nm.append(i)
        aqnum.append(len(aqdate.index))
        c+=1
        if len(aqdate.index)>m:
            m = len(aqdate.index)
            
        x=[]
        y=[]
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
            
        x.sort()
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='o', color='Steelblue')
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='o', color='Violet')
            F+=1
        
        
        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
                        
    else:
        c2+=1
        singles_nm.append(i)
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Midnightblue', marker='o')
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Darkviolet', marker='o')
            F2+=1
        
        #plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='k', marker='o')

plt.gcf().autofmt_xdate()
#plt.savefig('NM Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)      

 
print('Total Subjects: '+str(c))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))

plt.figure()
plt.title(sname+' Days Between Appointments: NM Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.legend()
#plt.savefig('NM TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n>Neuromelanin Modality:')
    seqfile.write('\nTotal Longitudinal Subjects: '+str(c))
    seqfile.write('\nMale Longitudinal Subjects: '+str(M))
    seqfile.write('\nFemale Longitudinal Subjects: '+str(F))
    seqfile.write('\nTotal Single Acquisition Subjects: '+str(c2))
    seqfile.write('\nMale Single Subjects: '+str(M2))
    seqfile.write('\nFemale Single Subjects: '+str(F2))
    seqfile.write('\nMax Acquisition Times : '+str(m))
    seqfile.write('\nMean Acquisition Times: %.2f'%(np.mean(aqnum)))
    seqfile.write('\nStandard deviation Acquisition Times: %.2f'%(np.std(aqnum)))
    seqfile.write('\nMean Days Between Appointments: %.2f'%(np.mean(tba)))
    seqfile.write('\nStandard deviation Days Between Appointments: %.2f'%(np.std(tba)))

#%% Number of subjects with T1 3D 


subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
long_t1=[] #list of longitudinal subjects
singles_t1=[] #List of singles subjects

plt.figure()
plt.title(sname+' T1 3D subject dates')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=200))

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0
m = 0
M=0  #Male-Female Countera
F=0
M2=0
F2=0
tba=[] #time between appointments
aqnum=[] #Number of acquisitions per subject

for j,i in enumerate(subj_t1.index):
    aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
    if len(aqdate.index) >1:
        long_t1.append(i)
        aqnum.append(len(aqdate.index))
        c+=1
        #Max number of acquisitions
        if len(aqdate.index)>m:
            m = len(aqdate.index)
            
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='o', color='Steelblue')
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='o', color='Violet')
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        singles_t1.append(i)
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Midnightblue', marker='o')
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Darkviolet', marker='o')
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
#plt.savefig('T13D Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Subjects: '+str(c))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))

plt.figure()
plt.title(sname+' Days Between Appointments: T1 3D Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.legend()
#plt.savefig('T13D TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n>T1 3D Modality:')
    seqfile.write('\nTotal Longitudinal Subjects: '+str(c))
    seqfile.write('\nMale Longitudinal Subjects: '+str(M))
    seqfile.write('\nFemale Longitudinal Subjects: '+str(F))
    seqfile.write('\nTotal Single Acquisition Subjects: '+str(c2))
    seqfile.write('\nMale Single Subjects: '+str(M2))
    seqfile.write('\nFemale Single Subjects: '+str(F2))
    seqfile.write('\nMax Acquisition Times : '+str(m))
    seqfile.write('\nMean Acquisition Times: %.2f'%(np.mean(aqnum)))
    seqfile.write('\nStandard deviation Acquisition Times: %.2f'%(np.std(aqnum)))
    seqfile.write('\nMean Days Between Appointments: %.2f'%(np.mean(tba)))
    seqfile.write('\nStandard deviation Days Between Appointments: %.2f'%(np.std(tba)))

#%% Number of subjects with DTI


subj_dti= revised_data_internal[revised_data_internal['Modality']=='DTI']['Subject'].value_counts()
long_dti=[] #list of longitudinal subjects
singles_dti=[] #list of single subjects


plt.figure(figsize=(7,7))
plt.title(sname+' DTI subject dates')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=200))

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0
m = 0
M=0  #Male-Female Countera
F=0
M2=0
F2=0
tba=[] #time between appointments
aqnum=[] #Number of acquisitions per subject

for j,i in enumerate(subj_dti.index):
    aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
    if len(aqdate.index) >1:
        long_dti.append(i)
        aqnum.append(len(aqdate.index))
        c+=1
        #Max number of acquisitions
        if len(aqdate.index)>m:
            m = len(aqdate.index)
            
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='o', color='Steelblue')
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='o', color='Violet')
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        singles_dti.append(i)
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Midnightblue', marker='o')
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Darkviolet', marker='o')
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
#plt.savefig('DTI Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Subjects: '+str(c))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure(figsize=(7,7))
plt.title(sname+' Days Between Appointments: DTI Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.legend()
#plt.savefig('DTI TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))

with open (sname+' - Session Log File.txt', 'a') as seqfile:
    seqfile.write('\n\n>DTI Modality:')
    seqfile.write('\n-Total Longitudinal Subjects: '+str(c))
    seqfile.write('\nMale Longitudinal Subjects: '+str(M))
    seqfile.write('\nFemale Longitudinal Subjects: '+str(F))
    seqfile.write('\n-Total Single Acquisition Subjects: '+str(c2))
    seqfile.write('\nMale Single Subjects: '+str(M2))
    seqfile.write('\nFemale Single Subjects: '+str(F2))
    seqfile.write('\nMax Acquisition Times : '+str(m))
    seqfile.write('\nMean Acquisition Times: %.2f'%(np.mean(aqnum)))
    seqfile.write('\nStandard deviation Acquisition Times: %.2f'%(np.std(aqnum)))
    seqfile.write('\nMean Days Between Appointments: %.2f'%(np.mean(tba)))
    seqfile.write('\nStandard deviation Days Between Appointments: %.2f'%(np.std(tba)))

#%% Subject file generation

subs_ls=pd.DataFrame([long_fmri, singles_fmri, long_t1, singles_t1, long_dti, singles_dti ,long_nm, singles_nm])
subs_ls=subs_ls.transpose()
subs_ls.columns=['Longitudinal fMRI Subjects','Single Aqc fMRI Subjects','Longitudinal T13D Subjects','Single Aqc T13D Subjects','Longitudinal DTI Subjects','Single Aqc DTI Subjects','Longitudinal NM Subjects','Single Aqc NM Subjects']

subs_ls.to_csv('SUBJECTS_LIST_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)

