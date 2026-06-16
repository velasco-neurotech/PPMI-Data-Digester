# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:48:33 2025


 ______     __         __     __   __     __        ______   ______     ______     __  __    
/\  ___\   /\ \       /\ \   /\ "-.\ \   /\ \      /\__  _\ /\  == \   /\  __ \   /\ \/ /    
\ \ \____  \ \ \____  \ \ \  \ \ \-.  \  \ \ \     \/_/\ \/ \ \  __<   \ \  __ \  \ \  _"-.  
 \ \_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_\       \ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_/        \/_/   \/_/ /_/   \/_/\/_/   \/_/\/_/                                                                                           
 ______   __         ______     ______   ______   ______     ______    
/\  == \ /\ \       /\  __ \   /\__  _\ /\__  _\ /\  ___\   /\  == \   
\ \  _-/ \ \ \____  \ \ \/\ \  \/_/\ \/ \/_/\ \/ \ \  __\   \ \  __<   
 \ \_\    \ \_____\  \ \_____\    \ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/     \/_____/   \/_____/     \/_/     \/_/   \/_____/   \/_/ /_/ 
                                                                      

@author: Miguel Velasco Orozco


//////////////Ver 3 Update/////////////

- Se añaden los módulos para hecer los plots para los pacientes prodrómicos junto con los demás 


//////////////Ver 4 Update/////////////

- Se añade módulo para seleccionar qué sujetos incluir según la modalidad de mri que tengan y no usar absolutamente
todos los sujetos sin importar la modalidad.

/////////////Ver 5 Update/////////////

- Se añade el módulo para hacer los plots de escala Hoehn Yahr

////////////Ver 5.1 Update ///////////

- En las gráficas de Hoehn-Yahr se pueden separar por estado ON-OFF después de haber actualizado la 
arquitectura de datos en Clini-Trak (v2.3)

