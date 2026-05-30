# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:40:36 2024
  __  __      _            _       _        
 |  \/  |    | |          | |     | |       
 | \  / | ___| |_ __ _  __| | __ _| |_ __ _ 
 | |\/| |/ _ \ __/ _` |/ _` |/ _` | __/ _` |
 | |  | |  __/ || (_| | (_| | (_| | || (_| |
 |_|__|_|\___|\__\__,_|\__,_|\__,_|\__\__,_|
  _____  _       _   _
 |  __ \| |     | | | |                     
 | |__) | | ___ | |_| |_ ___ _ __           
 |  ___/| |/ _ \| __| __/ _ \ '__|          
 | |    | | (_) | |_| ||  __/ |             
 |_|    |_|\___/ \__|\__\___|_|   

  

@author: Miguel Velasco         
                                
Usar el archivo INTERNAL de Metadata Refiner
    
"""

VER='1.0'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import easygui as eg
import os                #Sirve para el Manejo de archivos
from datetime import datetime 
import pandas as pd
import seaborn as sns
#import time
os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]


#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Metadata Plotter "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

# #Operator Name
# message = 'Please input Operator Name or ID'
# title = "Metadata Plotter "+VER+" - Start"
# oname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Metadata Plotter "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Metadata Internal Refined File'
title = "Metadata Plotter "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
fl_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)


#%%File open 

#--------Read File and ignore irrelevant columns
csvfile = pd.read_csv(fl_path)  
revised_data_internal=csvfile.iloc[:,0:11] 


#%% Number of subjects with fMRI 

unsorted_subj_fmri= revised_data_internal[revised_data_internal['Modality']=='fMRI']['Subject'].value_counts()
subj_fmri=unsorted_subj_fmri.sort_index()
long_fmri=[] #list of longitudinal subjects

plt.figure(figsize=(7,7))
plt.suptitle(sname+' \nfMRI Acquisition Dates', fontsize=16 )
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0 #Single Acq Subject counter
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
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.7)
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.7)
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Teal', marker='.', alpha =0.7)
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Peru', marker='.', alpha=0.7)
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
plt.title('Total Longitudinals: '+str(c)+' Total Singles: '+str(c2), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
         Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
         Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
         Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('fMRI Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Longitudinal Subjects: '+str(c))
print('Total Single Acq Subjects: '+str(c2))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure(figsize=(7,7))
plt.title(sname+'\n Days Between Appointments: fMRI Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.xlabel('Days Between Appointments')
plt.ylabel('Number of subjects')
plt.legend()
plt.savefig('fMRI TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))


#%% Number of subjects with NM

unsorted_subj_nm= revised_data_internal[revised_data_internal['Modality']=='NM']['Subject'].value_counts()
subj_nm=unsorted_subj_nm.sort_index()
long_nm=[] #list of longitudinal subjects

plt.figure(figsize=(7,7))
plt.suptitle(sname+' \nNeuromelanin Acquisition Dates', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0 #Single Acq Subject counter
m = 0 #Max number of acquisitions counter
M=0  #Male-Female Counters
F=0
M2=0
F2=0
tba=[] #time between appointments
aqnum=[] #Number of acquisitions per subject

for j,i in enumerate(subj_nm.index):
    aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Acq Date'].value_counts()
    
    if len(aqdate.index) >1:
        long_nm.append(i)
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
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.7)
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.7)
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Teal', marker='.', alpha =0.7)
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Peru', marker='.', alpha=0.7)
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
plt.title('Total Longitudinals: '+str(c)+' Total Singles: '+str(c2), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
         Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
         Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
         Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('NM Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Longitudinal Subjects: '+str(c))
print('Total Single Acq Subjects: '+str(c2))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure(figsize=(7,7))
plt.title(sname+'\n Days Between Appointments: Neuromelanin Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.xlabel('Days Between Appointments')
plt.ylabel('Number of subjects')
plt.legend()
plt.savefig('NM TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))


#%% Number of subjects with T1 3D 


unsorted_subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
subj_t1=unsorted_subj_t1.sort_index()
long_t1=[] #list of longitudinal subjects

plt.figure(figsize=(7,7))
plt.suptitle(sname+' \nStructural T1 3D Acquisition Dates', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0 #Single Acq Subject counter
m = 0 #Max number of acquisitions counter
M=0  #Male-Female Counters
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
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.7)
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.7)
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Teal', marker='.', alpha =0.7)
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Peru', marker='.', alpha=0.7)
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
plt.title('Total Longitudinals: '+str(c)+' Total Singles: '+str(c2), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
         Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
         Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
         Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('T13D Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Longitudinal Subjects: '+str(c))
print('Total Single Acq Subjects: '+str(c2))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure(figsize=(7,7))
plt.title(sname+' \nDays Between Appointments: Structural T13D Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.xlabel('Days Between Appointments')
plt.ylabel('Number of subjects')
plt.legend()
plt.savefig('T13D TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))


#%% Number of subjects with DTI


unsorted_subj_dti= revised_data_internal[revised_data_internal['Modality']=='DTI']['Subject'].value_counts()
subj_dti=unsorted_subj_dti.sort_index()
long_dti=[] #list of longitudinal subjects

plt.figure(figsize=(7,7))
plt.suptitle(sname+' \nDiffusion Tensor Acquisition Dates', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

#Longitudinals max values extraction for new dataframe
c = 0 #Longitudinal Subject counter
c2 =0 #Single Acq Subject counter
m = 0 #Max number of acquisitions counter
M=0  #Male-Female Counters
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
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.7)
            M+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.7)
            F+=1

        for a in range(len(x)-1):
            a+=1
            tba.append(int((x[-a]-x[-(a+1)]).total_seconds()/86400))
              
    else:
        c2+=1
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Teal', marker='.', alpha =0.7)
            M2+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(datetime.strptime(aqdate.index[0], '%m/%d/%Y'),j, color ='Peru', marker='.', alpha=0.7)
            F2+=1
        
    
plt.gcf().autofmt_xdate()   
plt.title('Total Longitudinals: '+str(c)+' Total Singles: '+str(c2), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
         Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
         Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
         Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('DTI Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('\n\nTotal Longitudinal Subjects: '+str(c))
print('Total Single Acq Subjects: '+str(c2))
print('Max Aq Dates : '+str(m))
print('Mean Aq times: '+str(np.mean(aqnum)))


plt.figure(figsize=(7,7))
plt.title(sname+'\n Days Between Appointments: Diffusion Tensor Longitudinal')
plt.hist(tba, bins=20)
plt.axvline(np.mean(tba), color='k',label = 'Mean %.2f'%(np.mean(tba)))
plt.axvline(np.mean(tba)-np.std(tba), color='grey',label = 'STD %.2f'%(np.std(tba)))
plt.axvline(np.mean(tba)+np.std(tba), color='grey')
plt.xlabel('Days Between Appointments')
plt.ylabel('Number of subjects')
plt.legend()
plt.savefig('DTI TBA_'+(os.path.basename(fl_path)[:-4])+'_'+sname)

print('Mean days Between Appointments '+str(np.mean(tba)))
print('Standard Deviation days Between Appointments '+str(np.std(tba)))

#%%----------------------------OVERLAPPERS------------------------------------------------------
#%%

#%%---------------------------OVERLAPPER fMRI-T1 3D----------------------------------------------

#---------------ONLY UNCOMMENT IF NOT PLOTTING EVERYTHING ELSE-----------------

# unsorted_subj_fmri= revised_data_internal[revised_data_internal['Modality']=='fMRI']['Subject'].value_counts()
# subj_fmri=unsorted_subj_fmri.sort_index()
# long_fmri=[] #list of longitudinal fmri subjects

# unsorted_subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
# subj_t1=unsorted_subj_t1.sort_index()
# long_t1=[] #list of longitudinal t13d subjects

                
# for j,i in enumerate(subj_fmri.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_fmrii.append(i) 
        
# for j,i in enumerate(subj_t1.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_t1.append(i)    
#------------------------------------------------------------------------------


plt.figure(figsize=(7,7))
plt.suptitle(sname+' \n fMRI - T13D Overlap', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

intersect_long_subjects = list(set(long_t1) & set(long_fmri))
intersect_long_subjects.sort()

for j,i in enumerate(intersect_long_subjects):
    
    if i in long_fmri:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='cornflowerblue')
    
    if i in long_t1:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='tomato', alpha=0.5)
    
    
    
    
plt.gcf().autofmt_xdate()   
plt.title('Total Overlap Subjects: '+str(len(intersect_long_subjects)), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'tomato',label='T13D', marker='>'),
         Line2D([0],[0], color = 'cornflowerblue',label='fMRI', marker='>')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('OVERLAP fMRI-T13D Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

#%%---------------------------OVERLAPPER T1 3D-DTI----------------------------------------------

#---------------ONLY UNCOMMENT IF NOT PLOTTING EVERYTHING ELSE-----------------

# unsorted_subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
# subj_t1=unsorted_subj_t1.sort_index()
# long_t1=[] #list of longitudinal t13d subjects

# unsorted_subj_dti= revised_data_internal[revised_data_internal['Modality']=='DTI']['Subject'].value_counts()
# subj_dti=unsorted_subj_dti.sort_index()
# long_dti=[] #list of longitudinal dti subjects

# for j,i in enumerate(subj_t1.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_t1.append(i)    
        
        
# for j,i in enumerate(subj_dti.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_dti.append(i) 
        
#------------------------------------------------------------------------------


plt.figure(figsize=(7,7))
plt.suptitle(sname+' \n Structural T13D-DTI Overlap', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

intersect_long_subjects = list(set(long_t1) & set(long_dti))
intersect_long_subjects.sort()

for j,i in enumerate(intersect_long_subjects):
    
    if i in long_t1:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='tomato', alpha=1)
    
    if i in long_dti:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='cornflowerblue', alpha=0.5)
    
    
plt.gcf().autofmt_xdate()   
plt.title('Total Overlap Subjects: '+str(len(intersect_long_subjects)), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'tomato',label='T13D', marker='>'),
         Line2D([0],[0], color = 'cornflowerblue',label='DTI', marker='>')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('OVERLAP T13D-DTI Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

#%%---------------------------OVERLAPPER T1 3D-DTI-NM----------------------------------------------

#---------------ONLY UNCOMMENT IF NOT PLOTTING EVERYTHING ELSE-----------------

# unsorted_subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
# subj_t1=unsorted_subj_t1.sort_index()
# long_t1=[] #list of longitudinal t13d subjects

# unsorted_subj_dti= revised_data_internal[revised_data_internal['Modality']=='DTI']['Subject'].value_counts()
# subj_dti=unsorted_subj_dti.sort_index()
# long_dti=[] #list of longitudinal dti subjects

# unsorted_subj_nm= revised_data_internal[revised_data_internal['Modality']=='NM']['Subject'].value_counts()
# subj_nm=unsorted_subj_nm.sort_index()
# long_nm=[] #list of longitudinal nm subjects

# for j,i in enumerate(subj_t1.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_t1.append(i)    
        
        
# for j,i in enumerate(subj_dti.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_dti.append(i) 

# for j,i in enumerate(subj_nm.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_nm.append(i) 
        
#------------------------------------------------------------------------------


plt.figure(figsize=(7,7))
plt.suptitle(sname+' \n Structural T13D-DTI-NM Overlap', fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1,1)))
plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(plt.gca().xaxis.get_major_locator()))
plt.xlabel('Acquisition Year')
plt.ylabel('Subject Number') 

        

#Adding NM over T13D-DTI
intersect_long_subjects = list(set(long_t1) & set(long_dti) ) #General 
intersect_long_subjects.sort()

intersect_long_subjects_2 = list(set(long_t1) & set(long_dti) & set(long_nm)) #Conditional 
intersect_long_subjects_2.sort()

for j,i in enumerate(intersect_long_subjects):
    
    if i in long_t1:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='tomato')
    
    if i in long_dti:
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        plt.plot(x,y,marker='>', color='cornflowerblue', alpha=0.5)

    if i in intersect_long_subjects_2:    
        
        aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Acq Date'].value_counts()
        x=[]
        y=[]
        #Date sorting
        for date in aqdate.index:
            x.append(datetime.strptime(date, '%m/%d/%Y'))
            y.append(j)
        x.sort()
        #plt.scatter(x,y,color='k')
        plt.plot(x,y, color = 'w', linestyle=(0,(1,10)),alpha=0.5, marker ='o', markerfacecolor='k')
            
        
    
plt.gcf().autofmt_xdate()   
plt.title('Total T13D-DTI-NM Overlap Subjects: '+str(len(intersect_long_subjects_2)), loc='right', pad=0, fontsize=10)
legends=[Line2D([0],[0], color = 'tomato',label='T13D', marker='.'),
         Line2D([0],[0], color = 'cornflowerblue',label='DTI', marker='.'),       
         Line2D([0],[0], color = 'w', markerfacecolor='k',label='NM', marker='o')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('OVERLAP T13D-DTI-NM Dates_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   


#%%----------------------------AGE AT ACQUISITION-----------------------------------------------
#%% 


#---------------ONLY UNCOMMENT IF NOT PLOTTING EVERYTHING ELSE-----------------

# unsorted_subj_t1= revised_data_internal[revised_data_internal['Modality']=='T13D']['Subject'].value_counts()
# subj_t1=unsorted_subj_t1.sort_index()
# long_t1=[] #list of longitudinal t13d subjects

# unsorted_subj_dti= revised_data_internal[revised_data_internal['Modality']=='DTI']['Subject'].value_counts()
# subj_dti=unsorted_subj_dti.sort_index()
# long_dti=[] #list of longitudinal dti subjects

# unsorted_subj_nm= revised_data_internal[revised_data_internal['Modality']=='NM']['Subject'].value_counts()
# subj_nm=unsorted_subj_nm.sort_index()
# long_nm=[] #list of longitudinal nm subjects

# for j,i in enumerate(subj_t1.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_t1.append(i)    
        
        
# for j,i in enumerate(subj_dti.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_dti.append(i) 

# for j,i in enumerate(subj_nm.index):
#     aqdate=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Acq Date'].value_counts()
    
#     if len(aqdate.index) >1:
#         long_nm.append(i) 
        
#------------------------------------------------------------------------------


#Ages fMRI 

plt.figure(figsize=(7,7))
ax=plt.gca()
plt.suptitle(sname+' \nfMRI Age at acquisition', fontsize=16 )
plt.xlabel('Age')
plt.ylabel('Subject Number') 

tpp=0 #Total points plotted

aqags=[] #Ages per subject
allages_male_fmri=[]
allages_female_fmri=[]

for j,i in enumerate(subj_fmri.index):
    aqage=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Age'].value_counts()
    
    if len(aqage.index) >1:
        aqags.append(len(aqdate.index))
            
        x=[]
        y=[]
        #Date sorting
        for age in aqage.index:
            x.append(age)
            y.append(j)
        x.sort()
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.4)
            
            for age in x:
                allages_male_fmri.append(age)
                tpp+=1
            
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.4)
            
            for age in x:
                allages_female_fmri.append(age)
                tpp+=1
            
              
    else:
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(aqage.index[0], j, color ='Teal', marker='.', alpha =0.4)
            
            allages_male_fmri.append(aqage.index[0])
            tpp+=1
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='fMRI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(aqage.index[0],j, color ='Peru', marker='.', alpha=0.4)
            
            allages_female_fmri.append(aqage.index[0])
            tpp+=1
        
 
plt.title('Male avg age: %.2f'%np.mean(allages_male_fmri)+'   Female avg age: %.2f'%np.mean(allages_female_fmri), loc='right', pad=0, fontsize=10)
sns.histplot(allages_male_fmri, bins=15, kde=True, color='mediumblue', element='step')
sns.histplot(allages_female_fmri, bins=15, kde=True, color='deeppink', element='step')
ax2=ax.twinx()
ax2.set_ylabel('Density')
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
          Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
          Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
          Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o'),
          Line2D([0],[0], color = 'mediumblue',label='Male Age Density'),
          Line2D([0],[0], color = 'deeppink',label='Female Density')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('fMRI Ages_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

print('Total Ages Plotted fMRI '+str(tpp))

#%% Ages T13D

plt.figure(figsize=(7,7))
ax=plt.gca()
plt.suptitle(sname+' \nT13D Age at acquisition', fontsize=16 )
plt.xlabel('Age')
plt.ylabel('Subject Number') 


aqags=[] #Ages per subject
allages_male_t13d=[]
allages_female_t13d=[]

for j,i in enumerate(subj_t1.index):
    aqage=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Age'].value_counts()
    
    if len(aqage.index) >1:
        aqags.append(len(aqdate.index))
            
        x=[]
        y=[]
        #Date sorting
        for age in aqage.index:
            x.append(age)
            y.append(j)
        x.sort()
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.4)
            
            for age in x:
                allages_male_t13d.append(age)
            
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.4)
            
            for age in x:
                allages_female_t13d.append(age)
            
              
    else:
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] =='M':
            plt.plot(aqage.index[0], j, color ='Teal', marker='.', alpha =0.4)
            
            allages_male_t13d.append(aqage.index[0])
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='T13D')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(aqage.index[0],j, color ='Peru', marker='.', alpha=0.4)
            
            allages_female_t13d.append(aqage.index[0])
        
 
plt.title('Male avg age: %.2f'%np.mean(allages_male_t13d)+'   Female avg age: %.2f'%np.mean(allages_female_t13d), loc='right', pad=0, fontsize=10)
sns.histplot(allages_male_t13d, bins=15, kde=True, color='mediumblue', element='step')
sns.histplot(allages_female_t13d, bins=15, kde=True, color='deeppink', element='step')
ax2=ax.twinx()
ax2.set_ylabel('Density')
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
          Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
          Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
          Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o'),
          Line2D([0],[0], color = 'mediumblue',label='Male Age Density'),
          Line2D([0],[0], color = 'deeppink',label='Female Density')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('T13D Ages_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   


#%% Ages DTI

plt.figure(figsize=(7,7))
ax=plt.gca()
plt.suptitle(sname+' \nDTI Age at acquisition', fontsize=16 )
plt.xlabel('Age')
plt.ylabel('Subject Number') 


aqags=[] #Ages per subject
allages_male_dti=[]
allages_female_dti=[]

for j,i in enumerate(subj_dti.index):
    aqage=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Age'].value_counts()
    
    if len(aqage.index) >1:
        aqags.append(len(aqdate.index))
            
        x=[]
        y=[]
        #Date sorting
        for age in aqage.index:
            x.append(age)
            y.append(j)
        x.sort()
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.4)
            
            for age in x:
                allages_male_dti.append(age)
            
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.4)
            
            for age in x:
                allages_female_dti.append(age)
            
              
    else:
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] =='M':
            plt.plot(aqage.index[0], j, color ='Teal', marker='.', alpha =0.4)
            
            allages_male_dti.append(aqage.index[0])
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='DTI')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(aqage.index[0],j, color ='Peru', marker='.', alpha=0.4)
            
            allages_female_dti.append(aqage.index[0])
        
 
plt.title('Male avg age: %.2f'%np.mean(allages_male_dti)+'   Female avg age: %.2f'%np.mean(allages_female_dti), loc='right', pad=0, fontsize=10)
sns.histplot(allages_male_dti, bins=15, kde=True, color='mediumblue', element='step')
sns.histplot(allages_female_dti, bins=15, kde=True, color='deeppink', element='step')
ax2=ax.twinx()
ax2.set_ylabel('Density')
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
          Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
          Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
          Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o'),
          Line2D([0],[0], color = 'mediumblue',label='Male Age Density'),
          Line2D([0],[0], color = 'deeppink',label='Female Density')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('DTI Ages_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

#%% Ages NM

plt.figure(figsize=(7,7))
ax=plt.gca()
plt.suptitle(sname+' \nNM Age at acquisition', fontsize=16 )
plt.xlabel('Age')
plt.ylabel('Subject Number') 


aqags=[] #Ages per subject
allages_male_nm=[]
allages_female_nm=[]

for j,i in enumerate(subj_nm.index):
    aqage=revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Age'].value_counts()
    
    if len(aqage.index) >1:
        aqags.append(len(aqdate.index))
            
        x=[]
        y=[]
        #Date sorting
        for age in aqage.index:
            x.append(age)
            y.append(j)
        x.sort()
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(x,y,marker='>', color='Steelblue', alpha=0.4)
            
            for age in x:
                allages_male_nm.append(age)
            
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(x,y,marker='>', color='Violet', alpha=0.4)
            
            for age in x:
                allages_female_nm.append(age)
            
              
    else:
        
        #Male-Female color selection
        if revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] =='M':
            plt.plot(aqage.index[0], j, color ='Teal', marker='.', alpha =0.4)
            
            allages_male_nm.append(aqage.index[0])
        
        elif revised_data_internal[(revised_data_internal['Subject']==i) & (revised_data_internal['Modality']=='NM')]['Sex'].value_counts().index[0] == 'F':
            plt.plot(aqage.index[0],j, color ='Peru', marker='.', alpha=0.4)
            
            allages_female_nm.append(aqage.index[0])
        
 
plt.title('Male avg age: %.2f'%np.mean(allages_male_nm)+'   Female avg age: %.2f'%np.mean(allages_female_nm), loc='right', pad=0, fontsize=10)
sns.histplot(allages_male_nm, bins=15, kde=True, color='mediumblue', element='step')
sns.histplot(allages_female_nm, bins=15, kde=True, color='deeppink', element='step')
ax2=ax.twinx()
ax2.set_ylabel('Density')
legends=[Line2D([0],[0], color = 'Steelblue',label='Male Longitudinal', marker='>'),
          Line2D([0],[0], color = 'Violet',label='Female Longitudinal', marker='>'),
          Line2D([0],[0], color = 'w', markerfacecolor='Teal',label='Male Singles', marker='o'),
          Line2D([0],[0], color = 'w', markerfacecolor='Peru',label='Female Singles', marker='o'),
          Line2D([0],[0], color = 'mediumblue',label='Male Age Density'),
          Line2D([0],[0], color = 'deeppink',label='Female Density')]
plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('NM Ages_'+(os.path.basename(fl_path)[:-4])+'_'+sname)   

#%% Ages csv


ages=pd.DataFrame([allages_male_fmri, [np.mean(allages_male_fmri), np.std(allages_male_fmri), len(allages_male_fmri)], 
                   allages_female_fmri,[np.mean(allages_female_fmri), np.std(allages_female_fmri), len(allages_female_fmri)], 
                   allages_male_fmri+allages_female_fmri, [np.mean(allages_male_fmri+allages_female_fmri), np.std(allages_male_fmri+allages_female_fmri), len(allages_male_fmri+allages_female_fmri)],
                   
                   allages_male_t13d, [np.mean(allages_male_t13d), np.std(allages_male_t13d), len(allages_male_t13d)], 
                   allages_female_t13d,[np.mean(allages_female_t13d), np.std(allages_female_t13d), len(allages_female_t13d)], 
                   allages_male_t13d+allages_female_t13d, [np.mean(allages_male_t13d+allages_female_t13d), np.std(allages_male_t13d+allages_female_t13d), len(allages_male_t13d+allages_female_t13d)],
                   
                   allages_male_dti, [np.mean(allages_male_dti), np.std(allages_male_dti), len(allages_male_dti)], 
                   allages_female_dti,[np.mean(allages_female_dti), np.std(allages_female_dti), len(allages_female_dti)], 
                   allages_male_dti+allages_female_dti, [np.mean(allages_male_dti+allages_female_dti), np.std(allages_male_dti+allages_female_dti), len(allages_male_dti+allages_female_dti)],
                   
                   allages_male_nm, [np.mean(allages_male_nm), np.std(allages_male_nm), len(allages_male_nm)], 
                   allages_female_nm,[np.mean(allages_female_nm), np.std(allages_female_nm), len(allages_female_nm)], 
                   allages_male_nm+allages_female_nm, [np.mean(allages_male_nm+allages_female_nm), np.std(allages_male_nm+allages_female_nm), len(allages_male_nm+allages_female_nm)]])
                   
ages=ages.transpose()
ages.columns=['Male fMRI Ages','Male fMRI Mean,STD,N','Female fMRI Ages','Female fMRI Mean,STD,N','All ages fMRI','Totals fMRI Mean,STD,N',
              'Male T13D Ages','Male T13D Mean,STD,N','Female T13D Ages','Female T13D Mean,STD,N','All ages T13D','Totals T13D Mean,STD,N',
              'Male DTI Ages','Male DTI Mean,STD,N','Female DTI Ages','Female DTI Mean,STD,N','All ages DTI','Totals DTI Mean,STD,N',
              'Male NM Ages','Male NM Mean,STD,N','Female NM Ages','Female NM Mean,STD,N','All ages NM','Totals NM Mean,STD,N']

ages.to_csv('AGES_LIST_'+(os.path.basename(fl_path)[:-4])+'_'+sname+'.csv', index=False)








