# -*- coding: utf-8 -*-
"""
      ___           ___                       ___           ___              
     /\__\         /\  \          ___        /\  \         /\  \             
    /::|  |       /::\  \        /\  \      /::\  \       /::\  \            
   /:|:|  |      /:/\:\  \       \:\  \    /:/\:\  \     /:/\:\  \           
  /:/|:|__|__   /::\~\:\  \      /::\__\   \:\~\:\  \   /:/  \:\  \          
 /:/ |::::\__\ /:/\:\ \:\__\  __/:/\/__/    \:\ \:\__\ /:/__/ \:\__\         
 \/__/~~/:/  / \/_|::\/:/  / /\/:/  /        \:\/:/  / \:\  \  \/__/         
       /:/  /     |:|::/  /  \::/__/          \::/  /   \:\  \               
      /:/  /      |:|\/__/    \:\__\          /:/  /     \:\  \              
     /:/  /       |:|  |       \/__/         /:/  /       \:\__\             
     \/__/         \|__|                     \/__/         \/__/        
     
      ___           ___       ___           ___     
     /\  \         /\__\     /\  \         /\  \    
    /::\  \       /:/  /     \:\  \       /::\  \   
   /:/\:\  \     /:/  /       \:\  \     /:/\:\  \  
  /::\~\:\  \   /:/  /        /::\  \   /::\~\:\  \ 
 /:/\:\ \:\__\ /:/__/        /:/\:\__\ /:/\:\ \:\__\
 \/__\:\ \/__/ \:\  \       /:/  \/__/ \/_|::\/:/  /
      \:\__\    \:\  \     /:/  /         |:|::/  / 
       \/__/     \:\  \    \/__/          |:|\/__/  
                  \:\__\                  |:|  |    
                   \/__/                   \|__|    
                                                              
Created on Tue Nov 11 13:15:12 2025

@author: LNC Miguel Velasco Orozco 

Evalua: SNR, CNR, CJV, EFC


UPDATE 1.1:
    
    Se añade la generación de archivo 'EXCLUSIONS' el cual enlista en una sola columna los nombres de archivos a excluir, el ID del sujeto y el ID de imagen
    
    Se remueve la línea del log que incluía los comandos del Sun Grid Engine, ya que añadir la edad de cada paciente no es necesario para la segmentación, 
    solamente añade en el resultado el rango promedio de cerebro esperado para su edad y sexo.

"""

VER='1.1'

import matplotlib.pyplot as plt
import easygui as eg
import os                #Sirve para el Manejo de archivos
import pandas as pd
import numpy as np
from datetime import datetime
#from matplotlib.lines import Line2D

#%%----------------------------PATH MANAGER------------------------------------

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "MRIQCplot "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "MRIQCplot "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open MRIQC group File
message = 'Please Select MRIQC Group TSV File'
title = "MRIQCplot "+VER+" - Open"
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
fl_path = temp_path.replace(os.path.sep ,"/")

message = 'Please Select Clini-Trak Subjects CSV File'
title = "MRIQCplot "+VER+" - Open"
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
subs_path = temp_path.replace(os.path.sep ,"/")

message = 'Please Select Metadata Refiner Internal CSV File'
title = "MRIQCplot "+VER+" - Open"
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
mr_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)

#%%-----------------------------FILE OPEN--------------------------------------

df_file = pd.read_csv(fl_path, sep='\t')

subs_file = pd.read_csv(subs_path)

mr_file = pd.read_csv(mr_path)

#Setting subjects column as integer
#subs_file['Subjects With All Data']=subs_file['Subjects With All Data'].astype(int)
subs_withall=subs_file['Subjects With All Data']
subs_withall=subs_withall.dropna()
subs_withall=subs_withall.astype(int)

#Setting date columns as datetime
mr_file['Acq Date']=pd.to_datetime(mr_file['Acq Date'])

#%%--------------Table build

#Extract subjects from MRIQC
sbs_in_mriqc=[]

for i in df_file['bids_name']:  #Reads each BIDS name, extracts subject and appends it in list
    tmp = i.split('_',1)[0]
    tmp = tmp.split('-',1)[1]
    tmp = int(tmp)
    if tmp not in sbs_in_mriqc:
        sbs_in_mriqc.append(tmp)
