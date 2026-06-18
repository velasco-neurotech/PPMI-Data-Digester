# -*- coding: utf-8 -*-
"""
Created on Tue Jan 6 15:05:02 2026

 /$$$$$$$             /$$$$$$  /$$ /$$   /$$      /$$$$$$$$                 /$$      
| $$__  $$           /$$__  $$|__/| $$$ | $$     |__  $$__/                | $$      
| $$  \ $$  /$$$$$$ | $$  \ $$ /$$| $$$$| $$        | $$  /$$$$$$  /$$$$$$ | $$   /$$
| $$$$$$$  /$$__  $$| $$$$$$$$| $$| $$ $$ $$ /$$$$$$| $$ /$$__  $$|____  $$| $$  /$$/
| $$__  $$| $$  \__/| $$__  $$| $$| $$  $$$$|______/| $$| $$  \__/ /$$$$$$$| $$$$$$/ 
| $$  \ $$| $$      | $$  | $$| $$| $$\  $$$        | $$| $$      /$$__  $$| $$_  $$ 
| $$$$$$$/| $$      | $$  | $$| $$| $$ \  $$        | $$| $$     |  $$$$$$$| $$ \  $$
|_______/ |__/      |__/  |__/|__/|__/  \__/        |__/|__/      \_______/|__/  \__/
                                                                                     
                                                                                     
@author: Miguel Velasco Orozco 

Clinical and radiological data concatenator and homologator
Finds closest date between MoCA / HY evaluation and MRI imaging 

Creates Dataframe with only MRI Data and LINMOD file with clinical data 

//////////////UPDATE v1.1/////////////////////

- Data management to include HY Status ON-OFF on cols

//////////////UPDATE v1.2////////////////////

- Drop columns with repeated values coming from Clini-Trak v2.4

"""


VER='1.1'

import easygui as eg
import os                #Sirve para el Manejo de archivos
from datetime import datetime 
import pandas as pd
from itertools import tee, islice, zip_longest

#%%----------------------FUNCTION MANAGER--------------------------------------

def closest_dates(l1, l2):
    """
    For each date in l1, finds the closest date in l2,
    assuming the lists are already sorted.
    """
    
    dates1 = [d.to_pydatetime() for d in l1]
    dates2 = [d.to_pydatetime() for d in l2]
    
    if len(l1)>1:
        
        # dates1 = l1
        # dates2 = l2
        dinf, dsup = tee(dates2)
        enum_middles = enumerate(d1 + (d2-d1)/2 
                                 for d1, d2 in zip_longest(dinf, islice(dsup, 1, None), 
                                                           fillvalue=datetime.max))
        out = []
        index, middle = next(enum_middles)
    
        for d in dates1:
            while d > middle:
                index, middle = next(enum_middles)
            out.append(l2[index])
    
    else:
        print('Only one Element in L1')
        out=[min(dates2, key=lambda x: abs(x - dates1[0]))]

    return out


#%%----------------------PATH MANAGER------------------------------------------

#-----Session Values Input
#Session Name
message = 'Please Select Data Type'
title = "BrAiN-Trak "+VER+" - Start"
sname = eg.choicebox(message, title, ['Longitudinal','Single']) #Session Name

#Subject Type
message = 'Please select Subject Type'
title = "BrAiN-Trak "+VER+" - Start"
choices = ['Control-Parkinsons','Control-Prodromal','Prodromal-Parkinsons','Control-Prodromal-Parkinsons']
stype = eg.choicebox(message, title, choices) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "BrAiN-Trak "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")


if 'Parkinsons' in stype:
    
    #PDD
    #AssemblyNet Batch Files path 
    message = 'Please Select AssemblyNet '+sname+' PD Batch Files Directory'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pd_AN_batch_path = temp_path.replace(os.path.sep ,"/")
    #MRIQC FLTRD File path
    message = 'Please Select FLTRD MRIQC '+sname+' PD File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pd_fltrd_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD MOCA File path
    message = 'Please Select Clini-Trak LINMOD MOCA PD File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pd_moca_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD HY File path
    message = 'Please Select Clini-Trak LINMOD HY PD File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pd_hy_path = temp_path.replace(os.path.sep ,"/")
    
    
