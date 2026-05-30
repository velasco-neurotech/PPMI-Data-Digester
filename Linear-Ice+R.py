# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 15:54:02 2026


 _       _________ _        _______  _______  _______     
( \      \__   __/( (    /|(  ____ \(  ___  )(  ____ )    
| (         ) (   |  \  ( || (    \/| (   ) || (    )|    
| |         | |   |   \ | || (__    | (___) || (____)|    
| |         | |   | (\ \) ||  __)   |  ___  ||     __)    
| |         | |   | | \   || (      | (   ) || (\ (       
| (____/\___) (___| )  \  || (____/\| )   ( || ) \ \__    
(_______/\_______/|/    )_)(_______/|/     \||/   \__/    
                                                          
         _________ _______  _______               _______ 
         \__   __/(  ____ \(  ____ \      _      (  ____ )
            ) (   | (    \/| (    \/     ( )     | (    )|
 _____      | |   | |      | (__       __| |__   | (____)|
(_____)     | |   | |      |  __)     (__   __)  |     __)
            | |   | |      | (           | |     | (\ (   
         ___) (___| (____/\| (____/\     (_)     | ) \ \__
         \_______/(_______/(_______/             |/   \__/
                                                          
                       

@author: Miguel Velasco Orozco 

ICE: Inferences from Clinical Evidence + Radiological 

"""

VER = '2.0'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import easygui as eg
import os                #Sirve para el Manejo de archivos
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from scipy.stats import false_discovery_control as FDR
from scipy.stats import pearsonr
#import matplotlib as mpl
from matplotlib.lines import Line2D
from statsmodels.stats.outliers_influence import variance_inflation_factor as VIF
#from statsmodels import graphics
from scipy import stats as stats
#from sklearn.linear_model import LinearRegression
import seaborn as sb
#import bambi as bmb
#import arviz as az

os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]


#%%---------------------------PATH MANAGER-------------------------------------

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Linear-ICE+R"+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Linear-ICE+R "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select PD Long BrAiN-Trak LINMOD File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pd_long_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select PD Single BrAiN-Trak LINMOD File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pd_single_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Ctrl Long BrAiN-Trak LINMOD File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_long_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Ctrl Single BrAiN-Trak LINMOD File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_single_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)

#%%---------------------------DATA LOAD----------------------------------------

pd_long_file = pd.read_csv(pd_long_path)  
pd_single_file = pd.read_csv(pd_single_path)  
ctrl_long_file = pd.read_csv(ctrl_long_path)  
ctrl_single_file = pd.read_csv(ctrl_single_path)  

#----Outlier subject Removal

#pd_long_file = pd_long_file[pd_long_file.Subject_ID!=3771]

#-------------MoCA Compensation to raw data correction (revert +1 pt in subs with <=12 YOE)
pd_long_corrected = pd_long_file.copy()
pd_single_corrected = pd_single_file.copy()
ctrl_long_corrected = ctrl_long_file.copy()
ctrl_single_corrected = ctrl_single_file.copy()

#PDD Long
for index, row in pd_long_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =pd_long_corrected['MoCA_Scores'][index]
        pd_long_corrected.loc[index,'MoCA_Scores'] = prev-1

#PDD Single
for index, row in pd_single_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =pd_single_corrected['MoCA_Scores'][index]
        pd_single_corrected.loc[index,'MoCA_Scores'] = prev-1

#Ctrl Long
for index, row in ctrl_long_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =ctrl_long_corrected['MoCA_Scores'][index]
        ctrl_long_corrected.loc[index,'MoCA_Scores'] = prev-1

#Ctrl Single
for index, row in ctrl_single_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =ctrl_single_corrected['MoCA_Scores'][index]
        ctrl_single_corrected.loc[index,'MoCA_Scores'] = prev-1

#%%---------------------------Database Merge / Early-Late Onset selection------

#----Outlier subject Removal

#pd_long_corrected = pd_long_corrected[pd_long_corrected.Subject_ID != 3771]
#ctrl_long_corrected = ctrl_long_corrected[ctrl_long_corrected.Subject_ID != 3112]

#------Single + Longitudinal files merge
pd_db= pd.concat([pd_long_corrected, pd_single_corrected], ignore_index=True)
ctrl_db = pd.concat([ctrl_long_corrected, ctrl_single_corrected], ignore_index=True)
merge_db = pd.concat([pd_db, ctrl_db], ignore_index=True)

#------Column renaming
#Remove Parentheses
pd_db.columns = pd_db.columns.str.replace('(', '')
ctrl_db.columns = pd_db.columns.str.replace('(', '')
merge_db.columns = pd_db.columns.str.replace('(', '')
pd_db.columns = pd_db.columns.str.replace(')', '')
ctrl_db.columns = pd_db.columns.str.replace(')', '')
merge_db.columns = pd_db.columns.str.replace(')', '')
#Remove Spacing
pd_db.columns = pd_db.columns.str.replace(' ', '_')
ctrl_db.columns = pd_db.columns.str.replace(' ', '_')
merge_db.columns = pd_db.columns.str.replace(' ', '_')
#Remove Percentage
pd_db.columns = pd_db.columns.str.replace('%', 'PR')
ctrl_db.columns = pd_db.columns.str.replace('%', 'PR')
merge_db.columns = pd_db.columns.str.replace('%', 'PR')
#Remove Plus
pd_db.columns = pd_db.columns.str.replace('+', '_plus_')
ctrl_db.columns = pd_db.columns.str.replace('+', '_plus_')
merge_db.columns = pd_db.columns.str.replace('+', '_plus_')
#Remove dot
pd_db.columns = pd_db.columns.str.replace('.', '_')
ctrl_db.columns = pd_db.columns.str.replace('.', '_')
merge_db.columns = pd_db.columns.str.replace('.', '_')
#Remove -
pd_db.columns = pd_db.columns.str.replace('-', '_')
ctrl_db.columns = pd_db.columns.str.replace('-', '_')
merge_db.columns = pd_db.columns.str.replace('-', '_')
#Remove numbers
pd_db.columns = pd_db.columns.str.replace('3rd', 'Third')
ctrl_db.columns = pd_db.columns.str.replace('3rd', 'Third')
merge_db.columns = pd_db.columns.str.replace('3rd', 'Third')
pd_db.columns = pd_db.columns.str.replace('4th', 'Fourth')
ctrl_db.columns = pd_db.columns.str.replace('4th', 'Fourth')
merge_db.columns = pd_db.columns.str.replace('4th', 'Fourth')

#Set Subjects ID as int
pd_db['Subject_ID']= pd_db['Subject_ID'].astype(int) 
ctrl_db['Subject_ID']= ctrl_db['Subject_ID'].astype(int) 
merge_db['Subject_ID']= merge_db['Subject_ID'].astype(int) 

#Longitudinal Subjects 
eo_l_pd_subs =[]
lo_l_pd_subs =[]
eo_l_matched_subs=[]
lo_l_matched_subs =[]

#Single Subjects
eo_s_pd_subs =[]
lo_s_pd_subs =[]
eo_s_matched_subs=[]
lo_s_matched_subs =[]

#Parkinsons
allsubs = pd_db['Subject_ID'].unique()

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(pd_db[pd_db['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if pd_db[pd_db['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55: 
            eo_l_pd_subs.append(i)
        else:
            lo_l_pd_subs.append(i)
    else:
        #Extract Subjects 
        if pd_db[pd_db['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55: 
            eo_s_pd_subs.append(i)
        else:
            lo_s_pd_subs.append(i)


#Controls
allsubs = ctrl_db['Subject_ID'].unique()

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(ctrl_db[ctrl_db['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if ctrl_db[ctrl_db['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55: 
            eo_l_matched_subs.append(i)
        else:
            lo_l_matched_subs.append(i)
    else:
        #Extract Subjects 
        if ctrl_db[ctrl_db['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55:
            eo_s_matched_subs.append(i)
        else:
            lo_s_matched_subs.append(i)

#----------Add Years Since Onset to PD Database

tmp = pd_db['Age']-pd_db['Onset_Age']
pd_db['YSO']=tmp #Years Since Onset column

#----------Add Early-Late Flag

tmp = pd.Series(np.zeros(len(pd_db)))
pd_db['EoL']=tmp   #Early or Late column
pd_db['EoL']= pd_db['EoL'].astype(str) 
pd_db.loc[pd_db['Subject_ID'].isin(eo_s_pd_subs+eo_l_pd_subs), 'EoL'] = 'Early'
pd_db.loc[pd_db['Subject_ID'].isin(lo_s_pd_subs+lo_l_pd_subs), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(ctrl_db)))
ctrl_db['EoL']=tmp
ctrl_db['EoL']= ctrl_db['EoL'].astype(str) 
ctrl_db.loc[ctrl_db['Subject_ID'].isin(eo_s_matched_subs+eo_l_matched_subs), 'EoL'] = 'Early'
ctrl_db.loc[ctrl_db['Subject_ID'].isin(lo_s_matched_subs+lo_l_matched_subs), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(merge_db)))
merge_db['EoL']=tmp
merge_db['EoL']= merge_db['EoL'].astype(str) 
merge_db.loc[merge_db['Subject_ID'].isin(eo_s_pd_subs+eo_l_pd_subs+eo_s_matched_subs+eo_l_matched_subs), 'EoL'] = 'Early'
merge_db.loc[merge_db['Subject_ID'].isin(lo_s_pd_subs+lo_l_pd_subs+lo_s_matched_subs+lo_l_matched_subs), 'EoL'] = 'Late'

#-------Separate databases by subject group

#L+S
whole_eo_subs=eo_l_pd_subs + eo_s_pd_subs + eo_l_matched_subs + eo_s_matched_subs 
whole_lo_subs=lo_l_pd_subs + lo_s_pd_subs + lo_l_matched_subs + lo_s_matched_subs

eo_db = merge_db.loc[merge_db['Subject_ID'].isin(whole_eo_subs)]
lo_db = merge_db.loc[merge_db['Subject_ID'].isin(whole_lo_subs)]

#Longitudinal + Grouped S (Change single subjects to barcode group)
eo_lgs_db = eo_db.copy()
lo_lgs_db = lo_db.copy()

eo_lgs_db.loc[eo_lgs_db['Subject_ID'].isin(eo_s_pd_subs+eo_s_matched_subs), 'Subject_ID'] = 101010
lo_lgs_db.loc[lo_lgs_db['Subject_ID'].isin(lo_s_pd_subs+lo_s_matched_subs), 'Subject_ID'] = 201010

pd_lgs_db = pd_db.copy()
pd_lgs_db.loc[pd_lgs_db['Subject_ID'].isin(eo_s_pd_subs+lo_s_pd_subs), 'Subject_ID'] = 102010

ctrl_lgs_db = ctrl_db.copy()
ctrl_lgs_db.loc[ctrl_lgs_db['Subject_ID'].isin(eo_s_matched_subs+lo_s_matched_subs), 'Subject_ID'] = 102010

#Only longitudinal 

pd_l_subs = eo_l_pd_subs + lo_l_pd_subs
pd_l_db = pd_db.loc[pd_db['Subject_ID'].isin(pd_l_subs)]

ctrl_l_subs = eo_l_matched_subs + lo_l_matched_subs
ctrl_l_db = ctrl_db.loc[ctrl_db['Subject_ID'].isin(ctrl_l_subs)]

#--------------------Scaler

pd_db_scaled = pd_db.copy()     #Parkinsons Database
ctrl_db_scaled = ctrl_db.copy() #Controls Database
merge_db_scaled = merge_db.copy() #Parkinsons + Controls Database 
eo_db_scaled = eo_db.copy()  #Early Onset PD+Matched Database
lo_db_scaled = lo_db.copy()  #Late Onset PD+Matched Database

#Longitudinal + Grouped Singles 
pd_lgs_db_scaled = pd_lgs_db.copy()  #Parkinsons Longitudinal + Grouped Singles Database
ctrl_lgs_db_scaled = ctrl_lgs_db.copy()  #Controls Longitudinal + Grouped Singles Database
eo_lgs_db_scaled = eo_lgs_db.copy()  #Early Onset PD+Matched+Grouped Singles Database
lo_lgs_db_scaled = lo_lgs_db.copy()  #Late Onset PD+Matched+Grouped Singles Database

#Longitudinal 
pd_l_db_scaled = pd_l_db.copy()
ctrl_l_db_scaled = ctrl_l_db.copy()


#Obtain Structures 
tmp = list(merge_db.columns)
#Values to remove (not structures)
to_remove = ['Subject_ID', 'Test_Number','Sex', 'Birthdate', 'Group','Modality', 'Years_of_education',
             'MoCA_Scores', 'MoCA_Dates', 'Age_at_Test', 'Days_between_Tests','Slope','Onset_Age',
             'Diagnosis_Age', 'Subject','Report_date','Image_orientation', 'Scale_factor', 'Quality_control',
             'Filename','ImageID', 'SubjectID','Group_1','Sex_1','Age','Date','SNR_y','CNR','EFC','CJV', 'SNR_x', 'EoL',
             'HY_Scores','HY_Dates','Test_Number_1','Age_at_Test_1', 'Days_between_Tests_1','Slope_1']
#Left Structures
structures_left = [x for x in tmp if 'left' in x] #Remove everything but left structures
structures_left = [x for x in structures_left if 'cm3' not in x] #Remove cm3 values
#Right Structures 
structures_right = [x for x in tmp if 'right' in x] #Remove everything but right structures
structures_right = [x for x in structures_right if 'cm3' not in x] #Remove cm3 values 
#Structures Full (Left+Right)
structures_LR = structures_right + structures_left
#Structures Total (Only total volumes)
structures_total = [x for x in tmp if x not in structures_left+structures_right] #Remove left+right structures
structures_total = [x for x in structures_total if 'asymmetry' not in x] #Remove Asymmetry values
structures_total = [x for x in structures_total if 'cm3' not in x] #Remove cm3 values 
structures_total = [x for x in structures_total if x not in to_remove] #Remove other values 



#Continuous variables to include in scaler
cont = ['Years_of_education', 'Age_at_Test', 'Age_at_Test_1', 'Days_between_Tests', 'Onset_Age', 'Diagnosis_Age', 'Age',
        'SNR_y','CNR','EFC','CJV', 'SNR_x']
var = structures_total+cont

#Database Scaling 
scaler = StandardScaler()
pd_db_scaled[var+['YSO']] = scaler.fit_transform(pd_db_scaled[var+['YSO']])
ctrl_db_scaled[var] = scaler.fit_transform(ctrl_db_scaled[var])
merge_db_scaled[var] = scaler.fit_transform(merge_db_scaled[var])
eo_db_scaled[var]= scaler.fit_transform(eo_db_scaled[var])
lo_db_scaled[var] = scaler.fit_transform(lo_db_scaled[var])

#Longitudinal + Grouped singles
pd_lgs_db_scaled[var+['YSO']] = scaler.fit_transform(pd_lgs_db_scaled[var+['YSO']])
ctrl_lgs_db_scaled[var] = scaler.fit_transform(ctrl_lgs_db_scaled[var])
eo_lgs_db_scaled[var] = scaler.fit_transform(eo_lgs_db_scaled[var])
lo_lgs_db_scaled[var] = scaler.fit_transform(lo_lgs_db_scaled[var])

#Longitudinal only 
pd_l_db_scaled[var+['YSO']] = scaler.fit_transform(pd_l_db_scaled[var+['YSO']])
ctrl_l_db_scaled[var] = scaler.fit_transform(ctrl_l_db_scaled[var])



#%%---------/////////////Linear Model Implementation-MoCA ONLY\\\\\\\\\\\\-------
#%%----------------------Early / Late Models + Interaction---------------------

#--------------Longitudinal + Single

#Early Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education ", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model (Subsample L+S)')
print(eo_lm.summary())

#Late Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model (Subsample L+S)')
print(lo_lm.summary())


#Early Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model + interaction (Subsample L+S)')
print(eo_lm.summary())

#Late Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model + interaction (Subsample L+S)')
print(lo_lm.summary())


#-------Longitudinal + grouped single 

#Early Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education ", 
                 eo_lgs_db, groups=eo_lgs_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model (Subsample L+ Grouped S)')
print(eo_lm.summary())

#Late Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
                 lo_lgs_db_scaled, groups=lo_lgs_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model (Subsample L+ Grouped S)')
print(lo_lm.summary())

#%%----------------------PD / Ctrl Models + Interaction------------------------

#PDD Model
lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
                 pd_db, groups=pd_db["Subject_ID"], re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model (Subsample L+S)')
print(pd_lm.summary())

lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 pd_db, groups=pd_db["Subject_ID"], re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model 2 (Subsample L+S)')
print(pd_lm.summary())

#Ctrl Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 ctrl_db, groups=ctrl_db["Subject_ID"], re_formula='~Age_at_Test')
ctrl_lm = lm.fit()
print('\nCtrl Model (Subsample L+S)')
print(ctrl_lm.summary())

#Merge Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group", 
                 merge_db, groups=merge_db["Subject_ID"], re_formula='~Age_at_Test')
merge_lm = lm.fit()
print('\nMerged Model (Subsample L+S)')
print(merge_lm.summary())

#Merge Model + interaction
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group+ Age_at_Test*Group", 
                 merge_db, groups=merge_db["Subject_ID"], re_formula='~Age_at_Test')
merge_lm_i = lm.fit()
print('\nMerged Model + interaction (Subsample L+S)')
print(merge_lm_i.summary())

#-----------Longitudinal + Grouped Single 
#PDD Model
lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
                 pd_lgs_db, groups=pd_lgs_db["Subject_ID"], re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model (Subsample L+ Grouped S)')
print(pd_lm.summary())


#%%--------------//////////Model Implementation-MoCA+Structural\\\\\\\\\-------
#%%----------------------Full Structural model PD  test 1 ---------------------
#PDD Model

lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + "
                 "Subcortical_GM_volume_PR + Cortical_GM_volume_PR + Cerebellar_GM_volume_PR +"
                 "Accumbens_total_volume_PR + Amygdala_total_volume_PR + Basal_forebrain_total_volume_PR + "
                 "Caudate_total_volume_PR + Hippocampus_total_volume_PR + Pallidum_total_volume_PR + " 
                 "Putamen_total_volume_PR + Thalamus_total_volume_PR + Ventral_DC_total_volume_PR +"
                 "Frontal_lobe_total_volume_PR + Parietal_lobe_total_volume_PR + Temporal_lobe_total_volume_PR +"
                 "Occipital_lobe_total_volume_PR + Limbic_cortex_total_volume_PR + Insular_cortex_total_volume_PR", 
                 pd_db, groups="Subject_ID", re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model Structures All Structures (Subsample L+S)')
print(pd_lm.summary())


lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + "
                 "Subcortical_GM_volume_PR + Cortical_GM_volume_PR + Cerebellar_GM_volume_PR", 
                 pd_db, groups="Subject_ID", re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model Structures Whole Brain (Subsample L+S)')
print(pd_lm.summary())


lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + "
                 "Accumbens_total_volume_PR + Amygdala_total_volume_PR + Basal_forebrain_total_volume_PR + "
                 "Caudate_total_volume_PR + Hippocampus_total_volume_PR + Pallidum_total_volume_PR + " 
                 "Putamen_total_volume_PR + Thalamus_total_volume_PR + Ventral_DC_total_volume_PR", 
                 pd_db, groups="Subject_ID", re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model Structures Subcortical (Subsample L+S)')
print(pd_lm.summary())


lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + "
                 "Frontal_lobe_total_volume_PR + Parietal_lobe_total_volume_PR + Temporal_lobe_total_volume_PR +"
                 "Occipital_lobe_total_volume_PR + Limbic_cortex_total_volume_PR + Insular_cortex_total_volume_PR", 
                 pd_db, groups="Subject_ID", re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model Structures Cortices (Subsample L+S)')
print(pd_lm.summary())


lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + "
                 "Caudate_total_volume_PR + Thalamus_total_volume_PR + Frontal_lobe_total_volume_PR", 
                 pd_db, groups="Subject_ID", re_formula='~Age_at_Test')
pd_lm = lm.fit()
print('\n\n\nPDD Model Structures Selected Structures (Subsample L+S)')
print(pd_lm.summary())

#%%----------------------Chi Squared variable test PD--------------------------

# test_vars = ['Years_of_education', 'Sex', 'Subcortical_GM_volume_PR', 'White_Matter_WM_volume_PR',
#              'Grey_Matter_GM_volume_PR', 'Cortical_GM_volume_PR', 'Cerebellar_GM_volume_PR', 'Accumbens_total_volume_PR',
#              'Amygdala_total_volume_PR', 'Basal_forebrain_total_volume_PR','Caudate_total_volume_PR', 'Hippocampus_total_volume_PR',
#              'Pallidum_total_volume_PR','Putamen_total_volume_PR', 'Thalamus_total_volume_PR', 'Ventral_DC_total_volume_PR',
#              'Frontal_lobe_total_volume_PR','Parietal_lobe_total_volume_PR','Temporal_lobe_total_volume_PR',
#              'Occipital_lobe_total_volume_PR', 'Limbic_cortex_total_volume_PR','Insular_cortex_total_volume_PR']

# test_results = []

# #----Base Model
# base_lm_pd = sm.MixedLM.from_formula(
#     formula="MoCA_Scores ~ Age_at_Test",
#     groups = "Subject_ID",
#     re_formula = "~Age_at_Test",
#     data = pd_db_scaled).fit(reml=False)

# print('PD Base Model')
# print(base_lm_pd.summary())

# test_results.append({
#     'modelo': 'base (Age)',
#     'formula': base_lm_pd.model.formula,
#     'loglik': base_lm_pd.llf,
#     'aic': base_lm_pd.aic,
#     'bic': base_lm_pd.bic,
#     'n_params': len(base_lm_pd.params)
# })


# current_model = base_lm_pd

# for i,j in enumerate(test_vars):
    
#     #For first predictor
#     if i == 0:
#         new_formula = f"MoCA_Scores ~ Age_at_Test + {j} "

#     else: #Concat next predictors
#         new_formula = test_results[-1]['formula']+ f" + {j} "

#     #Adjust new model 
#     try:
#         new_model = sm.MixedLM.from_formula(
#             formula = new_formula,
#             groups= 'Subject_ID',
#             re_formula='~Age_at_Test',
#             data = pd_db_scaled).fit(reml=False, maxiter=1000, method='bfgs')
        
#         #Obtain LRT
#         lrt_stat = -2*(test_results[-1]['loglik'] - new_model.llf)
#         df_diff = len(new_model.params) - test_results[-1]['n_params']
#         pval = chi2.sf(lrt_stat,df_diff)
        
#         #Save Results 
#         test_results.append({
#             'modelo': f"base + {' + '.join(test_vars[:i+1])}",
#             'formula' : new_formula,
#             'loglik' : new_model.llf,
#             'aic': new_model.aic,
#             'bic': new_model.bic,
#             'n_params': len(new_model.params),
#             'lrt_vs_prev' : lrt_stat,
#             'df_diff' : df_diff,
#             'p_value' : pval})
        
#         #Model update 
#         current_model = new_model
        
#     except Exception as e:
#         print(f"Cannot adjust model with {j}:{e}")
#         break
    
# chisq_pd_results = pd.DataFrame(test_results)
# print(chisq_pd_results)



#%%-------------//////////Model Implementation Only Structural\\\\\\\\\\-------
#%%----------------------VIF Colinearity Test----------------------------------

#Colinearity Test PD
tmp = pd_db_scaled[["Age_at_Test", "Years_of_education", "YSO", "Sex", "EoL", 'MoCA_Scores', 'HY_Scores']]

tmp['Sex'] = tmp['Sex'].map({'M':0, 'F':1}) #Convert levels to zeros and ones 
tmp['EoL'] = tmp['EoL'].map({'Early':0, 'Late':1})

vif_data = pd.DataFrame()
vif_data['Features'] = tmp.columns
vif_data['VIF'] = [VIF(tmp.values,i) for i in range(len(tmp.columns))]

#Colinearity Test Ctrl
tmp = ctrl_db_scaled[["Age_at_Test", "Years_of_education", "Sex", "EoL", 'MoCA_Scores','HY_Scores']]

tmp['Sex'] = tmp['Sex'].map({'M':0, 'F':1}) #Convert levels to zeros and ones 
tmp['EoL'] = tmp['EoL'].map({'Early':0, 'Late':1})

vif_data = pd.DataFrame()
vif_data['Features'] = tmp.columns
vif_data['VIF'] = [VIF(tmp.values,i) for i in range(len(tmp.columns))]

#%%----------------------Non Lateralized (only totals vols) PD Model-----------
pd_results = []
pd_models_plot_db = pd.DataFrame()
pd_models_plot_db['Subject_ID']= pd_db['Subject_ID']
pd_models_plot_db['YSO']= pd_db['YSO']
pd_models_plot_db['Age_at_Test']= pd_db['Age_at_Test']
pd_models_plot_db['Onset_Age']= pd_db['Onset_Age']
pd_models_plot_db['EoL']= pd_db['EoL']

for i in structures_total:
    
    formula = i + " ~ MoCA_Scores + EoL + YSO + Age_at_Test + Sex + Years_of_education "
    print(formula)
    
    lm = smf.mixedlm(formula, pd_db_scaled, groups=pd_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    pd_lm = lm.fit()
    
    print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = pd_lm.pvalues 
    params = pd_lm.params
    zvals = pd_lm.tvalues

    pd_results.append({
        'modelo': i,
        'formula': pd_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'MoCA_Scores': params['MoCA_Scores'],
        'MoCA_Scores z': zvals['MoCA_Scores'],
        'MoCA_Scores pvalue': pvals['MoCA_Scores'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test z': zvals['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'EoL': params['EoL[T.Late]'],
        'EoL z': zvals['EoL[T.Late]'],
        'EoL pvalue': pvals['EoL[T.Late]'],
        'YSO': params['YSO'],
        'YSO z': zvals['YSO'],
        'YSO pvalue': pvals['YSO']
        
    })
    
    if pd_lm.converged:
        pd_models_plot_db[i]=pd_lm.fittedvalues
        
    
    print(pd_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(pd_lm.fittedvalues)), pd_lm.resid)
        
pd_model_results_df = pd.DataFrame(pd_results)
pd_model_results_df = pd_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','MoCA_Scores pvalue','Age_at_Test pvalue', 'Years_of_education pvalue',
              'EoL pvalue','YSO pvalue' ]


for i in pvals_index:
    tmp_pvals = pd_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    pd_model_results_df[new_index]= tmp_pvals_fdr

#%%----------------------Non Lateralized Ctrl Model----------------------------

ctrl_results = []


for i in structures_total:
    
    formula = i + " ~ MoCA_Scores + Age_at_Test + Sex + Years_of_education"
    print(formula)
    
    lm = smf.mixedlm(formula, ctrl_db_scaled, groups=ctrl_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    ctrl_lm = lm.fit()
    
    print('Ctrl Full '+i+' Model')
   
    pvals = ctrl_lm.pvalues 
    params = ctrl_lm.params

    ctrl_results.append({
        'modelo': i,
        'formula': ctrl_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'MoCA_Scores': params['MoCA_Scores'],
        'MoCA_Scores pvalue': pvals['MoCA_Scores'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Group Var': params['Group Var'],
        'Group Var pvalue': pvals['Group Var'],
        
    })
    
    print(ctrl_lm.summary())
    
ctrl_model_results_df = pd.DataFrame(ctrl_results)
ctrl_model_results_df = ctrl_model_results_df.dropna()

#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','MoCA_Scores pvalue','Age_at_Test pvalue', 'Years_of_education pvalue','Group Var pvalue' ]


for i in pvals_index:
    tmp_pvals = ctrl_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    ctrl_model_results_df[new_index]= tmp_pvals_fdr
    
#%%----------------------Left+ Right PD Subsample Model------------------------ <CURRENT
pd_results = []
pd_models_plot_db = pd.DataFrame()
pd_models_plot_db['Subject_ID']= pd_db['Subject_ID']
pd_models_plot_db['YSO']= pd_db['YSO']
pd_models_plot_db['Age_at_Test']= pd_db['Age_at_Test']
pd_models_plot_db['Onset_Age']= pd_db['Onset_Age']
pd_models_plot_db['EoL']= pd_db['EoL']

for i in structures_LR:
    
    formula = i + " ~ Onset_Age + Age_at_Test + Sex + Years_of_education "
    print(formula)
    
    lm = smf.mixedlm(formula, pd_db_scaled, groups=pd_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    pd_lm = lm.fit()
    
    print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = pd_lm.pvalues 
    params = pd_lm.params
    zvals = pd_lm.tvalues

    pd_results.append({
        'modelo': i,
        'formula': pd_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Onset_Age': params['Onset_Age'],
        'Onset_Age z': zvals['Onset_Age'],
        'Onset_Age pvalue': pvals['Onset_Age'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test z': zvals['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education']
        
    })
    
    if pd_lm.converged:
        pd_models_plot_db[i]=pd_lm.fittedvalues
        
    
    print(pd_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(pd_lm.fittedvalues)), pd_lm.resid)
        
pd_model_results_df = pd.DataFrame(pd_results)
pd_model_results_df = pd_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Age_at_Test pvalue', 'Years_of_education pvalue', 'Onset_Age pvalue' ]


for i in pvals_index:
    tmp_pvals = pd_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    pd_model_results_df[new_index]= tmp_pvals_fdr
    
    


#%%----------------------Preliminary  Plot-------------------------------------

ticks = list(pd_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD Subsample Models L+R (Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(pd_model_results_df['modelo'], pd_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
#ax[0,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Onset_Age FDR Corrected")
ax[1,0].scatter(pd_model_results_df['modelo'], pd_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[1,1].set_title("Age At Test FDR Corrected")
ax[1,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

# ax[1,1].set_title("Onset Age FDR Corrected")
# ax[1,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
# ax[1,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['EoL pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("HY Scores FDR Corrected")
# ax[1,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['HY_Scores pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])


# ax[2,1].set_title("Years Since Onset FDR Corrected")
# ax[2,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['YSO pvalue FDR'], mouseover=True)
# ax[2,1].axhline(0.05, color ='red')
# ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Left+ Right Ctrl Subsample Model---------------------- <CURRENT
ctrl_results = []
ctrl_models_plot_db = pd.DataFrame()
ctrl_models_plot_db['Subject_ID']= ctrl_db['Subject_ID']
ctrl_models_plot_db['Age_at_Test']= ctrl_db['Age_at_Test']
# ctrl_models_plot_db['Onset_Age']= ctrl_db['Onset_Age']
ctrl_models_plot_db['EoL']= ctrl_db['EoL']

for i in structures_LR:
    
    formula = i + " ~  Age_at_Test + Sex + Years_of_education "
    print(formula)
    
    lm = smf.mixedlm(formula, ctrl_db_scaled, groups=ctrl_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    ctrl_lm = lm.fit()
    
    print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = ctrl_lm.pvalues 
    params = ctrl_lm.params
    zvals = ctrl_lm.tvalues

    ctrl_results.append({
        'modelo': i,
        'formula': ctrl_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        # 'Onset_Age': params['Onset_Age'],
        # 'Onset_Age z': zvals['Onset_Age'],
        # 'Onset_Age pvalue': pvals['Onset_Age'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test z': zvals['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education']
        
    })
    
    if ctrl_lm.converged:
        ctrl_models_plot_db[i]=ctrl_lm.fittedvalues
        
    
    print(ctrl_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(ctrl_lm.fittedvalues)), ctrl_lm.resid)
        
ctrl_model_results_df = pd.DataFrame(ctrl_results)
ctrl_model_results_df = ctrl_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Age_at_Test pvalue', 'Years_of_education pvalue']#, 'Onset_Age pvalue' ]


for i in pvals_index:
    tmp_pvals = ctrl_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    ctrl_model_results_df[new_index]= tmp_pvals_fdr
    
    


#%%----------------------Preliminary  Plot-------------------------------------

ticks = list(ctrl_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - Ctrl Subsample Models L+R (Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
#ax[0,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

# ax[1,0].set_title("Onset_Age FDR Corrected")
# ax[1,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['MoCA_Scores pvalue FDR'], mouseover=True)
# ax[1,0].axhline(0.05, color ='red')
# ax[1,0].set_xticks([])

ax[1,0].set_title("Age At Test FDR Corrected")
ax[1,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

# ax[1,1].set_title("Onset Age FDR Corrected")
# ax[1,1].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
# ax[1,1].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['EoL pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("HY Scores FDR Corrected")
# ax[1,1].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['HY_Scores pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])


# ax[2,1].set_title("Years Since Onset FDR Corrected")
# ax[2,1].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['YSO pvalue FDR'], mouseover=True)
# ax[2,1].axhline(0.05, color ='red')
# ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Left+ Right Merge Subsample Model---------------------- <CURRENT
merge_results = []
merge_models_plot_db = pd.DataFrame()
merge_models_plot_db['Subject_ID']= merge_db['Subject_ID']
merge_models_plot_db['Age_at_Test']= merge_db['Age_at_Test']
# merge_models_plot_db['Onset_Age']= merge_db['Onset_Age']
merge_models_plot_db['EoL']= merge_db['EoL']

for i in structures_LR:
    
    formula = i + " ~  Age_at_Test + Group + Sex + Years_of_education + Group*Age_at_Test"
    print(formula)
    
    lm = smf.mixedlm(formula, merge_db_scaled, groups=merge_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    merge_lm = lm.fit()
    
    print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = merge_lm.pvalues 
    params = merge_lm.params
    zvals = merge_lm.tvalues

    merge_results.append({
        'modelo': i,
        'formula': merge_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Group': params['Group[T.PD]'],
        'Group z': zvals['Group[T.PD]'],
        'Group pvalue': pvals['Group[T.PD]'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test z': zvals['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Group*Age_at_Test': params['Group[T.PD]:Age_at_Test'],
        'Group*Age_at_Test z': zvals['Group[T.PD]:Age_at_Test'],
        'Group*Age_at_Test pvalue': pvals['Group[T.PD]:Age_at_Test'],
        
    })
    
    if merge_lm.converged:
        merge_models_plot_db[i]=merge_lm.fittedvalues
        
    
    print(merge_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(merge_lm.fittedvalues)), merge_lm.resid)
        
merge_model_results_df = pd.DataFrame(merge_results)
merge_model_results_df = merge_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Age_at_Test pvalue', 'Years_of_education pvalue', 'Group pvalue','Group*Age_at_Test pvalue' ]


for i in pvals_index:
    tmp_pvals = merge_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    merge_model_results_df[new_index]= tmp_pvals_fdr
    
    


#%%----------------------Preliminary  Plot-------------------------------------

ticks = list(merge_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD/Ctrl Subsample Models L+R (Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
#ax[0,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

# ax[1,0].set_title("Onset_Age FDR Corrected")
# ax[1,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['MoCA_Scores pvalue FDR'], mouseover=True)
# ax[1,0].axhline(0.05, color ='red')
# ax[1,0].set_xticks([])

ax[1,0].set_title("Age At Test FDR Corrected")
ax[1,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

ax[1,1].set_title("Group FDR Corrected")
ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Group pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks([])

# ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['EoL pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("HY Scores FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['HY_Scores pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])


ax[2,0].set_title("Group*Age_at_Test FDR Corrected")
ax[2,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Group*Age_at_Test pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Reduced Plot PD Model --------------------------------
ticks = list(pd_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(1,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('P values PD Full Model_'+sname, fontsize=16)
ax[0].set_title("Sex [M] FDR Corrected")
ax[0].scatter(pd_model_results_df['Sex[T.M] pvalue FDR'], pd_model_results_df['modelo'], mouseover=True)
ax[0].scatter(ctrl_model_results_df['Sex[T.M] pvalue FDR'], ctrl_model_results_df['modelo'], mouseover=True)
ax[0].axvline(0.05, color ='red')
ax[0].set_yticks(range(len(ticks)),labels=ticks)
ax[1].set_title("Onset Age FDR Corrected")
ax[1].scatter( pd_model_results_df['Onset_Age pvalue FDR'],pd_model_results_df['modelo'], mouseover=True)
ax[1].axvline(0.05, color ='red')
ax[1].set_yticks([])
plt.tight_layout()


#%%----------------------Left+ Right Merge (PD + Ctrl) MoCA  Model------------------ <CURRENT
merge_results = []
merge_models_plot_db = pd.DataFrame()
merge_models_plot_db['Subject_ID']= merge_db_scaled['Subject_ID']
merge_models_plot_db['Age_at_Test']= merge_db_scaled['Age_at_Test']

for i in structures_LR:
    
    formula = "MoCA_Scores ~ " + i + " + Group  + Age + Sex + Years_of_education + Group*Age"
    print(formula)
    
    lm = smf.mixedlm(formula, merge_db_scaled, groups=merge_db_scaled["Subject_ID"], re_formula='~Age')
    merge_lm = lm.fit()
    
    #print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = merge_lm.pvalues 
    params = merge_lm.params
    zvals = merge_lm.tvalues

    merge_results.append({
        'modelo': i,
        'formula': merge_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Volume':params[i],
        'Volume z':zvals[i],
        'Volume pvalue':pvals[i],
        # 'MoCA_Scores': params['MoCA_Scores'],
        # 'MoCA_Scores z': zvals['MoCA_Scores'],
        # 'MoCA_Scores pvalue': pvals['MoCA_Scores'],
        # 'HY_Scores': params['HY_Scores'],
        # 'HY_Scores z': zvals['HY_Scores'],
        # 'HY_Scores pvalue': pvals['HY_Scores'],
        'Age_at_Test': params['Age'],
        'Age_at_Test z': zvals['Age'],
        'Age_at_Test pvalue': pvals['Age'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Group':params['Group[T.PD]'], 
        'Group z':zvals['Group[T.PD]'], 
        'Group pvalue':pvals['Group[T.PD]'],
        'Group*Age':params['Group[T.PD]:Age'], 
        'Group*Age z':zvals['Group[T.PD]:Age'], 
        'Group*Age pvalue':pvals['Group[T.PD]:Age'] 
    })
    
    if merge_lm.converged:
        merge_models_plot_db[i]=merge_lm.fittedvalues
        
    
    print(merge_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(merge_lm.fittedvalues)), merge_lm.resid)
        
merge_model_results_df = pd.DataFrame(merge_results)
merge_model_results_df = merge_model_results_df.dropna()

#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Volume pvalue','Age_at_Test pvalue', 'Years_of_education pvalue',
              'Group pvalue', 'Group*Age pvalue' ]


for i in pvals_index:
    print(i)
    tmp_pvals = merge_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    merge_model_results_df[new_index]= tmp_pvals_fdr
    
    
#%%----------------------Preliminary  Plot-------------------------------------

ticks = list(merge_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD Models by structure L+R (x=Age at Test, Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
#ax[0,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Volume FDR Corrected")
ax[1,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Volume pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[2,0].set_title("Age At Test FDR Corrected")
ax[2,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

# ax[1,1].set_title("Onset Age FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['EoL pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("HY Scores FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['HY_Scores pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])


ax[2,1].set_title("Group*Age FDR Corrected")
ax[2,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Group*Age pvalue FDR'], mouseover=True)
ax[2,1].axhline(0.05, color ='red')
ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Left+ Right Merge (PD + Ctrl) HY Model------------------ <CURRENT
merge_results_hy = []
merge_models_plot_db_hy = pd.DataFrame()
merge_models_plot_db_hy['Subject_ID']= merge_db_scaled['Subject_ID']
merge_models_plot_db_hy['Age_at_Test']= merge_db_scaled['Age_at_Test']

for i in structures_LR:
    
    formula = "HY_Scores ~ " + i + " + Group  + Age + Sex + Years_of_education + Group*Age"
    print(formula)
    
    lm = smf.mixedlm(formula, merge_db_scaled, groups=merge_db_scaled["Subject_ID"], re_formula='~Age')
    merge_lm = lm.fit()
    
    #print('Longitudinal + Single Acq'+i+' Model')
   
    pvals = merge_lm.pvalues 
    params = merge_lm.params
    zvals = merge_lm.tvalues

    merge_results_hy.append({
        'modelo': i,
        'formula': merge_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Volume':params[i],
        'Volume z':zvals[i],
        'Volume pvalue':pvals[i],
        # 'MoCA_Scores': params['MoCA_Scores'],
        # 'MoCA_Scores z': zvals['MoCA_Scores'],
        # 'MoCA_Scores pvalue': pvals['MoCA_Scores'],
        # 'HY_Scores': params['HY_Scores'],
        # 'HY_Scores z': zvals['HY_Scores'],
        # 'HY_Scores pvalue': pvals['HY_Scores'],
        'Age_at_Test': params['Age'],
        'Age_at_Test z': zvals['Age'],
        'Age_at_Test pvalue': pvals['Age'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Group':params['Group[T.PD]'], 
        'Group z':zvals['Group[T.PD]'], 
        'Group pvalue':pvals['Group[T.PD]'],
        'Group*Age':params['Group[T.PD]:Age'], 
        'Group*Age z':zvals['Group[T.PD]:Age'], 
        'Group*Age pvalue':pvals['Group[T.PD]:Age'] 
    })
    
    if merge_lm.converged:
        merge_models_plot_db_hy[i]=merge_lm.fittedvalues
        
    
    print(merge_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(merge_lm.fittedvalues)), merge_lm.resid)
        
merge_model_results_df = pd.DataFrame(merge_results_hy)
merge_model_results_df = merge_model_results_df.dropna()

#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Volume pvalue','Age_at_Test pvalue', 'Years_of_education pvalue',
              'Group pvalue', 'Group*Age pvalue' ]


for i in pvals_index:
    print(i)
    tmp_pvals = merge_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    merge_model_results_df[new_index]= tmp_pvals_fdr
    
    
#%%----------------------Preliminary  Plot-------------------------------------

ticks = list(merge_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD Models by structure L+R (x=Age at Test, Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
#ax[0,0].scatter(ctrl_model_results_df['modelo'], ctrl_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Volume FDR Corrected")
ax[1,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Volume pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[2,0].set_title("Age At Test FDR Corrected")
ax[2,0].scatter(merge_model_results_df['modelo'], merge_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

# ax[1,1].set_title("Onset Age FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['EoL pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

# ax[1,1].set_title("HY Scores FDR Corrected")
# ax[1,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['HY_Scores pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])


ax[2,1].set_title("Group*Age FDR Corrected")
ax[2,1].scatter(merge_model_results_df['modelo'], merge_model_results_df['Group*Age pvalue FDR'], mouseover=True)
ax[2,1].axhline(0.05, color ='red')
ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Slopes Plot (Years Since Onset Centered)--------------

#Remove Non-Significative Structures (Check if any pvalue < 0.05, OR for each row)
# rows = pd_model_results_df[(pd_model_results_df["Sex[T.M] pvalue FDR"] < 0.05) | (pd_model_results_df["MoCA_Scores pvalue FDR"] < 0.05) | (pd_model_results_df["Years_of_education pvalue FDR"] < 0.05) | (pd_model_results_df["EoL pvalue FDR"] < 0.05) | (pd_model_results_df["YSO pvalue FDR"] < 0.05) | (pd_model_results_df["Age_at_Test pvalue FDR"] < 0.05)].index
# pd_model_sig_results_df =pd_model_results_df.loc[rows]
#Remove Non-Significative YSO sctructures 
rows = pd_model_results_df[(pd_model_results_df["YSO pvalue FDR"] < 0.05)].index
pd_model_sig_results_df =pd_model_results_df.loc[rows]


fig, ax = plt.subplots(5,3)
plt.suptitle('Adjusted Volumes vs Years Since Onset '+sname, fontsize=16)
fig.set_figheight(8)
fig.set_figwidth(12)
c=0 #Counter 
#Iterate only through models with significative variables
for i in pd_model_sig_results_df['modelo'].values[:5]:
    ax[c,0].set_title(i, pad =0, fontsize=10)
    ax[2,0].set_ylabel('Zscore % Volume')
    print(i)
    #Iterate trough subjects for plotting
    for j in pd_models_plot_db['Subject_ID'].unique(): 
        
        yso = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['YSO']
        eol = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['EoL'].unique()[0]
        fitted = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j][i]
        
        if eol == 'Early':    
            ax[c,0].plot(yso, fitted, color = 'midnightblue', alpha =0.5)
        
        elif eol == 'Late':    
            ax[c,0].plot(yso, fitted, color = 'firebrick', alpha =0.5)
    
    if c == 4:
        ax[c,0].set_xlabel('Years Since Onset')
    else:
        ax[c,0].set_xticks([])
    c+=1
c=0 #Counter 
#Iterate only through models with significative variables
for i in pd_model_sig_results_df['modelo'].values[5:10]:
    ax[c,1].set_title(i, pad =0, fontsize=10)
    print(i)
    #Iterate trough subjects for plotting
    for j in pd_models_plot_db['Subject_ID'].unique(): 
        
        yso = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['YSO']
        eol = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['EoL'].unique()[0]
        fitted = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j][i]
        
        if eol == 'Early':    
            ax[c,1].plot(yso, fitted, color = 'midnightblue', alpha =0.5)
        
        elif eol == 'Late':    
            ax[c,1].plot(yso, fitted, color = 'firebrick', alpha =0.5)
    
    if c == 4:
        ax[c,1].set_xlabel('Years Since Onset')
    else:
        ax[c,1].set_xticks([])
    c+=1
c=0 #Counter 
#Iterate only through models with significative variables
for i in pd_model_sig_results_df['modelo'].values[10:15]:
    ax[c,2].set_title(i, pad =0, fontsize=10)
    print(i)
    #Iterate trough subjects for plotting
    for j in pd_models_plot_db['Subject_ID'].unique(): 
        
        yso = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['YSO']
        eol = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j]['EoL'].unique()[0]
        fitted = pd_models_plot_db[pd_models_plot_db['Subject_ID']==j][i]
        
        if eol == 'Early':    
            ax[c,2].plot(yso, fitted, color = 'midnightblue', alpha =0.5)
        
        elif eol == 'Late':    
            ax[c,2].plot(yso, fitted, color = 'firebrick', alpha =0.5)
    
    if c == 4:
        ax[c,2].set_xlabel('Years Since Onset')
    else:
        ax[c,2].set_xticks([])
    c+=1
plt.tight_layout()


ax[0].set(ylabel='Parkinsons\n\n MoCA Score')
ax[0].set(xlabel='Age at Test')
ax[1].set(xlabel='Age at Test')

# ax[0].set_ylim([16,30])
# ax[1].set_ylim([16,30])
# ax[0].set_ylim([16,30])
# ax[1].set_ylim([16,30])


#%%----------------------Non Lateralized Early/Late Model----------------------

eol_results = []


for i in structures_total:
    
    formula = i + " ~ Group + MoCA_Scores + Age_at_Test + Sex + Years_of_education + EoL"
    print(formula)
    
    lm = smf.mixedlm(formula, merge_db_scaled, groups=merge_db_scaled["Subject_ID"], re_formula='~Age_at_Test')
    eol_lm = lm.fit()
    
    print('Longitudinal + Grouped PD '+i+' Model')
   
    pvals = eol_lm.pvalues 
    params = eol_lm.params

    eol_results.append({
        'modelo': i,
        'formula': eol_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'MoCA_Scores': params['MoCA_Scores'],
        'MoCA_Scores pvalue': pvals['MoCA_Scores'],
        'Age_at_Test': params['Age_at_Test'],
        'Age_at_Test pvalue': pvals['Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Group':params['Group[T.PD]'],
        'Group pvalue':pvals['Group[T.PD]'],
        'EoL': params['EoL[T.Late]'],
        'EoL pvalue': pvals['EoL[T.Late]']
        
    })
    
    #print(pd_lm.summary())
    
eol_model_results_df = pd.DataFrame(eol_results)
eol_model_results_df = eol_model_results_df.dropna()

#Pvalue FDR Correction 

# pvals_index= ['Sex[T.M] pvalue','MoCA_Scores pvalue','Age_at_Test pvalue', 'Years_of_education pvalue',
#               'Onset_Age pvalue','EoL pvalue','YSO pvalue' ]

pvals_index= ['Sex[T.M] pvalue','MoCA_Scores pvalue','Age_at_Test pvalue', 'Years_of_education pvalue',
              'EoL pvalue','Group pvalue']


for i in pvals_index:
    tmp_pvals = eol_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    eol_model_results_df[new_index]= tmp_pvals_fdr
    
#%%----------------------Preliminary Plot -------------------------------------
ticks = list(eol_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Early/Late PD+Ctrl Models by structure', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(eol_model_results_df['modelo'], eol_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Group Scores FDR Corrected")
ax[1,0].scatter(eol_model_results_df['modelo'], eol_model_results_df['Group pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[2,0].set_title("Age At Test FDR Corrected")
ax[2,0].scatter(eol_model_results_df['modelo'], eol_model_results_df['Age_at_Test pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(eol_model_results_df['modelo'], eol_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

# ax[1,1].set_title("Onset Age FDR Corrected")
# ax[1,1].scatter(pd_model_results_df['modelo'], pd_model_results_df['Onset_Age pvalue FDR'], mouseover=True)
# ax[1,1].axhline(0.05, color ='red')
# ax[1,1].set_xticks([])

ax[1,1].set_title("Early/Late [T.Late] FDR Corrected")
ax[1,1].scatter(eol_model_results_df['modelo'], eol_model_results_df['EoL pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks([])

ax[2,1].set_title("Years Since Onset FDR Corrected")
ax[2,1].scatter(eol_model_results_df['modelo'], eol_model_results_df['YSO pvalue FDR'], mouseover=True)
ax[2,1].axhline(0.05, color ='red')
ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)


#%%----------------------Obtain Delta MoCA / Delta HY / Delta Ages------------- <CURRENT

#-----------To Obtain Delta MoCA vs Delta Volume PD
delta_structures_LR = ['Delta_'+i+'_y' for i in structures_LR]

c=0 #Counter 
for i in pd_l_db['Subject_ID'].unique(): #Iterate through subject IDs

    #Obtain delta Ages
    d_age_moca = (pd_l_db[pd_l_db['Subject_ID']==i]['Age_at_Test_1'].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i]['Age_at_Test_1'].values[0])
    d_age_hy = (pd_l_db[pd_l_db['Subject_ID']==i]['Age_at_Test'].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i]['Age_at_Test'].values[0])
    d_age_vol = (pd_l_db[pd_l_db['Subject_ID']==i]['Age'].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i]['Age'].values[0])
    #Avg delta age 
    d_age= (d_age_moca + d_age_hy + d_age_vol)/3
    #Obtain Delta scores
    d_moca = (pd_l_db[pd_l_db['Subject_ID']==i]['MoCA_Scores'].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i]['MoCA_Scores'].values[0])
    d_hy = (pd_l_db[pd_l_db['Subject_ID']==i]['HY_Scores'].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i]['HY_Scores'].values[0])
    #Control by years
    d_std_moca = d_moca/d_age_moca
    d_std_hy = d_hy/d_age_hy
    #Create Dictionary 
    tmp_dict = {'Subject_ID':i,
                'Group':pd_l_db[pd_l_db['Subject_ID']==i]['Group'].values[0],
                'Sex':pd_l_db[pd_l_db['Subject_ID']==i]['Sex'].values[0],
                'EoL':pd_l_db[pd_l_db['Subject_ID']==i]['EoL'].values[0],
                'YSO':pd_l_db[pd_l_db['Subject_ID']==i]['YSO'].values[0],
                'Years_of_education':pd_l_db[pd_l_db['Subject_ID']==i]['Years_of_education'].values[0],
                'Delta_Age_at_Test':d_age,
                'Delta_MoCA':d_moca,
                'Delta_MoCA_y':d_std_moca,
                'Delta_HY':d_hy,
                'Delta_HY_y':d_std_hy
                }
    
    #Obtain Delta Volume per structure 
    for j in structures_LR:
        
        #Obtain Delta Volume
        d_vol = (pd_l_db[pd_l_db['Subject_ID']==i][j].values[-1])-(pd_l_db[pd_l_db['Subject_ID']==i][j].values[0])
        #Control by years
        d_std_vol = d_vol/d_age_vol
        #Add delta volumes to dictionary
        tmp_dict['Delta_'+j]=[0]+d_vol
        tmp_dict['Delta_'+j+'_y']=[0]+d_std_vol
 
    #Create dataframe 
    if not c: #If First iteration 
        pd_delta_df = pd.DataFrame.from_dict(tmp_dict)
        c=1
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        pd_delta_df = pd.concat([pd_delta_df,tmp])

pd_delta_df.reset_index(inplace=True, drop=True)


#-----------To Obtain Delta MoCA vs Delta Volume Ctrl

c=0 #Counter 
for i in ctrl_l_db['Subject_ID'].unique(): #Iterate through subject IDs

    #Obtain delta Ages
    d_age_moca = (ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age_at_Test_1'].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age_at_Test_1'].values[0])
    d_age_hy = (ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age_at_Test'].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age_at_Test'].values[0])
    d_age_vol = (ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age'].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Age'].values[0])
    #Avg delta age 
    d_age= (d_age_moca + d_age_hy + d_age_vol)/3
    #Obtain Delta scores
    d_moca = (ctrl_l_db[ctrl_l_db['Subject_ID']==i]['MoCA_Scores'].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i]['MoCA_Scores'].values[0])
    d_hy = (ctrl_l_db[ctrl_l_db['Subject_ID']==i]['HY_Scores'].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i]['HY_Scores'].values[0])
    #Control by years
    d_std_moca = d_moca/d_age_moca
    d_std_hy = d_hy/d_age_hy
    #Create Dictionary 
    tmp_dict = {'Subject_ID':i,
                'Group':ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Group'].values[0],
                'Sex':ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Sex'].values[0],
                'EoL':ctrl_l_db[ctrl_l_db['Subject_ID']==i]['EoL'].values[0],
                'Years_of_education':ctrl_l_db[ctrl_l_db['Subject_ID']==i]['Years_of_education'].values[0],
                'Delta_Age_at_Test':d_age,
                'Delta_MoCA':d_moca,
                'Delta_MoCA_y':d_std_moca,
                'Delta_HY':d_hy,
                'Delta_HY_y':d_std_hy
                }
    
    #Obtain Delta Volume per structure 
    for j in structures_LR:
        
        #Obtain Delta Volume
        d_vol = (ctrl_l_db[ctrl_l_db['Subject_ID']==i][j].values[-1])-(ctrl_l_db[ctrl_l_db['Subject_ID']==i][j].values[0])
        #Control by years
        d_std_vol = d_vol/d_age
        #Add delta volumes to dictionary
        tmp_dict['Delta_'+j]=[0]+d_vol
        tmp_dict['Delta_'+j+'_y']=[0]+d_std_vol
        
    #Create dataframe 
    if not c: #If First iteration 
        ctrl_delta_df = pd.DataFrame.from_dict(tmp_dict)
        c=1
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        ctrl_delta_df = pd.concat([ctrl_delta_df,tmp])

ctrl_delta_df.reset_index(inplace=True, drop=True)


#%%----------------------Outlier check-----------------------------------------
# print('Normality Test Delta MoCA PD')
# print(stats.shapiro(pd_delta_df['Delta_MoCA_y']))

# print('Normality Test Delta MoCA Ctrl')
# print(stats.shapiro(ctrl_delta_df['Delta_MoCA_y']))


# #----------------MoCA Outliers (IQR Method)

# # Calculate quartiles
# Q1 = pd_delta_df['Delta_MoCA_y'].quantile(0.25)
# Q3 = pd_delta_df['Delta_MoCA_y'].quantile(0.75)
# IQR = Q3 - Q1
# # Calculate bounds
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# # Detect outliers
# pd_delta_df['Outlier_MoCA'] = (pd_delta_df['Delta_MoCA_y'] < lower_bound) | (pd_delta_df['Delta_MoCA_y'] > upper_bound)
# pd_moca_outliers = pd_delta_df[pd_delta_df['Outlier_MoCA']==True]

# # Calculate quartiles
# Q1 = ctrl_delta_df['Delta_MoCA_y'].quantile(0.25)
# Q3 = ctrl_delta_df['Delta_MoCA_y'].quantile(0.75)
# IQR = Q3 - Q1
# # Calculate bounds
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# # Detect outliers
# ctrl_delta_df['Outlier_MoCA'] = (ctrl_delta_df['Delta_MoCA_y'] < lower_bound) | (ctrl_delta_df['Delta_MoCA_y'] > upper_bound)
# ctrl_moca_outliers = ctrl_delta_df[ctrl_delta_df['Outlier_MoCA']==True]


#MoCA Outliers 
tmp_delta_df = pd.concat([pd_delta_df, ctrl_delta_df])
tmp_delta_df.reset_index(inplace=True, drop=True)
tmp_delta_df['Zscore_MoCA']=stats.zscore(tmp_delta_df['Delta_MoCA_y'])
tmp_delta_df['Outlier_MoCA'] = (tmp_delta_df['Zscore_MoCA'] < -3) | (tmp_delta_df['Zscore_MoCA'] > 3)
moca_outliers = tmp_delta_df[tmp_delta_df['Outlier_MoCA']==True]


#HY Outliers
tmp_delta_df['Zscore_HY']=stats.zscore(tmp_delta_df['Delta_HY_y'])
tmp_delta_df['Outlier_HY'] = (tmp_delta_df['Zscore_HY'] < -3) | (tmp_delta_df['Zscore_HY'] > 3)
hy_outliers = tmp_delta_df[tmp_delta_df['Outlier_HY']==True]

##
# print('Normality Test Delta MoCA')
# print(stats.shapiro(tmp_delta_moca['Delta_MoCA_y'])[1])

# # Calculate quartiles
# Q1 = tmp_delta_moca['Delta_MoCA_y'].quantile(0.25)
# Q3 = tmp_delta_moca['Delta_MoCA_y'].quantile(0.75)
# IQR = Q3 - Q1
# # Calculate bounds
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# # Detect outliers
# tmp_delta_moca['Outlier_MoCA'] = (tmp_delta_moca['Delta_MoCA_y'] < lower_bound) | (tmp_delta_moca['Delta_MoCA_y'] > upper_bound)
# moca_outliers = tmp_delta_moca[tmp_delta_moca['Outlier_MoCA']==True]


# #----------------HY Outliers (IQR Method)
# print('Normality Test Delta HY PD')
# print(stats.shapiro(pd_delta_df['Delta_HY_y']))

# print('Normality Test Delta HY Ctrl')
# print(stats.shapiro(ctrl_delta_df['Delta_HY_y']))

# # Calculate quartiles
# Q1 = pd_delta_df['Delta_HY_y'].quantile(0.25)
# Q3 = pd_delta_df['Delta_HY_y'].quantile(0.75)
# IQR = Q3 - Q1
# # Calculate bounds
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# # Detect outliers
# pd_delta_df['Outlier_HY'] = (pd_delta_df['Delta_HY_y'] < lower_bound) | (pd_delta_df['Delta_HY_y'] > upper_bound)
# pd_hy_outliers = pd_delta_df[pd_delta_df['Outlier_HY']==True]

# # Calculate quartiles
# Q1 = ctrl_delta_df['Delta_HY_y'].quantile(0.25)
# Q3 = ctrl_delta_df['Delta_HY_y'].quantile(0.75)
# IQR = Q3 - Q1
# # Calculate bounds
# lower_bound = Q1 - 1.5 * IQR
# upper_bound = Q3 + 1.5 * IQR
# # Detect outliers
# ctrl_delta_df['Outlier_HY'] = (ctrl_delta_df['Delta_HY_y'] < lower_bound) | (ctrl_delta_df['Delta_HY_y'] > upper_bound)
# ctrl_hy_outliers = ctrl_delta_df[ctrl_delta_df['Outlier_HY']==True]

#%%----------------------PD Delta Volume Model Implementation------------------
pd_delta_results = []
pd_delta_models_plot_db = pd.DataFrame()
pd_delta_models_plot_db['Subject_ID']= pd_delta_df['Subject_ID']
pd_delta_models_plot_db['EoL']= pd_delta_df['EoL']
pd_delta_df['EoL'] = pd_delta_df['EoL'].map({'Early':0, 'Late':1})

for i in delta_structures_LR:
    
    formula = i + " ~ Delta_MoCA_y + Delta_HY_y + Delta_Age_at_Test + Sex + Years_of_education + YSO + EoL"
    print(formula)
    
    lm = smf.ols(formula, pd_delta_df)
    pd_lm = lm.fit()
    
   
    pvals = pd_lm.pvalues 
    params = pd_lm.params
    zvals = pd_lm.tvalues

    pd_delta_results.append({
        'modelo': i,
        'formula': pd_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'EoL': params['EoL'],
        'EoL z': zvals['EoL'],
        'EoL pvalue': pvals['EoL'],
        'Delta_MoCA': params['Delta_MoCA_y'],
        'Delta_MoCA z': zvals['Delta_MoCA_y'],
        'Delta_MoCA pvalue': pvals['Delta_MoCA_y'],
        'Delta_Age_at_Test': params['Delta_Age_at_Test'],
        'Delta_Age_at_Test z': zvals['Delta_Age_at_Test'],
        'Delta_Age_at_Test pvalue': pvals['Delta_Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Delta_HY': params['Delta_HY_y'],
        'Delta_HY z': zvals['Delta_HY_y'],
        'Delta_HY pvalue': pvals['Delta_HY_y']
        
    })
    
    # if pd_lm.converged:
    pd_delta_models_plot_db[i]=pd_lm.fittedvalues
        
    
    print(pd_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(pd_lm.fittedvalues)), pd_lm.resid)
        
pd_delta_model_results_df = pd.DataFrame(pd_delta_results)
pd_delta_model_results_df = pd_delta_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Delta_MoCA pvalue','Years_of_education pvalue','Delta_HY pvalue', 
              'Delta_Age_at_Test pvalue','EoL pvalue' ]


for i in pvals_index:
    print(i)
    tmp_pvals = pd_delta_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    pd_delta_model_results_df[new_index]= tmp_pvals_fdr


pd_delta_sig_models = pd_delta_model_results_df[pd_delta_model_results_df['Delta_MoCA pvalue FDR']<0.05]


#%%----------------------Preliminary pvalues Plot------------------------------

ticks = list(pd_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD Delta Models by structure L+R ( Scaled)', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Delta MoCA FDR Corrected")
ax[1,0].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['Delta_MoCA pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[2,0].set_title("Age At Test FDR Corrected")
ax[2,0].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['Delta_Age_at_Test pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

ax[1,1].set_title("Delta HY  FDR Corrected")
ax[1,1].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['Delta_HY pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks([])

ax[2,1].set_title("Early/Late [T.Late] FDR Corrected")
ax[2,1].scatter(pd_delta_model_results_df['modelo'], pd_delta_model_results_df['EoL pvalue FDR'], mouseover=True)
ax[2,1].axhline(0.05, color ='red')
ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()

#%%----------------------Significative MoCA models Chisquared variable test----

# test_vars = ['Years_of_education', 'Sex', 'Subcortical_GM_volume_PR', 'White_Matter_WM_volume_PR',
#              'Grey_Matter_GM_volume_PR', 'Cortical_GM_volume_PR', 'Cerebellar_GM_volume_PR', 'Accumbens_total_volume_PR',
#              'Amygdala_total_volume_PR', 'Basal_forebrain_total_volume_PR','Caudate_total_volume_PR', 'Hippocampus_total_volume_PR',
#              'Pallidum_total_volume_PR','Putamen_total_volume_PR', 'Thalamus_total_volume_PR', 'Ventral_DC_total_volume_PR',
#              'Frontal_lobe_total_volume_PR','Parietal_lobe_total_volume_PR','Temporal_lobe_total_volume_PR',
#              'Occipital_lobe_total_volume_PR', 'Limbic_cortex_total_volume_PR','Insular_cortex_total_volume_PR']

# test_results = []

# #----Base Model
# base_lm_pd = sm.MixedLM.from_formula(
#     formula="MoCA_Scores ~ Age_at_Test",
#     groups = "Subject_ID",
#     re_formula = "~Age_at_Test",
#     data = pd_db_scaled).fit(reml=False)

# print('PD Base Model')
# print(base_lm_pd.summary())

# test_results.append({
#     'modelo': 'base (Age)',
#     'formula': base_lm_pd.model.formula,
#     'loglik': base_lm_pd.llf,
#     'aic': base_lm_pd.aic,
#     'bic': base_lm_pd.bic,
#     'n_params': len(base_lm_pd.params)
# })


# current_model = base_lm_pd

# for i,j in enumerate(test_vars):
    
#     #For first predictor
#     if i == 0:
#         new_formula = f"MoCA_Scores ~ Age_at_Test + {j} "

#     else: #Concat next predictors
#         new_formula = test_results[-1]['formula']+ f" + {j} "

#     #Adjust new model 
#     try:
#         new_model = sm.MixedLM.from_formula(
#             formula = new_formula,
#             groups= 'Subject_ID',
#             re_formula='~Age_at_Test',
#             data = pd_db_scaled).fit(reml=False, maxiter=1000, method='bfgs')
        
#         #Obtain LRT
#         lrt_stat = -2*(test_results[-1]['loglik'] - new_model.llf)
#         df_diff = len(new_model.params) - test_results[-1]['n_params']
#         pval = chi2.sf(lrt_stat,df_diff)
        
#         #Save Results 
#         test_results.append({
#             'modelo': f"base + {' + '.join(test_vars[:i+1])}",
#             'formula' : new_formula,
#             'loglik' : new_model.llf,
#             'aic': new_model.aic,
#             'bic': new_model.bic,
#             'n_params': len(new_model.params),
#             'lrt_vs_prev' : lrt_stat,
#             'df_diff' : df_diff,
#             'p_value' : pval})
        
#         #Model update 
#         current_model = new_model
        
#     except Exception as e:
#         print(f"Cannot adjust model with {j}:{e}")
#         break
    
# chisq_pd_results = pd.DataFrame(test_results)
# print(chisq_pd_results)



#%%----------------------Delta MoCA PD+Ctrl Model implementation------------- <CURRENT

#MoCA Outlier Removal
#full_delta_df = tmp_delta_df[tmp_delta_df['Outlier_MoCA']==False]

full_delta_df = pd.concat([pd_delta_df, ctrl_delta_df])

full_delta_results = []
full_delta_models_plot_db = pd.DataFrame()
full_delta_models_plot_db['Subject_ID']= full_delta_df['Subject_ID']
full_delta_models_plot_db['Group']= full_delta_df['Group']
full_delta_df['Group'] = full_delta_df['Group'].map({'Control':0, 'PD':1})
full_delta_df.fillna(0, inplace=True)

for i in delta_structures_LR:
    
    formula = "Delta_MoCA_y ~ "+ i + " + Group + Delta_Age_at_Test + Sex + Years_of_education + Group*"+i
    print(formula)
    
    lm = smf.ols(formula, full_delta_df)
    full_lm = lm.fit()
    
   
    pvals = full_lm.pvalues 
    params = full_lm.params
    zvals = full_lm.tvalues

    full_delta_results.append({
        'modelo': i,
        'formula': full_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Delta_Volume': params[i],
        'Delta_Volume z': zvals[i],
        'Delta_Volume pvalue': pvals[i],
        # 'Delta_HY': params['Delta_HY_y'],
        # 'Delta_HY z': zvals['Delta_HY_y'],
        # 'Delta_HY pvalue': pvals['Delta_HY_y'],
        'Group': params['Group'],
        'Group z': zvals['Group'],
        'Group pvalue': pvals['Group'],
        'Delta_Age_at_Test': params['Delta_Age_at_Test'],
        'Delta_Age_at_Test z': zvals['Delta_Age_at_Test'],
        'Delta_Age_at_Test pvalue': pvals['Delta_Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Group*Delta_Volume_y': params['Group:'+i],
        'Group*Delta_Volume_y z': zvals['Group:'+i],
        'Group*Delta_Volume_y pvalue': pvals['Group:'+i],
        })
    
    # if full_lm.converged:
    full_delta_models_plot_db[i]=full_lm.fittedvalues
        
    
    print(full_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(full_lm.fittedvalues)), full_lm.resid)
        
full_delta_model_results_df = pd.DataFrame(full_delta_results)
full_delta_model_results_df = full_delta_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Delta_Volume pvalue','Years_of_education pvalue', #'Delta_HY pvalue', 
              'Delta_Age_at_Test pvalue','Group pvalue','Group*Delta_Volume_y pvalue' ]


for i in pvals_index:
    print(i)
    tmp_pvals = full_delta_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    full_delta_model_results_df[new_index]= tmp_pvals_fdr


full_delta_sig_models = full_delta_model_results_df[full_delta_model_results_df['Group*Delta_Volume_y pvalue FDR']<0.05]
full_delta_sig_models.reset_index(inplace=True, drop = True)

#%%----------------------Preliminary pvalues Plot MoCA-------------------------

ticks = list(full_delta_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD/Ctrl Delta Models by structure L+R + Interaction', fontsize=16)
ax[0,0].set_title("Sex [M] ")
ax[0,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Delta Volume pvalue")
ax[1,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Delta_Volume pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

ax[1,1].set_title("Group*Delta_Volume_y pvalue ")
ax[1,1].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Group*Delta_Volume_y pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks([])

ax[0,1].set_title("Years of Education")
ax[0,1].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

ax[2,0].set_title("Group FDR Corrected")
ax[2,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Group pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)
plt.tight_layout()
#%%----------------------Sig Models Delta Vol / Delta MoCA scatter plots-------


plt.figure()
plt.suptitle(r'$\Delta$ MoCA vs $\Delta$ % Volume ', fontsize=16)
plt.subplot(221)
ax = sb.regplot(pd_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][0], color ='Steelblue', label='Parkinsons')
ax = sb.regplot(ctrl_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][0], color='green', label='Controls')
plt.xlabel(r'$\Delta$ Volume / Years')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.title(full_delta_sig_models['modelo'][0], loc='right', fontsize=10, pad=0)
plt.legend()

plt.subplot(222)
ax = sb.regplot(pd_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][1], color ='Steelblue')
ax = sb.regplot(ctrl_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][1], color='green')
plt.title(full_delta_sig_models['modelo'][1], loc='right', fontsize=10, pad=0)
plt.xlabel(r'$\Delta$ % Volume / Years')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.legend()

plt.subplot(223)
ax = sb.regplot(pd_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][2], color ='Steelblue', label='Parkinsons')
ax = sb.regplot(ctrl_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][2], color='green', label='Controls')
plt.xlabel(r'$\Delta$ Volume / Years')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.title(full_delta_sig_models['modelo'][2], loc='right', fontsize=10, pad=0)
plt.legend()

plt.subplot(224)
ax = sb.regplot(pd_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][3], color ='Steelblue')
ax = sb.regplot(ctrl_delta_df,y='Delta_MoCA_y', x=full_delta_sig_models['modelo'][3], color='green')
plt.title(full_delta_sig_models['modelo'][3], loc='right', fontsize=10, pad=0)
plt.xlabel(r'$\Delta$ % Volume / Years')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.legend()

# plt.subplot(323)
# ax = sb.regplot(pd_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][2], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][2], color='green')
# plt.title(full_delta_sig_models['modelo'][2], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ HY / Years')
# plt.legend()

# plt.subplot(324)
# ax = sb.regplot(pd_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][3], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][3], color='green')
# plt.title(full_delta_sig_models['modelo'][3], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ HY / Years')
# plt.legend()
# plt.tight_layout()

# plt.subplot(325)
# ax = sb.regplot(pd_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][4], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][4], color='green')
# plt.title(full_delta_sig_models['modelo'][4], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ HY / Years')
# plt.legend()
# plt.tight_layout()

# plt.subplot(326)
# ax = sb.regplot(pd_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][5], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_HY_y', y=full_delta_sig_models['modelo'][5], color='green')
# plt.title(full_delta_sig_models['modelo'][5], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ HY / Years')
# plt.legend()
# plt.tight_layout()

# #----------------
# plt.figure()
# plt.suptitle(r'$\Delta$ Volume vs $\Delta$ % MoCA ', fontsize=16)
# plt.subplot(221)
# ax = sb.regplot(pd_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][6], color ='Steelblue', label='Parkinsons')
# ax = sb.regplot(ctrl_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][6], color='green', label='Controls')
# plt.xlabel(r'$\Delta$ Volume / Years')
# plt.ylabel(r'$\Delta$ MoCA / Years')
# plt.title(full_delta_sig_models['modelo'][6], loc='right', fontsize=10, pad=0)
# plt.legend()

# plt.subplot(222)
# ax = sb.regplot(pd_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][7], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][7], color='green')
# plt.title(full_delta_sig_models['modelo'][7], loc='right', fontsize=10, pad=0)
# plt.xlabel(r'$\Delta$ % Volume / Years')
# plt.ylabel(r'$\Delta$ MoCA / Years')
# plt.legend()

# plt.subplot(223)
# ax = sb.regplot(pd_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][8], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][8], color='green')
# plt.title(full_delta_sig_models['modelo'][8], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ MoCA / Years')
# plt.legend()

# plt.subplot(224)
# ax = sb.regplot(pd_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][9], color ='Steelblue')
# ax = sb.regplot(ctrl_delta_df,x='Delta_MoCA_y', y=full_delta_sig_models['modelo'][9], color='green')
# plt.title(full_delta_sig_models['modelo'][9], loc='right', fontsize=10, pad=0)
# plt.ylabel(r'$\Delta$ % Volume / Years')
# plt.xlabel(r'$\Delta$ MoCA / Years')
# plt.legend()
# plt.tight_layout()

#%%----------------------Delta HY PD+Ctrl Model implementation------------- <CURRENT

full_delta_df = pd.concat([pd_delta_df, ctrl_delta_df])
full_delta_results = []
full_delta_models_plot_db = pd.DataFrame()
full_delta_models_plot_db['Subject_ID']= full_delta_df['Subject_ID']
full_delta_models_plot_db['Group']= full_delta_df['Group']
full_delta_df['Group'] = full_delta_df['Group'].map({'Control':0, 'PD':1})
full_delta_df.fillna(0, inplace=True)

for i in delta_structures_LR:
    
    formula = "Delta_MoCA_y ~ "+ i + " + Group + Delta_Age_at_Test + Sex + Years_of_education + Group*"+i
    print(formula)
    
    lm = smf.ols(formula, full_delta_df)
    full_lm = lm.fit()
    
   
    pvals = full_lm.pvalues 
    params = full_lm.params
    zvals = full_lm.tvalues

    full_delta_results.append({
        'modelo': i,
        'formula': full_lm.model.formula,
        'Intercept': params['Intercept'],
        'Intercept z': zvals['Intercept'],
        'Intercept pvalue': pvals['Intercept'],
        'Delta_Volume': params[i],
        'Delta_Volume z': zvals[i],
        'Delta_Volume pvalue': pvals[i],
        # 'Delta_HY': params['Delta_HY_y'],
        # 'Delta_HY z': zvals['Delta_HY_y'],
        # 'Delta_HY pvalue': pvals['Delta_HY_y'],
        'Group': params['Group'],
        'Group z': zvals['Group'],
        'Group pvalue': pvals['Group'],
        'Delta_Age_at_Test': params['Delta_Age_at_Test'],
        'Delta_Age_at_Test z': zvals['Delta_Age_at_Test'],
        'Delta_Age_at_Test pvalue': pvals['Delta_Age_at_Test'],
        'Years_of_education': params['Years_of_education'],
        'Years_of_education z': zvals['Years_of_education'],
        'Years_of_education pvalue': pvals['Years_of_education'],
        'Sex[T.M]':params['Sex[T.M]'],
        'Sex[T.M] z':zvals['Sex[T.M]'],
        'Sex[T.M] pvalue':pvals['Sex[T.M]'],
        'Group*Delta_Volume_y': params['Group:'+i],
        'Group*Delta_Volume_y z': zvals['Group:'+i],
        'Group*Delta_Volume_y pvalue': pvals['Group:'+i],
        })
    
    # if full_lm.converged:
    full_delta_models_plot_db[i]=full_lm.fittedvalues
        
    
    print(full_lm.summary())
    # plt.figure()
    # plt.scatter(range(len(full_lm.fittedvalues)), full_lm.resid)
        
full_delta_model_results_df = pd.DataFrame(full_delta_results)
full_delta_model_results_df = full_delta_model_results_df.dropna()



#Pvalue FDR Correction 

pvals_index= ['Sex[T.M] pvalue','Delta_Volume pvalue','Years_of_education pvalue', #'Delta_HY pvalue', 
              'Delta_Age_at_Test pvalue','Group pvalue','Group*Delta_Volume_y pvalue' ]


for i in pvals_index:
    print(i)
    tmp_pvals = full_delta_model_results_df[i]
    tmp_pvals_fdr = FDR(tmp_pvals)
    new_index = i + ' FDR'
    full_delta_model_results_df[new_index]= tmp_pvals_fdr


full_delta_sig_models = full_delta_model_results_df[full_delta_model_results_df['Group*Delta_Volume_y pvalue FDR']<0.05]
full_delta_sig_models.reset_index(inplace=True, drop = True)
#%%----------------------Preliminary pvalues Plot HY---------------------------

ticks = list(full_delta_model_results_df['modelo'])
ticks = [x.replace('_volume_PR','') for x in ticks]

fig, ax = plt.subplots(3,2)
fig.set_figheight(10)
fig.set_figwidth(15)
plt.suptitle('Variable P-values - PD/Ctrl Delta Models by structure L+R + Interaction', fontsize=16)
ax[0,0].set_title("Sex [M] FDR Corrected")
ax[0,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Sex[T.M] pvalue FDR'], mouseover=True)
ax[0,0].axhline(0.05, color ='red')
ax[0,0].set_xticks([])

ax[1,0].set_title("Delta MoCA FDR Corrected")
ax[1,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Delta_MoCA pvalue FDR'], mouseover=True)
ax[1,0].axhline(0.05, color ='red')
ax[1,0].set_xticks([])

# ax[2,0].set_title("Age At Test FDR Corrected")
# ax[2,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Delta_Age_at_Test pvalue FDR'], mouseover=True)
# ax[2,0].axhline(0.05, color ='red')
# ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[2,0].set_title("Group*Delta_HY_y pvalue FDR Corrected")
ax[2,0].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Group*Delta_MoCA_y pvalue FDR'], mouseover=True)
ax[2,0].axhline(0.05, color ='red')
ax[2,0].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

ax[0,1].set_title("Years of Education FDR Corrected")
ax[0,1].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Years_of_education pvalue FDR'], mouseover=True)
ax[0,1].axhline(0.05, color ='red')
ax[0,1].set_xticks([])

ax[1,1].set_title("Delta HY  FDR Corrected")
ax[1,1].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Delta_HY pvalue FDR'], mouseover=True)
ax[1,1].axhline(0.05, color ='red')
ax[1,1].set_xticks([])

ax[2,1].set_title("Group FDR Corrected")
ax[2,1].scatter(full_delta_model_results_df['modelo'], full_delta_model_results_df['Group pvalue FDR'], mouseover=True)
ax[2,1].axhline(0.05, color ='red')
ax[2,1].set_xticks(range(len(ticks)),labels=ticks, rotation=90)

plt.tight_layout()




#%%----------------------Pearson R Correlation L & R---------------------------


#-------------------PD
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(pd_delta_df['Delta_MoCA_y'],pd_delta_df[i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        pd_r_corr_df = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        pd_r_corr_df = pd.concat([pd_r_corr_df,tmp])
        
pd_r_corr_df = pd_r_corr_df.dropna()
pd_r_corr_df.reset_index(inplace=True, drop=True)

#Correct by FDR
pd_r_corr_df['FDR_Pvalue'] = FDR(pd_r_corr_df['Pvalue'])

#-----------------------Ctrl
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(ctrl_delta_df['Delta_MoCA_y'],ctrl_delta_df[i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        ctrl_r_corr_df = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        ctrl_r_corr_df = pd.concat([ctrl_r_corr_df,tmp])
        
ctrl_r_corr_df = ctrl_r_corr_df.dropna()
ctrl_r_corr_df.reset_index(inplace=True, drop=True)

#Correct by FDR
ctrl_r_corr_df['FDR_Pvalue'] = FDR(ctrl_r_corr_df['Pvalue'])


#------P Value plot 

plt.suptitle('Pearsons R $\Delta$MoCA / $\Delta$Volume P-Values L + R FDR corrected', fontsize=16)
plt.subplot(211)
plt.title('Controls', loc='right', pad=0, fontsize=10)
plt.scatter(np.arange(0,len(ctrl_r_corr_df['FDR_Pvalue']),1),ctrl_r_corr_df['FDR_Pvalue'], color='Green', label='Controls')
plt.axhline(0.05,0,len(ctrl_r_corr_df['FDR_Pvalue']), color='r')
plt.ylabel('p-value')

plt.subplot(212)
plt.title('Parkinsons', loc='right', pad=0, fontsize=10)
plt.scatter(np.arange(0,len(pd_r_corr_df['FDR_Pvalue']),1),pd_r_corr_df['FDR_Pvalue'], color='Steelblue', label='Parkinsons')
plt.axhline(0.05,0,len(pd_r_corr_df['FDR_Pvalue']), color='r')
plt.ylabel('p-value')
plt.xticks(range(len(pd_r_corr_df['Structure'])),labels=[x.replace('Delta_','') for x in pd_r_corr_df['Structure']], rotation=-90, fontsize=8)
plt.tight_layout()

#%%----------------------Plot Longitudinals Delta V vs Delta M Sig [Scatter]---


plt.figure()
plt.suptitle(r'$\Delta$ MoCA vs $\Delta$ % Volume ', fontsize=16)
plt.subplot(211)
ax = sb.regplot(pd_delta_df,x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue', label = 'Parkinsons R=%.4f'%pd_r_corr_df[pd_r_corr_df['Structure']=='Delta_Insular_cortex_left_volume_PR_y']['R']+' p=%.4f'%pd_r_corr_df[pd_r_corr_df['Structure']=='Delta_Insular_cortex_left_volume_PR_y']['FDR_Pvalue'])
ax = sb.regplot(ctrl_delta_df,x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color='green', label = 'Controls R=%.4f'%ctrl_r_corr_df[ctrl_r_corr_df['Structure']=='Delta_Insular_cortex_left_volume_PR_y']['R']+' p=%.4f'%ctrl_r_corr_df[ctrl_r_corr_df['Structure']=='Delta_Insular_cortex_left_volume_PR_y']['FDR_Pvalue'])
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.xlabel('')
plt.title('Insular cortex_left ', loc='right', fontsize=10, pad=0)
plt.legend()

plt.subplot(212)
ax = sb.regplot(pd_delta_df,x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue', label = 'Parkinsons R=%.4f'%pd_r_corr_df[pd_r_corr_df['Structure']=='Delta_Posterior_cingulate_gyrus_left_volume_PR_y']['R']+' p=%.4f'%pd_r_corr_df[pd_r_corr_df['Structure']=='Delta_Posterior_cingulate_gyrus_left_volume_PR_y']['FDR_Pvalue'])
ax = sb.regplot(ctrl_delta_df,x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color='green', label = 'Controls R=%.4f'%ctrl_r_corr_df[ctrl_r_corr_df['Structure']=='Delta_Posterior_cingulate_gyrus_left_volume_PR_y']['R']+' p=%.4f'%ctrl_r_corr_df[ctrl_r_corr_df['Structure']=='Delta_Posterior_cingulate_gyrus_left_volume_PR_y']['FDR_Pvalue'])
plt.title('Posterior cingulate gyrus_left ', loc='right', fontsize=10, pad=0)
plt.xlabel(r'$\Delta$ % Volume / Years')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.legend()
plt.tight_layout()

#-------------------------

plt.figure()
plt.suptitle(r'$\Delta$ MoCA vs $\Delta$ % Volume ', fontsize=16)
plt.subplot(221)
ax = sb.regplot(pd_delta_df[pd_delta_df['EoL']=='Early'],x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue')
ax = sb.regplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early'],x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color='green')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.xlabel('')
plt.title('Insular cortex_left Early Onset', loc='right', fontsize=10, pad=0)

plt.subplot(222)
ax = sb.regplot(pd_delta_df[pd_delta_df['EoL']=='Early'],x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue')
ax = sb.regplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early'],x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color='green')
plt.title('Posterior cingulate gyrus_left Early Onset', loc='right', fontsize=10, pad=0)
plt.xlabel('')
plt.ylabel('')

plt.subplot(223)
ax = sb.regplot(pd_delta_df[pd_delta_df['EoL']=='Late'],x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue')
ax = sb.regplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late'],x='Delta_Insular_cortex_left_volume_PR_y', y='Delta_MoCA_y', color='green')
plt.ylabel(r'$\Delta$ MoCA / Years')
plt.xlabel(r'$\Delta$% Volume / Years')
plt.title('Insular cortex_left Late Onset', loc='right', fontsize=10, pad=0)

plt.subplot(224)
ax = sb.regplot(pd_delta_df[pd_delta_df['EoL']=='Late'],x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color ='Steelblue')
ax = sb.regplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late'],x='Delta_Posterior_cingulate_gyrus_left_volume_PR_y', y='Delta_MoCA_y', color='green')
plt.xlabel(r'$\Delta$% Volume / Years')
plt.title('Posterior cingulate gyrus_left', loc='right', fontsize=10, pad=0)
plt.ylabel('')
plt.tight_layout()

#---------------------------


#%%----------------------Plot Delta MoCA/years Distributions-------------------

plt.figure()
plt.suptitle('$\Delta$MoCA / years Distribution ', fontsize =16)
plt.subplot(121)
plt.title('$\Delta$MoCA/years Count', loc = 'Right', fontsize=10, pad =0)
sb.histplot(pd_delta_df['Delta_MoCA_y'], color = 'Steelblue', alpha = 0.5)
sb.histplot(ctrl_delta_df['Delta_MoCA_y'], color = 'Green', alpha = 0.5)

plt.subplot(122)
plt.title('$\Delta$MoCA/years Density', loc = 'Right', fontsize=10, pad =0)
sb.kdeplot(pd_delta_df['Delta_MoCA_y'], color = 'Steelblue', label = 'Parkinsons')
sb.kdeplot(ctrl_delta_df['Delta_MoCA_y'], color = 'Green', label = 'Controls')
plt.legend()

#----------------------

plt.figure()
plt.suptitle('$\Delta$MoCA / years Distribution ', fontsize =16)
plt.subplot(221)
plt.title('$\Delta$MoCA/years Count', loc = 'Right', fontsize=10, pad =0)
sb.histplot(pd_delta_df[pd_delta_df['EoL']=='Late']['Delta_MoCA_y'], color = 'Navy')
sb.histplot(pd_delta_df[pd_delta_df['EoL']=='Early']['Delta_MoCA_y'], color = 'Steelblue')
plt.xlabel('')
plt.xlim(-5,3)

plt.subplot(222)
plt.title('$\Delta$MoCA/years Density', loc = 'Right', fontsize=10, pad =0)
sb.kdeplot(pd_delta_df[pd_delta_df['EoL']=='Late']['Delta_MoCA_y'], color = 'Navy', label = 'Parkinsons Late')
sb.kdeplot(pd_delta_df[pd_delta_df['EoL']=='Early']['Delta_MoCA_y'], color = 'Steelblue', label = 'Parkinsons Early')
plt.xlabel('')
plt.xlim(-7,5)
plt.ylim(0,1)
plt.legend()

plt.subplot(223)
sb.histplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late']['Delta_MoCA_y'], color = 'Darkgreen')
sb.histplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early']['Delta_MoCA_y'], color = 'Green')
plt.xlim(-5,3)

plt.subplot(224)
sb.kdeplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late']['Delta_MoCA_y'], color = 'Darkgreen', label = 'Controls Late')
sb.kdeplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early']['Delta_MoCA_y'], color = 'Green', label = 'Controls Early')
plt.xlim(-7,5)
plt.ylim(0,1)
plt.legend()

#%%----------------------Plot Delta years Distributions-------------------

plt.figure()
plt.suptitle('$\Delta$Years Distribution ', fontsize =16)
plt.subplot(121)
plt.title('$\Delta$Years Count', loc = 'Right', fontsize=10, pad =0)
sb.histplot(pd_delta_df['Delta_Age_at_Test'], color = 'Steelblue', alpha = 0.5)
sb.histplot(ctrl_delta_df['Delta_Age_at_Test'], color = 'Green', alpha = 0.5)

plt.subplot(122)
plt.title('$\Delta$Years Density', loc = 'Right', fontsize=10, pad =0)
sb.kdeplot(pd_delta_df['Delta_Age_at_Test'], color = 'Steelblue', label = 'Parkinsons')
sb.kdeplot(ctrl_delta_df['Delta_Age_at_Test'], color = 'Green', label = 'Controls')
plt.legend()

#----------------------

plt.figure()
plt.suptitle('$\Delta$Years Distribution ', fontsize =16)
plt.subplot(221)
plt.title('$\Delta$Years Count', loc = 'Right', fontsize=10, pad =0)
sb.histplot(pd_delta_df[pd_delta_df['EoL']=='Late']['Delta_Age_at_Test'], color = 'Navy')
sb.histplot(pd_delta_df[pd_delta_df['EoL']=='Early']['Delta_Age_at_Test'], color = 'Steelblue')
plt.xlabel('')
#plt.xlim(-5,3)

plt.subplot(222)
plt.title('$\Delta$Years Density', loc = 'Right', fontsize=10, pad =0)
sb.kdeplot(pd_delta_df[pd_delta_df['EoL']=='Late']['Delta_Age_at_Test'], color = 'Navy', label = 'Parkinsons Late')
sb.kdeplot(pd_delta_df[pd_delta_df['EoL']=='Early']['Delta_Age_at_Test'], color = 'Steelblue', label = 'Parkinsons Early')
plt.xlabel('')
# plt.xlim(-7,5)
# plt.ylim(0,1)
plt.legend()

plt.subplot(223)
sb.histplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late']['Delta_Age_at_Test'], color = 'Darkgreen')
sb.histplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early']['Delta_Age_at_Test'], color = 'Green')
# plt.xlim(-5,3)

plt.subplot(224)
sb.kdeplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Late']['Delta_Age_at_Test'], color = 'Darkgreen', label = 'Controls Late')
sb.kdeplot(ctrl_delta_df[ctrl_delta_df['EoL']=='Early']['Delta_Age_at_Test'], color = 'Green', label = 'Controls Early')
# plt.xlim(-7,5)
# plt.ylim(0,1)
plt.legend()

#%%----------------------Plot YSO Distributions-------------------

plt.figure()
plt.suptitle('Years Since Onset Distribution ', fontsize =16)
plt.subplot(121)
plt.title('Years Since Onset Count', loc = 'Right', fontsize=10, pad =0)
sb.histplot(pd_delta_df['YSO'], color = 'Steelblue', alpha = 0.5)

plt.subplot(122)
plt.title('Years Since Onset Density', loc = 'Right', fontsize=10, pad =0)
sb.kdeplot(pd_delta_df['YSO'], color = 'Steelblue', label = 'Parkinsons')
plt.legend()
#%%----------------------Pearson R Correlation L & R Subgroups-----------------


#-------------------PD (Delta MoCA >-1)
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(pd_delta_df[pd_delta_df['Delta_MoCA_y']>-1]['Delta_MoCA_y'],pd_delta_df[pd_delta_df['Delta_MoCA_y']>-1][i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        pd_r_corr_df_one = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        pd_r_corr_df_one = pd.concat([pd_r_corr_df_one,tmp])
        
pd_r_corr_df_one.dropna(inplace=True)
pd_r_corr_df_one.reset_index(inplace=True, drop=True)

#Correct by FDR
pd_r_corr_df_one['FDR_Pvalue'] = FDR(pd_r_corr_df_one['Pvalue'])

#-------------------PD (Delta MoCA -2<x<-1)
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(pd_delta_df[(pd_delta_df['Delta_MoCA_y']>-2)&(pd_delta_df['Delta_MoCA_y']<-1)]['Delta_MoCA_y'],pd_delta_df[(pd_delta_df['Delta_MoCA_y']>-2)&(pd_delta_df['Delta_MoCA_y']<-1)][i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        pd_r_corr_df_two = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        pd_r_corr_df_two = pd.concat([pd_r_corr_df_two,tmp])
        
pd_r_corr_df_two.dropna(inplace=True)
pd_r_corr_df_two.reset_index(inplace=True, drop=True)

#Correct by FDR
pd_r_corr_df_two['FDR_Pvalue'] = FDR(pd_r_corr_df_two['Pvalue'])

#-------------------PD (Delta MoCA <-2)
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(pd_delta_df[pd_delta_df['Delta_MoCA_y']<-2]['Delta_MoCA_y'],pd_delta_df[pd_delta_df['Delta_MoCA_y']<-2][i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        pd_r_corr_df_three = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        pd_r_corr_df_three = pd.concat([pd_r_corr_df_three,tmp])
        
pd_r_corr_df_three.dropna(inplace=True)
pd_r_corr_df_three.reset_index(inplace=True, drop=True)

#Correct by FDR
pd_r_corr_df_three['FDR_Pvalue'] = FDR(pd_r_corr_df_three['Pvalue'])

#-----------------------Ctrl
c=1
for j,i in enumerate(delta_structures_LR):
    
    r,p = pearsonr(ctrl_delta_df['Delta_MoCA_y'],ctrl_delta_df[i])
    print(i)
    print(r)
    print('P')
    print(p)
    print('\n')
    
    tmp_dict = {'Structure':[i],
           'R':[r],
           'Pvalue':[p]}
    
    #Create dataframe 
    if c: #If First iteration 
        ctrl_r_corr_df = pd.DataFrame.from_dict(tmp_dict)
        c=0
        
    else:
        tmp = pd.DataFrame.from_dict(tmp_dict)
        ctrl_r_corr_df = pd.concat([ctrl_r_corr_df,tmp])
        
ctrl_r_corr_df = ctrl_r_corr_df.dropna()
ctrl_r_corr_df.reset_index(inplace=True, drop=True)

#Correct by FDR
ctrl_r_corr_df['FDR_Pvalue'] = FDR(ctrl_r_corr_df['Pvalue'])


#------P Value plot 

plt.suptitle('Pearsons R $\Delta$MoCA / $\Delta$Volume P-Values L + R FDR corrected', fontsize=16)
plt.subplot(211)
plt.title('Controls', loc='right', pad=0, fontsize=10)
plt.scatter(np.arange(0,len(ctrl_r_corr_df['FDR_Pvalue']),1),ctrl_r_corr_df['FDR_Pvalue'], color='Green', label='Controls')
plt.axhline(0.05,0,len(ctrl_r_corr_df['FDR_Pvalue']), color='r')
plt.ylabel('p-value')

plt.subplot(212)
plt.title('Parkinsons', loc='right', pad=0, fontsize=10)
plt.scatter(np.arange(0,len(pd_r_corr_df_one['FDR_Pvalue']),1),pd_r_corr_df_one['FDR_Pvalue'], color='lightsteelblue',alpha =0.8, label='Parkinsons $\Delta$MoCA >-1')
plt.scatter(np.arange(0,len(pd_r_corr_df_two['FDR_Pvalue']),1),pd_r_corr_df_two['FDR_Pvalue'], color='Steelblue', alpha =0.8, label='Parkinsons $\Delta$MoCA -2<x<-1')
plt.scatter(np.arange(0,len(pd_r_corr_df_three['FDR_Pvalue']),1),pd_r_corr_df_three['FDR_Pvalue'], color='Navy',  alpha =0.8,label='Parkinsons$\Delta$MoCA <-2')
plt.axhline(0.05,0,len(pd_r_corr_df_one['FDR_Pvalue']), color='r')
plt.ylabel('p-value')
plt.xticks(range(len(pd_r_corr_df_one['Structure'])),labels=[x.replace('Delta_','') for x in pd_r_corr_df_one['Structure']], rotation=-90, fontsize=8)
plt.legend()
plt.tight_layout()

#%%///////////////////////////BAYESIAN MODELS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%----------------------Merge Model-------------------------------------------

merge_db_scaled['Group'] = pd.Categorical(merge_db_scaled['Group'], categories=['Control','PD'])

bm_model= bmb.Model('MoCA_Scores ~ Precentral_gyrus_total_volume_PR + Sex + Group*Age_at_Test_1 + (1+ Age_at_Test_1 | Subject_ID)', data = merge_db_scaled)
merge_bm = bm_model.fit(draws=2000, chains=4, target_accept=0.95)

az.summary(merge_bm, var_names = ['Precentral_gyrus_total_volume_PR', 'Sex','Age_at_Test_1','Group','Group:Age_at_Test_1'])


#%%///////////////////////////ONLY VOLUME MODELS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%

VER = '2.0'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import easygui as eg
import os                #Sirve para el Manejo de archivos
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from scipy.stats import false_discovery_control as FDR
from scipy.stats import pearsonr
#import matplotlib as mpl
from matplotlib.lines import Line2D
from statsmodels.stats.outliers_influence import variance_inflation_factor as VIF
#from statsmodels import graphics
from scipy import stats as stats
#from sklearn.linear_model import LinearRegression
import seaborn as sb

os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]


#%%---------------------------PATH MANAGER-------------------------------------

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Linear-ICE+R"+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Linear-ICE+R "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select PD Long BrAiN-Trak DATAFRAME File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pd_long_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select PD Single BrAiN-Trak DATAFRAME File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pd_single_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Ctrl Long BrAiN-Trak DATAFRAME File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_long_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Ctrl Single BrAiN-Trak DATAFRAME File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_single_path = temp_path.replace(os.path.sep ,"/")

#Demographics File path
message = 'Please Select Demographics File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
dems_path = temp_path.replace(os.path.sep ,"/")

#Socio-Economics File path
message = 'Please Select Socio-Economics File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
socec_path = temp_path.replace(os.path.sep ,"/")

#PDD_Diagnosis_History File path
message = 'Please Select PD_Diagnosis_History File'
title = "Linear-ICE+R "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pdiag_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)

#%%---------------------------DATA LOAD----------------------------------------

pd_long_file = pd.read_csv(pd_long_path)  
pd_single_file = pd.read_csv(pd_single_path)  
ctrl_long_file = pd.read_csv(ctrl_long_path)  
ctrl_single_file = pd.read_csv(ctrl_single_path)  

#----Outlier subject Removal

#pd_long_file = pd_long_file[pd_long_file.Subject_ID!=3771]

#-------------MoCA Compensation to raw data correction (revert +1 pt in subs with <=12 YOE)
pd_long_corrected = pd_long_file.copy()
pd_single_corrected = pd_single_file.copy()
ctrl_long_corrected = ctrl_long_file.copy()
ctrl_single_corrected = ctrl_single_file.copy()


#%%---------------------------Database Merge / Early-Late Onset selection------

#----Outlier subject Removal

#pd_long_corrected = pd_long_corrected[pd_long_corrected.Subject_ID != 3771]
#ctrl_long_corrected = ctrl_long_corrected[ctrl_long_corrected.Subject_ID != 3771]

#------Single + Longitudinal files merge
pd_db= pd.concat([pd_long_corrected, pd_single_corrected], ignore_index=True)
ctrl_db = pd.concat([ctrl_long_corrected, ctrl_single_corrected], ignore_index=True)
merge_db = pd.concat([pd_db, ctrl_db], ignore_index=True)

#------Column renaming
#Remove Parentheses
pd_db.columns = pd_db.columns.str.replace('(', '')
ctrl_db.columns = pd_db.columns.str.replace('(', '')
merge_db.columns = pd_db.columns.str.replace('(', '')
pd_db.columns = pd_db.columns.str.replace(')', '')
ctrl_db.columns = pd_db.columns.str.replace(')', '')
merge_db.columns = pd_db.columns.str.replace(')', '')
#Remove Spacing
pd_db.columns = pd_db.columns.str.replace(' ', '_')
ctrl_db.columns = pd_db.columns.str.replace(' ', '_')
merge_db.columns = pd_db.columns.str.replace(' ', '_')
#Remove Percentage
pd_db.columns = pd_db.columns.str.replace('%', 'PR')
ctrl_db.columns = pd_db.columns.str.replace('%', 'PR')
merge_db.columns = pd_db.columns.str.replace('%', 'PR')
#Remove Plus
pd_db.columns = pd_db.columns.str.replace('+', '_plus_')
ctrl_db.columns = pd_db.columns.str.replace('+', '_plus_')
merge_db.columns = pd_db.columns.str.replace('+', '_plus_')
#Remove dot
pd_db.columns = pd_db.columns.str.replace('.', '_')
ctrl_db.columns = pd_db.columns.str.replace('.', '_')
merge_db.columns = pd_db.columns.str.replace('.', '_')
#Remove -
pd_db.columns = pd_db.columns.str.replace('-', '_')
ctrl_db.columns = pd_db.columns.str.replace('-', '_')
merge_db.columns = pd_db.columns.str.replace('-', '_')
#Remove numbers
pd_db.columns = pd_db.columns.str.replace('3rd', 'Third')
ctrl_db.columns = pd_db.columns.str.replace('3rd', 'Third')
merge_db.columns = pd_db.columns.str.replace('3rd', 'Third')
pd_db.columns = pd_db.columns.str.replace('4th', 'Fourth')
ctrl_db.columns = pd_db.columns.str.replace('4th', 'Fourth')
merge_db.columns = pd_db.columns.str.replace('4th', 'Fourth')

#Set Subjects ID as int
pd_db['Subject_ID']= pd_db['Subject_ID'].astype(int) 
ctrl_db['Subject_ID']= ctrl_db['Subject_ID'].astype(int) 
merge_db['Subject_ID']= merge_db['Subject_ID'].astype(int) 

#Longitudinal Subjects 
eo_l_pd_subs =[]
lo_l_pd_subs =[]
eo_l_matched_subs=[]
lo_l_matched_subs =[]

#Single Subjects
eo_s_pd_subs =[]
lo_s_pd_subs =[]
eo_s_matched_subs=[]
lo_s_matched_subs =[]

#Parkinsons
allsubs = pd_db['Subject_ID'].unique()

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(pd_db[pd_db['Subject_ID']==i]['ImageID'])>1:
        #Extract Subjects 
        if pd_db[pd_db['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 50: 
            eo_l_pd_subs.append(i)
        else:
            lo_l_pd_subs.append(i)
    else:
        #Extract Subjects 
        if pd_db[pd_db['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 50: 
            eo_s_pd_subs.append(i)
        else:
            lo_s_pd_subs.append(i)


#Controls
allsubs = ctrl_db['Subject_ID'].unique()

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(ctrl_db[ctrl_db['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if ctrl_db[ctrl_db['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 50: 
            eo_l_matched_subs.append(i)
        else:
            lo_l_matched_subs.append(i)
    else:
        #Extract Subjects 
        if ctrl_db[ctrl_db['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 50:
            eo_s_matched_subs.append(i)
        else:
            lo_s_matched_subs.append(i)

#----------Add Years Since Onset to PD Database

tmp = pd_db['Age']-pd_db['Onset_Age']
pd_db['YSO']=tmp #Years Since Onset column

#----------Add Early-Late Flag

tmp = pd.Series(np.zeros(len(pd_db)))
pd_db['EoL']=tmp   #Early or Late column
pd_db['EoL']= pd_db['EoL'].astype(str) 
pd_db.loc[pd_db['Subject_ID'].isin(eo_s_pd_subs+eo_l_pd_subs), 'EoL'] = 'Early'
pd_db.loc[pd_db['Subject_ID'].isin(lo_s_pd_subs+lo_l_pd_subs), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(ctrl_db)))
ctrl_db['EoL']=tmp
ctrl_db['EoL']= ctrl_db['EoL'].astype(str) 
ctrl_db.loc[ctrl_db['Subject_ID'].isin(eo_s_matched_subs+eo_l_matched_subs), 'EoL'] = 'Early'
ctrl_db.loc[ctrl_db['Subject_ID'].isin(lo_s_matched_subs+lo_l_matched_subs), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(merge_db)))
merge_db['EoL']=tmp
merge_db['EoL']= merge_db['EoL'].astype(str) 
merge_db.loc[merge_db['Subject_ID'].isin(eo_s_pd_subs+eo_l_pd_subs+eo_s_matched_subs+eo_l_matched_subs), 'EoL'] = 'Early'
merge_db.loc[merge_db['Subject_ID'].isin(lo_s_pd_subs+lo_l_pd_subs+lo_s_matched_subs+lo_l_matched_subs), 'EoL'] = 'Late'

#-------Separate databases by subject group

#L+S
whole_eo_subs=eo_l_pd_subs + eo_s_pd_subs + eo_l_matched_subs + eo_s_matched_subs 
whole_lo_subs=lo_l_pd_subs + lo_s_pd_subs + lo_l_matched_subs + lo_s_matched_subs

eo_db = merge_db.loc[merge_db['Subject_ID'].isin(whole_eo_subs)]
lo_db = merge_db.loc[merge_db['Subject_ID'].isin(whole_lo_subs)]

#Longitudinal + Grouped S (Change single subjects to barcode group)
eo_lgs_db = eo_db.copy()
lo_lgs_db = lo_db.copy()

eo_lgs_db.loc[eo_lgs_db['Subject_ID'].isin(eo_s_pd_subs+eo_s_matched_subs), 'Subject_ID'] = 101010
lo_lgs_db.loc[lo_lgs_db['Subject_ID'].isin(lo_s_pd_subs+lo_s_matched_subs), 'Subject_ID'] = 201010

pd_lgs_db = pd_db.copy()
pd_lgs_db.loc[pd_lgs_db['Subject_ID'].isin(eo_s_pd_subs+lo_s_pd_subs), 'Subject_ID'] = 102010

ctrl_lgs_db = ctrl_db.copy()
ctrl_lgs_db.loc[ctrl_lgs_db['Subject_ID'].isin(eo_s_matched_subs+lo_s_matched_subs), 'Subject_ID'] = 102010

#Only longitudinal 

pd_l_subs = eo_l_pd_subs + lo_l_pd_subs
pd_l_db = pd_db.loc[pd_db['Subject_ID'].isin(pd_l_subs)]

ctrl_l_subs = eo_l_matched_subs + lo_l_matched_subs
ctrl_l_db = ctrl_db.loc[ctrl_db['Subject_ID'].isin(ctrl_l_subs)]

#--------------------Scaler

pd_db_scaled = pd_db.copy()     #Parkinsons Database
ctrl_db_scaled = ctrl_db.copy() #Controls Database
merge_db_scaled = merge_db.copy() #Parkinsons + Controls Database 
eo_db_scaled = eo_db.copy()  #Early Onset PD+Matched Database
lo_db_scaled = lo_db.copy()  #Late Onset PD+Matched Database

#Longitudinal + Grouped Singles 
pd_lgs_db_scaled = pd_lgs_db.copy()  #Parkinsons Longitudinal + Grouped Singles Database
ctrl_lgs_db_scaled = ctrl_lgs_db.copy()  #Controls Longitudinal + Grouped Singles Database
eo_lgs_db_scaled = eo_lgs_db.copy()  #Early Onset PD+Matched+Grouped Singles Database
lo_lgs_db_scaled = lo_lgs_db.copy()  #Late Onset PD+Matched+Grouped Singles Database

#Longitudinal 
pd_l_db_scaled = pd_l_db.copy()
ctrl_l_db_scaled = ctrl_l_db.copy()


#Obtain Structures 
tmp = list(merge_db.columns)
#Values to remove (not structures)
to_remove = ['Subject_ID', 'Test_Number','Sex', 'Birthdate', 'Group','Modality', 'Years_of_education',
             'MoCA_Scores', 'MoCA_Dates', 'Age_at_Test', 'Days_between_Tests','Slope','Onset_Age',
             'Diagnosis_Age', 'Subject','Report_date','Image_orientation', 'Scale_factor', 'Quality_control',
             'Filename','ImageID', 'SubjectID','Group_1','Sex_1','Age','Date','SNR_y','CNR','EFC','CJV', 'SNR_x', 'EoL',
             'HY_Scores','HY_Dates','Test_Number_1','Age_at_Test_1', 'Days_between_Tests_1','Slope_1']
#Left Structures
structures_left = [x for x in tmp if 'left' in x] #Remove everything but left structures
structures_left = [x for x in structures_left if 'cm3' not in x] #Remove cm3 values
#Right Structures 
structures_right = [x for x in tmp if 'right' in x] #Remove everything but right structures
structures_right = [x for x in structures_right if 'cm3' not in x] #Remove cm3 values 
#Structures Full (Left+Right)
structures_LR = structures_right + structures_left
#Structures Total (Only total volumes)
structures_total = [x for x in tmp if x not in structures_left+structures_right] #Remove left+right structures
structures_total = [x for x in structures_total if 'asymmetry' not in x] #Remove Asymmetry values
structures_total = [x for x in structures_total if 'cm3' not in x] #Remove cm3 values 
structures_total = [x for x in structures_total if x not in to_remove] #Remove other values 



#Continuous variables to include in scaler
cont = ['Years_of_education', 'Age_at_Test', 'Days_between_Tests', 'Onset_Age', 'Diagnosis_Age', 'Age',
        'SNR_y','CNR','EFC','CJV', 'SNR_x','MoCA_Scores','HY_Scores']
var = structures_total+cont

#Database Scaling 
scaler = StandardScaler()
pd_db_scaled[var+['YSO']] = scaler.fit_transform(pd_db_scaled[var+['YSO']])
ctrl_db_scaled[var] = scaler.fit_transform(ctrl_db_scaled[var])
merge_db_scaled[var] = scaler.fit_transform(merge_db_scaled[var])
eo_db_scaled[var]= scaler.fit_transform(eo_db_scaled[var])
lo_db_scaled[var] = scaler.fit_transform(lo_db_scaled[var])

#Longitudinal + Grouped singles
pd_lgs_db_scaled[var+['YSO']] = scaler.fit_transform(pd_lgs_db_scaled[var+['YSO']])
ctrl_lgs_db_scaled[var] = scaler.fit_transform(ctrl_lgs_db_scaled[var])
eo_lgs_db_scaled[var] = scaler.fit_transform(eo_lgs_db_scaled[var])
lo_lgs_db_scaled[var] = scaler.fit_transform(lo_lgs_db_scaled[var])

#Longitudinal only 
pd_l_db_scaled[var+['YSO']] = scaler.fit_transform(pd_l_db_scaled[var+['YSO']])
ctrl_l_db_scaled[var] = scaler.fit_transform(ctrl_l_db_scaled[var])