sbs_in_mriqc=np.array(sbs_in_mriqc)        

#Subjects in Clini-Trak File with all data 
sbs_in_ct = subs_withall.values

#Intersect the two arrays 
sbs_to_analyze= np.intersect1d(sbs_in_mriqc, sbs_in_ct)


#Build dictionaries 
c=True

for i in sbs_to_analyze:   
    print(i)
    #Extract and sort from Metadata Internal
    mr_list = mr_file[(mr_file['Subject']==i) & (mr_file['Modality']=='T13D')]
    mr_list = mr_list.sort_values(by='Acq Date')
    
    #Extract from MRIQC
    mrqc_list = df_file[df_file['bids_name'].str.contains(str(i))]
    
    #Check for extra numbers that could contain same number series but extended (ej: i = 3101 extended 103101)
    for j in mrqc_list['bids_name']:
        tmp = j.split('_',1)[0]
        tmp = tmp.split('-',1)[1]
        tmp = int(tmp)
        if tmp != i:
            print(j)
            mrqc_list = mrqc_list[~mrqc_list['bids_name'].isin([j])]
            
    #Check for different number of images 
    if len(mr_list) > len(mrqc_list):
        mr_list = mr_list.iloc[0:len(mrqc_list)]
        
    elif len(mrqc_list) > len(mr_list):
        mrqc_list = mrqc_list.iloc[0:len(mr_list)]
        
    
    if c:
        
        #Build first dictionary
        tmp_dict={
            'ImageID':mr_list['Image Data ID'].values,
            'Filename':mrqc_list['bids_name'].values,
            'SubjectID':mr_list['Subject'].values,
            'Group':mr_list['Group'].values,
            'Sex':mr_list['Sex'].values,
            'Age':mr_list['Age'].values,
            'Date':mr_list['Acq Date'].astype('str').values,
            'SNR':mrqc_list['snr_total'].values,
            'CNR':mrqc_list['cnr'].values,
            'EFC':mrqc_list['efc'].values,
            'CJV':mrqc_list['cjv'].values
            }
        dataframe = pd.DataFrame(tmp_dict)
        c=False
        
    else:
        
        #Build next dictionary
        tmp_dict={
            'ImageID':mr_list['Image Data ID'].values,
            'Filename':mrqc_list['bids_name'].values,
            'SubjectID':mr_list['Subject'].values,
            'Group':mr_list['Group'].values,
            'Sex':mr_list['Sex'].values,
            'Age':mr_list['Age'].values,
            'Date':mr_list['Acq Date'].astype('str').values,
            'SNR':mrqc_list['snr_total'].values,
            'CNR':mrqc_list['cnr'].values,
            'EFC':mrqc_list['efc'].values,
            'CJV':mrqc_list['cjv'].values
            }
        tmp_df = pd.DataFrame(tmp_dict)
        
        dataframe=pd.concat([dataframe, tmp_df])

#Reset Dataframe indexes 
dataframe = dataframe.reset_index(drop=True)
#%%--------- Outlier selection 

cjv = dataframe['CJV']
snr = dataframe['SNR']
cnr = dataframe['CNR']
efc = dataframe['EFC']


#Selecting outliers 

#Coefficient of Joint variation- higher values are worse
cjv_outliers = dataframe.loc[dataframe['CJV'] > np.mean(cjv.values)+2*np.std(cjv.values)]['CJV']

#Signal to noise ratio - Lower values are worse
snr_outliers = dataframe.loc[dataframe['SNR'] < np.mean(snr.values)-2*np.std(snr.values)]['SNR']

#Contrast to noise ratio - Lower values are worse
cnr_outliers = dataframe.loc[dataframe['CNR'] < np.mean(cnr.values)-2*np.std(cnr.values)]['CNR']

#Entropy focus criterion - Higher values are worse 
efc_outliers = dataframe.loc[dataframe['EFC'] > np.mean(efc.values)+2*np.std(efc.values)]['EFC']


#%%--------------Table Drop (Outlier removal)

#Check if outlier is in subjects to analyze
cjv_o_filenames = []   
for i in dataframe.loc[cjv_outliers.index]['Filename'].values:
    tmp = i.split('_',1)[0]
    tmp = tmp.split('-',1)[1]
    tmp = int(tmp)
    if tmp in sbs_to_analyze:
        cjv_o_filenames.append(i)
    