"""

VER='5.1'

import easygui as eg
import os                #Sirve para el Manejo de archivos
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime 
from sklearn.linear_model import LinearRegression
import seaborn as sns
from matplotlib.lines import Line2D
from scipy import stats as sp
from scikit_posthocs import posthoc_dunn as dunn

#%%----------------------------Define Functions--------------------------------


#%%----------------------------PATH MANAGER------------------------------------

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Clini-Trak Plotter "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Subject Type
message = 'Please select Subject Type'
title = "Clini-Trak Plotter "+VER+" - Start"
choices = ['Control-Parkinsons','Control-Prodromal','Prodromal-Parkinsons','Control-Prodromal-Parkinsons']
stype = eg.choicebox(message, title, choices) #Session Name

#Image Type
message = 'Please select Modalities to include'
title = "Clini-Trak Plotter "+VER+" - Start"
choices = ['T13D','DTI','NM','fMRI','Only Clinical Data']
itype = eg.multchoicebox(message, title, choices) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Clini-Trak Plotter "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")


if 'Control' in stype:
    
    #Ctrl
    #Clini-Trak Dataframe File Path 
    message = 'Please Select Clini-Trak Controls Dataframe File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_ct_df_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak Subjects File Path 
    message = 'Please Select Clini-Trak Controls Subjects File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_ct_subs_path = temp_path.replace(os.path.sep ,"/")
    #MRI modality File Path 
    message = 'Please Metdata Internal Subjects List File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    ctrl_mi_subs_path = temp_path.replace(os.path.sep ,"/")
    
if 'Parkinsons' in stype:
    
    #PDD
    #Clini-Trak Dataframe File Path 
    message = 'Please Select Clini-Trak PD Dataframe File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pdd_ct_df_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak Subjects File Path 
    message = 'Please Select Clini-Trak PD Subjects File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pdd_ct_subs_path = temp_path.replace(os.path.sep ,"/")
    #MRI modality File Path 
    message = 'Please Metdata Internal Subjects List File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    pdd_mi_subs_path = temp_path.replace(os.path.sep ,"/")
    
    
if 'Prodromal' in stype:
    
    #Prodromal
    #Clini-Trak Dataframe File Path 
    message = 'Please Select Clini-Trak Prodromals Dataframe File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_ct_df_path = temp_path.replace(os.path.sep ,"/")
    #Clini-Trak Subjects File Path 
    message = 'Please Select Clini-Trak Prodomals Subjects File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_ct_subs_path = temp_path.replace(os.path.sep ,"/")
    #MRI modality File Path 
    message = 'Please Metdata Internal Subjects List File'
    title = "Clini-Trak Plotter "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
    prod_mi_subs_path = temp_path.replace(os.path.sep ,"/")
        
#-------Change working directory to save path 
os.chdir(sv_path)

#%%-----------------------------FILE OPEN--------------------------------------

if 'Control-Parkinsons' in stype:
    
    #PDD
    #Read Clini-Trak PD Dataframe File
    pdd_ct_df_file = pd.read_csv(pdd_ct_df_path)
    #Read Clini-Trak PD Subjects File
    pdd_ct_subs_file = pd.read_csv(pdd_ct_subs_path)
    #Read Metadata Internal PD Subjects List File
    pdd_mi_subs_file = pd.read_csv(pdd_mi_subs_path)
    
    #Ctrl
    #Read Clini-Trak Controls Dataframe File
    ctrl_ct_df_file = pd.read_csv(ctrl_ct_df_path)
    #Read Clini-Trak Controls Subjects File
    ctrl_ct_subs_file = pd.read_csv(ctrl_ct_subs_path)
    #Read Metadata Internal Controls Subjects List File
    ctrl_mi_subs_file = pd.read_csv(ctrl_mi_subs_path)

elif 'Control-Prodromal-Parkinsons' in stype:
    
    #PDD
    #Read Clini-Trak PDD Dataframe File
    pdd_ct_df_file = pd.read_csv(pdd_ct_df_path)
    #Read Clini-Trak PDD Subjects File
    pdd_ct_subs_file = pd.read_csv(pdd_ct_subs_path)
    #Read Metadata Internal PD Subjects List File
    pdd_mi_subs_file = pd.read_csv(pdd_mi_subs_path)
    
    #Ctrl
    #Read Clini-Trak Controls Dataframe File
    ctrl_ct_df_file = pd.read_csv(ctrl_ct_df_path)
    #Read Clini-Trak Controls Subjects File
    ctrl_ct_subs_file = pd.read_csv(ctrl_ct_subs_path)
    #Read Metadata Internal Controls Subjects List File
    ctrl_mi_subs_file = pd.read_csv(ctrl_mi_subs_path)
    
    #Prodromal
    #Read Clini-Trak Prodromals Dataframe File
    prod_ct_df_file = pd.read_csv(prod_ct_df_path)
    #Read Clini-Trak Prodromals Subjects File
    prod_ct_subs_file = pd.read_csv(prod_ct_subs_path)
    #Read Clini-Trak Prodromals Subjects File
    prod_mi_subs_file = pd.read_csv(prod_mi_subs_path)


#%%---------------Subjects to include by modality 

if 'Parkinsons' in stype:
    pd_subs_bymod= []  #Subjects with all data longitudinal + single
    pd_subs_bymod_long= [] #Subjects with all data only longitudinal
    
    if 'Only Clinical Data':
        print('Include All Subjects-Only Clinical Data')
        
        pd_subs_bymod_long= [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
        
        
    else:
    
        if 'T13D' in itype:
            print('Include T13D')
            tmp = pdd_mi_subs_file['Longitudinal T13D Subjects'].dropna().values #Remove NaNs
            tmp2 = [int(i) for i in tmp] #Convert to integer
            pd_subs_bymod=pd_subs_bymod+tmp2 #Add to lists
            pd_subs_bymod_long=pd_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc T13D Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
            
        if 'DTI' in itype:
            print('Include DTI')
            tmp = pdd_mi_subs_file['Longitudinal DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
            pd_subs_bymod_long=pd_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
        
        if 'fMRI' in itype:
            print('Include fMRI')
            tmp = pdd_mi_subs_file['Longitudinal fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
            pd_subs_bymod_long=pd_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
            
        if 'NM' in itype:
            print('Include NM')
            tmp = pdd_mi_subs_file['Longitudinal NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
            pd_subs_bymod_long=pd_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            pd_subs_bymod=pd_subs_bymod+tmp2
        
        pd_subs_bymod= list(set(pd_subs_bymod))
        pd_subs_bymod_long= list(set(pd_subs_bymod_long))
    
if 'Control' in stype:
    ctrl_subs_bymod=[]
    ctrl_subs_bymod_long=[]
    
    if 'Only Clinical Data':
        print('Include All Subjects-Only Clinical Data')
        
        ctrl_subs_bymod_long= [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]
    
    else:
    
        if 'T13D' in itype:
            tmp = ctrl_mi_subs_file['Longitudinal T13D Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            ctrl_subs_bymod_long=ctrl_subs_bymod_long+tmp2
            
            tmp = ctrl_mi_subs_file['Single Aqc T13D Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            
        if 'DTI' in itype:
            tmp = ctrl_mi_subs_file['Longitudinal DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            ctrl_subs_bymod_long=ctrl_subs_bymod_long+tmp2
            
            tmp = ctrl_mi_subs_file['Single Aqc DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
        
        if 'fMRI' in itype:
            tmp = ctrl_mi_subs_file['Longitudinal fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            ctrl_subs_bymod_long=ctrl_subs_bymod_long+tmp2
            
            tmp = ctrl_mi_subs_file['Single Aqc fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            
        if 'NM' in itype:
            tmp = ctrl_mi_subs_file['Longitudinal NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
            ctrl_subs_bymod_long=ctrl_subs_bymod_long+tmp2
            
            tmp = ctrl_mi_subs_file['Single Aqc NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            ctrl_subs_bymod=ctrl_subs_bymod+tmp2
        
        ctrl_subs_bymod= list(set(ctrl_subs_bymod))
        ctrl_subs_bymod_long= list(set(ctrl_subs_bymod_long))

if 'Prodromal' in stype: 
    prod_subs_bymod= []
    prod_subs_bymod_long= []
    
    if 'Only Clinical Data':
        print('Include All Subjects-Only Clinical Data')
        
        prod_subs_bymod_long= [int(x) for x in prod_ct_subs_file['Subjects With All Data'].dropna()]
    
    else:
        
        if 'T13D' in itype:
            tmp = prod_mi_subs_file['Longitudinal T13D Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            prod_subs_bymod_long=prod_subs_bymod_long+tmp2
            
            tmp = prod_mi_subs_file['Single Aqc T13D Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            
        if 'DTI' in itype:
            tmp = prod_mi_subs_file['Longitudinal DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            prod_subs_bymod_long=prod_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc DTI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
        
        if 'fMRI' in itype:
            tmp = pdd_mi_subs_file['Longitudinal fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            prod_subs_bymod_long=prod_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc fMRI Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            
        if 'NM' in itype:
            tmp = pdd_mi_subs_file['Longitudinal NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
            prod_subs_bymod_long=prod_subs_bymod_long+tmp2
            
            tmp = pdd_mi_subs_file['Single Aqc NM Subjects'].dropna().values 
            tmp2 = [int(i) for i in tmp]
            prod_subs_bymod=prod_subs_bymod+tmp2
        
        prod_subs_bymod= list(set(prod_subs_bymod))
        prod_subs_bymod_long= list(set(prod_subs_bymod_long))
    
#%%-------------------------//////PLOTS\\\\\\----------------------------------    
#%%---------------MoCA Score vs years since onset graph (ONLY PDD)

#List of subjects with all data
pdd_wholedata_pre_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]

pdd_wholedata_subs=[i for i in pdd_wholedata_pre_subs if i in pd_subs_bymod]

#Filter dataframe and extract data only from whole data subjects
pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]

#Sort subjects by age 
pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')

#Extract sorted ages
pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]



#-------------------Age Onset-Centered Graph

#Extract number of ages (colorbar length)
N=len(pdd_ages)
#Assign Colormap
cmap = plt.get_cmap('seismic',N)
#Initialize Figure
fig, ax = plt.subplots()
fig.set_figheight(7)
fig.set_figwidth(10)
plt.title('Evolution Trayectories of MoCA Score vs Years \nsince onset PDD_'+sname)

#Iterate through subjects 
for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
    print(str(i))
    
    #--Subject MoCA Dates
    #Redefine as list of values (was string)
    pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    pdd_dates = eval(pdd_dates)
    
    #--Subject Years since since onset
    #Extract Onset date
    onset_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Date'].values[0],'%m/%Y')
    #Onset date minus test date in years 
    x =np.array([(datetime.strptime(a, '%m/%Y')-onset_date).days/365 for a in pdd_dates])
    
    #--Subject MoCA Scores
    #Redefine as list of values (was string)
    y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
    if 'n' in y:
        y= y.replace('nan','10101') #Barcoding to remove date in case of nan
    y = np.array(eval(y))
    
    #--Remove date if nan in score
    if 10101 in y:
        #print('Nan in data')
        x=x[y!=10101]
        y=y[y!=10101]
      
    #------X (years since onset) and Y (MoCA Score) Ready to plot
    plot = ax.plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2)



plt.xlabel('Years since Onset ')
plt.ylabel('MoCA Score')

#Normalize color data for colorbar 
norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, label = 'Onset Age')



plt.savefig('Evolution Trayectories of MoCA Score vs Years since onset PDD_'+(os.path.basename(sv_path)[:-4])+'_'+sname)   

#%%---------------MoCA Score vs age trajectories

if 'Control-Parkinsons' in stype:
    print('Plotting MoCA Score vs Age - PDD vs Ctrl')
    
    #List of subjects with all data
    pdd_wholedata_pre_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
    pdd_wholedata_subs=[i for i in pdd_wholedata_pre_subs if i in pd_subs_bymod_long]
    
    ctrl_wholedata_pre_subs = [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]
    ctrl_wholedata_subs=[i for i in ctrl_wholedata_pre_subs if i in ctrl_subs_bymod_long]
    
    #Filter dataframe and extract data only from whole data subjects
    pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]
    ctrl_filtered_df_file = ctrl_ct_df_file[(ctrl_ct_df_file['Subject_ID'].isin(ctrl_wholedata_subs))]
    
    #Convert Birthdate column to datetime
    ctrl_filtered_df_file['Birthdate'] = pd.to_datetime(ctrl_filtered_df_file['Birthdate'])
    
    #Sort subjects by age 
    pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')
    ctrl_sorted_ct_df_file = ctrl_filtered_df_file.sort_values('Birthdate', ascending=False)
    
    
    #Convert Birthdate column to string
    ctrl_sorted_ct_df_file['Birthdate'] = ctrl_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')
    
    #Extract sorted ages
    pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]
    
    #Slopes by age rank
    rank_30_40_pdd_slopes=[]
    rank_30_40_ctrl_slopes=[]
    
    rank_40_50_pdd_slopes=[]
    rank_40_50_ctrl_slopes=[]
    
    rank_50_60_pdd_slopes=[]
    rank_50_60_ctrl_slopes=[]
    
    rank_60_70_pdd_slopes=[]
    rank_60_70_ctrl_slopes=[]
    
    rank_70_80_pdd_slopes=[]
    rank_70_80_ctrl_slopes=[]
    
    rank_80_90_pdd_slopes=[]
    rank_80_90_ctrl_slopes=[]
    
    #Years of education by age rank
    rank_30_40_pdd_yoe=[]
    rank_30_40_ctrl_yoe=[]
    
    rank_40_50_pdd_yoe=[]
    rank_40_50_ctrl_yoe=[]
    
    rank_50_60_pdd_yoe=[]
    rank_50_60_ctrl_yoe=[]
    
    rank_60_70_pdd_yoe=[]
    rank_60_70_ctrl_yoe=[]
    
    rank_70_80_pdd_yoe=[]
    rank_70_80_ctrl_yoe=[]
    
    rank_80_90_pdd_yoe=[]
    rank_80_90_ctrl_yoe=[]
    
    #-------------------MoCA vs Age
    
    #Initialize Figure
    fig, ax = plt.subplots(2,1)
    fig.set_figheight(7)
    fig.set_figwidth(14)
    plt.suptitle('Evolution Trayectories MoCA Score vs Age_'+sname, fontsize=16)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    #Extract number of ages (colorbar length)
    N=len(pdd_ages)
    #Assign Colormap
    cmap = plt.get_cmap('seismic',N)
    #Slopes
    pdd_slopes=[]
    pdd_rsq=[]
    #Plotted Subjects List
    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA score
            plot = ax[0].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2)
            
            #-----Obtain Subjects years of education
            yoe = float(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #print(str(model.coef_ [0]))
            #if model.coef_[0]!=0:
            pdd_rsq.append(model.score(x_lr,y))
            pdd_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_pdd_slopes.append(model.coef_ [0])
                rank_30_40_pdd_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_pdd_slopes.append(model.coef_ [0])
                rank_40_50_pdd_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_pdd_slopes.append(model.coef_ [0])
                rank_50_60_pdd_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_pdd_slopes.append(model.coef_ [0])
                rank_60_70_pdd_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_pdd_slopes.append(model.coef_ [0])
                rank_70_80_pdd_yoe.append(yoe)
            else:
                rank_80_90_pdd_slopes.append(model.coef_ [0])
                rank_80_90_pdd_yoe.append(yoe)
                
                
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[0], label = 'Onset Age')
    
    
    #Iterate through control subjects
    print('_init_Controls')
    
    #Ccolorbar length
    N=len(ctrl_wholedata_subs)
    #Assign Colormap
    cmap = plt.get_cmap('gnuplot_r',N)
    #Slopes
    ctrl_slopes=[]
    ctrl_rsq=[]
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA Score Plot
            plot = ax[1].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2) 
            
            #-----Obtain Subjects years of education
            yoe = float(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #if model.coef_[0]!=0:
            ctrl_rsq.append(model.score(x_lr,y))
            ctrl_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_ctrl_slopes.append(model.coef_ [0])
                rank_30_40_ctrl_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_ctrl_slopes.append(model.coef_ [0])
                rank_40_50_ctrl_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_ctrl_slopes.append(model.coef_ [0])
                rank_50_60_ctrl_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_ctrl_slopes.append(model.coef_ [0])
                rank_60_70_ctrl_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_ctrl_slopes.append(model.coef_ [0])
                rank_70_80_ctrl_yoe.append(yoe)
            else:
                rank_80_90_ctrl_slopes.append(model.coef_ [0])
                rank_80_90_ctrl_yoe.append(yoe)
              
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='MoCA Score')
    ax[1].set(xlabel='Age', ylabel='MoCA Score')
    ax[0].set_ylim([0,31])
    ax[1].set_ylim([0,31])
    ax[0].set_xlim([28,93])
    ax[1].set_xlim([28,93])
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[1], label ='Age at first MoCA')
    plt.show()
     
    
    plt.savefig('Evolution Trayectories MoCA Score vs Age_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

elif 'Control-Prodromal-Parkinsons' in stype:
    
    print('Plotting MoCA Score vs Age - PDD vs Prodromal vs Ctrl')
    
    #List of subjects with all data
    pdd_wholedata_pre_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
    pdd_wholedata_subs=[i for i in pdd_wholedata_pre_subs if i in pd_subs_bymod_long]
    
    ctrl_wholedata_pre_subs = [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]
    ctrl_wholedata_subs=[i for i in ctrl_wholedata_pre_subs if i in ctrl_subs_bymod_long]
    
    prod_wholedata_pre_subs = [int(x) for x in prod_ct_subs_file['Subjects With All Data'].dropna()]
    prod_wholedata_subs=[i for i in prod_wholedata_pre_subs if i in prod_subs_bymod_long]

    
    #Filter dataframe and extract data only from whole data subjects
    pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]
    ctrl_filtered_df_file = ctrl_ct_df_file[(ctrl_ct_df_file['Subject_ID'].isin(ctrl_wholedata_subs))]
    prod_filtered_df_file = prod_ct_df_file[(prod_ct_df_file['Subject_ID'].isin(prod_wholedata_subs))]
    
    #Convert Birthdate column to datetime
    ctrl_filtered_df_file['Birthdate'] = pd.to_datetime(ctrl_filtered_df_file['Birthdate'])
    prod_filtered_df_file['Birthdate'] = pd.to_datetime(prod_filtered_df_file['Birthdate'])
    
    #Sort subjects by age 
    pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')
    ctrl_sorted_ct_df_file = ctrl_filtered_df_file.sort_values('Birthdate', ascending=False)
    prod_sorted_ct_df_file = prod_filtered_df_file.sort_values('Birthdate', ascending=False)
    
    #Convert Birthdate column to string
    ctrl_sorted_ct_df_file['Birthdate'] = ctrl_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')
    prod_sorted_ct_df_file['Birthdate'] = prod_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')
    
    #Extract sorted ages
    pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]
    
    #Slopes by age rank
    rank_30_40_pdd_slopes=[]
    rank_30_40_ctrl_slopes=[]
    rank_30_40_prod_slopes=[]
    
    rank_40_50_pdd_slopes=[]
    rank_40_50_ctrl_slopes=[]
    rank_40_50_prod_slopes=[]
    
    rank_50_60_pdd_slopes=[]
    rank_50_60_ctrl_slopes=[]
    rank_50_60_prod_slopes=[]
    
    rank_60_70_pdd_slopes=[]
    rank_60_70_ctrl_slopes=[]
    rank_60_70_prod_slopes=[]
    
    rank_70_80_pdd_slopes=[]
    rank_70_80_ctrl_slopes=[]
    rank_70_80_prod_slopes=[]
    
    rank_80_90_pdd_slopes=[]
    rank_80_90_ctrl_slopes=[]
    rank_80_90_prod_slopes=[]
    
    #Years of education by age rank
    rank_30_40_pdd_yoe=[]
    rank_30_40_ctrl_yoe=[]
    rank_30_40_prod_yoe=[]
    
    rank_40_50_pdd_yoe=[]
    rank_40_50_ctrl_yoe=[]
    rank_40_50_prod_yoe=[]
    
    rank_50_60_pdd_yoe=[]
    rank_50_60_ctrl_yoe=[]
    rank_50_60_prod_yoe=[]
    
    rank_60_70_pdd_yoe=[]
    rank_60_70_ctrl_yoe=[]
    rank_60_70_prod_yoe=[]
    
    rank_70_80_pdd_yoe=[]
    rank_70_80_ctrl_yoe=[]
    rank_70_80_prod_yoe=[]
    
    rank_80_90_pdd_yoe=[]
    rank_80_90_ctrl_yoe=[]
    rank_80_90_prod_yoe=[]
    
    #-------------------MoCA vs Age
    
    #Initialize Figure
    fig, ax = plt.subplots(3,1)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    plt.suptitle('Evolution Trayectories MoCA Score vs Age_'+sname, fontsize=16)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    #Extract number of ages (colorbar length)
    N=len(pdd_ages)
    #Assign Colormap
    cmap = plt.get_cmap('seismic',N)
    #Slopes
    pdd_slopes=[]
    pdd_rsq=[]
    #Plotted Subjects List
    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    plotted_subs_prod=[]
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA score
            plot = ax[0].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2)
            
            #-----Obtain Subjects years of education
            yoe = float(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #print(str(model.coef_ [0]))
            #if model.coef_[0]!=0:
            pdd_rsq.append(model.score(x_lr,y))
            pdd_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_pdd_slopes.append(model.coef_ [0])
                rank_30_40_pdd_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_pdd_slopes.append(model.coef_ [0])
                rank_40_50_pdd_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_pdd_slopes.append(model.coef_ [0])
                rank_50_60_pdd_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_pdd_slopes.append(model.coef_ [0])
                rank_60_70_pdd_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_pdd_slopes.append(model.coef_ [0])
                rank_70_80_pdd_yoe.append(yoe)
            else:
                rank_80_90_pdd_slopes.append(model.coef_ [0])
                rank_80_90_pdd_yoe.append(yoe)
                
                
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[0], label = 'Onset Age')
    
    
    #Iterate through prodromal subjects
    print('_init_Prodromals')
    
    #Ccolorbar length
    N=len(prod_wholedata_subs)
    #Assign Colormap
    cmap = plt.get_cmap('PiYG',N)
    #Slopes
    prod_slopes=[]
    prod_rsq=[]
    
    for j,i in enumerate(list(prod_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        prod_dates = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        prod_dates = eval(prod_dates)
        
        if len(prod_dates)>1:
            
            plotted_subs_prod.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in prod_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA Score Plot
            plot = ax[1].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2) 
            
            #-----Obtain Subjects years of education
            yoe = float(prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #if model.coef_[0]!=0:
            prod_rsq.append(model.score(x_lr,y))
            prod_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_prod_slopes.append(model.coef_ [0])
                rank_30_40_prod_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_prod_slopes.append(model.coef_ [0])
                rank_40_50_prod_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_prod_slopes.append(model.coef_ [0])
                rank_50_60_prod_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_prod_slopes.append(model.coef_ [0])
                rank_60_70_prod_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_prod_slopes.append(model.coef_ [0])
                rank_70_80_prod_yoe.append(yoe)
            else:
                rank_80_90_prod_slopes.append(model.coef_ [0])
                rank_80_90_prod_yoe.append(yoe)
              

    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[1], label ='Matched age')
    plt.show()
    
    #Iterate through control subjects
    print('_init_Controls')
    
    #Ccolorbar length
    N=len(ctrl_wholedata_subs)
    #Assign Colormap
    cmap = plt.get_cmap('gnuplot_r',N)
    #Slopes
    ctrl_slopes=[]
    ctrl_rsq=[]
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA Score Plot
            plot = ax[2].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2) 
            
            #-----Obtain Subjects years of education
            yoe = float(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #if model.coef_[0]!=0:
            ctrl_rsq.append(model.score(x_lr,y))
            ctrl_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_ctrl_slopes.append(model.coef_ [0])
                rank_30_40_ctrl_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_ctrl_slopes.append(model.coef_ [0])
                rank_40_50_ctrl_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_ctrl_slopes.append(model.coef_ [0])
                rank_50_60_ctrl_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_ctrl_slopes.append(model.coef_ [0])
                rank_60_70_ctrl_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_ctrl_slopes.append(model.coef_ [0])
                rank_70_80_ctrl_yoe.append(yoe)
            else:
                rank_80_90_ctrl_slopes.append(model.coef_ [0])
                rank_80_90_ctrl_yoe.append(yoe)
              
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Prodromals         n='+str(len(plotted_subs_prod)), pad = 0, fontsize= 10, loc = 'right')
    ax[2].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='MoCA Score')
    ax[1].set(ylabel='MoCA Score')
    ax[2].set(xlabel='Age', ylabel='MoCA Score')
    ax[0].set_ylim([0,31])
    ax[1].set_ylim([0,31])
    ax[2].set_ylim([0,31])
    ax[0].set_xlim([28,93])
    ax[1].set_xlim([28,93])
    ax[2].set_xlim([28,93])
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[2], label ='Age at first MoCA')
    plt.show()
    plt.tight_layout()
    plt.savefig('Evolution Trayectories MoCA Score vs Age_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    
    
#%%---------------MoCA Slopes Histogram

if 'Control-Parkinsons' in stype:
    plt.figure(figsize=(7,6))
    plt.title('Slopes Distribution by group_'+sname)
    plt.xlabel('Evolution Trajectory Slope')
    sns.histplot(pdd_slopes, bins=50, kde=True, element='step', label='Parkinsons')
    plt.axvline(np.median(pdd_slopes), c = 'blue', label ='Median Parkinsons')
    plt.axvline(np.median(ctrl_slopes), c = 'green', label = 'Median Controls')
    sns.histplot(ctrl_slopes, color='green', bins=50, kde=True, element='step', label='Controls')
    plt.legend()
    plt.tight_layout()
    plt.savefig('Slopes Distribution by group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    

elif 'Control-Prodromal-Parkinsons' in stype:
    plt.figure(figsize=(7,6))
    plt.title('Slopes Distribution by group_'+sname)
    plt.xlabel('Evolution Trajectory Slope')
    
    sns.histplot(pdd_slopes, bins=50, kde=True, element='step', label='Parkinsons')
    sns.histplot(prod_slopes, bins=50, kde=True, element='step', label='Prodromals')
    sns.histplot(ctrl_slopes, bins=50, kde=True, element='step', label='Controls')
    
    plt.axvline(np.median(pdd_slopes), c = 'blue', label ='Median Parkinsons')
    plt.axvline(np.median(prod_slopes), c = 'orange', label = 'Median Prodromals')
    plt.axvline(np.median(ctrl_slopes), c = 'green', label = 'Median Controls')
    
    
    plt.legend()
    plt.savefig('Slopes Distribution by group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Boxplot PDD vs Ctrl slopes 

print('PDD')
n= 0
normal = sp.shapiro(pdd_slopes)
print(str(normal.pvalue))
if normal.pvalue < 0.05:
    n=1

print('Ctrl')
normal = sp.shapiro(ctrl_slopes)
print(str(normal.pvalue))
if normal.pvalue < 0.05:
    n=1

pvals_whole =[]
if n==1:  #Data not normal, perform U Mann Whitney
    pvals_whole.append(sp.mannwhitneyu(pdd_slopes, ctrl_slopes)[1])


if 'Control-Parkinsons' in stype:
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(8)
    plt.suptitle('MoCA Slopes Parkinsons vs Controls', fontsize = 16)
    if n==1:
        plt.title('U Mann-Whitney Test', fontsize=10, loc='right', pad=0)
    ##
    #PDD Boxplot 
    colors = ['steelblue']
    bplot = ax.boxplot(pdd_slopes, positions=[1], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Controls Boxplot
    colors = ['green']
    bplot=ax.boxplot(ctrl_slopes, positions=[2], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    ##
    
    plt.xticks([1,2],['Parkinsons','Controls'])

    
    plt.xlabel('Groups')
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'Green',label='Controls')]
    
    #Tests between groups 
    plt.text(1.4,-1.3,'p=%.4f'%pvals_whole[0], fontsize = 7)
    plt.plot([1,2],[-1.25,-1.25], color ='k')
    
    
    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Change in MoCA Score evolution PDD vs Ctrl_'+(os.path.basename(sv_path)[:-4])+'_'+sname)






#%%---------------MoCA Slopes Stats by age bracket test 

if 'Control-Parkinsons' in stype:
    
    pdd_ranks=[rank_30_40_pdd_slopes,
               rank_40_50_pdd_slopes,
               rank_50_60_pdd_slopes,
               rank_60_70_pdd_slopes,
               rank_70_80_pdd_slopes,
               rank_80_90_pdd_slopes]
    
    ctrl_ranks=[rank_30_40_ctrl_slopes,
                rank_40_50_ctrl_slopes,
                rank_50_60_ctrl_slopes,
                rank_60_70_ctrl_slopes,
                rank_70_80_ctrl_slopes, 
                rank_80_90_ctrl_slopes]
    
    print('PDD')
    n= 0
    for i in pdd_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    print('Ctrl')
    for i in ctrl_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    pvals =[]
    if n==1:  #Data not normal, perform U Mann Whitney
        for j,i in enumerate(pdd_ranks):
            pvals.append(sp.mannwhitneyu(i, ctrl_ranks[j])[1])

elif 'Control-Prodromal-Parkinsons' in stype:
    
    pdd_ranks=[rank_30_40_pdd_slopes,
               rank_40_50_pdd_slopes,
               rank_50_60_pdd_slopes,
               rank_60_70_pdd_slopes,
               rank_70_80_pdd_slopes,
               rank_80_90_pdd_slopes]
    
    prod_ranks=[rank_30_40_prod_slopes,
                rank_40_50_prod_slopes,
                rank_50_60_prod_slopes,
                rank_60_70_prod_slopes,
                rank_70_80_prod_slopes, 
                rank_80_90_prod_slopes]
    
    ctrl_ranks=[rank_30_40_ctrl_slopes,
                rank_40_50_ctrl_slopes,
                rank_50_60_ctrl_slopes,
                rank_60_70_ctrl_slopes,
                rank_70_80_ctrl_slopes, 
                rank_80_90_ctrl_slopes]
    
    print('PDD')
    n= 0
    for i in pdd_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    print('Prod')
    for i in prod_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
            
    print('Ctrl')
    for i in ctrl_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    kw_pvals =[]
    if n==1:  #Data not normal, perform Kruskal-wallis
    
        for i in range(6):
            kw_pvals.append(sp.kruskal(pdd_ranks[i],prod_ranks[i],ctrl_ranks[i])[1])
            
        dunn_pvals=[]
    #Perform Post-Hoc Dunn test
        for i in range(6):
            if kw_pvals[i]<0.05: #If K-W significative, selec
                print(i)
                pd_tmp= pdd_ranks[i]
                pr_tmp= prod_ranks[i]
                ct_tmp= ctrl_ranks[i]
                dt = [pd_tmp,pr_tmp,ct_tmp]
                dunn_pvals.append(dunn(dt,p_adjust='fdr_tsbky'))
    

#%%---------------Violin plot by age bracket /// [DEPRECATED]

# if 'Control-Parkinsons' in stype:
#     plt.figure(figsize=(7,6))
#     plt.title('Change in MoCA Score evolution by Age Bracket')
#     plt.violinplot(pdd_ranks, positions=[1,2,3,4,5,6])
#     plt.violinplot(ctrl_ranks, positions=[1.2,2.2,3.3,4.2,5.2,6.2])
#     plt.xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    
#     positions=[1,2,3,4,5,6]
#     for j,i in enumerate(pdd_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)
    
#     positions=[1.2,2.2,3.3,4.2,5.2,6.2]
#     for j,i in enumerate(ctrl_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'green',s = 10, alpha =0.7)
    
#     plt.xlabel('Age Bracket')
#     plt.ylabel('$\Delta$ MoCA Score')
    
#     legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
#              Line2D([0],[0], color = 'green',label='Controls')]
    
#     plt.text(1,min(rank_30_40_pdd_slopes+rank_30_40_ctrl_slopes)-0.3,'p=%.4f'%pvals[0], fontsize = 7)
#     plt.text(2,min(rank_40_50_pdd_slopes+rank_40_50_ctrl_slopes)-0.3,'p=%.4f'%pvals[1], fontsize = 7)
#     plt.text(3,min(rank_50_60_pdd_slopes+rank_50_60_ctrl_slopes)-0.3,'p=%.4f'%pvals[2], fontsize = 7)
#     plt.text(4,min(rank_60_70_pdd_slopes+rank_60_70_ctrl_slopes)-0.3,'p=%.4f'%pvals[3], fontsize = 7)
#     plt.text(5,min(rank_70_80_pdd_slopes+rank_70_80_ctrl_slopes)-0.3,'p=%.4f'%pvals[4], fontsize = 7)
#     plt.text(6,min(rank_80_90_pdd_slopes+rank_80_90_ctrl_slopes)-0.3,'p=%.4f'%pvals[5], fontsize = 7)
    
#     plt.legend(handles=legends)
    
#     plt.savefig('Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

# elif 'Control-Prodromal-Parkinsons' in stype:
#     plt.figure(figsize=(7,6))
#     plt.suptitle('Change in MoCA Score evolution by Age Bracket')
#     if n==1:
#         plt.title('Kruskal-Wallis Test', fontsize=10, loc='right', pad=0)
#     plt.violinplot(pdd_ranks, positions=[1,2,3,4,5,6])
#     plt.violinplot(prod_ranks, positions=[1.2,2.2,3.3,4.2,5.2,6.2])
#     plt.violinplot(ctrl_ranks, positions=[1.4,2.4,3.4,4.4,5.4,6.4])
#     plt.xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    
#     positions=[1,2,3,4,5,6]
#     for j,i in enumerate(pdd_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)
            
#     positions=[1.2,2.2,3.3,4.2,5.2,6.2]
#     for j,i in enumerate(prod_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'orange',s = 10, alpha =0.7)
    
#     positions=[1.4,2.4,3.4,4.4,5.4,6.4]
#     for j,i in enumerate(ctrl_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'green',s = 10, alpha =0.7)
    
#     plt.xlabel('Age Bracket')
#     plt.ylabel('$\Delta$ MoCA Score')
    
#     legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
#              Line2D([0],[0], color = 'orange',label='Prodromals'),
#              Line2D([0],[0], color = 'green',label='Controls')]
    
#     plt.text(1,min(rank_30_40_pdd_slopes+rank_30_40_ctrl_slopes+rank_30_40_prod_slopes)-0.3,'p=%.4f'%kw_pvals[0], fontsize = 7)
#     plt.text(2,min(rank_40_50_pdd_slopes+rank_40_50_ctrl_slopes+rank_40_50_prod_slopes)-0.3,'p=%.4f'%kw_pvals[1], fontsize = 7)
#     plt.text(3,min(rank_50_60_pdd_slopes+rank_50_60_ctrl_slopes+rank_50_60_prod_slopes)-0.3,'p=%.4f'%kw_pvals[2], fontsize = 7)
#     plt.text(4,min(rank_60_70_pdd_slopes+rank_60_70_ctrl_slopes+rank_60_70_prod_slopes)-0.3,'p=%.4f'%kw_pvals[3], fontsize = 7)
#     plt.text(5,min(rank_70_80_pdd_slopes+rank_70_80_ctrl_slopes+rank_70_80_prod_slopes)-0.3,'p=%.4f'%kw_pvals[4], fontsize = 7)
#     plt.text(6,min(rank_80_90_pdd_slopes+rank_80_90_ctrl_slopes+rank_80_90_prod_slopes)-0.3,'p=%.4f'%kw_pvals[5], fontsize = 7)
    
#     plt.ylim(-7,10)
    
#     plt.legend(handles=legends)
    
#     plt.savefig('Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%---------------Post Hoc violin Plots (PDD-Prod-Ctrl) /// [DEPRECATED]

# if 'Control-Prodromal-Parkinsons' in stype:
#     plt.figure(figsize=(7,6))
#     plt.suptitle('Change in MoCA Score evolution by Age Bracket')
#     if n==1:
#         plt.title('Post-hoc Dunn Test', fontsize=10, loc='right', pad=0)
    
#     ageranks=['30-40','40-50','50-60','60-70','70-80','80-90']
#     pos_a=[1,2,3,4,5,6]
#     kw_pvals = np.array(kw_pvals)
        
#     plt.violinplot([pdd_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i] for i in range(6) if kw_pvals[i]<0.05])
#     plt.violinplot([prod_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i]+0.2 for i in range(6) if kw_pvals[i]<0.05])
#     plt.violinplot([ctrl_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i]+0.4 for i in range(6) if kw_pvals[i]<0.05])
#     plt.xticks([pos_a[i] for i in range(6) if kw_pvals[i]<0.05], [ageranks[i] for i in range(6) if kw_pvals[i]<0.05])
    
    
#     c=0 #Iteration counter for Dunn pvals selection
#     for j,i in enumerate(kw_pvals): 
#         if i <0.05: #Only iterate through age gaps that are KW significative
#             #Data Scatter
#             for a in pdd_ranks[j]: 
#                 plt.scatter(pos_a[j],a, color = 'steelblue',s = 10, alpha =0.7)
            
#             for a in prod_ranks[j]: 
#                 plt.scatter(pos_a[j]+0.2,a, color = 'orange',s = 10, alpha =0.7)
            
#             for a in ctrl_ranks[j]: 
#                 plt.scatter(pos_a[j]+0.4,a, color = 'green',s = 10, alpha =0.7)
        
#             #Comparisons whithin groups
#             #PD vs Prodromal 
#             plt.plot([pos_a[j],pos_a[j]+0.2],[-7.5,-7.5],color ='k')
#             plt.text(pos_a[j],-7.4,'p=%.3f'%dunn_pvals[c][1][2], fontsize = 7) #Select first row, second col (1vs2)
            
#             #PD vs Ctrl 
#             plt.plot([pos_a[j],pos_a[j]+0.4],[-8.5,-8.5],color ='k')
#             plt.text(pos_a[j]+0.1,-8.4,'p=%.3f'%dunn_pvals[c][1][3], fontsize = 7) #Select first row, third col (1vs3)
            
#             #Prod vs Ctrl
#             plt.plot([pos_a[j]+0.2,pos_a[j]+0.4],[-9.5,-9.5],color ='k')
#             plt.text(pos_a[j]+0.2,-9.4,'p=%.3f'%dunn_pvals[c][2][3], fontsize = 7) #Select first row, third col (2vs3)
#             c+=1
            
#     plt.ylim(-10.2,10.2)
#     plt.xlabel('Age Bracket')
#     plt.ylabel('$\Delta$ MoCA Score')
    
#     legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
#              Line2D([0],[0], color = 'orange',label='Prodromals'),
#              Line2D([0],[0], color = 'green',label='Controls')]

#     plt.legend(handles=legends)
#     plt.savefig('Post Hoc Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%---------------Boxplot by age bracket

if 'Control-Parkinsons' in stype:
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(8)
    plt.title('Change in MoCA Score evolution by Age Bracket')
    
    ##
    #PDD Boxplot 
    colors = ['steelblue']*6
    bplot = ax.boxplot(pdd_ranks, positions=[1,3,5,7,9,11], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Controls Boxplot
    colors = ['green']*6
    bplot=ax.boxplot(ctrl_ranks, positions=[1.7,3.7,5.7,7.7,9.7,11.7], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        
    plt.xticks([1,3,5,7,9,11],['30-40','40-50','50-60','60-70','70-80','80-90'])
    
    plt.xlabel('Age Bracket')
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'green',label='Controls')]
    
    plt.text(1,-2.5,'p=%.4f'%pvals[0], fontsize = 7)
    plt.text(3,-2.5,'p=%.4f'%pvals[1], fontsize = 7)
    plt.text(5,-2.5,'p=%.4f'%pvals[2], fontsize = 7)
    plt.text(7,-2.5,'p=%.4f'%pvals[3], fontsize = 7)#, color='red')
    plt.text(9,-2.5,'p=%.4f'%pvals[4], fontsize = 7)
    plt.text(11,-2.5,'p=%.4f'%pvals[5], fontsize = 7)
    
    plt.plot([1,1.7],[-2.4,-2.4], color ='k')
    plt.plot([3,3.7],[-2.4,-2.4], color ='k')
    plt.plot([5,5.7],[-2.4,-2.4], color ='k')
    plt.plot([7,7.7],[-2.4,-2.4], color ='k')
    plt.plot([9,9.7],[-2.4,-2.4], color ='k')
    plt.plot([11,11.7],[-2.4,-2.4], color ='k')
    
    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Boxplot Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

elif 'Control-Prodromal-Parkinsons' in stype:
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(8)
    plt.suptitle('Change in MoCA Score evolution by Age Bracket', fontsize=16)
    if n==1:
        plt.title('Kruskal-Wallis Test', fontsize=10, loc='right', pad=0)
        
    #PDD Boxplot 
    colors = ['steelblue']*6
    bplot = ax.boxplot(pdd_ranks, positions=[1,5,9,13,17,21], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Prodormals Boxplot
    colors = ['orange']*6
    bplot = ax.boxplot(prod_ranks, positions=[2,6,10,14,18,22], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Controls Boxplot
    colors = ['green']*6
    bplot=ax.boxplot(ctrl_ranks, positions=[3,7,11,15,19,23], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.xticks([1,5,9,13,17,21],['30-40','40-50','50-60','60-70','70-80','80-90'])
        
    plt.xlabel('Age Bracket')
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'orange',label='Prodromals'),
             Line2D([0],[0], color = 'green',label='Controls')]
    
    plt.text(1,-3,'p=%.4f'%kw_pvals[0], fontsize = 7)
    plt.text(5,-3,'p=%.4f'%kw_pvals[1], fontsize = 7)
    plt.text(9,-3,'p=%.4f'%kw_pvals[2], fontsize = 7)
    plt.text(13,-3,'p=%.4f'%kw_pvals[3], fontsize = 7)
    plt.text(17,-3,'p=%.4f'%kw_pvals[4], fontsize = 7)
    plt.text(21,-3,'p=%.4f'%kw_pvals[5], fontsize = 7)
    
    plt.plot([1,3],[-2.8,-2.8], color ='k')
    plt.plot([5,7],[-2.8,-2.8], color ='k')
    plt.plot([9,11],[-2.8,-2.8], color ='k')
    plt.plot([13,15],[-2.8,-2.8], color ='k')
    plt.plot([17,19],[-2.8,-2.8], color ='k')
    plt.plot([21,23],[-2.8,-2.8], color ='k')
    
    plt.legend(handles=legends)
    plt.tight_layout()
    
    plt.savefig('Boxplot Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%---------------Boxplot Post Hoc violin Plots (PDD-Prod-Ctrl)

if 'Control-Prodromal-Parkinsons' in stype:
    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(7)
    plt.suptitle('Change in MoCA Score evolution by Age Bracket')
    if n==1:
        plt.title('Post-hoc Dunn Test', fontsize=10, loc='right', pad=0)
    
    ageranks=['30-40','40-50','50-60','60-70','70-80','80-90']
    pos_a=[1,5,9,13,17,21]
    kw_pvals = np.array(kw_pvals)
    
    ##
    #PDD Boxplot 
    colors = ['steelblue']*sum(kw_pvals<0.05)
    bplot = ax.boxplot([pdd_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i]-0.8 for i in range(6) if kw_pvals[i]<0.05], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Prodormals Boxplot
    colors = ['orange']*sum(kw_pvals<0.05)
    bplot = ax.boxplot([prod_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i] for i in range(6) if kw_pvals[i]<0.05], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Controls Boxplot
    colors = ['green']*sum(kw_pvals<0.05)
    bplot=ax.boxplot([ctrl_ranks[i] for i in range(6) if kw_pvals[i]<0.05], positions=[pos_a[i]+0.8 for i in range(6) if kw_pvals[i]<0.05], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.xticks([pos_a[i] for i in range(6) if kw_pvals[i]<0.05], [ageranks[i] for i in range(6) if kw_pvals[i]<0.05])
    
    
    c=0 #Iteration counter for Dunn pvals selection
    for j,i in enumerate(kw_pvals): 
        if i <0.05: #Only iterate through age gaps that are KW significative

            #Comparisons whithin groups
            #PD vs Prodromal 
            plt.plot([pos_a[j]-0.8,pos_a[j]],[-2.9,-2.9],color ='k')
            plt.text(pos_a[j]-0.7,-2.8,'p=%.3f'%dunn_pvals[c][1][2], fontsize = 7) #Select first row, second col (1vs2)
            
            #PD vs Ctrl 
            plt.plot([pos_a[j]-0.8,pos_a[j]+0.8],[-3.3,-3.3],color ='k')
            plt.text(pos_a[j]-0.55,-3.2,'p=%.3f'%dunn_pvals[c][1][3], fontsize = 7) #Select first row, third col (1vs3)
            
            #Prod vs Ctrl
            plt.plot([pos_a[j],pos_a[j]+0.8],[-3.7,-3.7],color ='k')
            plt.text(pos_a[j]+0.1,-3.6,'p=%.3f'%dunn_pvals[c][2][3], fontsize = 7) #Select first row, third col (2vs3)
            c+=1
            
    # plt.ylim(-10.2,10.2)
    plt.xlabel('Age Bracket')
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'orange',label='Prodromals'),
             Line2D([0],[0], color = 'green',label='Controls')]

    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Boxplot Post Hoc Change in MoCA Score evolution vs Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------MoCA Slopes Stats by Early-Late Group

if 'Control-Parkinsons' in stype:
    elo_pdd_ranks=[rank_30_40_pdd_slopes + rank_40_50_pdd_slopes, 
                   rank_50_60_pdd_slopes+rank_60_70_pdd_slopes+rank_70_80_pdd_slopes+rank_80_90_pdd_slopes]
    
    matched_ctrl_ranks=[rank_30_40_ctrl_slopes + rank_40_50_ctrl_slopes, 
                        rank_50_60_ctrl_slopes+ rank_60_70_ctrl_slopes + rank_70_80_ctrl_slopes + rank_80_90_ctrl_slopes]
    
    print('PDD Normality')
    n= 0
    for i in elo_pdd_ranks:
        normal = sp.shapiro(i)
        print(str(normal))
        if normal.pvalue < 0.05:
            n=1
    
    print('\n\nCtrl Normality')
    for i in matched_ctrl_ranks:
        normal = sp.shapiro(i)
        print(str(normal))
        if normal.pvalue < 0.05:
            n=1
    
    pvals_elo =[] #Between groups
    if n==1:  #Data not normal, perform U Mann Whitney
        for j,i in enumerate(elo_pdd_ranks):
            print('\n\nBetween groups ')
            pvals_elo.append(sp.mannwhitneyu(i, matched_ctrl_ranks[j])[1])
            print('U '+str(sp.mannwhitneyu(i, matched_ctrl_ranks[j])))
            
    pvals_elo_wg =[] #within group
    if n==1:  #Data not normal, perform U Mann Whitney
        print('\n\nWithin groups ')
        pvals_elo_wg.append(sp.mannwhitneyu(elo_pdd_ranks[0],elo_pdd_ranks[1])[1])
        print(str(sp.mannwhitneyu(elo_pdd_ranks[0],elo_pdd_ranks[1])))
        pvals_elo_wg.append(sp.mannwhitneyu(matched_ctrl_ranks[0],matched_ctrl_ranks[1])[1])
        print(str(sp.mannwhitneyu(matched_ctrl_ranks[0],matched_ctrl_ranks[1])))
            
elif 'Control-Prodromal-Parkinsons' in stype:
    elo_pdd_ranks=[rank_30_40_pdd_slopes + rank_40_50_pdd_slopes, 
                   rank_50_60_pdd_slopes + rank_60_70_pdd_slopes+rank_70_80_pdd_slopes+rank_80_90_pdd_slopes]
    
    matched_ctrl_ranks=[rank_30_40_ctrl_slopes + rank_40_50_ctrl_slopes, 
                        rank_50_60_ctrl_slopes + rank_60_70_ctrl_slopes + rank_70_80_ctrl_slopes + rank_80_90_ctrl_slopes]
    
    matched_prod_ranks=[rank_30_40_prod_slopes + rank_40_50_prod_slopes, 
                        rank_50_60_prod_slopes + rank_60_70_prod_slopes + rank_70_80_prod_slopes + rank_80_90_prod_slopes]
    
    print('PDD')
    n= 0
    for i in elo_pdd_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    print('Prod')
    for i in matched_prod_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    print('Ctrl')
    for i in matched_ctrl_ranks:
        normal = sp.shapiro(i)
        print(str(normal.pvalue))
        if normal.pvalue < 0.05:
            n=1
    
    kw_pvals_elo =[]
    if n==1:  #Data not normal, perform kruskal wallis test 
        for i in range(2):
            kw_pvals_elo.append(sp.kruskal(elo_pdd_ranks[i],matched_prod_ranks[i],matched_ctrl_ranks[i])[1])
        
        dunn_pvals_elo=[] #Post Hoc Dunn test
        for i in range(2):
            if kw_pvals_elo[i]<0.05: #If K-W significative, selec
                print(i)
                pd_tmp= elo_pdd_ranks[i]
                pr_tmp= matched_prod_ranks[i]
                ct_tmp= matched_ctrl_ranks[i]
                dt = [pd_tmp,pr_tmp,ct_tmp]
                dunn_pvals_elo.append(dunn(dt,p_adjust='fdr_tsbky'))
                
    #FALTA HACER LA COMPARACION DENTRO DE GRUPOS 
    kw_pvals_elo_wg=[] #within groups
            

#%%---------------Violin plot by Early-Late onset group /// [DEPRECATED]

# if 'Control-Parkinsons' in stype:
#     plt.figure(figsize=(7,6))
#     plt.title('Change in MoCA Score evolution by group')
#     plt.violinplot(elo_pdd_ranks, positions=[1,2])
#     plt.violinplot(matched_ctrl_ranks, positions=[1.2,2.2])
#     plt.xticks([1,2],['Early Onset','Late Onset'])
    
#     positions=[1,2]
#     for j,i in enumerate(elo_pdd_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)
    
#     positions=[1.2,2.2]
#     for j,i in enumerate(matched_ctrl_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'orange',s = 10, alpha =0.7)
    
#     plt.xlabel('Groups')
#     plt.ylabel('$\Delta$ MoCA Score')
    
#     legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
#              Line2D([0],[0], color = 'orange',label='Controls')]
    
#     plt.text(1,min(elo_pdd_ranks[0]+matched_ctrl_ranks[0])-0.3,'p=%.4f'%pvals_elo[0], fontsize = 7)
#     plt.text(2,min(elo_pdd_ranks[1]+matched_ctrl_ranks[1])-0.3,'p=%.4f'%pvals_elo[1], fontsize = 7)
    
    
#     plt.legend(handles=legends)
    
#     plt.savefig('Change in MoCA Score evolution by Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

# elif 'Control-Prodromal-Parkinsons' in stype:
    
#     plt.figure(figsize=(7,6))
#     plt.suptitle('Change in MoCA Score evolution by group', fontsize=16)
#     if n==1:
#         plt.title('Kruskal-Wallis Test', fontsize=10, loc='right', pad=0)
#     plt.violinplot(elo_pdd_ranks, positions=[1,2])
#     plt.violinplot(matched_prod_ranks, positions=[1.2,2.2])
#     plt.violinplot(matched_ctrl_ranks, positions=[1.4,2.4])
#     plt.xticks([1,2],['Early Onset','Late Onset'])
    
#     positions=[1,2]
#     for j,i in enumerate(elo_pdd_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)
    
#     positions=[1.2,2.2]
#     for j,i in enumerate(matched_prod_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'orange',s = 10, alpha =0.7)
            
#     positions=[1.4,2.4]
#     for j,i in enumerate(matched_ctrl_ranks):
#         for a in i:
#             plt.scatter(positions[j],a, color = 'green',s = 10, alpha =0.7)
            
#     plt.plot([1,1.4],[-8.2,-8.2], color ='k')
#     plt.plot([2,2.4],[-8.2,-8.2], color ='k')
    
#     plt.text(1.1,-8.1,'p=%.3f'%kw_pvals_elo[0], fontsize = 9)
#     plt.text(2.1,-8.1,'p=%.3f'%kw_pvals_elo[1], fontsize = 9)
    
#     plt.xlabel('Groups')
#     plt.ylabel('$\Delta$ MoCA Score')
#     plt.ylim(-9,9.2)
    
#     legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
#              Line2D([0],[0], color = 'orange',label='Controls')]

#     plt.legend(handles=legends)
#     plt.savefig('Change in MoCA Score evolution by Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Box plot by Early-Late onset group

if 'Control-Parkinsons' in stype:
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(8)
    plt.suptitle('Change in MoCA Score evolution by group', fontsize = 16)
    if n==1:
        plt.title('U Mann-Whitney Test', fontsize=10, loc='right', pad=0)
    ##
    #PDD Boxplot 
    colors = ['steelblue']*2
    bplot = ax.boxplot(elo_pdd_ranks, positions=[1,2], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    #Controls Boxplot
    colors = ['green']*2
    bplot=ax.boxplot(matched_ctrl_ranks, positions=[1.2,2.2], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    ##
    
    plt.xticks([1,2],['Early Onset','Late Onset'])

    
    plt.xlabel('Groups')
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'Green',label='Controls')]
    
    #Tests between groups 
    plt.text(1,-1.56,'p=%.4f'%pvals_elo[0], fontsize = 7)
    plt.text(2,-1.56,'p=%.4f'%pvals_elo[1], fontsize = 7)#, color='red')
    plt.plot([1,1.2],[-1.5,-1.5], color ='k')
    plt.plot([2,2.2],[-1.5,-1.5], color ='k')
    
    #Tests within groups
    plt.text(1.4,-1.7,'p=%.4f'%pvals_elo_wg[0], fontsize = 7, color = 'red')
    plt.text(1.6,-1.8,'p=%.4f'%pvals_elo_wg[1], fontsize = 7)
    plt.plot([1,2],[-1.64,-1.64], color ='k')
    plt.plot([1.2,2.2],[-1.74,-1.74], color ='k')
    
    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Change in MoCA Score evolution by Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

elif 'Control-Prodromal-Parkinsons' in stype:
    
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(8)
    plt.suptitle('Change in MoCA Score evolution by group', fontsize=16)
    if n==1:
        plt.title('Kruskal-Wallis Test', fontsize=10, loc='right', pad=0)
        
    #PDD Boxplot 
    colors = ['steelblue']*2
    bplot = ax.boxplot(elo_pdd_ranks, positions=[0.8,1.8], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        
    #Prodormals Boxplot
    colors = ['orange']*2
    bplot = ax.boxplot(matched_prod_ranks, positions=[1,2], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
     
    #Controls Boxplot
    colors = ['green']*2
    bplot=ax.boxplot(matched_ctrl_ranks, positions=[1.2,2.2], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.xticks([1,2],['Early Onset','Late Onset'])
    
    plt.plot([0.8,1.2],[-2.2,-2.2], color ='k')
    plt.plot([1.8,2.2],[-2.2,-2.2], color ='k')
    
    plt.text(0.9,-2.1,'p=%.3f'%kw_pvals_elo[0], fontsize = 9)
    plt.text(1.9,-2.1,'p=%.3f'%kw_pvals_elo[1], fontsize = 9)
    
    plt.xlabel('Groups')
    plt.ylabel('$\Delta$ MoCA Score')
    plt.xlim(0.6,2.4)
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'orange',label='Prodromals'),
             Line2D([0],[0], color = 'green',label='Controls')]

    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Boxplot Change in MoCA Score evolution by Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Boxplot Post Hoc Early vs late onset 

if 'Control-Prodromal-Parkinsons' in stype:
    
    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(7)
    plt.suptitle('Change in MoCA score evolution by Age Group')
    if n==1:
        plt.title('Post-hoc Dunn Test', fontsize=10, loc='right', pad=0)
    
    ageranks=['Early Onset','Late Onset']
    pos_a=[1,2]
    kw_pvals_elo = np.array(kw_pvals_elo)
    
    #PDD Boxplot 
    colors = ['steelblue']*sum(kw_pvals_elo<0.05)
    bplot = ax.boxplot([elo_pdd_ranks[i] for i in range(2) if kw_pvals_elo[i]<0.05], positions=[pos_a[i] for i in range(2) if kw_pvals_elo[i]<0.05], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        
    #Prodormals Boxplot
    colors = ['orange']*sum(kw_pvals_elo<0.05)
    bplot = ax.boxplot([matched_prod_ranks[i] for i in range(2) if kw_pvals_elo[i]<0.05], positions=[pos_a[i]+0.2 for i in range(2) if kw_pvals_elo[i]<0.05], notch=True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
     
    #Controls Boxplot
    colors = ['green']*2
    bplot=ax.boxplot([matched_ctrl_ranks[i] for i in range(2) if kw_pvals_elo[i]<0.05], positions=[pos_a[i]+0.4 for i in range(2) if kw_pvals_elo[i]<0.05], notch = True, showfliers=False, patch_artist=True)
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
   
    plt.xticks([pos_a[i]+0.2 for i in range(2) if kw_pvals_elo[i]<0.05], [ageranks[i] for i in range(2) if kw_pvals_elo[i]<0.05])
    
    
    c=0 #Iteration counter for Dunn pvals selection
    for j,i in enumerate(kw_pvals_elo): 
        if i <0.05: #Only iterate through groups that are KW significative
 
            #Comparisons whithin groups
            #PD vs Prodromal 
            plt.plot([pos_a[j],pos_a[j]+0.2],[-2.5,-2.5],color ='k')
            plt.text(pos_a[j],-2.45,'p=%.3f'%dunn_pvals_elo[c][1][2], fontsize = 7) #Select first row, second col (1vs2)
            
            #PD vs Ctrl 
            plt.plot([pos_a[j],pos_a[j]+0.4],[-2.7,-2.7],color ='k')
            plt.text(pos_a[j]+0.1,-2.65,'p=%.3f'%dunn_pvals_elo[c][1][3], fontsize = 7) #Select first row, third col (1vs3)
            
            #Prod vs Ctrl
            plt.plot([pos_a[j]+0.2,pos_a[j]+0.4],[-2.9,-2.9],color ='k')
            plt.text(pos_a[j]+0.2,-2.85,'p=%.3f'%dunn_pvals_elo[c][2][3], fontsize = 7) #Select first row, third col (2vs3)
            c+=1
            
    plt.ylabel('$\Delta$ MoCA Score')
    
    legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
             Line2D([0],[0], color = 'orange',label='Prodromals'),
             Line2D([0],[0], color = 'green',label='Controls')]

    plt.legend(handles=legends)
    plt.tight_layout()
    plt.savefig('Boxplot Post Hoc Change in MoCA score evolution vs Age Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%---------------Absolutes  violin plot by age bracket

abs_pdd_ranks=[np.abs(rank_30_40_pdd_slopes),
               np.abs(rank_40_50_pdd_slopes),
               np.abs(rank_50_60_pdd_slopes),
               np.abs(rank_60_70_pdd_slopes),
               np.abs(rank_70_80_pdd_slopes),
               np.abs(rank_80_90_pdd_slopes)]

abs_ctrl_ranks=[np.abs(rank_30_40_ctrl_slopes),
                np.abs(rank_40_50_ctrl_slopes),
                np.abs(rank_50_60_ctrl_slopes),
                np.abs(rank_60_70_ctrl_slopes),
                np.abs(rank_70_80_ctrl_slopes), 
                np.abs(rank_80_90_ctrl_slopes)]

print('PDD')
n= 0
for i in abs_pdd_ranks:
    normal = sp.shapiro(i)
    print(str(normal.pvalue))
    if normal.pvalue < 0.05:
        n=1

print('Ctrl')
for i in abs_ctrl_ranks:
    normal = sp.shapiro(i)
    print(str(normal.pvalue))
    if normal.pvalue < 0.05:
        n=1

abs_pvals =[]
if n==1:  #Data not normal, perform U Mann Whitney
    for j,i in enumerate(abs_pdd_ranks):
        abs_pvals.append(sp.mannwhitneyu(i, abs_ctrl_ranks[j])[1])

plt.figure(figsize=(7,6))
plt.title('Absolute Change in MoCA Score evolution by Age Bracket')
plt.violinplot(abs_pdd_ranks, positions=[1,2,3,4,5,6])
plt.violinplot(abs_ctrl_ranks, positions=[1.2,2.2,3.3,4.2,5.2,6.2])
plt.xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
plt.xlabel('Age bracket')
plt.ylabel('Magnitude $\Delta$ MoCA Score')

legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
         Line2D([0],[0], color = 'orange',label='Controls')]

positions=[1,2,3,4,5,6]
for j,i in enumerate(abs_pdd_ranks):
    for a in i:
        plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)

positions=[1.2,2.2,3.3,4.2,5.2,6.2]
for j,i in enumerate(abs_ctrl_ranks):
    for a in i:
        plt.scatter(positions[j],a, color = 'orange',s = 10, alpha =0.7)

plt.text(1,max(np.abs(rank_30_40_pdd_slopes+rank_30_40_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[0], fontsize = 7)
plt.text(2,max(np.abs(rank_40_50_pdd_slopes+rank_40_50_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[1], fontsize = 7)
plt.text(3,max(np.abs(rank_50_60_pdd_slopes+rank_50_60_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[2], fontsize = 7)
plt.text(4,max(np.abs(rank_60_70_pdd_slopes+rank_60_70_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[3], fontsize = 7)
plt.text(5,max(np.abs(rank_70_80_pdd_slopes+rank_70_80_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[4], fontsize = 7)
plt.text(6,max(np.abs(rank_80_90_pdd_slopes+rank_80_90_ctrl_slopes))+0.1,'p=%.4f'%abs_pvals[5], fontsize = 7)

plt.legend(handles=legends)

plt.savefig('Absolute Change in MoCA Score evolution by Age Bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Absolutes  violin plot by group

abs_elo_pdd_ranks=[np.abs(rank_30_40_pdd_slopes + rank_40_50_pdd_slopes),
                   np.abs(rank_50_60_pdd_slopes+rank_60_70_pdd_slopes+rank_70_80_pdd_slopes+rank_80_90_pdd_slopes)]

abs_matched_ctrl_ranks=[np.abs(rank_30_40_ctrl_slopes + rank_40_50_ctrl_slopes),
                        np.abs(rank_50_60_ctrl_slopes + rank_60_70_ctrl_slopes + rank_70_80_ctrl_slopes + rank_80_90_ctrl_slopes)]

print('PDD')
n= 0
for i in abs_elo_pdd_ranks:
    normal = sp.shapiro(i)
    print(str(normal.pvalue))
    if normal.pvalue < 0.05:
        n=1

print('Ctrl')
for i in abs_matched_ctrl_ranks:
    normal = sp.shapiro(i)
    print(str(normal.pvalue))
    if normal.pvalue < 0.05:
        n=1

abs_elo_pvals =[]
if n==1:  #Data not normal, perform U Mann Whitney
    for j,i in enumerate(abs_elo_pdd_ranks):
        abs_elo_pvals.append(sp.mannwhitneyu(i, abs_matched_ctrl_ranks[j])[1])

plt.figure(figsize=(7,6))
plt.title('Absolute Change in MoCA Score evolution by group')
plt.violinplot(abs_elo_pdd_ranks, positions=[1,2])
plt.violinplot(abs_matched_ctrl_ranks, positions=[1.2,2.2])
plt.xticks([1,2],['Early Onset','Late Onset'])
plt.xlabel('Group')
plt.ylabel('Magnitude $\Delta$ MoCA Score')

legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
         Line2D([0],[0], color = 'orange',label='Controls')]
plt.legend(handles=legends)

positions=[1,2]
for j,i in enumerate(abs_elo_pdd_ranks):
    for a in i:
        plt.scatter(positions[j],a, color = 'steelblue',s = 10, alpha =0.7)

positions=[1.2,2.2]
for j,i in enumerate(abs_matched_ctrl_ranks):
    for a in i:
        plt.scatter(positions[j],a, color = 'orange',s = 10, alpha =0.7)
        
plt.text(1,max(np.abs(rank_30_40_pdd_slopes + rank_40_50_pdd_slopes+ 
                      rank_30_40_ctrl_slopes + rank_40_50_ctrl_slopes))+0.1,'p=%.4f'%abs_elo_pvals[0], fontsize = 7)
plt.text(2,max(np.abs(rank_50_60_pdd_slopes+ rank_60_70_pdd_slopes+rank_70_80_pdd_slopes+rank_80_90_pdd_slopes+
                      rank_50_60_ctrl_slopes+ rank_60_70_ctrl_slopes+rank_70_80_ctrl_slopes+rank_80_90_ctrl_slopes))+0.1,'p=%.4f'%abs_elo_pvals[1], fontsize = 7)

plt.savefig('Absolute Change in MoCA Score evolution by group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Years of education distributions

if 'Control-Parkinsons' in stype:
    
    plt.figure(figsize=(7,6))
    plt.title('Years of Education Distribution_'+sname)
    plt.xlabel('Years of Education')
    sns.histplot(rank_30_40_pdd_yoe+ rank_40_50_pdd_yoe+ rank_50_60_pdd_yoe+
                 rank_60_70_pdd_yoe+ rank_70_80_pdd_yoe+ rank_80_90_pdd_yoe, 
                 bins=10, kde=True, element='step', label='Parkinsons')
    sns.histplot(rank_30_40_ctrl_yoe+ rank_40_50_ctrl_yoe+ rank_50_60_ctrl_yoe+
                 rank_60_70_ctrl_yoe+ rank_70_80_ctrl_yoe+ rank_80_90_ctrl_yoe, 
                 bins=10, kde=True, element='step', label='Controls')
    plt.legend()
    
    plt.savefig('Years of Education Distribution_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    
elif 'Control-Prodromal-Parkinsons' in stype:
    
    plt.figure(figsize=(7,6))
    plt.title('Years of Education Distribution_'+sname)
    plt.xlabel('Years of Education')
    sns.histplot(rank_30_40_pdd_yoe+ rank_40_50_pdd_yoe+ rank_50_60_pdd_yoe+
                 rank_60_70_pdd_yoe+ rank_70_80_pdd_yoe+ rank_80_90_pdd_yoe, 
                 bins=10, kde=True, element='step', label='Parkinsons')
    sns.histplot(rank_30_40_prod_yoe+ rank_40_50_prod_yoe+ rank_50_60_prod_yoe+
                 rank_60_70_prod_yoe+ rank_70_80_prod_yoe+ rank_80_90_prod_yoe, 
                 bins=10, kde=True, element='step', label='Prodromals')
    sns.histplot(rank_30_40_ctrl_yoe+ rank_40_50_ctrl_yoe+ rank_50_60_ctrl_yoe+
                 rank_60_70_ctrl_yoe+ rank_70_80_ctrl_yoe+ rank_80_90_ctrl_yoe, 
                 bins=10, kde=True, element='step', label='Controls')
    plt.legend()
    
    plt.savefig('Years of Education Distribution_'+(os.path.basename(sv_path)[:-4])+'_'+sname)



#%%---------------Delta Slopes vs years of education

if 'Control-Parkinsons' in stype:
    #PDD yoe Lists
    yoe_pdd_list=[rank_30_40_pdd_yoe, rank_40_50_pdd_yoe, rank_50_60_pdd_yoe,
                  rank_60_70_pdd_yoe, rank_70_80_pdd_yoe, rank_80_90_pdd_yoe]
    
    #Ctrl yoe lists
    yoe_ctrl_list=[rank_30_40_ctrl_yoe, rank_40_50_ctrl_yoe, rank_50_60_ctrl_yoe,
                  rank_60_70_ctrl_yoe, rank_70_80_ctrl_yoe, rank_80_90_ctrl_yoe]
    
    
    #Initialize Figure
    fig, ax = plt.subplots(1,2)
    fig.set_figheight(7)
    fig.set_figwidth(12)
    plt.suptitle('MoCA Slope by age bracket vs Years of Education\n'+sname, fontsize=16)
    
    positions_pdd = [[j+1]*len(i) for j,i in enumerate(pdd_ranks)]  #Creating lists of positions by slopes rank
    positions_ctrl = [[j+1]*len(i) for j,i in enumerate(ctrl_ranks)]  #Creating lists of positions by slopes rank
    
    df = pd.DataFrame({'Positions_PDD':np.concatenate(positions_pdd), #concatenate all lists to have single data cols
                       'Slopes_PDD':np.concatenate(pdd_ranks), 
                       'YOE_PDD':np.concatenate(yoe_pdd_list)})
    
    ax[0].scatter(df.Positions_PDD, df.Slopes_PDD, c = df.YOE_PDD, cmap='CMRmap', s = 15)
    
    df = pd.DataFrame({'Positions_Ctrl':np.concatenate(positions_ctrl),
                       'Slopes_Ctrl':np.concatenate(ctrl_ranks),
                       'YOE_Ctrl':np.concatenate(yoe_ctrl_list)})
    
    ax[1].scatter(df.Positions_Ctrl, df.Slopes_Ctrl, c = df.YOE_Ctrl, cmap='CMRmap', s = 15)
    
    #Normalize Colorbar
    N=len(np.concatenate(yoe_pdd_list))
    cmap = plt.get_cmap('CMRmap',N)
    norm = mpl.colors.Normalize(vmin=min([min(np.concatenate(yoe_pdd_list)),min(np.concatenate(yoe_ctrl_list))]),
                                vmax=max([max(np.concatenate(yoe_pdd_list)),max(np.concatenate(yoe_ctrl_list))]))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=ax[1], label = 'Years of Education ')
    
    #-------
    
    
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='$\Delta$ MoCA Score')
    ax[0].set(xlabel='Age Bracket')
    ax[1].set(xlabel='Age Bracket')
    ax[0].set_xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    ax[1].set_xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    
    plt.show()
    plt.savefig('MoCA Slope by age bracket vs Years of Education_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    

elif 'Control-Prodromal-Parkinsons' in stype:
    #PDD yoe Lists
    yoe_pdd_list=[rank_30_40_pdd_yoe, rank_40_50_pdd_yoe, rank_50_60_pdd_yoe,
                  rank_60_70_pdd_yoe, rank_70_80_pdd_yoe, rank_80_90_pdd_yoe]
    
    #Ctrl yoe lists
    yoe_ctrl_list=[rank_30_40_ctrl_yoe, rank_40_50_ctrl_yoe, rank_50_60_ctrl_yoe,
                  rank_60_70_ctrl_yoe, rank_70_80_ctrl_yoe, rank_80_90_ctrl_yoe]
    
    
    #Initialize Figure
    fig, ax = plt.subplots(1,2)
    fig.set_figheight(7)
    fig.set_figwidth(12)
    plt.suptitle('MoCA Slope by age bracket vs Years of Education\n'+sname, fontsize=16)
    
    positions_pdd = [[j+1]*len(i) for j,i in enumerate(pdd_ranks)]  #Creating lists of positions by slopes rank
    positions_ctrl = [[j+1]*len(i) for j,i in enumerate(ctrl_ranks)]  #Creating lists of positions by slopes rank
    
    df = pd.DataFrame({'Positions_PDD':np.concatenate(positions_pdd), #concatenate all lists to have single data cols
                       'Slopes_PDD':np.concatenate(pdd_ranks), 
                       'YOE_PDD':np.concatenate(yoe_pdd_list)})
    
    ax[0].scatter(df.Positions_PDD, df.Slopes_PDD, c = df.YOE_PDD, cmap='CMRmap', s = 15)
    
    df = pd.DataFrame({'Positions_Ctrl':np.concatenate(positions_ctrl),
                       'Slopes_Ctrl':np.concatenate(ctrl_ranks),
                       'YOE_Ctrl':np.concatenate(yoe_ctrl_list)})
    
    ax[1].scatter(df.Positions_Ctrl, df.Slopes_Ctrl, c = df.YOE_Ctrl, cmap='CMRmap', s = 15)
    
    #Normalize Colorbar
    N=len(np.concatenate(yoe_pdd_list))
    cmap = plt.get_cmap('CMRmap',N)
    norm = mpl.colors.Normalize(vmin=min([min(np.concatenate(yoe_pdd_list)),min(np.concatenate(yoe_ctrl_list))]),
                                vmax=max([max(np.concatenate(yoe_pdd_list)),max(np.concatenate(yoe_ctrl_list))]))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    fig.colorbar(sm, ax=ax[1], label = 'Years of Education ')
    
    #-------
    
    
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='$\Delta$ MoCA Score')
    ax[0].set(xlabel='Age Bracket')
    ax[1].set(xlabel='Age Bracket')
    ax[0].set_xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    ax[1].set_xticks([1,2,3,4,5,6],['30-40','40-50','50-60','60-70','70-80','80-90'])
    
    plt.show()
    plt.savefig('MoCA Slope by age bracket vs Years of Education_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------Correlations slope vs years of education by age bracket 

fig, ax = plt.subplots (2,3)
fig.set_figheight(7)
fig.set_figwidth(10)

plt.suptitle('Slopes vs Years of Education by age bracket\n'+sname, fontsize=15)
plt.subplot(2,3,1)
plt.scatter(rank_30_40_pdd_yoe,rank_30_40_pdd_slopes, alpha =0.5)
plt.scatter(rank_30_40_ctrl_yoe,rank_30_40_ctrl_slopes, color='orange', alpha =0.5)
plt.ylabel('$\Delta$ MoCA Score')
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 30-40', fontsize=8, loc='right', pad =0)
legends=[Line2D([0],[0], color = 'white',label='Parkinsons', marker='o', markerfacecolor='Steelblue'),
         Line2D([0],[0], color = 'white',label='Controls', marker='o', markerfacecolor='Orange')]
plt.legend(handles=legends)

plt.subplot(2,3,2)
plt.scatter(rank_40_50_pdd_yoe,rank_40_50_pdd_slopes, alpha=0.5)
plt.scatter(rank_40_50_ctrl_yoe,rank_40_50_ctrl_slopes, color='orange', alpha=0.5)
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 40-50', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,3)
plt.scatter(rank_50_60_pdd_yoe,rank_50_60_pdd_slopes, alpha=0.5)
plt.scatter(rank_50_60_ctrl_yoe,rank_50_60_ctrl_slopes, color='orange', alpha=0.5)
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 50-60', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,4)
plt.scatter(rank_60_70_pdd_yoe,rank_60_70_pdd_slopes, alpha=0.5)
plt.scatter(rank_60_70_ctrl_yoe,rank_60_70_ctrl_slopes, color='orange', alpha=0.5)
plt.ylabel('$\Delta$ MoCA Score')
plt.xlabel('Years of Education')
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 60-70', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,5)
plt.scatter(rank_70_80_pdd_yoe,rank_70_80_pdd_slopes, alpha=0.5)
plt.scatter(rank_70_80_ctrl_yoe,rank_70_80_ctrl_slopes, color='orange', alpha=0.5)
plt.xlabel('Years of Education')
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 70-80', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,6)
plt.scatter(rank_80_90_pdd_yoe,rank_80_90_pdd_slopes, alpha=0.5)
plt.scatter(rank_80_90_ctrl_yoe,rank_80_90_ctrl_slopes, color='orange', alpha=0.5)
plt.xlabel('Years of Education')
plt.ylim(-4.5,4.5)
plt.xlim(4.5,25.5)
plt.title('Ages 80-90', fontsize=8, loc='right', pad =0)

plt.savefig('Slopes vs Years of Education by age bracket_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------First MoCA Score vs Last MoCA Score

#Initialize Figure
fig, ax = plt.subplots (2,3)
plt.suptitle('First vs Last MoCA Score by Onset age group\n'+sname, fontsize=15)

fig.set_figheight(7)
fig.set_figwidth(10)

#Iterate through Ctrl subjects 
print('_init_Controls')

for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
    
    #---Extract age at first MoCA
    ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    ctrl_dates = eval(ctrl_dates)
    
    #Extract birth date 
    birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
    #Age at test
    x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
    
    #--Subject MoCA Scores
    #Redefine as list of values (was string)
    y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
    if 'n' in y:
        y= y.replace('nan','10101') #Barcoding to remove date in case of nan
    y = np.array(eval(y))
    
    #--Remove date if nan in score
    if 10101 in y:
        print('Nan in data')
        x=x[y!=10101]
        y=y[y!=10101]
        
        
    #---Plot by Age group
    
    if x[0]<=40:
        plt.subplot(2,3,1)
        #plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.5, s =15)
        plt.title('Ages 30-40', fontsize=8, loc='right', pad =0)
        plt.ylabel('First MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
        
    elif x[0]<=50:
        plt.subplot(2,3,2)
        #plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.7, s =15)
        plt.title('Ages 40-50', fontsize=8, loc='right', pad =0)
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif x[0]<=60:
        plt.subplot(2,3,3)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.7, s =15)
        plt.title('Ages 50-60', fontsize=8, loc='right', pad =0)
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif x[0]<=70:
        plt.subplot(2,3,4)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.7, s =15)
        plt.title('Ages 60-70', fontsize=8, loc='right', pad =0)
        plt.ylabel('First MoCA Score')
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif x[0]<=80:
        plt.subplot(2,3,5)
        #plt.plot([-33, 33], [-33, 33], ls="--", alpha =0.3, c ='k')
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.7, s =15)
        plt.title('Ages 70-80', fontsize=8, loc='right', pad =0)
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    else:
        plt.subplot(2,3,6)
        #plt.plot([-33, 33], [-33, 33], ls="--", c ='k')
        plt.scatter(y[-1],y[0], c='Orange', alpha = 0.7, s =15)
        plt.title('Ages 80-90', fontsize=8, loc='right', pad =0)
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        

#Iterate through PDD subjects 
print('_init_Parkinsons')

for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
    
    #---Extract Onset age 
    onset_age = int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
    
    #--Subject MoCA Scores
    #Redefine as list of values (was string)
    y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
    if 'n' in y:
        y= y.replace('nan','10101') #Barcoding to remove date in case of nan
    y = np.array(eval(y))
    
    #--Remove date if nan in score
    if 10101 in y:
        #print('Nan in data')
        y=y[y!=10101]
        
    #---Plot by Age group
    
    if onset_age<=40:
        plt.subplot(2,3,1)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 30-40', fontsize=8, loc='right', pad =0)
        plt.ylabel('First MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
        
    elif onset_age<=50:
        plt.subplot(2,3,2)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 40-50', fontsize=8, loc='right', pad =0)
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif onset_age<=60:
        plt.subplot(2,3,3)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 50-60', fontsize=8, loc='right', pad =0)
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif onset_age<=70:
        plt.subplot(2,3,4)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='0.3', alpha =0.3)
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 60-70', fontsize=8, loc='right', pad =0)
        plt.ylabel('First MoCA Score')
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    elif onset_age<=80:
        plt.subplot(2,3,5)
        plt.plot([-33, 33], [-33, 33], ls="--", alpha =0.3, c ='k')
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 70-80', fontsize=8, loc='right', pad =0)
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
    else:
        plt.subplot(2,3,6)
        plt.plot([-33, 33], [-33, 33], ls="--", c ='k')
        plt.scatter(y[-1],y[0], c='Steelblue', alpha = 0.5, s =15)
        plt.title('Ages 80-90', fontsize=8, loc='right', pad =0)
        plt.xlabel('Last MoCA Score')
        plt.xlim(0,33)
        plt.ylim(0,33)
        
plt.subplot(2,3,1)
legends=[Line2D([0],[0], color = 'white',label='Parkinsons', marker='o', markerfacecolor='Steelblue'),
         Line2D([0],[0], color = 'white',label='Controls', marker='o', markerfacecolor='Orange')]
plt.legend(handles=legends)

plt.savefig('First vs Last MoCA Score by Onset age group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------MoCA Slope vs Age

if 'Control-Parkinsons' in stype:

    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    
    #For PDD 
    eo_subs=[]
    eo_slopes=[]
    eo_onsetAge=[]
    lo_subs=[]
    lo_slopes=[]
    lo_onsetAge=[]
    
    #For Ctrl
    eo_matched_subs=[]
    eo_matched_slopes=[]
    eo_matched_age=[]
    lo_matched_subs=[]
    lo_matched_slopes=[]
    lo_matched_age=[]
    
    #Initialize Figure
    fig, ax = plt.subplots(2,1)
    plt.suptitle('Onset age vs MoCA Slope'+sname, fontsize=16)
    fig.set_figheight(8)
    fig.set_figwidth(12)
    # ax[0].axvline(50, c='k', alpha=0.5)
    # ax[1].axvline(50, c='k', alpha=0.5)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Extract onset age
            #onset_age= int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
            
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #Age at test
            #Onset date minus test date in years 
            #x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #Age of first MoCA
            onset_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
        
            #------Age vs MoCA score
            plot = ax[0].scatter(onset_age ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='steelblue')
            
            # #------Separate lave-early onset subs
            # if onset_age<50:
            #     eo_subs.append(i)
            #     eo_slopes.append(model.coef_[0])
            #     eo_onsetAge.append(onset_age)
            
            # elif onset_age>=50:
            #     lo_subs.append(i)
            #     lo_slopes.append(model.coef_[0])
            #     lo_onsetAge.append(onset_age)
                
                
                
    #Iterate through control subjects
    print('_init_Controls')
    
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[1].scatter(matched_age,model.coef_[0],alpha = 0.5, c='green', marker ='o', s=12) 
            
            # #------Separate lave-early matched subs
            # if matched_age<50:
            #     eo_matched_subs.append(i)
            #     eo_matched_slopes.append(model.coef_[0])
            #     eo_matched_age.append(onset_age)
            
            # elif matched_age>=50:
            #     lo_matched_subs.append(i)
            #     lo_matched_slopes.append(model.coef_[0])
            #     lo_matched_age.append(onset_age)
                
                
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set( ylabel='$\Delta$ MoCA Score')
    ax[1].set(xlabel='Age at First MoCA', ylabel='$\Delta$ MoCA Score')
    ax[0].set_ylim([-5.5,4.2])
    ax[1].set_ylim([-5.5,4.2])
    ax[0].set_xlim([24,85])
    ax[1].set_xlim([24,85])
    ax[0].hlines(0,xmin=24, xmax=85, alpha = 0.7, color = 'k')
    ax[1].hlines(0,xmin=24, xmax=85, alpha = 0.7, color = 'k')
    # ax[1].hlines(np.mean(eo_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='green')
    # ax[1].hlines(np.mean(lo_matched_slopes),xmin=50, xmax=85, alpha = 0.7, color ='green', label='Mean')
    # ax[0].legend()
    # ax[0].text(29, -4, 'Early Onset')
    # ax[0].text(51, -4, 'Late Onset')
    # ax[1].legend()
    
    plt.tight_layout()
    plt.savefig('Age vs MoCA Slope_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    
#____
elif 'Control-Prodromal-Parkinsons' in stype:
    
    plotted_subs_pdd=[]
    plotted_subs_prod=[]
    plotted_subs_ctrl=[]
    
    #For PDD 
    eo_subs=[]
    eo_slopes=[]
    eo_onsetAge=[]
    lo_subs=[]
    lo_slopes=[]
    lo_onsetAge=[]
    
    #For prod
    eo_p_matched_subs=[]
    eo_p_matched_slopes=[]
    eo_p_matched_age=[]
    lo_p_matched_subs=[]
    lo_p_matched_slopes=[]
    lo_p_matched_age=[]
    
    #For Ctrl
    eo_matched_subs=[]
    eo_matched_slopes=[]
    eo_matched_age=[]
    lo_matched_subs=[]
    lo_matched_slopes=[]
    lo_matched_age=[]
    
    #Initialize Figure
    fig, ax = plt.subplots(3,1)
    plt.suptitle('Onset age vs MoCA Slope'+sname, fontsize=16)
    fig.set_figheight(9)
    fig.set_figwidth(12)
    ax[0].axvline(50, c='k', alpha=0.5)
    ax[1].axvline(50, c='k', alpha=0.5)
    ax[2].axvline(50, c='k', alpha=0.5)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Extract onset age
            onset_age= int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
            
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
        
            #------Age vs MoCA score
            plot = ax[0].scatter(onset_age ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='steelblue')
            
            #------Separate lave-early onset subs
            if onset_age<50:
                eo_subs.append(i)
                eo_slopes.append(model.coef_[0])
                eo_onsetAge.append(onset_age)
            
            elif onset_age>=50:
                lo_subs.append(i)
                lo_slopes.append(model.coef_[0])
                lo_onsetAge.append(onset_age)
                
                
    
    #Iterate through prodromal subjects
    print('_init_Prodromals')
    
    for j,i in enumerate(list(prod_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        prod_dates = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        prod_dates = eval(prod_dates)
        
        if len(prod_dates)>1:
            
            plotted_subs_prod.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in prod_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[1].scatter(matched_age,model.coef_[0],alpha = 0.5, c='orange', marker ='o', s=12) 
            
            #------Separate lave-early matched subs
            if matched_age<50:
                eo_p_matched_subs.append(i)
                eo_p_matched_slopes.append(model.coef_[0])
                eo_p_matched_age.append(matched_age)
            
            elif matched_age>=50:
                lo_p_matched_subs.append(i)
                lo_p_matched_slopes.append(model.coef_[0])
                lo_p_matched_age.append(matched_age)
                
    #Iterate through control subjects
    print('_init_Controls')
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[2].scatter(matched_age,model.coef_[0],alpha = 0.5, c='green', marker ='o', s=12) 
            
            #------Separate lave-early matched subs
            if matched_age<50:
                eo_matched_subs.append(i)
                eo_matched_slopes.append(model.coef_[0])
                eo_matched_age.append(matched_age)
            
            elif matched_age>=50:
                lo_matched_subs.append(i)
                lo_matched_slopes.append(model.coef_[0])
                lo_matched_age.append(matched_age)
                
                
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Prodromals          n='+str(len(plotted_subs_prod)), pad = 0, fontsize= 10, loc = 'right')
    ax[2].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    
    ax[0].set(xlabel='Onset Age', ylabel='$\Delta$ MoCA Score')
    ax[1].set(xlabel='First MoCA Matched Age', ylabel='$\Delta$ MoCA Score')
    ax[2].set(xlabel='First MoCA Matched Age', ylabel='$\Delta$ MoCA Score')
    
    ax[0].set_ylim([-6.5,5.2])
    ax[1].set_ylim([-6.5,5.2])
    ax[2].set_ylim([-6.5,5.2])
    
    ax[0].set_xlim([24,86])
    ax[1].set_xlim([24,86])
    ax[2].set_xlim([24,86])
    
    ax[0].hlines(np.mean(eo_slopes),xmin=24, xmax=50, alpha = 0.7)
    ax[0].hlines(np.mean(lo_slopes),xmin=50, xmax=86, alpha = 0.7, label='Mean')
    ax[1].hlines(np.mean(eo_p_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='orange')
    ax[1].hlines(np.mean(lo_p_matched_slopes),xmin=50, xmax=86, alpha = 0.7, color ='orange', label='Mean')
    ax[2].hlines(np.mean(eo_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='green')
    ax[2].hlines(np.mean(lo_matched_slopes),xmin=50, xmax=86, alpha = 0.7, color ='green', label='Mean')
    
    
    ax[0].text(29, -4, 'Early Onset')
    ax[0].text(51, -4, 'Late Onset')
    
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    
    plt.savefig('Onset age vs MoCA Slope_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
#%%---------------MoCA Slope vs Onset age

if 'Control-Parkinsons' in stype:

    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    
    #For PDD 
    eo_subs=[]
    eo_slopes=[]
    eo_onsetAge=[]
    lo_subs=[]
    lo_slopes=[]
    lo_onsetAge=[]
    
    #For Ctrl
    eo_matched_subs=[]
    eo_matched_slopes=[]
    eo_matched_age=[]
    lo_matched_subs=[]
    lo_matched_slopes=[]
    lo_matched_age=[]
    
    #Initialize Figure
    fig, ax = plt.subplots(2,1)
    plt.suptitle('Onset age vs MoCA Slope'+sname, fontsize=16)
    fig.set_figheight(8)
    fig.set_figwidth(12)
    ax[0].axvline(50, c='k', alpha=0.5)
    ax[1].axvline(50, c='k', alpha=0.5)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Extract onset age
            onset_age= int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
            
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
        
            #------Age vs MoCA score
            plot = ax[0].scatter(onset_age ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='steelblue')
            
            #------Separate lave-early onset subs
            if onset_age<50:
                eo_subs.append(i)
                eo_slopes.append(model.coef_[0])
                eo_onsetAge.append(onset_age)
            
            elif onset_age>=50:
                lo_subs.append(i)
                lo_slopes.append(model.coef_[0])
                lo_onsetAge.append(onset_age)
                
                
                
    #Iterate through control subjects
    print('_init_Controls')
    
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[1].scatter(matched_age,model.coef_[0],alpha = 0.5, c='green', marker ='o', s=12) 
            
            #------Separate lave-early matched subs
            if matched_age<50:
                eo_matched_subs.append(i)
                eo_matched_slopes.append(model.coef_[0])
                eo_matched_age.append(onset_age)
            
            elif matched_age>=50:
                lo_matched_subs.append(i)
                lo_matched_slopes.append(model.coef_[0])
                lo_matched_age.append(onset_age)
                
                
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(xlabel='Onset Age', ylabel='$\Delta$ MoCA Score')
    ax[1].set(xlabel='First MoCA Matched Age', ylabel='$\Delta$ MoCA Score')
    ax[0].set_ylim([-5.5,4.2])
    ax[1].set_ylim([-5.5,4.2])
    ax[0].set_xlim([24,85])
    ax[1].set_xlim([24,85])
    ax[0].hlines(np.mean(eo_slopes),xmin=24, xmax=50, alpha = 0.7)
    ax[0].hlines(np.mean(lo_slopes),xmin=50, xmax=85, alpha = 0.7, label='Mean')
    ax[1].hlines(np.mean(eo_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='green')
    ax[1].hlines(np.mean(lo_matched_slopes),xmin=50, xmax=85, alpha = 0.7, color ='green', label='Mean')
    ax[0].legend()
    ax[0].text(29, -4, 'Early Onset')
    ax[0].text(51, -4, 'Late Onset')
    ax[1].legend()
    
    plt.tight_layout()
    plt.savefig('Onset age vs MoCA Slope_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
    
#____
elif 'Control-Prodromal-Parkinsons' in stype:
    
    plotted_subs_pdd=[]
    plotted_subs_prod=[]
    plotted_subs_ctrl=[]
    
    #For PDD 
    eo_subs=[]
    eo_slopes=[]
    eo_onsetAge=[]
    lo_subs=[]
    lo_slopes=[]
    lo_onsetAge=[]
    
    #For prod
    eo_p_matched_subs=[]
    eo_p_matched_slopes=[]
    eo_p_matched_age=[]
    lo_p_matched_subs=[]
    lo_p_matched_slopes=[]
    lo_p_matched_age=[]
    
    #For Ctrl
    eo_matched_subs=[]
    eo_matched_slopes=[]
    eo_matched_age=[]
    lo_matched_subs=[]
    lo_matched_slopes=[]
    lo_matched_age=[]
    
    #Initialize Figure
    fig, ax = plt.subplots(3,1)
    plt.suptitle('Onset age vs MoCA Slope'+sname, fontsize=16)
    fig.set_figheight(9)
    fig.set_figwidth(12)
    ax[0].axvline(50, c='k', alpha=0.5)
    ax[1].axvline(50, c='k', alpha=0.5)
    ax[2].axvline(50, c='k', alpha=0.5)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Extract onset age
            onset_age= int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
            
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
        
            #------Age vs MoCA score
            plot = ax[0].scatter(onset_age ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='steelblue')
            
            #------Separate lave-early onset subs
            if onset_age<50:
                eo_subs.append(i)
                eo_slopes.append(model.coef_[0])
                eo_onsetAge.append(onset_age)
            
            elif onset_age>=50:
                lo_subs.append(i)
                lo_slopes.append(model.coef_[0])
                lo_onsetAge.append(onset_age)
                
                
    
    #Iterate through prodromal subjects
    print('_init_Prodromals')
    
    for j,i in enumerate(list(prod_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        prod_dates = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        prod_dates = eval(prod_dates)
        
        if len(prod_dates)>1:
            
            plotted_subs_prod.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in prod_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = prod_sorted_ct_df_file[(prod_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[1].scatter(matched_age,model.coef_[0],alpha = 0.5, c='orange', marker ='o', s=12) 
            
            #------Separate lave-early matched subs
            if matched_age<50:
                eo_p_matched_subs.append(i)
                eo_p_matched_slopes.append(model.coef_[0])
                eo_p_matched_age.append(matched_age)
            
            elif matched_age>=50:
                lo_p_matched_subs.append(i)
                lo_p_matched_slopes.append(model.coef_[0])
                lo_p_matched_age.append(matched_age)
                
    #Iterate through control subjects
    print('_init_Controls')
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #Age of first MoCA
            matched_age=int(x[0])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
    
            #------Age vs MoCA Score Plot
            plot = ax[2].scatter(matched_age,model.coef_[0],alpha = 0.5, c='green', marker ='o', s=12) 
            
            #------Separate lave-early matched subs
            if matched_age<50:
                eo_matched_subs.append(i)
                eo_matched_slopes.append(model.coef_[0])
                eo_matched_age.append(matched_age)
            
            elif matched_age>=50:
                lo_matched_subs.append(i)
                lo_matched_slopes.append(model.coef_[0])
                lo_matched_age.append(matched_age)
                
                
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Prodromals          n='+str(len(plotted_subs_prod)), pad = 0, fontsize= 10, loc = 'right')
    ax[2].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    
    ax[0].set(xlabel='Onset Age', ylabel='$\Delta$ MoCA Score')
    ax[1].set(xlabel='First MoCA Matched Age', ylabel='$\Delta$ MoCA Score')
    ax[2].set(xlabel='First MoCA Matched Age', ylabel='$\Delta$ MoCA Score')
    
    ax[0].set_ylim([-6.5,5.2])
    ax[1].set_ylim([-6.5,5.2])
    ax[2].set_ylim([-6.5,5.2])
    
    ax[0].set_xlim([24,86])
    ax[1].set_xlim([24,86])
    ax[2].set_xlim([24,86])
    
    ax[0].hlines(np.mean(eo_slopes),xmin=24, xmax=50, alpha = 0.7)
    ax[0].hlines(np.mean(lo_slopes),xmin=50, xmax=86, alpha = 0.7, label='Mean')
    ax[1].hlines(np.mean(eo_p_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='orange')
    ax[1].hlines(np.mean(lo_p_matched_slopes),xmin=50, xmax=86, alpha = 0.7, color ='orange', label='Mean')
    ax[2].hlines(np.mean(eo_matched_slopes),xmin=24, xmax=50, alpha = 0.7, color ='green')
    ax[2].hlines(np.mean(lo_matched_slopes),xmin=50, xmax=86, alpha = 0.7, color ='green', label='Mean')
    
    
    ax[0].text(29, -4, 'Early Onset')
    ax[0].text(51, -4, 'Late Onset')
    
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    
    plt.savefig('Onset age vs MoCA Slope_'+(os.path.basename(sv_path)[:-4])+'_'+sname)



#%%---------------MoCA Slope vs Chronological Age PDD

#Initialize Figure
fig, ax = plt.subplots()
plt.suptitle('MoCA Slope vs First MoCA Age by Onset Group'+sname, fontsize=16)
fig.set_figheight(7)
fig.set_figwidth(10)

#Iterate through PDD subjects 
print('_init_Parkinsons')


for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
    
    #--Subject MoCA Dates
    #Redefine as list of values (was string)
    pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    pdd_dates = eval(pdd_dates)
    
    if len(pdd_dates)>1:
        
        plotted_subs_pdd.append(i)
        
        #--Subjects Age at evaluation 
        #Extract birth date 
        birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
        
        #Extract onset age
        onset_age= int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
        
        #Age at test
        #Onset date minus test date in years 
        x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
        
        #--Subject MoCA Scores
        #Redefine as list of values (was string)
        y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
        if 'n' in y:
            y= y.replace('nan','10101') #Barcoding to remove date in case of nan
        y = np.array(eval(y))
        
        #--Remove date if nan in score
        if 10101 in y:
            #print('Nan in data')
            x=x[y!=10101]
            y=y[y!=10101]
          
        #-----Linear regression 
        x_lr= x.reshape((-1,1)) #Reshape x
        model=LinearRegression().fit(x_lr,y)
    
        #------Separate late-early onset subs
        if onset_age<50:
            plt.scatter(x[0] ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='blue')


        elif onset_age>=50:
            plt.scatter(x[0] ,model.coef_[0],alpha = 0.5, marker ='o', s=12, c='red')

plt.xlabel('Age at First MoCA Test')
plt.ylabel('$\Delta$MoCA')
plt.scatter(0,0,alpha = 0.5, marker ='o', s=10, c='blue', label ='Early Onset')    
plt.scatter(0,0,alpha = 0.5, marker ='o', s=10, c='red', label ='Late Onset')       
plt.ylim(-4.5,4.5)
plt.xlim(30,86)
plt.axvline(50, color='k', alpha=0.7)
plt.legend()

plt.savefig('MoCA Slope vs First MoCA Age by Onset Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------MoCA Score vs years since first MoCA

#Arrays of all MoCA Scores by onset group
gen_early_score=[]
gen_late_score=[]
#Arrays of all MoCA Years Since first MoCA by onset Group
gen_early_time=[]
gen_late_time=[]

ec=0 #Early Patients Counter
lc=0 #Late Patients Counter

#Initialize Figure
fig, ax = plt.subplots(1,2)
fig.set_figheight(10)
fig.set_figwidth(17)
plt.suptitle('MoCA Score vs Years since first MoCA by onset group\n'+sname, fontsize=16)

#-------------------MoCA Zero-Centered Graph

#Iterate through subjects 
for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
    #print(str(i))
    
    #--Subject MoCA Dates
    #Redefine as list of values (was string)
    pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    pdd_dates = eval(pdd_dates)
    
    if len(pdd_dates)>1:
        
        #--Subjects Age at evaluation 
        #Extract birth date 
        birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
        
        #Extract Onset Age
        onset_age = int(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Onset_Age'].values[0])
        
        #Age at test
        x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
        
        #Center time at Moca 0
        x = x-x[0]
        
        
    
        #--Subject MoCA Scores
        #Redefine as list of values (was string)
        y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
        if 'n' in y:
            y= y.replace('nan','10101') #Barcoding to remove data in case of nan
        y = np.array(eval(y))
        
        #--Remove date if nan in score
        if 10101 in y:
            #print('Nan in data')
            x=x[y!=10101]
            y=y[y!=10101]
            
            
        
        #-----Linear regression 
        x_lr= x.reshape((-1,1)) #Reshape x
        model=LinearRegression().fit(x_lr,y)
        pred= model.predict(x_lr) #create predicted values for slope plot 
        

        #------X (years since last MoCA) and Y (MoCA Score) Ready to plot
        
        #Separate early-Late onset plot
        if onset_age <50:
            #print('early')
            if not np.any(x<0): #Data Check bc some subjs have dates in wrong order in og database 
                plot = ax[0].plot(x,y,alpha = 0.05, c ='k')
                plot= ax[0].plot(x,pred, alpha = 0.1, c = 'blue')
                gen_early_score.append(y)
                gen_early_time.append(x)
                ec+=1
        
        else:
            #print('late')
            if not np.any(x<0): #Data Check bc some subjs have dates in wrong order in og database 
                plot = ax[1].plot(x,y,alpha = 0.05, c ='k')
                plot= ax[1].plot(x,pred, alpha = 0.1, c = 'red')
                gen_late_score.append(y)
                gen_late_time.append(x)
                lc+=1
            
            
gen_early_score = np.concatenate(gen_early_score)
gen_early_time = np.concatenate(gen_early_time)
gen_late_score = np.concatenate(gen_late_score)
gen_late_time = np.concatenate(gen_late_time)

#All Early Patients Model
tmp_x_lr = gen_early_time.reshape((-1,1))
gen_early_model = LinearRegression().fit(tmp_x_lr,gen_early_score)

#All Late Patients Model 
tmp_x_lr = gen_late_time.reshape((-1,1))
gen_late_model = LinearRegression().fit(tmp_x_lr,gen_late_score)

#General models Plot 
tmp_x_lr= np.linspace(min(gen_early_time), max(gen_early_time),10)
gen_early_pred= gen_early_model.predict(tmp_x_lr.reshape((-1,1)))
ax[0].plot(tmp_x_lr, gen_early_pred, linewidth=3, c = 'navy')

tmp_x_lr= np.linspace(min(gen_late_time), max(gen_late_time),10)
gen_late_pred= gen_late_model.predict(tmp_x_lr.reshape((-1,1)))
ax[1].plot(tmp_x_lr, gen_late_pred, linewidth=3, c = 'darkred')

legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'),
         Line2D([0],[0], color = 'blue',label='Early Onset LR'),
         Line2D([0],[0], color = 'navy',label='Whole Data LR', linewidth=3)]
ax[0].legend(handles=legends)

legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'), 
         Line2D([0],[0], color = 'red',label='Late Onset LR'),
         Line2D([0],[0], color = 'darkred',label='Whole Data LR', linewidth=3)]
ax[1].legend(handles=legends)

ax[0].set_title('Early Onset n='+str(ec), pad = 0, fontsize= 10, loc = 'right')
ax[1].set_title('Late Onset n='+str(lc), pad = 0, fontsize= 10, loc = 'right')
ax[0].set(ylabel='MoCA Score',xlabel='Years since first MoCA')
ax[1].set(xlabel='Years since first MoCA')
ax[0].set_ylim([0,31])
ax[1].set_ylim([0,31])
ax[0].set_xlim([-0.5,14])
ax[1].set_xlim([-0.5,14])


plt.savefig('MoCA Score vs Years since first MoCA by onset group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------MoCA Score vs age (PDD vs CTRL) {SciPy Linregress}

#List of subjects with all data
pdd_wholedata_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
ctrl_wholedata_subs = [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]

#Filter dataframe and extract data only from whole data subjects
pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]
ctrl_filtered_df_file = ctrl_ct_df_file[(ctrl_ct_df_file['Subject_ID'].isin(ctrl_wholedata_subs))]

#Convert Birthdate column to datetime
ctrl_filtered_df_file['Birthdate'] = pd.to_datetime(ctrl_filtered_df_file['Birthdate'])

#Sort subjects by age 
pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')
ctrl_sorted_ct_df_file = ctrl_filtered_df_file.sort_values('Birthdate', ascending=False)


#Convert Birthdate column to string
ctrl_sorted_ct_df_file['Birthdate'] = ctrl_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')

#Extract sorted ages
pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]

#Slopes by age rank
rank_30_40_pdd_slopes=[]
rank_30_40_ctrl_slopes=[]

rank_40_50_pdd_slopes=[]
rank_40_50_ctrl_slopes=[]

rank_50_60_pdd_slopes=[]
rank_50_60_ctrl_slopes=[]

rank_60_70_pdd_slopes=[]
rank_60_70_ctrl_slopes=[]

rank_70_80_pdd_slopes=[]
rank_70_80_ctrl_slopes=[]

rank_80_90_pdd_slopes=[]
rank_80_90_ctrl_slopes=[]

#Years of education by age rank
rank_30_40_pdd_yoe=[]
rank_30_40_ctrl_yoe=[]

rank_40_50_pdd_yoe=[]
rank_40_50_ctrl_yoe=[]

rank_50_60_pdd_yoe=[]
rank_50_60_ctrl_yoe=[]

rank_60_70_pdd_yoe=[]
rank_60_70_ctrl_yoe=[]

rank_70_80_pdd_yoe=[]
rank_70_80_ctrl_yoe=[]

rank_80_90_pdd_yoe=[]
rank_80_90_ctrl_yoe=[]

#Intercepts
pdd_intercepts=[]
ctrl_intercepts=[]

rank_30_40_pdd_intercept=[]
rank_30_40_ctrl_intercept=[]

rank_40_50_pdd_intercept=[]
rank_40_50_ctrl_intercept=[]

rank_50_60_pdd_intercept=[]
rank_50_60_ctrl_intercept=[]

rank_60_70_pdd_intercept=[]
rank_60_70_ctrl_intercept=[]

rank_70_80_pdd_intercept=[]
rank_70_80_ctrl_intercept=[]

rank_80_90_pdd_intercept=[]
rank_80_90_ctrl_intercept=[]

#-------------------MoCA vs Age

#Initialize Figure
fig, ax = plt.subplots(2,1)
plt.suptitle('Evolution Trayectories MoCA Score vs Age_'+sname+' {SciPy}', fontsize=16)

#Iterate through PDD subjects 
print('_init_Parkinsons')

#Extract number of ages (colorbar length)
N=len(pdd_ages)
#Assign Colormap
cmap = plt.get_cmap('seismic',N)
#Slopes
pdd_slopes=[]
pdd_rsq=[]
#Plotted Subjects List
plotted_subs_pdd=[]
plotted_subs_ctrl=[]

for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
    #print(str(i))
    
    #--Subject MoCA Dates
    #Redefine as list of values (was string)
    pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    pdd_dates = eval(pdd_dates)
    
    if len(pdd_dates)>1:
        
        plotted_subs_pdd.append(i)
        
        #--Subjects Age at evaluation 
        #Extract birth date 
        birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
        #Age at test 
        x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
        
        #--Subject MoCA Scores
        #Redefine as list of values (was string)
        y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
        if 'n' in y:
            y= y.replace('nan','10101') #Barcoding to remove date in case of nan
        y = np.array(eval(y))
        
        #--Remove date if nan in score
        if 10101 in y:
            #print('Nan in data')
            x=x[y!=10101]
            y=y[y!=10101]
          
        #------Age vs MoCA score
        plot = ax[0].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2)
        
        #-----Linear regression 
        
        slope, intercept =sp.linregress(x,y)[:2]
        pdd_slopes.append(slope)
        pdd_intercepts.append(intercept)
        
    
        #Rank slope append
        if x[0]<=40:
            rank_30_40_pdd_slopes.append(slope)
            rank_30_40_pdd_intercept.append(intercept)
        elif x[0]<=50:
            rank_40_50_pdd_slopes.append(slope)
            rank_40_50_pdd_intercept.append(intercept)
        elif x[0]<=60:
            rank_50_60_pdd_slopes.append(slope)
            rank_50_60_pdd_intercept.append(intercept)
        elif x[0]<=70:
            rank_60_70_pdd_slopes.append(slope)
            rank_60_70_pdd_intercept.append(intercept)
        elif x[0]<=80:
            rank_70_80_pdd_slopes.append(slope)
            rank_70_80_pdd_intercept.append(intercept)
        else:
            rank_80_90_pdd_slopes.append(slope)
            rank_80_90_pdd_intercept.append(intercept)
            
            

#Normalize color data for colorbar 
norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax[0])


#Iterate through control subjects
print('_init_Controls')

#Ccolorbar length
N=len(ctrl_wholedata_subs)
#Assign Colormap
cmap = plt.get_cmap('gnuplot_r',N)
#Slopes
ctrl_slopes=[]
ctrl_rsq=[]

for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
    #print(str(i))
    
    #--Subject MoCA Dates
    #Redefine as list of values (was string)
    ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
    ctrl_dates = eval(ctrl_dates)
    
    if len(ctrl_dates)>1:
        
        plotted_subs_ctrl.append(i)
        
        #--Subjects Age at evaluation 
        #Extract birth date 
        birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
        #Age at test
        #Onset date minus test date in years 
        x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
        
        #--Subject MoCA Scores
        #Redefine as list of values (was string)
        y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
        if 'n' in y:
            y= y.replace('nan','10101') #Barcoding to remove date in case of nan
        y = np.array(eval(y))
        
        #--Remove date if nan in score
        if 10101 in y:
            #print('Nan in data')
            x=x[y!=10101]
            y=y[y!=10101]
          
        #------Age vs MoCA Score Plot
        plot = ax[1].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2) 

        #-----Linear regression 
        
        slope, intercept =sp.linregress(x,y)[:2]
        ctrl_slopes.append(slope)
        ctrl_intercepts.append(intercept)
        
    
        #Rank slope append
        if x[0]<=40:
            rank_30_40_ctrl_slopes.append(slope)
            rank_30_40_ctrl_intercept.append(intercept)
        elif x[0]<=50:
            rank_40_50_ctrl_slopes.append(slope)
            rank_40_50_ctrl_intercept.append(intercept)
        elif x[0]<=60:
            rank_50_60_ctrl_slopes.append(slope)
            rank_50_60_ctrl_intercept.append(intercept)
        elif x[0]<=70:
            rank_60_70_ctrl_slopes.append(slope)
            rank_60_70_ctrl_intercept.append(intercept)
        elif x[0]<=80:
            rank_70_80_ctrl_slopes.append(slope)
            rank_70_80_ctrl_intercept.append(intercept)
        else:
            rank_80_90_ctrl_slopes.append(slope)
            rank_80_90_ctrl_intercept.append(intercept)
          
        
    
ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
ax[0].set(ylabel='MoCA Score')
ax[1].set(xlabel='Age', ylabel='MoCA Score')
ax[0].set_ylim([0,31])
ax[1].set_ylim([0,31])
ax[0].set_xlim([28,93])
ax[1].set_xlim([28,93])

#Normalize color data for colorbar 
norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax[1])
plt.show()        
#%%---------------MoCA Slopes Plot {SciPy}

plt.figure(figsize=(7,6))
plt.title('Slopes Distribution by group_'+sname)
plt.xlabel('Evolution Trajectory Slope')
sns.histplot(pdd_slopes, bins=50, kde=True, element='step', label='Parkinsons')
plt.axvline(np.median(pdd_slopes), c = 'blue', label ='Median Parkinsons')
plt.axvline(np.median(ctrl_slopes), c = 'orange', label = 'Median Controls')
sns.histplot(ctrl_slopes, bins=50, kde=True, element='step', label='Controls')
plt.legend()
       
#%%---------------MoCA Intercepts Plot {SciPy}

plt.figure(figsize=(7,6))
plt.title('Intercepts Distribution by group_'+sname)
plt.xlabel('Evolution Trajectory Intercept')
sns.histplot(pdd_intercepts, bins=50, kde=True, element='step', label='Parkinsons')
plt.axvline(np.median(pdd_intercepts), c = 'blue', label ='Median Parkinsons')
plt.axvline(np.median(ctrl_intercepts), c = 'orange', label = 'Median Controls')
sns.histplot(ctrl_intercepts, bins=50, kde=True, element='step', label='Controls')
plt.legend() 

#%%---------------Correlations slope vs intercept by age bracket 

fig, ax = plt.subplots (2,3)
plt.suptitle('Slopes vs Intercept by age bracket\n'+sname, fontsize=15)
plt.subplot(2,3,1)
plt.scatter(rank_30_40_pdd_intercept,rank_30_40_pdd_slopes, alpha =0.5)
plt.scatter(rank_30_40_ctrl_intercept,rank_30_40_ctrl_slopes, color='orange', alpha =0.5)
plt.ylabel('$\Delta$ MoCA Score')
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 30-40', fontsize=8, loc='right', pad =0)
legends=[Line2D([0],[0], color = 'white',label='Parkinsons', marker='o', markerfacecolor='Steelblue'),
         Line2D([0],[0], color = 'white',label='Controls', marker='o', markerfacecolor='Orange')]
plt.legend(handles=legends)

plt.subplot(2,3,2)
plt.scatter(rank_40_50_pdd_intercept,rank_40_50_pdd_slopes, alpha=0.5)
plt.scatter(rank_40_50_ctrl_intercept,rank_40_50_ctrl_slopes, color='orange', alpha=0.5)
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 40-50', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,3)
plt.scatter(rank_50_60_pdd_intercept,rank_50_60_pdd_slopes, alpha=0.5)
plt.scatter(rank_50_60_ctrl_intercept,rank_50_60_ctrl_slopes, color='orange', alpha=0.5)
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 50-60', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,4)
plt.scatter(rank_60_70_pdd_intercept,rank_60_70_pdd_slopes, alpha=0.5)
plt.scatter(rank_60_70_ctrl_intercept,rank_60_70_ctrl_slopes, color='orange', alpha=0.5)
plt.ylabel('$\Delta$ MoCA Score')
plt.xlabel('Intercept')
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 60-70', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,5)
plt.scatter(rank_70_80_pdd_intercept,rank_70_80_pdd_slopes, alpha=0.5)
plt.scatter(rank_70_80_ctrl_intercept,rank_70_80_ctrl_slopes, color='orange', alpha=0.5)
plt.xlabel('Intercept')
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 70-80', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,6)
plt.scatter(rank_80_90_pdd_intercept,rank_80_90_pdd_slopes, alpha=0.5)
plt.scatter(rank_80_90_ctrl_intercept,rank_80_90_ctrl_slopes, color='orange', alpha=0.5)
plt.xlabel('Intercept')
plt.ylim(-4.5,4.5)
plt.xlim(-200,400)
plt.title('Ages 80-90', fontsize=8, loc='right', pad =0)

#%%---------------Histograms intercept by age bracket 

fig, ax = plt.subplots (2,3)
plt.suptitle('Intercept histograms by age bracket\n'+sname, fontsize=15)
plt.subplot(2,3,1)
sns.histplot(rank_30_40_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_30_40_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 30-40', fontsize=8, loc='right', pad =0)
legends=[Line2D([0],[0], color = 'white',label='Parkinsons', marker='o', markerfacecolor='Steelblue'),
         Line2D([0],[0], color = 'white',label='Controls', marker='o', markerfacecolor='Orange')]
plt.legend(handles=legends)

plt.subplot(2,3,2)
sns.histplot(rank_40_50_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_40_50_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 40-50', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,3)
sns.histplot(rank_50_60_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_50_60_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 50-60', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,4)
sns.histplot(rank_60_70_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_60_70_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.xlabel('Intercept')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 60-70', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,5)
sns.histplot(rank_70_80_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_70_80_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.xlabel('Intercept')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 70-80', fontsize=8, loc='right', pad =0)

plt.subplot(2,3,6)
sns.histplot(rank_80_90_pdd_intercept, bins=50, kde=True, element='step', label='Parkinsons')
sns.histplot(rank_80_90_ctrl_intercept, bins=50, kde=True, element='step', label='Controls')
plt.xlabel('Intercept')
plt.ylim(0,30)
plt.xlim(-200,400)
plt.title('Ages 80-90', fontsize=8, loc='right', pad =0)


#%%////////////////////////////////LOG PLOTS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%

if 'Control-Parkinsons' in stype:
    print('Plotting MoCA Score vs Log Age - PDD vs Ctrl')

    #List of subjects with all data
    pdd_wholedata_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
    ctrl_wholedata_subs = [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]
    
    #Filter dataframe and extract data only from whole data subjects
    pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]
    ctrl_filtered_df_file = ctrl_ct_df_file[(ctrl_ct_df_file['Subject_ID'].isin(ctrl_wholedata_subs))]
    
    #Convert Birthdate column to datetime
    ctrl_filtered_df_file['Birthdate'] = pd.to_datetime(ctrl_filtered_df_file['Birthdate'])
    
    #Sort subjects by age 
    pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')
    ctrl_sorted_ct_df_file = ctrl_filtered_df_file.sort_values('Birthdate', ascending=False)
    
    
    #Convert Birthdate column to string
    ctrl_sorted_ct_df_file['Birthdate'] = ctrl_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')
    
    #Extract sorted ages
    pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]
    
    #Slopes by age rank
    rank_30_40_pdd_slopes=[]
    rank_30_40_ctrl_slopes=[]
    
    rank_40_50_pdd_slopes=[]
    rank_40_50_ctrl_slopes=[]
    
    rank_50_60_pdd_slopes=[]
    rank_50_60_ctrl_slopes=[]
    
    rank_60_70_pdd_slopes=[]
    rank_60_70_ctrl_slopes=[]
    
    rank_70_80_pdd_slopes=[]
    rank_70_80_ctrl_slopes=[]
    
    rank_80_90_pdd_slopes=[]
    rank_80_90_ctrl_slopes=[]
    
    #Years of education by age rank
    rank_30_40_pdd_yoe=[]
    rank_30_40_ctrl_yoe=[]
    
    rank_40_50_pdd_yoe=[]
    rank_40_50_ctrl_yoe=[]
    
    rank_50_60_pdd_yoe=[]
    rank_50_60_ctrl_yoe=[]
    
    rank_60_70_pdd_yoe=[]
    rank_60_70_ctrl_yoe=[]
    
    rank_70_80_pdd_yoe=[]
    rank_70_80_ctrl_yoe=[]
    
    rank_80_90_pdd_yoe=[]
    rank_80_90_ctrl_yoe=[]
    
    #-------------------MoCA vs Age
    
    #Initialize Figure
    fig, ax = plt.subplots(2,1)
    fig.set_figheight(7)
    fig.set_figwidth(14)
    plt.suptitle('Evolution Trayectories MoCA Score vs Log Age_'+sname, fontsize=16)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons')
    
    #Extract number of ages (colorbar length)
    N=len(pdd_ages)
    #Assign Colormap
    cmap = plt.get_cmap('seismic',N)
    #Slopes
    pdd_slopes=[]
    pdd_rsq=[]
    #Plotted Subjects List
    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA score
            plot = ax[0].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2)
            
            
            #-----Obtain Subjects years of education
            yoe = float(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #print(str(model.coef_ [0]))
            #if model.coef_[0]!=0:
            pdd_rsq.append(model.score(x_lr,y))
            pdd_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_pdd_slopes.append(model.coef_ [0])
                rank_30_40_pdd_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_pdd_slopes.append(model.coef_ [0])
                rank_40_50_pdd_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_pdd_slopes.append(model.coef_ [0])
                rank_50_60_pdd_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_pdd_slopes.append(model.coef_ [0])
                rank_60_70_pdd_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_pdd_slopes.append(model.coef_ [0])
                rank_70_80_pdd_yoe.append(yoe)
            else:
                rank_80_90_pdd_slopes.append(model.coef_ [0])
                rank_80_90_pdd_yoe.append(yoe)
                
                
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[0], label = 'Onset Age')
    
    
    #Iterate through control subjects
    print('_init_Controls')
    
    #Ccolorbar length
    N=len(ctrl_wholedata_subs)
    #Assign Colormap
    cmap = plt.get_cmap('gnuplot_r',N)
    #Slopes
    ctrl_slopes=[]
    ctrl_rsq=[]
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject MoCA Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #--Subject MoCA Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['MoCA_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
              
            #------Age vs MoCA Score Plot
            plot = ax[1].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=2) 
            
            #-----Obtain Subjects years of education
            yoe = float(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            #-----Linear regression 
            x_lr= x.reshape((-1,1)) #Reshape x
            model=LinearRegression().fit(x_lr,y)
            #if model.coef_[0]!=0:
            ctrl_rsq.append(model.score(x_lr,y))
            ctrl_slopes.append(model.coef_[0])
        
            #Rank slope append
            if x[0]<=40:
                rank_30_40_ctrl_slopes.append(model.coef_ [0])
                rank_30_40_ctrl_yoe.append(yoe)
            elif x[0]<=50:
                rank_40_50_ctrl_slopes.append(model.coef_ [0])
                rank_40_50_ctrl_yoe.append(yoe)
            elif x[0]<=60:
                rank_50_60_ctrl_slopes.append(model.coef_ [0])
                rank_50_60_ctrl_yoe.append(yoe)
            elif x[0]<=70:
                rank_60_70_ctrl_slopes.append(model.coef_ [0])
                rank_60_70_ctrl_yoe.append(yoe)
            elif x[0]<=80:
                rank_70_80_ctrl_slopes.append(model.coef_ [0])
                rank_70_80_ctrl_yoe.append(yoe)
            else:
                rank_80_90_ctrl_slopes.append(model.coef_ [0])
                rank_80_90_ctrl_yoe.append(yoe)
              
            
        
    ax[0].set_title('Parkinsons          n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='MoCA Score')
    ax[1].set(xlabel='Age', ylabel='MoCA Score')
    ax[0].set_ylim([0,31])
    ax[1].set_ylim([0,31])
    ax[0].set_xlim([28,93])
    ax[1].set_xlim([28,93])
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[1], label ='Age at first MoCA')
    plt.show()
     
    
    plt.savefig('Evolution Trayectories MoCA Score vs Age_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%////////////////////////////////HOEHN-YAHR \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%---------------HY Score vs age trajectories

if 'Control-Parkinsons' in stype:
    print('Plotting HY Score vs Age - PDD vs Ctrl')
    
    #List of subjects with all data
    pdd_wholedata_pre_subs = [int(x) for x in pdd_ct_subs_file['Subjects With All Data'].dropna()]
    pdd_wholedata_subs=[i for i in pdd_wholedata_pre_subs if i in pd_subs_bymod_long]
    
    ctrl_wholedata_pre_subs = [int(x) for x in ctrl_ct_subs_file['Subjects With All Data'].dropna()]
    ctrl_wholedata_subs=[i for i in ctrl_wholedata_pre_subs if i in ctrl_subs_bymod_long]
    
    #Filter dataframe and extract data only from whole data subjects
    pdd_filtered_df_file = pdd_ct_df_file[(pdd_ct_df_file['Subject_ID'].isin(pdd_wholedata_subs))]
    ctrl_filtered_df_file = ctrl_ct_df_file[(ctrl_ct_df_file['Subject_ID'].isin(ctrl_wholedata_subs))]
    
    #Convert Birthdate column to datetime
    ctrl_filtered_df_file['Birthdate'] = pd.to_datetime(ctrl_filtered_df_file['Birthdate'])
    
    #Sort subjects by age 
    pdd_sorted_ct_df_file = pdd_filtered_df_file.sort_values('Onset_Age')
    ctrl_sorted_ct_df_file = ctrl_filtered_df_file.sort_values('Birthdate', ascending=False)
    
    #Convert Birthdate column to string
    ctrl_sorted_ct_df_file['Birthdate'] = ctrl_sorted_ct_df_file['Birthdate'].dt.strftime('%m/%Y')
    

    #-------------------HY vs Age
    
    #Initialize Figure
    fig, ax = plt.subplots(3,1)
    fig.set_figheight(7)
    fig.set_figwidth(14)
    plt.suptitle('Evolution Trayectories H-Y Score vs Age_'+sname, fontsize=16)
    
    #Iterate through PDD subjects 
    print('_init_Parkinsons OFF')
    
    
    #Extract sorted ages
    pdd_ages= [int(a) for a in pdd_sorted_ct_df_file['Onset_Age']]
    #Extract number of ages (colorbar length)
    N=len(pdd_ages)
    #Assign Colormap
    cmap = plt.get_cmap('seismic',N)
    #Slopes
    pdd_slopes=[]
    pdd_rsq=[]
    #Plotted Subjects List
    plotted_subs_pdd=[]
    plotted_subs_ctrl=[]
    
    for j,i in enumerate(list(pdd_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject HY Dates
        #Redefine as list of values (was string)
        pdd_dates = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['HY_Dates'].values[0]
        pdd_dates = eval(pdd_dates)
        
        if len(pdd_dates)>1:
            
            plotted_subs_pdd.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x =np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in pdd_dates])
            
            #--Subject HY Scores
            #Redefine as list of values (was string)
            y = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['HY_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #-- Subject Hy Status 
            #Redefine as list of values (was string)
            stat = pdd_sorted_ct_df_file[(pdd_sorted_ct_df_file['Subject_ID']==i)]['HY_Status'].values[0]
            stat = stat.replace('NoTrtOFF','0') #Change OFF values to 0 
            stat = stat.replace('OFF','0')
            stat = stat.replace('ON','1') #Change ON values to 1
            stat = np.array(eval(stat)) #Define Array
            stat = np.array([int(z) for z in stat]) #Set values as integer
                        
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
                stat = stat[y!=10101]
            
            #--Age-Score dataframe 
            tmp = pd.DataFrame({'x':x, 'y':y, 'status':stat})
            tmp.sort_values(by='x', inplace =True)
            tmp.reset_index(inplace=True, drop = True)
            tmp = tmp[tmp['y']!=101]
            x = tmp['x'].values
            y = tmp['y'].values
            z = tmp['status'].values 
            
            
            #------Age vs HY score
            plot = ax[0].plot(tmp[tmp['status']==0]['x'],tmp[tmp['status']==0]['y'],alpha = 0.7, c=cmap(j), marker ='o', markersize=3, linestyle='--')
            plot = ax[1].plot(tmp[tmp['status']==1]['x'],tmp[tmp['status']==1]['y'],alpha = 0.7, c=cmap(j), marker ='o', markersize=3, linestyle='--')
            
            
                
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[0], label = 'Onset Age')
    fig.colorbar(sm, ax=ax[1], label = 'Onset Age')
    
    #Iterate through control subjects
    print('_init_Controls')
    
    #Ccolorbar length
    N=len(ctrl_wholedata_subs)
    #Assign Colormap
    cmap = plt.get_cmap('gnuplot_r',N)
    #Slopes
    ctrl_slopes=[]
    ctrl_rsq=[]
    
    for j,i in enumerate(list(ctrl_sorted_ct_df_file['Subject_ID'])):
        #print(str(i))
        
        #--Subject HY Dates
        #Redefine as list of values (was string)
        ctrl_dates = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['HY_Dates'].values[0]
        ctrl_dates = eval(ctrl_dates)
        
        if len(ctrl_dates)>1:
            
            plotted_subs_ctrl.append(i)
            
            #--Subjects Age at evaluation 
            #Extract birth date 
            birth_date = datetime.strptime(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Birthdate'].values[0],'%m/%Y')
            #Age at test
            #Onset date minus test date in years 
            x=np.array([(datetime.strptime(a, '%m/%Y')-birth_date).days/365 for a in ctrl_dates])
            
            #--Subject HY Scores
            #Redefine as list of values (was string)
            y = ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['HY_Scores'].values[0]
            if 'n' in y:
                y= y.replace('nan','10101') #Barcoding to remove date in case of nan
            y = np.array(eval(y))
            
            #--Remove date if nan in score
            if 10101 in y:
                #print('Nan in data')
                x=x[y!=10101]
                y=y[y!=10101]
                
            #--Age-Score dataframe 
            tmp = pd.DataFrame({'x':x, 'y':y})
            tmp.sort_values(by='x', inplace =True)
            tmp.reset_index(inplace=True, drop = True)
            tmp = tmp[tmp['y']!=101]
            x = tmp['x'].values
            y = tmp['y'].values
                    
            #------Age vs HY Score Plot
            plot = ax[2].plot(x,y,alpha = 0.5, c=cmap(j), marker ='o', markersize=3, linestyle='--') 
            
            #-----Obtain Subjects years of education
            yoe = float(ctrl_sorted_ct_df_file[(ctrl_sorted_ct_df_file['Subject_ID']==i)]['Years_of_education'].value_counts().index[0])
            
            
            
        
    ax[0].set_title('Parkinsons   OFF       n='+str(len(plotted_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
    ax[1].set_title('Parkinsons   ON       ', pad = 0, fontsize= 10, loc = 'right')
    ax[2].set_title('Controls          n='+str(len(plotted_subs_ctrl)), pad = 0, fontsize= 10, loc = 'right')
    ax[0].set(ylabel='HY Score')
    ax[1].set(ylabel='HY Score')
    ax[2].set(xlabel='Age', ylabel='HY Score')
    ax[0].set_ylim([5.5,-0.5])
    ax[1].set_ylim([5.5,-0.5])
    ax[2].set_ylim([5.5,-0.5])
    ax[0].set_xlim([28,93])
    ax[1].set_xlim([28,93])
    ax[2].set_xlim([28,93])
    
    #Normalize color data for colorbar 
    norm = mpl.colors.Normalize(vmin=min(pdd_ages),vmax=max(pdd_ages))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm, ax=ax[2], label ='Age at first HY')
    plt.show()
    
    plt.tight_layout()
    
    plt.savefig('Evolution Trayectories HY Score vs Age_'+(os.path.basename(sv_path)[:-4])+'_'+sname)