if 'Control' in stype:
    #Ctrl
    #AssemblyNet Batch Files path 
    message = 'Please Select AssemblyNet '+sname+' Ctrl Batch Files Directory'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_AN_batch_path = temp_path.replace(os.path.sep ,"/")
    #MRIQC FLTRD File path
    message = 'Please Select FLTRD MRIQC '+sname+' Ctrl File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_fltrd_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD MOCA File path
    message = 'Please Select Clini-Trak LINMOD MOCA Ctrl File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_moca_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD HY File path
    message = 'Please Select Clini-Trak LINMOD HY Ctrl File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_hy_path = temp_path.replace(os.path.sep ,"/")
   
    
if 'Prodromal' in stype:
    
    
    #Prodromals
    #AssemblyNet Batch Files path 
    message = 'Please Select AssemblyNet '+sname+' Prodromals Batch Files Directory'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_AN_batch_path = temp_path.replace(os.path.sep ,"/")
    #MRIQC FLTRD File path
    message = 'Please Select FLTRD MRIQC '+sname+' Prodromals File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_fltrd_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD MOCA File path
    message = 'Please Select Clini-Trak LINMOD MOCA Prodromals File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_moca_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak LINMOD HY File path
    message = 'Please Select Clini-Trak LINMOD HY Prodromals File'
    title = "BrAiN-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_hy_path = temp_path.replace(os.path.sep ,"/")
    
#-------Change working directory to save path 
os.chdir(sv_path)

#%%----------------------FILE OPEN AND CONCAT----------------------------------