snr_o_filenames = []
for i in dataframe.loc[snr_outliers.index]['Filename'].values:
    tmp = i.split('_',1)[0]
    tmp = tmp.split('-',1)[1]
    tmp = int(tmp)
    if tmp in sbs_to_analyze:
        snr_o_filenames.append(i)
        
cnr_o_filenames = []
for i in dataframe.loc[cnr_outliers.index]['Filename'].values:
    tmp = i.split('_',1)[0]
    tmp = tmp.split('-',1)[1]
    tmp = int(tmp)
    if tmp in sbs_to_analyze:
        cnr_o_filenames.append(i)

efc_o_filenames = []
for i in dataframe.loc[efc_outliers.index]['Filename'].values:
    tmp = i.split('_',1)[0]
    tmp = tmp.split('-',1)[1]
    tmp = int(tmp)
    if tmp in sbs_to_analyze:
        efc_o_filenames.append(i)

#List of subjects before removal
subs_pre= dataframe['SubjectID'].unique()
#List of filenames before removal
img_pre= dataframe['ImageID'].unique()

#-----Remove entries from table
to_remove = list(set(efc_o_filenames + cnr_o_filenames + cjv_o_filenames + snr_o_filenames))

#Remove entries (select inverse of list to remove )
filtered_dataframe = dataframe[~dataframe['Filename'].isin(to_remove)]

removals_dataframe = dataframe[dataframe['Filename'].isin(to_remove)]

#List of subjects after removal 
subs_post = filtered_dataframe['SubjectID'].unique()

dropped_subs = [i for i in subs_pre if i not in subs_post]

#%%--------Metrics Plot 

#Initialize Figure
fig, ax = plt.subplots(2,2)
fig.set_figheight(9)
fig.set_figwidth(14)
plt.suptitle('MRIQC Metrics_'+sname, fontsize=16)

#------SNR
ax[0,0].axhline(np.mean(snr.values)-2*np.std(snr.values), color ='red', linestyle='--', label='Lower Limit 2$\sigma$: %.2f'%(np.mean(snr.values)-2*np.std(snr.values)))
ax[0,0].axhspan(np.mean(snr.values)-2*np.std(snr.values), np.min(snr.values)-np.std(snr.values), color ='red',alpha=0.1)
ax[0,0].scatter(snr.index, snr.values,alpha = 0.5)
ax[0,0].scatter(snr_outliers.index, snr_outliers.values,alpha = 0.5, color='r', label='# Outliers: '+str(len(snr_outliers)))
ax[0,0].axhline(np.mean(snr.values), color = 'k', label='Mean %.2f'%np.mean(snr.values))
ax[0,0].set_ylabel('SNR')
ax[0,0].set_title('Signal-to-Noise Ratio')
ax[0,0].set_ylim(bottom=np.min(snr.values)-(np.std(snr.values)/2))
ax[0,0].legend(loc=2, fontsize='small', framealpha=0.5)


#------CNR
ax[0,1].axhline(np.mean(cnr.values)-2*np.std(cnr.values), color ='red', linestyle='--', label='Lower Limit 2$\sigma$: %.2f'%(np.mean(cnr.values)-2*np.std(cnr.values)))
ax[0,1].axhspan(np.mean(cnr.values)-2*np.std(cnr.values), np.min(cnr.values)-np.std(cnr.values), color ='red',alpha=0.1)
ax[0,1].scatter(cnr.index, cnr.values,alpha = 0.5)
ax[0,1].scatter(cnr_outliers.index, cnr_outliers.values,alpha = 0.5, color ='r', label='# Outliers: '+str(len(cnr_outliers)))
ax[0,1].axhline(np.mean(cnr.values), color = 'k', label='Mean %.2f'%np.mean(cnr.values))
ax[0,1].set_ylabel('CNR')
ax[0,1].set_title('Contrast-to-Noise Ratio')
ax[0,1].set_ylim(bottom=np.min(cnr.values)-(np.std(cnr.values)/2))
ax[0,1].legend(loc=2, fontsize='small', framealpha=0.5)


#------CJV
ax[1,0].axhline(np.mean(cjv.values)+2*np.std(cjv.values), color ='red', linestyle='--', label='Upper lower Limit 2$\sigma$: %.2f'%(np.mean(cjv.values)+2*np.std(cjv.values)))
ax[1,0].axhspan(np.mean(cjv.values)+2*np.std(cjv.values),np.max(cjv.values)+np.std(cjv.values), color ='red',alpha=0.1)
ax[1,0].scatter(cjv.index, cjv.values,alpha = 0.5)
ax[1,0].scatter(cjv_outliers.index, cjv_outliers.values,alpha = 0.5, color='r', label='# Outliers: '+str(len(cjv_outliers)))
ax[1,0].axhline(np.mean(cjv.values), color = 'k', label='Mean %.2f'%np.mean(cjv.values))
ax[1,0].set_xlabel('Image Num.')
ax[1,0].set_ylabel('CJV')
ax[1,0].set_title('Coefficient of Joint Variation')
ax[1,0].set_ylim(top=np.max(cjv.values)+(np.std(cjv.values)/2))
ax[1,0].legend(loc=2, fontsize='small', framealpha=0.5)


#------EFC
ax[1,1].axhline(np.mean(efc.values)+2*np.std(efc.values), color ='red', linestyle='--', label='Upper lower Limit 2$\sigma$: %.2f'%(np.mean(efc.values)+2*np.std(efc.values)))
ax[1,1].axhspan(np.mean(efc.values)+2*np.std(efc.values),np.max(efc.values)+np.std(efc.values), color ='red',alpha=0.1)
ax[1,1].scatter(efc.index, efc.values,alpha = 0.5)
ax[1,1].scatter(efc_outliers.index, efc_outliers.values,alpha = 0.5, color='r', label='# Outliers: '+str(len(efc_outliers)))
ax[1,1].axhline(np.mean(efc.values), color = 'k', label='Mean %.2f'%np.mean(efc.values))
ax[1,1].set_xlabel('Image Num.')
ax[1,1].set_ylabel('EFC')
ax[1,1].set_title('Entropy Focus Criterion')
ax[1,1].set_ylim(top=np.max(efc.values)+(np.std(efc.values)/2))
ax[1,1].legend(loc=2, fontsize='small', framealpha=0.5)

plt.tight_layout()
plt.savefig(sname+'_MRIQC Metrics_'+(os.path.basename(sv_path)[:-4])+'_')   


#%%--------------Dataframe to csv