if 'Parkinsons' in stype:
    
    #PDD
    #Read Clini-Trak MoCA File
    pd_moca_file = pd.read_csv(pd_moca_path)
    #Read Clini-Trak HY File
    pd_hy_file = pd.read_csv(pd_hy_path)
    #Read MRIQC FLTRD File
    pd_fltrd_file = pd.read_csv(pd_fltrd_path)
    tmp_filelist = os.listdir(pd_AN_batch_path)
    c=True
    for i in tmp_filelist:
        #First iteration, read file, create dataframe
        if c: 
            temp_path= pd_AN_batch_path+'/'+i
            pd_AN_dataframe = pd.read_csv(temp_path, delimiter=';')
            c=False
        
        #Read next files and concatenate
        else:
            temp_path= pd_AN_batch_path+'/'+i
            tmp_df = pd.read_csv(temp_path, delimiter=';')
            pd_AN_dataframe=pd.concat([pd_AN_dataframe, tmp_df])
    #Sort Dataframe by filename (ID)
    pd_AN_dataframe = pd_AN_dataframe.sort_values(by=['Subject'])
    #Reset Dataframe indexes 
    pd_AN_dataframe = pd_AN_dataframe.reset_index(drop=True)
    #Drop AssemblyNet Age and Sex columns (Filled UNKNOWN)
    pd_AN_dataframe.drop(columns=['Age','Sex'], axis =1, inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in pd_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    pd_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    pd_dataframe= pd.merge(pd_AN_dataframe, pd_fltrd_file, on='Filename', how='left') #Left in case AN data is less than fltrd data 
    pd_dataframe = pd_dataframe.dropna() #Drop rows with NaN values 

if 'Control' in stype:
    #Ctrl
    #Read Clini-Trak File 
    ctrl_moca_file = pd.read_csv(ctrl_moca_path)
    #Read Clini-Trak HY File
    ctrl_hy_file = pd.read_csv(ctrl_hy_path)
    #Read MRIQC FLTRD File
    ctrl_fltrd_file = pd.read_csv(ctrl_fltrd_path)
    tmp_filelist = os.listdir(ctrl_AN_batch_path)
    c=True
    for i in tmp_filelist:
        #First iteration, read file, create dataframe
        if c: 
            temp_path= ctrl_AN_batch_path+'/'+i
            ctrl_AN_dataframe = pd.read_csv(temp_path, delimiter=';')
            c=False
        
        #Read next files and concatenate
        else:
            temp_path= ctrl_AN_batch_path+'/'+i
            tmp_df = pd.read_csv(temp_path, delimiter=';')
            ctrl_AN_dataframe=pd.concat([ctrl_AN_dataframe, tmp_df])
    #Sort Dataframe by filename (ID)
    ctrl_AN_dataframe = ctrl_AN_dataframe.sort_values(by=['Subject'])
    #Reset Dataframe indexes 
    ctrl_AN_dataframe = ctrl_AN_dataframe.reset_index(drop=True)
    #Drop AssemblyNet Age and Sex columns (Filled UNKNOWN)
    ctrl_AN_dataframe.drop(columns=['Age','Sex'], axis =1, inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in ctrl_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    ctrl_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    ctrl_dataframe= pd.merge(ctrl_AN_dataframe, ctrl_fltrd_file, on='Filename', how='left') #Left in case AN data is less than fltrd data 
    ctrl_dataframe = ctrl_dataframe.dropna() #Drop rows with NaN values 

if 'Prodromal' in stype:
    
    #Prod
    #Read Clini-Trak File
    prod_moca_file = pd.read_csv(prod_moca_path)
    #Read Clini-Trak HY File
    prod_hy_file = pd.read_csv(prod_hy_path)
    #Read MRIQC FLTRD File
    prod_fltrd_file = pd.read_csv(prod_fltrd_path)
    tmp_filelist = os.listdir(prod_AN_batch_path)
    c=True
    for i in tmp_filelist:
        #First iteration, read file, create dataframe
        if c: 
            temp_path= prod_AN_batch_path+'/'+i
            prod_AN_dataframe = pd.read_csv(temp_path, delimiter=';')
            c=False
        
        #Read next files and concatenate
        else:
            temp_path= prod_AN_batch_path+'/'+i
            tmp_df = pd.read_csv(temp_path, delimiter=';')
            prod_AN_dataframe=pd.concat([prod_AN_dataframe, tmp_df])
    #Sort Dataframe by filename (ID)
    prod_AN_dataframe = prod_AN_dataframe.sort_values(by=['Subject'])
    #Reset Dataframe indexes 
    prod_AN_dataframe = prod_AN_dataframe.reset_index(drop=True)
    #Drop AssemblyNet Age and Sex columns (Filled UNKNOWN)
    prod_AN_dataframe.drop(columns=['Age','Sex'], axis =1, inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in prod_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    prod_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    prod_dataframe= pd.merge(prod_AN_dataframe, prod_fltrd_file, on='Filename', how='left') #Left in case AN data is less than fltrd data 
    prod_dataframe = prod_dataframe.dropna() #Drop rows with NaN values 
#%%----------------------Dataframes to Master CSV------------------------------

if 'Parkinsons' in stype:
    pd_dataframe.to_csv('PD_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)

if 'Control' in stype:
    ctrl_dataframe.to_csv('CTRL_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
elif 'Prodromal' in stype:
    prod_dataframe.to_csv('PROD_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
    
#%%----------------------Clini-Trak MoCA Validation---------------------------------

#Date matching
if 'Parkinsons' in stype:
    
    #------Set Dates from string to datetime object 
    #Clini-Trak MocA Files 
    pd_moca_file['MoCA_Dates'] = pd.to_datetime(pd_moca_file['MoCA_Dates'], format='%m/%Y')
    ctrl_moca_file['MoCA_Dates'] = pd.to_datetime(ctrl_moca_file['MoCA_Dates'], format='%m/%Y')
    #Clini-Trak HY Files 
    pd_hy_file['HY_Dates'] = pd.to_datetime(pd_hy_file['HY_Dates'], format='%m/%Y')
    ctrl_hy_file['HY_Dates'] = pd.to_datetime(ctrl_hy_file['HY_Dates'], format='%m/%Y')
    #BrAiN-Trak Dataframe
    pd_dataframe['Date'] = pd.to_datetime(pd_dataframe['Date'], format = '%Y-%m-%d')
    ctrl_dataframe['Date'] = pd.to_datetime(ctrl_dataframe['Date'], format = '%Y-%m-%d')
    
    #-----PD Validation Loop
    pd_dataframe['SubjectID']= pd_dataframe['SubjectID'].astype(int) #Set Subject ID as Integer 
    pd_moca_file['Subject_ID']= pd_moca_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    pd_hy_file['Subject_ID']= pd_hy_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    pd_sub_id = list(set(pd_dataframe['SubjectID'])) #List of subject ids
    pd_sub_id.sort()
    
    #MoCA Validation 
    c=True #First iteration build counter 
    for i in pd_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = pd_moca_file[pd_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = pd_dataframe[pd_dataframe['SubjectID']==i] #Brain-Trak data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                pd_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                pd_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = pd_moca_file[pd_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = pd_dataframe[pd_dataframe['SubjectID']==i] #Braint-Track data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            pd_pre_validated_df = pd.concat([pd_pre_validated_df, tmp_df], axis =0) #Stack Concat
        
    pd_pre_validated_df = pd_pre_validated_df.dropna() #Drop NaN values 
    pd_pre_validated_df = pd_pre_validated_df[pd_pre_validated_df['Quality control']!= 'C']
    pd_pre_validated_df = pd_pre_validated_df.reset_index(drop=True) #Reset indexes 
     
    #HY Validation 
    c=True #First iteration build counter 
    for i in pd_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = pd_hy_file[pd_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = pd_pre_validated_df[pd_pre_validated_df['SubjectID']==i] #Brain-Trak data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                pd_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                pd_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = pd_hy_file[pd_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = pd_pre_validated_df[pd_pre_validated_df['SubjectID']==i] #Braint-Track data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            pd_validated_df = pd.concat([pd_validated_df, tmp_df], axis =0) #Stack Concat
    
    pd_validated_df = pd_validated_df.dropna() #Drop NaN values 
    pd_validated_df = pd_validated_df[pd_validated_df['Quality control']!= 'C']
    pd_validated_df = pd_validated_df.reset_index(drop=True) #Reset indexes 
    
if 'Control' in stype:
    #-----Ctrl Validation Loop
    ctrl_dataframe['SubjectID']= ctrl_dataframe['SubjectID'].astype(int) #Set Subject ID as Integer 
    ctrl_moca_file['Subject_ID']= ctrl_moca_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    ctrl_hy_file['Subject_ID']= ctrl_hy_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    ctrl_sub_id = list(set(ctrl_dataframe['SubjectID'])) #List of subject ids
    ctrl_sub_id.sort()
    
    #MoCA Validation 
    c=True #First iteration build counter 
    for i in ctrl_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = ctrl_moca_file[ctrl_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = ctrl_dataframe[ctrl_dataframe['SubjectID']==i] #Brain-Trak data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                ctrl_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                ctrl_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = ctrl_moca_file[ctrl_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = ctrl_dataframe[ctrl_dataframe['SubjectID']==i] #Braint-Track data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            ctrl_pre_validated_df = pd.concat([ctrl_pre_validated_df, tmp_df], axis =0) #Stack Concat
        
    ctrl_pre_validated_df = ctrl_pre_validated_df.dropna() #Drop NaN values 
    ctrl_pre_validated_df = ctrl_pre_validated_df[ctrl_pre_validated_df['Quality control']!= 'C']
    ctrl_pre_validated_df = ctrl_pre_validated_df.reset_index(drop=True) #Reset indexes 
     
    #HY Validation 
    c=True #First iteration build counter 
    for i in ctrl_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = ctrl_hy_file[ctrl_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = ctrl_pre_validated_df[ctrl_pre_validated_df['SubjectID']==i] #Brain-Trak data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                ctrl_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                ctrl_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = ctrl_hy_file[ctrl_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = ctrl_pre_validated_df[ctrl_pre_validated_df['SubjectID']==i] #Braint-Track data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            ctrl_validated_df = pd.concat([ctrl_validated_df, tmp_df], axis =0) #Stack Concat
    
    ctrl_validated_df = ctrl_validated_df.dropna() #Drop NaN values 
    ctrl_validated_df = ctrl_validated_df[ctrl_validated_df['Quality control']!= 'C']
    ctrl_validated_df = ctrl_validated_df.reset_index(drop=True) #Reset indexes 
    
    
if 'Prodromal' in stype:
    #-----Prodromal Validation Loop
    prod_dataframe['SubjectID']= prod_dataframe['SubjectID'].astype(int) #Set Subject ID as Integer 
    prod_moca_file['Subject_ID']= prod_moca_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    prod_hy_file['Subject_ID']= prod_hy_file['Subject_ID'].astype(int) #Set Subject ID as Integer 
    prod_sub_id = list(set(prod_dataframe['SubjectID'])) #List of subject ids
    prod_sub_id.sort()
    
    #MoCA Validation 
    c=True #First iteration build counter 
    for i in prod_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = prod_moca_file[prod_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = prod_dataframe[prod_dataframe['SubjectID']==i] #Brain-Trak data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                prod_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                prod_pre_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = prod_moca_file[prod_moca_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = prod_dataframe[prod_dataframe['SubjectID']==i] #Braint-Track data for current subject
            ct_tmp = ct_tmp.drop(columns=['Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education','Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'])
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['MoCA_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['MoCA_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            prod_pre_validated_df = pd.concat([prod_pre_validated_df, tmp_df], axis =0) #Stack Concat
        
    prod_pre_validated_df = prod_pre_validated_df.dropna() #Drop NaN values 
    prod_pre_validated_df = prod_pre_validated_df[prod_pre_validated_df['Quality control']!= 'C']
    prod_pre_validated_df = prod_pre_validated_df.reset_index(drop=True) #Reset indexes 
     
    #HY Validation 
    c=True #First iteration build counter 
    for i in prod_sub_id: #Read by subject 
        if c: #First Iteration
            print(i)
            ct_tmp = prod_hy_file[prod_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = prod_pre_validated_df[prod_pre_validated_df['SubjectID']==i] #Brain-Trak data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                prod_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            else: 
                print('1stpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                prod_validated_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat 
            c=False
        else: #Next Iterations
            print(i)
            ct_tmp = prod_hy_file[prod_hy_file['Subject_ID']==i]  #Clini-Trak data for current subject
            bt_tmp = prod_pre_validated_df[prod_pre_validated_df['SubjectID']==i] #Braint-Track data for current subject
            if len(ct_tmp)>1 and len(ct_tmp)>1: #If List is longer than 1
                matcher= closest_dates(list(bt_tmp['Date']), list(ct_tmp['HY_Dates'])) #Find closest dates for BrainTrak in CliniTrak 
                ct_tmp = ct_tmp[ct_tmp['HY_Dates'].isin(matcher)] #Drop all rows of dates not as close to orginal dates
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            else:
                print('2ndpass')
                ct_tmp = ct_tmp.reset_index(drop=True) #Index Reset 
                bt_tmp = bt_tmp.reset_index(drop=True) 
                tmp_df = pd.concat([ct_tmp, bt_tmp], axis =1) #Sidewise concat
            prod_validated_df = pd.concat([prod_validated_df, tmp_df], axis =0) #Stack Concat
    
    prod_validated_df = prod_validated_df.dropna() #Drop NaN values 
    prod_validated_df = prod_validated_df[prod_validated_df['Quality control']!= 'C']
    prod_validated_df = prod_validated_df.reset_index(drop=True) #Reset indexes 


#%%----------------------Validated Dataframes to Linear Model CSV--------------

if 'Control-Parkinsons' in stype:
    pd_validated_df.to_csv('PD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    ctrl_validated_df.to_csv('CTRL_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
elif 'Control-Prodromal-Parkinsons' in stype:
    pd_validated_df.to_csv('PD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    ctrl_validated_df.to_csv('CTRL_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    prod_validated_df.to_csv('PROD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    