filtered_dataframe.to_csv(sname+'_MRIQC_FLTRD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)

removals_dataframe.to_csv(sname+'_MRIQC_REMOVALS_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)

#%%--------------Log File 

#Create Log File 
with open (sname+' - MRIQCFLTR Log File.txt', 'w') as savefile:
    savefile.write('      ___           ___                       ___           ___ \n')  
    savefile.write('     /\__\         /\  \          ___        /\  \         /\  \  \n' ) 
    savefile.write('    /::|  |       /::\  \        /\  \      /::\  \       /::\  \  \n' )
    savefile.write('   /:|:|  |      /:/\:\  \       \:\  \    /:/\:\  \     /:/\:\  \   \n')
    savefile.write('  /:/|:|__|__   /::\~\:\  \      /::\__\   \:\~\:\  \   /:/  \:\  \ \n')       
    savefile.write(' /:/ |::::\__\ /:/\:\ \:\__\  __/:/\/__/    \:\ \:\__\ /:/__/ \:\__\  \n')  
    savefile.write(' \/__/~~/:/  / \/_|::\/:/  / /\/:/  /        \:\/:/  / \:\  \  \/__/  \n')  
    savefile.write('       /:/  /     |:|::/  /  \::/__/          \::/  /   \:\  \  \n')  
    savefile.write('      /:/  /      |:|\/__/    \:\__\          /:/  /     \:\  \  \n')  
    savefile.write('     /:/  /       |:|  |       \/__/         /:/  /       \:\__\  \n')  
    savefile.write('     \/__/         \|__|                     \/__/         \/__/   \n\n\n')  
    savefile.write('      ___           ___       ___           ___     \n')            
    savefile.write('     /\  \         /\__\     /\  \         /\  \  \n') 
    savefile.write('    /::\  \       /:/  /     \:\  \       /::\  \ \n') 
    savefile.write('   /:/\:\  \     /:/  /       \:\  \     /:/\:\  \ \n') 
    savefile.write('  /::\~\:\  \   /:/  /        /::\  \   /::\~\:\  \ \n') 
    savefile.write(' /:/\:\ \:\__\ /:/__/        /:/\:\__\ /:/\:\ \:\__\ \n') 
    savefile.write(' \/__\:\ \/__/ \:\  \       /:/  \/__/ \/_|::\/:/  / \n') 
    savefile.write('      \:\__\    \:\  \     /:/  /         |:|::/  /  \n') 
    savefile.write('       \/__/     \:\  \    \/__/          |:|\/__/  \n') 
    savefile.write('                  \:\__\                  |:|  |    \n') 
    savefile.write('                   \/__/                   \|__| \n\n') 
    savefile.write('Created By: NeuroSc Miguel Velasco-Orozco \u00A9 2025\nVersion Control: '+VER+'\n\n\n')
    savefile.write('Session Name: '+sname+'\n')
    savefile.write('MRIQC Group File Path: \n'+fl_path+'\n\n')
    savefile.write('Clini-Trak Subjects File Path: \n'+subs_path+'\n\n')
    savefile.write('Metadata Refiner Internal File Path: \n'+subs_path+'\n\n')
    savefile.write('Save Folder Route: \n'+sv_path+'\n\n\n')
    savefile.write('Session Timestamp: '+str(datetime.now())+'\n\n')
    savefile.write('-----------------Subjects info--------------\n\n')
    savefile.write('> Processed MRIQC Subjects in group: '+str(len(sbs_in_mriqc))+'\n')
    savefile.write('> MRIQC Subjects with all Clini-Trak Data: '+str(len(sbs_to_analyze))+'\n')
    savefile.write('> Dropped subjects after MRIQC : '+str(len(dropped_subs))+'\n')
    savefile.write('> Final number of subjects : '+str(len(subs_post))+'\n\n')
    savefile.write('> Original number of images : '+str(len(dataframe))+'\n')
    savefile.write('> Number of dropped images : '+str(len(to_remove))+'\n')
    savefile.write('> Final number of images : '+str(len(filtered_dataframe))+'\n\n')
    
    
    savefile.write('-----------------Signal to Noise Ratio discarded outlier filenames---------\n\n')
    if len(snr_o_filenames) > 0:
        for i in snr_o_filenames:
            tmp_id= dataframe[dataframe['Filename']==i]['ImageID'].values[0]
            savefile.write('Filename : '+str(i)+'............Image ID : '+str(tmp_id)+'\n\n')
    else:
        savefile.write('NO SNR DISCARDED FILES\n\n')
        
    savefile.write('\n\n-----------------Contrast to Noise Ratio discarded outlier filenames---------\n\n')
    if len(cnr_o_filenames) > 0:
        for i in cnr_o_filenames:
            tmp_id= dataframe[dataframe['Filename']==i]['ImageID'].values[0]
            savefile.write('Filename : '+str(i)+'............Image ID : '+str(tmp_id)+'\n\n')
    else:
        savefile.write('NO CNR DISCARDED FILES\n\n')        
    
    savefile.write('\n\n-----------------Coefficient of Joint Variation discarded outlier filenames---------\n\n')
    if len(cjv_o_filenames) > 0:
        for i in cjv_o_filenames:
            tmp_id= dataframe[dataframe['Filename']==i]['ImageID'].values[0]
            savefile.write('Filename : '+str(i)+'............Image ID : '+str(tmp_id)+'\n\n')
    else:
        savefile.write('NO CJV DISCARDED FILES\n\n') 
            
    savefile.write('\n\n-----------------Entropy Focus Criterion discarded outlier filenames---------\n\n')
    if len(efc_o_filenames) > 0:
        for i in efc_o_filenames:
            tmp_id= dataframe[dataframe['Filename']==i]['ImageID'].values[0]
            savefile.write('Filename : '+str(i)+'............Image ID : '+str(tmp_id)+'\n\n')
    else:
        savefile.write('NO EFC DISCARDED FILES\n\n')   
        
    savefile.write('\n\n---------------Dropped Subjects IDs-----------------------\n\n')   
    if len(dropped_subs)>0:
        for i in dropped_subs:
            savefile.write('\n\n-Sub-'+str(i)+'\n\n') 
    else:
        savefile.write('NO DROPPED SUBS\n\n')          

    

  
 




 
 






