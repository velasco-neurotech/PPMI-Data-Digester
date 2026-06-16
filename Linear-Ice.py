# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:40:23 2025
 _       _________ _        _______  _______  _______ 
( \      \__   __/( (    /|(  ____ \(  ___  )(  ____ )
| (         ) (   |  \  ( || (    \/| (   ) || (    )|
| |         | |   |   \ | || (__    | (___) || (____)|
| |         | |   | (\ \) ||  __)   |  ___  ||     __)
| |         | |   | | \   || (      | (   ) || (\ (   
| (____/\___) (___| )  \  || (____/\| )   ( || ) \ \__
(_______/\_______/|/    )_)(_______/|/     \||/   \__/
                                                      
    _________ _______  _______                        
    \__   __/(  ____ \(  ____ \                       
       ) (   | (    \/| (    \/                       
 _____ | |   | |      | (__                           
(_____)| |   | |      |  __)                          
       | |   | |      | (                             
    ___) (___| (____/\| (____/\                       
    \_______/(_______/(_______/
                       

@author: Miguel Velasco Orozco 

ICE: Inferences from Clinical Evidence


///Ver 2 Update:
    
    En vez de separar las bases por early/late desde el principio y volverlas a concatenar (daba problemas) en 
    algunas gráficas) se cambia a tener una base de datos concatenada desde el principio y solamente filtrar 
    conforme sea requerido.
    Los datos corregidos (+1 if YOE <12) no se tomaban para los modelos early/late, se remedia ese error
    
    // Ver 2.1 Update:
        
        Se implementa que también se tomen en cuenta los datos de los sujetos con una sola evaluación y no 
        únicamente los longitudinales.


/// Ver 3 Update :
        
        Added Scaler to dataframes, included single subjects for models 

"""
#VER = '2.0'

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import easygui as eg
# import os                #Sirve para el Manejo de archivos
# import statsmodels.api as sm
# import statsmodels.formula.api as smf
# import matplotlib as mpl
# from matplotlib.lines import Line2D

# os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]

#%%-----PATH MANAGER

# #-----Session Values Input
# #Session Name
# message = 'Please input Session Name or ID'
# title = "Linear-ICE"+VER+" - Start"
# sname = eg.enterbox(message, title) #Session Name

# #Session Save path
# message = 'Please input Session Save Folder'
# title = "Linear-ICE "+VER+" - Start"
# temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
# sv_path = temp_path.replace(os.path.sep ,"/")

# #Session Open File
# message = 'Please Select Parkinsons LINMOD MoCA File'
# title = "Linear-ICE "+VER+" - "
# temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
# pdd_path = temp_path.replace(os.path.sep ,"/")

# #Session Open File
# message = 'Please Select Controls LINMOD MoCA File'
# title = "Linear-ICE "+VER+" - "
# temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
# ctrl_path = temp_path.replace(os.path.sep ,"/")

# #-------Change working directory to save path 
# os.chdir(sv_path)

#%%-----DATA LOAD

# pdd_csvfile = pd.read_csv(pdd_path)  
# ctrl_csvfile = pd.read_csv(ctrl_path)  

# #-------------MoCA Compensation to raw data correction (+1 pt in subs with <=12 YOE)
# pdd_corrected = pdd_csvfile.copy()
# ctrl_corrected = ctrl_csvfile.copy()

# #PDD
# for index, row in pdd_corrected.iterrows():
#     if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
#         prev =pdd_corrected['MoCA_Scores'][index]
#         pdd_corrected.loc[index,'MoCA_Scores'] = prev-1

# #Ctrl
# for index, row in ctrl_corrected.iterrows():
#     if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
#         prev =ctrl_corrected['MoCA_Scores'][index]
#         ctrl_corrected.loc[index,'MoCA_Scores'] = prev-1



#%% Random intercept by subject  (DEPRECATED)

# md = smf.mixedlm("MoCA_Scores ~ Sex + Test_Number + Onset_Age + Diagnosis_Age + Years_of_education", 
#                  pdd_csvfile, groups=pdd_csvfile["Subject_ID"])
# mdf = md.fit()
# print(mdf.summary())


#%% Random slope-intercept by subject in time (Deprecated)

# #PDD Model
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
#                  pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
# pdd_lm = lm.fit()
# print('\n\n\nPDD Model')
# print(pdd_lm.summary())

# lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
#                  pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
# pdd_lm = lm.fit()
# print('\n\n\nPDD Model 2')
# print(pdd_lm.summary())

# #Ctrl Model 
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
#                  ctrl_corrected, groups=ctrl_corrected["Subject_ID"], re_formula='~Age_at_Test')
# ctrl_lm = lm.fit()
# print('\nCtrl Model')
# print(ctrl_lm.summary())

# #Merge Model 
# merged_db = pd.concat([pdd_corrected, ctrl_corrected])
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group", 
#                  merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
# merged_lm = lm.fit()
# print('\nMerged Model')
# print(merged_lm.summary())

# #Merge Model + interaction
# merged_db = pd.concat([pdd_corrected, ctrl_corrected])
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group+ Age_at_Test*Group", 
#                  merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
# merged_lm_i = lm.fit()
# print('\nMerged Model + interaction')
# print(merged_lm_i.summary())

#%% Early vs Late onset groups clssification (DEPRECATED)

# eo_subs_pdd =[]
# lo_subs_pdd =[]
# eo_subs_matched =[]
# lo_subs_matched =[]

# #Parkinsons

# allsubs = pdd_csvfile['Subject_ID'].value_counts()
# allsubs= allsubs.sort_index()
# allsubs=allsubs.index

# for i in allsubs:
    
#     #Only Subjects with more than 1 MoCA eval 
    
#     if len(pdd_csvfile[pdd_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
    
#         #Extract Subjects 
        
#         if pdd_csvfile[pdd_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 50:
           
#             eo_subs_pdd.append(i)
        
#         else:
#             lo_subs_pdd.append(i)


# #Controls

# allsubs = ctrl_csvfile['Subject_ID'].value_counts()
# allsubs= allsubs.sort_index()
# allsubs=allsubs.index

# for i in allsubs:
    
#     #Only Subjects with more than 1 MoCA eval 
    
#     if len(ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
    
#         #Extract Subjects 
        
#         if ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 50:
           
#             eo_subs_matched.append(i)
        
#         else:
#             lo_subs_matched.append(i)


# #Separate databases by subject group
# eo_pdd_db = pdd_csvfile.loc[pdd_csvfile['Subject_ID'].isin(eo_subs_pdd)]
# lo_pdd_db = pdd_csvfile.loc[pdd_csvfile['Subject_ID'].isin(lo_subs_pdd)]

# eo_matched_db = ctrl_csvfile.loc[ctrl_csvfile['Subject_ID'].isin(eo_subs_matched)]
# lo_matched_db = ctrl_csvfile.loc[ctrl_csvfile['Subject_ID'].isin(lo_subs_matched)]



#%% Early vs late onset models (DEPRECATED)

# #----------Parkinsons
# #Early Onset
# lm = smf.mixedlm("MoCA_Scores ~ Years_of_education + Age_at_Test", 
#                  eo_pdd_db, groups=eo_pdd_db["Subject_ID"], re_formula='~Age_at_Test')
# eo_pdd_lm = lm.fit()
# print('Early Onset PDD')
# print(eo_pdd_lm.summary())

# #Late Onset
# lm = smf.mixedlm("MoCA_Scores ~ Years_of_education + Age_at_Test", 
#                  lo_pdd_db, groups=lo_pdd_db["Subject_ID"], re_formula='~Age_at_Test')
# lo_pdd_lm = lm.fit()
# print('Late Onset PDD')
# print(lo_pdd_lm.summary())


# #----------Controls
# #Matched Early Onset
# lm = smf.mixedlm("MoCA_Scores ~ Years_of_education + Age_at_Test", 
#                  eo_matched_db, groups=eo_matched_db["Subject_ID"], re_formula='~Age_at_Test')
# eo_matched_lm = lm.fit()
# print('Early Onset Ctrl')
# print(eo_matched_lm.summary())

# #Matched Late Onset
# lm = smf.mixedlm("MoCA_Scores ~ Years_of_education + Age_at_Test", 
#                  lo_matched_db, groups=lo_matched_db["Subject_ID"], re_formula='~Age_at_Test')
# lo_matched_lm = lm.fit()
# print('Late Onset PDD')
# print(lo_matched_lm.summary())

#%% Combined models Early-Late (DEPRECATED)

# merged_eo_db = pd.concat([eo_pdd_db, eo_matched_db])
# merged_lo_db = pd.concat([lo_pdd_db, lo_matched_db])

# whole_eo_subs= eo_subs_pdd + eo_subs_matched
# whole_lo_subs= lo_subs_pdd + lo_subs_matched


# #Early Onset
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education ", 
#                  merged_eo_db, groups=merged_eo_db["Subject_ID"], re_formula='~Age_at_Test')
# eo_lm = lm.fit()
# print('\n\n\nEarly Onset Model')
# print(eo_lm.summary())

# #Late Onset
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
#                  merged_lo_db, groups=merged_lo_db["Subject_ID"], re_formula='~Age_at_Test')
# lo_lm = lm.fit()
# print('\nLate Onset Model')
# print(lo_lm.summary())


# #Early Onset +interaction 
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
#                  merged_eo_db, groups=merged_eo_db["Subject_ID"], re_formula='~Age_at_Test')
# eo_lm = lm.fit()
# print('\n\n\nEarly Onset Model + interaction')
# print(eo_lm.summary())

# #Late Onset +interaction 
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
#                  merged_lo_db, groups=merged_lo_db["Subject_ID"], re_formula='~Age_at_Test')
# lo_lm = lm.fit()
# print('\nLate Onset Model + interaction')
# print(lo_lm.summary())

#%%/////////////////////////PLOTS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%----MoCA Score MGLM ovelap Early-Late Onset PDD Only 

# fig, ax = plt.subplots(1,2)
# plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
# fig.set_figheight(8)
# fig.set_figwidth(12)

# for i in eo_subs_pdd:
#     index = eo_pdd_db[eo_pdd_db['Subject_ID']==i].index
#     scores = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_pdd_lm.fittedvalues.loc[index]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1)
#     ax[0].plot(ages, fitted, color ='blue', alpha=0.5)
    


# for i in lo_subs_pdd:
#     index = lo_pdd_db[lo_pdd_db['Subject_ID']==i].index
#     scores = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_pdd_lm.fittedvalues.loc[index]
    
#     ax[1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1].plot(ages, fitted, color ='red', alpha=0.5)
    

# #Average
# eo_avg = [eo_pdd_lm.params[0]+(eo_pdd_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[0].plot(np.arange(30,66,1), eo_avg, color ='k', linewidth='3')
# lo_avg = [lo_pdd_lm.params[0]+(lo_pdd_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[1].plot(np.arange(50,90,1), lo_avg, color ='k', linewidth='3')

# #Labels
# legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'),
#          Line2D([0],[0], color = 'blue',label='Model fit by subject'),
#          Line2D([0],[0], color = 'darkblue',label='Mean Slope', linewidth=3)]
# ax[0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'),
#          Line2D([0],[0], color = 'red',label='Model fit by subject'),
#          Line2D([0],[0], color = 'darkred',label='Mean Slope', linewidth=3)]
# ax[1].legend(handles=legends)

# ax[0].set(xlabel='Age at Test', ylabel='MoCA Score')
# ax[1].set(xlabel='Age at Test')
# ax[0].set_ylim([4,30])
# ax[1].set_ylim([4,30])
# ax[0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
# ax[1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')

# plt.tight_layout()

# plt.savefig('PDD MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%----MoCA Score MGLM ovelap Early-Late Onset Ctrl Only 

# fig, ax = plt.subplots(1,2)
# plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
# fig.set_figheight(8)
# fig.set_figwidth(12)

# for i in eo_subs_matched:
#     index = eo_matched_db[eo_matched_db['Subject_ID']==i].index
#     scores = eo_matched_db[eo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_matched_db[eo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_matched_lm.fittedvalues.loc[index]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1)
#     ax[0].plot(ages, fitted, color ='yellow', alpha=0.5)
    


# for i in lo_subs_matched:
#     index = lo_matched_db[lo_matched_db['Subject_ID']==i].index
#     scores = lo_matched_db[lo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_matched_db[lo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_matched_lm.fittedvalues.loc[index]
    
#     ax[1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1].plot(ages, fitted, color ='purple', alpha=0.5)

# #Average
# eo_matched_avg = [eo_matched_lm.params[0]+(eo_matched_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[0].plot(np.arange(30,66,1), eo_matched_avg, color ='orange', linewidth='3')
# lo_matched_avg = [lo_matched_lm.params[0]+(lo_matched_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[1].plot(np.arange(50,90,1), lo_matched_avg, color ='darkmagenta', linewidth='3')

# #Labels
# legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'),
#          Line2D([0],[0], color = 'yellow',label='Model fit by subject'),
#          Line2D([0],[0], color = 'orange',label='Mean Slope', linewidth=3)]
# ax[0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', alpha =0.2,label='Patient trajectories'),
#          Line2D([0],[0], color = 'purple',label='Model fit by subject'),
#          Line2D([0],[0], color = 'darkmagenta',label='Mean Slope', linewidth=3)]
# ax[1].legend(handles=legends)

# ax[0].set(xlabel='Age at Test', ylabel='MoCA Score')
# ax[1].set(xlabel='Age at Test')
# ax[0].set_ylim([4,30])
# ax[1].set_ylim([4,30])
# ax[0].set_title('Early Onset n='+str(len(eo_subs_matched)), pad = 0, fontsize= 10, loc = 'right')
# ax[1].set_title('Late Onset n='+str(len(lo_subs_matched)), pad = 0, fontsize= 10, loc = 'right')
# plt.tight_layout()

# plt.savefig('Ctrl MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%----FULL MoCA Score MGLM ovelap Early-Late Onset PDD vs Ctrl

# fig, ax = plt.subplots(1,2)
# plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
# fig.set_figheight(8)
# fig.set_figwidth(12)

# for i in eo_subs_pdd:
#     index = eo_pdd_db[eo_pdd_db['Subject_ID']==i].index
#     scores = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_pdd_lm.fittedvalues.loc[index]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1)
#     ax[0].plot(ages, fitted, color ='blue')
    

# for i in lo_subs_pdd:
#     index = lo_pdd_db[lo_pdd_db['Subject_ID']==i].index
#     scores = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_pdd_lm.fittedvalues.loc[index]
    
#     ax[1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1].plot(ages, fitted, color ='red')
    
# for i in eo_subs_matched:
#     index = eo_matched_db[eo_matched_db['Subject_ID']==i].index
#     scores = eo_matched_db[eo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_matched_db[eo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_matched_lm.fittedvalues.loc[index]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1)
#     ax[0].plot(ages, fitted, color ='purple')
    

# for i in lo_subs_matched:
#     index = lo_matched_db[lo_matched_db['Subject_ID']==i].index
#     scores = lo_matched_db[lo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_matched_db[lo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_matched_lm.fittedvalues.loc[index]
    
#     ax[1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1].plot(ages, fitted, color ='green')
    
# ax[0].set(xlabel='Age at Test', ylabel='MoCA Score')
# ax[1].set(xlabel='Age at Test')
# ax[0].set_ylim([4,30])
# ax[1].set_ylim([4,30])
# ax[0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
# ax[1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')

#%%----FULL v2 MoCA Score MGLM ovelap Early-Late Onset PDD vs Ctrl

# fig, ax = plt.subplots(2,2)
# plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
# fig.set_figheight(8)
# fig.set_figwidth(12)

# for i in eo_subs_pdd:
#     index = eo_pdd_db[eo_pdd_db['Subject_ID']==i].index
#     scores = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_pdd_lm.fittedvalues.loc[index]
    
#     #ax[0,0].plot(ages, scores, color='k', alpha=0.1)
#     ax[0,0].plot(ages, fitted, color ='midnightblue')
    

# for i in lo_subs_pdd:
#     index = lo_pdd_db[lo_pdd_db['Subject_ID']==i].index
#     scores = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_pdd_lm.fittedvalues.loc[index]
    
#     #ax[0,1].plot(ages, scores, color='k', alpha=0.1)
#     ax[0,1].plot(ages, fitted, color ='firebrick')
    
# for i in eo_subs_matched:
#     index = eo_matched_db[eo_matched_db['Subject_ID']==i].index
#     scores = eo_matched_db[eo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_matched_db[eo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_matched_lm.fittedvalues.loc[index]
    
#     #ax[1,0].plot(ages, scores, color='k', alpha=0.1)
#     ax[1,0].plot(ages, fitted, color ='gold')
    

# for i in lo_subs_matched:
#     index = lo_matched_db[lo_matched_db['Subject_ID']==i].index
#     scores = lo_matched_db[lo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_matched_db[lo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_matched_lm.fittedvalues.loc[index]
    
#     #ax[1,1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1,1].plot(ages, fitted, color ='blueviolet')
    

# lo_matched_avg = [lo_matched_lm.params[0]+(lo_matched_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[1,1].plot(np.arange(50,90,1), lo_matched_avg, color ='k', linewidth='3', label='Average LO Controls Slope= %.3f'%lo_matched_lm.params[2])

# eo_pdd_ci=eo_pdd_lm.conf_int().loc['Age_at_Test']
# lo_pdd_ci=lo_pdd_lm.conf_int().loc['Age_at_Test']
# eo_matched_ci=eo_matched_lm.conf_int().loc['Age_at_Test']
# lo_matched_ci=lo_matched_lm.conf_int().loc['Age_at_Test']

# #----------Averages + Ci Intervals
# #PDD Eo
# eo_avg = [eo_pdd_lm.params[0]+(eo_pdd_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[0,0].plot(np.arange(30,66,1), eo_avg, color ='k', linewidth='3', label='Average EO Parkinsons Slope= %.3f'%eo_pdd_lm.params[2])

# eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[0]*x) for x in np.arange(30,66,1)]
# ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

# eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[1]*x) for x in np.arange(30,66,1)]
# ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

# #PDD Lo
# lo_avg = [lo_pdd_lm.params[0]+(lo_pdd_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[0,1].plot(np.arange(50,90,1), lo_avg, color ='k', linewidth='3', label='Average LO Parkinsons Slope= %.3f'%lo_pdd_lm.params[2])

# lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[0]*x) for x in np.arange(50,90,1)]
# ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

# lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[1]*x) for x in np.arange(50,90,1)]
# ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

# #Ctrl Eo
# eo_matched_avg = [eo_matched_lm.params[0]+(eo_matched_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[1,0].plot(np.arange(30,66,1), eo_matched_avg, color ='k',linewidth='3', label='Average EO Controls Slope= %.3f'%eo_matched_lm.params[2])

# eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[0]*x) for x in np.arange(30,66,1)]
# ax[1,0].fill_between(np.arange(30,66,1),eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

# eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[1]*x) for x in np.arange(30,66,1)]
# ax[1,0].fill_between(np.arange(30,66,1), eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

# #Ctrl Lo
# lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[0]*x) for x in np.arange(50,90,1)]
# ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)
# lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[1]*x) for x in np.arange(50,90,1)]
# ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)


# #Labels
# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_pdd_lm.params[2]),
#          Line2D([0],[0], color = 'midnightblue',label='Model fit by subject')]
# ax[0,0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k',label='Model Slope= %.3f'%lo_pdd_lm.params[2]),
#          Line2D([0],[0], color = 'firebrick',label='Model fit by subject')]
# ax[0,1].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_matched_lm.params[2]),
#          Line2D([0],[0], color = 'gold',label='Model fit by subject')]
# ax[1,0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%lo_matched_lm.params[2]),
#          Line2D([0],[0], color = 'blueviolet',label='Model fit by subject')]
# ax[1,1].legend(handles=legends)


    
# ax[0,0].set(ylabel='Parkinsons\n\n MoCA Score')
# ax[1,0].set(xlabel='Age at Test', ylabel='Controls\n\n MoCA Score')
# ax[1,1].set(xlabel='Age at Test')

# ax[0,0].set_ylim([16,30])
# ax[0,1].set_ylim([16,30])
# ax[1,0].set_ylim([16,30])
# ax[1,1].set_ylim([16,30])
# ax[0,0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 12)
# ax[0,1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 12)

# plt.savefig('Full Model MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%----FULL v3 MoCA Score MGLM ovelap Early-Late Onset PDD vs Ctrl

# fig, ax = plt.subplots(2,2)
# plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
# fig.set_figheight(8)
# fig.set_figwidth(12)

# c=0
# c1=0

# for i in whole_eo_subs:
#     index = merged_eo_db[merged_eo_db['Subject_ID']==i].index
#     scores = merged_eo_db[merged_eo_db['Subject_ID']==i]['MoCA_Scores']
#     ages = merged_eo_db[merged_eo_db['Subject_ID']==i]['Age_at_Test']
#     c1+=len(index)
#     fitted = eo_lm.fittedvalues.loc[c0:]
    
#     #ax[0,0].plot(ages, scores, color='k', alpha=0.1)
#     if i in eo_subs_pdd:
#         ax[0,0].plot(ages, fitted, color ='midnightblue')
        
#     elif i in eo_subs_matched:
#         ax[1,0].plot(ages, fitted, color ='gold')
    

# for i in lo_subs_pdd:
#     index = lo_pdd_db[lo_pdd_db['Subject_ID']==i].index
#     scores = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_pdd_lm.fittedvalues.loc[index]
    
#     #ax[0,1].plot(ages, scores, color='k', alpha=0.1)
#     ax[0,1].plot(ages, fitted, color ='firebrick')


# for i in lo_subs_matched:
#     index = lo_matched_db[lo_matched_db['Subject_ID']==i].index
#     scores = lo_matched_db[lo_matched_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_matched_db[lo_matched_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_matched_lm.fittedvalues.loc[index]
    
#     #ax[1,1].plot(ages, scores, color='k', alpha=0.1)
#     ax[1,1].plot(ages, fitted, color ='blueviolet')
    

# lo_matched_avg = [lo_matched_lm.params[0]+(lo_matched_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[1,1].plot(np.arange(50,90,1), lo_matched_avg, color ='k', linewidth='3', label='Average LO Controls Slope= %.3f'%lo_matched_lm.params[2])

# eo_pdd_ci=eo_pdd_lm.conf_int().loc['Age_at_Test']
# lo_pdd_ci=lo_pdd_lm.conf_int().loc['Age_at_Test']
# eo_matched_ci=eo_matched_lm.conf_int().loc['Age_at_Test']
# lo_matched_ci=lo_matched_lm.conf_int().loc['Age_at_Test']

# #----------Averages + Ci Intervals
# #PDD Eo
# eo_avg = [eo_pdd_lm.params[0]+(eo_pdd_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[0,0].plot(np.arange(30,66,1), eo_avg, color ='k', linewidth='3', label='Average EO Parkinsons Slope= %.3f'%eo_pdd_lm.params[2])

# eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[0]*x) for x in np.arange(30,66,1)]
# ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

# eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[1]*x) for x in np.arange(30,66,1)]
# ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

# #PDD Lo
# lo_avg = [lo_pdd_lm.params[0]+(lo_pdd_lm.params[2]*x) for x in np.arange(50,90,1)]
# ax[0,1].plot(np.arange(50,90,1), lo_avg, color ='k', linewidth='3', label='Average LO Parkinsons Slope= %.3f'%lo_pdd_lm.params[2])

# lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[0]*x) for x in np.arange(50,90,1)]
# ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

# lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[1]*x) for x in np.arange(50,90,1)]
# ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

# #Ctrl Eo
# eo_matched_avg = [eo_matched_lm.params[0]+(eo_matched_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
# ax[1,0].plot(np.arange(30,66,1), eo_matched_avg, color ='k',linewidth='3', label='Average EO Controls Slope= %.3f'%eo_matched_lm.params[2])

# eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[0]*x) for x in np.arange(30,66,1)]
# ax[1,0].fill_between(np.arange(30,66,1),eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

# eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[1]*x) for x in np.arange(30,66,1)]
# ax[1,0].fill_between(np.arange(30,66,1), eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

# #Ctrl Lo
# lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[0]*x) for x in np.arange(50,90,1)]
# ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)
# lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[1]*x) for x in np.arange(50,90,1)]
# ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)


# #Labels
# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_pdd_lm.params[2]),
#          Line2D([0],[0], color = 'midnightblue',label='Model fit by subject')]
# ax[0,0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k',label='Model Slope= %.3f'%lo_pdd_lm.params[2]),
#          Line2D([0],[0], color = 'firebrick',label='Model fit by subject')]
# ax[0,1].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_matched_lm.params[2]),
#          Line2D([0],[0], color = 'gold',label='Model fit by subject')]
# ax[1,0].legend(handles=legends)

# legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%lo_matched_lm.params[2]),
#          Line2D([0],[0], color = 'blueviolet',label='Model fit by subject')]
# ax[1,1].legend(handles=legends)


    
# ax[0,0].set(ylabel='Parkinsons\n\n MoCA Score')
# ax[1,0].set(xlabel='Age at Test', ylabel='Controls\n\n MoCA Score')
# ax[1,1].set(xlabel='Age at Test')

# ax[0,0].set_ylim([16,30])
# ax[0,1].set_ylim([16,30])
# ax[1,0].set_ylim([16,30])
# ax[1,1].set_ylim([16,30])
# ax[0,0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 12)
# ax[0,1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 12)

# plt.savefig('Full Model MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)




#%%----AVG MoCA Score MGLM ovelap Early-Late Onset PDD vs Ctrl

fig, ax = plt.subplots(1,2)
plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
fig.set_figheight(8)
fig.set_figwidth(12)

#PDD Average
eo_avg = [eo_pdd_lm.params[0]+(eo_pdd_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
ax[0].plot(np.arange(30,66,1), eo_avg, color ='darkblue', linewidth='3', label='Average Parkinsons Slope= %.3f'%eo_pdd_lm.params[2])
lo_avg = [lo_pdd_lm.params[0]+(lo_pdd_lm.params[2]*x) for x in np.arange(50,90,1)]
ax[1].plot(np.arange(50,90,1), lo_avg, color ='darkred', linewidth='3', label='Average Parkinsons Slope= %.3f'%lo_pdd_lm.params[2])


#Ctrls Average
eo_matched_avg = [eo_matched_lm.params[0]+(eo_matched_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
ax[0].plot(np.arange(30,66,1), eo_matched_avg, color ='orange', linestyle='--',linewidth='3', label='Average Controls Slope= %.3f'%eo_matched_lm.params[2])
lo_matched_avg = [lo_matched_lm.params[0]+(lo_matched_lm.params[2]*x) for x in np.arange(50,90,1)]
ax[1].plot(np.arange(50,90,1), lo_matched_avg, color ='darkmagenta', linewidth='3', label='Average Controls Slope= %.3f'%lo_matched_lm.params[2])

#Labels
ax[0].legend()
ax[1].legend()

ax[0].set(xlabel='Age at Test', ylabel='MoCA Score')
ax[1].set(xlabel='Age at Test')
ax[0].set_ylim([20,30])
ax[1].set_ylim([20,30])
ax[0].set_title('Early Onset n='+str(len(eo_subs_matched)+len(eo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
ax[1].set_title('Late Onset n='+str(len(lo_subs_matched)+len(lo_subs_pdd)), pad = 0, fontsize= 10, loc = 'right')
plt.legend()
plt.tight_layout()

plt.savefig('AVG MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%---------------MoCA Score vs age (PDD vs CTRL)

# #Extract parkinsons subjects sorted by onset age 
# sorted_eo_pdd_subs = eo_pdd_db.sort_values('Onset_Age')['Subject_ID'].unique()
# sorted_lo_pdd_subs = lo_pdd_db.sort_values('Onset_Age')['Subject_ID'].unique()

# #Initialize Figure
# fig, ax = plt.subplots(2,1)
# fig.set_figheight(7)
# fig.set_figwidth(14)
# plt.suptitle('Evolution Trayectories MoCA Score vs Age_'+sname, fontsize=16)

# # #Add Fitted Values column
# # eo_pdd_db['Fitted']=eo_pdd_lm.fittedvalues
# # lo_pdd_db['Fitted']=lo_pdd_lm.fittedvalues


# # for i in eo_pdd_db['Subject_ID']:
# #     ages=eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Age_at_Test']
# #     scores=eo_pdd_db[eo_pdd_db['Subject_ID']==i]['MoCA_Scores']
# #     fitted=eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Fitted']
# #     onset=eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Onset_Age']
    
# #     ax[0].plot(ages, scores, color='k', alpha=0.1, marker ='o', markersize=2)
# #     ax[0].plot(ages, fitted, c=cmap(j))


# # positions_pdd = [[j+1]*len(i) for j,i in enumerate(pdd_ranks)]  #Creating lists of positions by slopes rank
# # positions_ctrl = [[j+1]*len(i) for j,i in enumerate(ctrl_ranks)]  #Creating lists of positions by slopes rank

# # df = pd.DataFrame({'Positions_PDD':np.concatenate(positions_pdd), #concatenate all lists to have single data cols
# #                    'Slopes_PDD':np.concatenate(pdd_ranks), 
# #                    'YOE_PDD':np.concatenate(yoe_pdd_list)})

# # ax[0].scatter(df.Positions_PDD, df.Slopes_PDD, c = df.YOE_PDD, cmap='CMRmap', s = 15)

# # df = pd.DataFrame({'Positions_Ctrl':np.concatenate(positions_ctrl),
# #                    'Slopes_Ctrl':np.concatenate(ctrl_ranks),
# #                    'YOE_Ctrl':np.concatenate(yoe_ctrl_list)})

# # ax[1].scatter(df.Positions_Ctrl, df.Slopes_Ctrl, c = df.YOE_Ctrl, cmap='CMRmap', s = 15)



# #Iterate through PDD subjects 
# print('_init_Parkinsons')

# #Extract number of onset ages (one regression line color per onset age) (colorbar length)
# N=len(eo_pdd_db['Onset_Age']) + len(lo_pdd_db['Subject_ID'])
# #Assign Colormap
# cmap = plt.get_cmap('seismic',N)

# #Sorted by onset age order
# for i in sorted_eo_pdd_subs:

#     index = eo_pdd_db[eo_pdd_db['Subject_ID']==i].index
#     scores = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = eo_pdd_lm.fittedvalues.loc[index]
#     onset=list(eo_pdd_db[eo_pdd_db['Subject_ID']==i]['Onset_Age'])[0]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1, marker ='o', markersize=2)
#     ax[0].plot(ages, fitted, c=cmap(onset))

# for i in sorted_lo_pdd_subs:
    
#     index = lo_pdd_db[lo_pdd_db['Subject_ID']==i].index
#     scores = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['MoCA_Scores']
#     ages = lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Age_at_Test']
#     fitted = lo_pdd_lm.fittedvalues.loc[index]
#     onset=list(lo_pdd_db[lo_pdd_db['Subject_ID']==i]['Onset_Age'])[0]
    
#     ax[0].plot(ages, scores, color='k', alpha=0.1, marker ='o', markersize=2)
#     ax[0].plot(ages, fitted, c=cmap(onset))

# #Normalize Colorbar
# N=len(np.concatenate((eo_pdd_db['Onset_Age'].unique(), lo_pdd_db['Subject_ID'].unique)))
# cmap = plt.get_cmap('CMRmap',N)
# norm = mpl.colors.Normalize(vmin=min(np.concatenate((eo_pdd_db['Onset_Age'].unique(), lo_pdd_db['Subject_ID'].unique))),
#                             vmax=max(np.concatenate((eo_pdd_db['Onset_Age'].unique(), lo_pdd_db['Subject_ID'].unique))))
# b = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
# fig.colorbar(b, ax=ax[1], label = 'Years of Education ')

#%%---------------Models Residuals diagnosis


# fig, ax = plt.subplots(1,2)
# plt.suptitle('Early-Late Model Residuals_'+sname, fontsize=16)
# fig.set_figheight(5)
# fig.set_figwidth(12)

# ax[0].set_title('Early Onset Model')
# ax[0].scatter(eo_lm.fittedvalues, eo_lm.resid)
# ax[0].set_xlabel('Fitted Values')
# ax[0].set_ylabel('Residuals')

# ax[1].set_title('Late Onset Model')
# ax[1].scatter(lo_lm.fittedvalues, lo_lm.resid)
# ax[1].set_xlabel('Fitted Values')

#%%

# from statsmodels import graphics

# #Early-Late Models
# graphics.gofplots.qqplot(eo_lm.resid, line='r')
# plt.title('Early Onset Model Q-Q Plot')
# plt.savefig('EO LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

# graphics.gofplots.qqplot(lo_lm.resid, line='r')
# plt.title('Late Onset Model Q-Q Plot')
# plt.savefig('LO LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

# #PD vs Ctrl Models

# graphics.gofplots.qqplot(pdd_lm.resid, line='r')
# plt.title('Parkinsons Model Q-Q Plot')
# plt.savefig('PD LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

# graphics.gofplots.qqplot(ctrl_lm.resid, line='r')
# plt.title('Controls Model Q-Q Plot')
# plt.savefig('Ctrl LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)


#%%---------------------------FRESH START--------------------------------------

VER = '2.1'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import easygui as eg
import os                #Sirve para el Manejo de archivos
#import statsmodels.api as sm
import statsmodels.formula.api as smf
#import matplotlib as mpl
from matplotlib.lines import Line2D
from statsmodels import graphics
from scipy import stats as sp
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

os.chdir('C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto') #Carpeta de trabajo [modificable]

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Linear-ICE"+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Linear-ICE "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Parkinsons LINMOD MoCA File'
title = "Linear-ICE "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pdd_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Controls LINMOD MoCA File'
title = "Linear-ICE "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_path = temp_path.replace(os.path.sep ,"/")

# #Session Open File
# message = 'Please Select Prodromals LINMOD MoCA File'
# title = "Linear-ICE "+VER+" - "
# temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
# prod_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Parkinsons LINMOD HY File'
title = "Linear-ICE "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
pdd_hy_path = temp_path.replace(os.path.sep ,"/")

#Session Open File
message = 'Please Select Controls LINMOD HY File'
title = "Linear-ICE "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
ctrl_hy_path = temp_path.replace(os.path.sep ,"/")

# #Session Open File
# message = 'Please Select Prodromals LINMOD HY File'
# title = "Linear-ICE "+VER+" - "
# temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
# prod_hy_path = temp_path.replace(os.path.sep ,"/")

#-------Change working directory to save path 
os.chdir(sv_path)

#%%-----DATA LOAD

pdd_csvfile = pd.read_csv(pdd_path)  
ctrl_csvfile = pd.read_csv(ctrl_path)  
#prod_csvfile = pd.read_csv(prod_path)  

pdd_hy_csvfile = pd.read_csv(pdd_hy_path)  
ctrl_hy_csvfile = pd.read_csv(ctrl_hy_path) 
#prod_hy_csvfile = pd.read_csv(prod_hy_path)

pdd_hy_corrected = pd.read_csv(pdd_hy_path)  
ctrl_hy_corrected = pd.read_csv(ctrl_hy_path) 
#prod_hy_corrected = pd.read_csv(prod_hy_path)  

#-------------MoCA Compensation to raw data correction (+1 pt in subs with <=12 YOE)
pdd_corrected = pdd_csvfile.copy()
ctrl_corrected = ctrl_csvfile.copy()
#prod_corrected = prod_csvfile.copy()

#PDD
for index, row in pdd_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =pdd_corrected['MoCA_Scores'][index]
        pdd_corrected.loc[index,'MoCA_Scores'] = prev-1

#Ctrl
for index, row in ctrl_corrected.iterrows():
    if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
        prev =ctrl_corrected['MoCA_Scores'][index]
        ctrl_corrected.loc[index,'MoCA_Scores'] = prev-1
        
# #Prodromal
# for index, row in prod_corrected.iterrows():
#     if row['Years_of_education'] <= 12: #Selects only subjects with less than 12 YOE
#         prev =prod_corrected['MoCA_Scores'][index]
#         prod_corrected.loc[index,'MoCA_Scores'] = prev-1


#%%-----Database Merge / Early-Late Onset selection MoCA  PD-Ctrl

merged_db = pd.concat([pdd_corrected, ctrl_corrected], ignore_index=True)

#---------------Extract subjects 

#Longitudinal
eo_l_subs_pd =[]
lo_l_subs_pd =[]
eo_l_subs_matched =[]
lo_l_subs_matched =[]
#Single 
eo_s_subs_pd =[]
lo_s_subs_pd =[]
eo_s_subs_matched =[]
lo_s_subs_matched =[]

#Parkinsons

allsubs = pdd_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(pdd_csvfile[pdd_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if pdd_csvfile[pdd_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55:
            eo_l_subs_pd.append(i)
        
        else:
            lo_l_subs_pd.append(i)
    else: #Single Subjects 
        #Extract Subjects 
        if pdd_csvfile[pdd_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55:
            eo_s_subs_pd.append(i)
        else:
            lo_s_subs_pd.append(i)
        
        

#Controls

allsubs = ctrl_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55:
            eo_l_subs_matched.append(i)
        
        else:
            lo_l_subs_matched.append(i)
    else:
        #Extract Subjects 
        if ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55:
            eo_s_subs_matched.append(i)
        
        else:
            lo_s_subs_matched.append(i)



#Separate databases by subject group
whole_eo_subs=eo_l_subs_pd + eo_l_subs_matched + eo_s_subs_pd + eo_s_subs_matched
whole_lo_subs=lo_l_subs_pd + lo_l_subs_matched + lo_s_subs_pd + lo_s_subs_matched

eo_db = merged_db.loc[merged_db['Subject_ID'].isin(whole_eo_subs)]
lo_db = merged_db.loc[merged_db['Subject_ID'].isin(whole_lo_subs)]


#----------Add Years Since Onset to PD Database

tmp = pdd_corrected['Age_at_Test']-pdd_corrected['Onset_Age']
pdd_corrected['YSO']=tmp #Years Since Onset column

#----------Add Early-Late Flag

tmp = pd.Series(np.zeros(len(pdd_corrected)))
pdd_corrected['EoL']=tmp   #Early or Late column
pdd_corrected['EoL']= pdd_corrected['EoL'].astype(str) 
pdd_corrected.loc[pdd_corrected['Subject_ID'].isin(eo_s_subs_pd+eo_l_subs_pd), 'EoL'] = 'Early'
pdd_corrected.loc[pdd_corrected['Subject_ID'].isin(lo_s_subs_pd+lo_l_subs_pd), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(ctrl_corrected)))
ctrl_corrected['EoL']=tmp
ctrl_corrected['EoL']= ctrl_corrected['EoL'].astype(str) 
ctrl_corrected.loc[ctrl_corrected['Subject_ID'].isin(eo_s_subs_matched+eo_l_subs_matched), 'EoL'] = 'Early'
ctrl_corrected.loc[ctrl_corrected['Subject_ID'].isin(lo_s_subs_matched+lo_l_subs_matched), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(merged_db)))
merged_db['EoL']=tmp
merged_db['EoL']= merged_db['EoL'].astype(str) 
merged_db.loc[merged_db['Subject_ID'].isin(eo_s_subs_pd+eo_l_subs_pd+eo_s_subs_matched+eo_l_subs_matched), 'EoL'] = 'Early'
merged_db.loc[merged_db['Subject_ID'].isin(lo_s_subs_pd+lo_l_subs_pd+lo_s_subs_matched+lo_l_subs_matched), 'EoL'] = 'Late'

#--------------------Scaler

pd_db_scaled = pdd_corrected.copy()     #Parkinsons Database
ctrl_db_scaled = ctrl_corrected.copy() #Controls Database
merged_db_scaled = merged_db.copy() #Parkinsons + Controls Database 

var = ['Years_of_education','Age_at_Test']

scaler = StandardScaler()
pd_db_scaled[var+['YSO','Onset_Age','Diagnosis_Age']] = scaler.fit_transform(pd_db_scaled[var+['YSO','Onset_Age','Diagnosis_Age']])
ctrl_db_scaled[var] = scaler.fit_transform(ctrl_db_scaled[var])
merged_db_scaled[var] = scaler.fit_transform(merged_db_scaled[var])


#%%-----Database Merge / Early-Late Onset selection MoCA  PD-Ctrl


#------------------ Status Value replace 

pdd_hy_corrected['HY_Status']=pdd_hy_corrected['HY_Status'].replace('NoTrtOFF',0)
pdd_hy_corrected['HY_Status']=pdd_hy_corrected['HY_Status'].replace('OFF',0)
pdd_hy_corrected['HY_Status']=pdd_hy_corrected['HY_Status'].replace('ON',1)

ctrl_hy_corrected['HY_Status']=ctrl_hy_corrected['HY_Status'].replace('NoTrtOFF',0)

#------------------DB merge

merged_db_hy = pd.concat([pdd_hy_corrected, ctrl_hy_corrected], ignore_index=True)


#---------------Extract subjects 

#Longitudinal
eo_l_subs_pd_hy =[]
lo_l_subs_pd_hy =[]
eo_l_subs_matched_hy =[]
lo_l_subs_matched_hy =[]
#Single 
eo_s_subs_pd_hy =[]
lo_s_subs_pd_hy =[]
eo_s_subs_matched_hy =[]
lo_s_subs_matched_hy =[]

#Parkinsons

allsubs = pdd_hy_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(pdd_hy_csvfile[pdd_hy_csvfile['Subject_ID']==i]['HY_Scores'])>1:
        #Extract Subjects 
        if pdd_hy_csvfile[pdd_hy_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55:
            eo_l_subs_pd_hy.append(i)
        
        else:
            lo_l_subs_pd_hy.append(i)
    else: #Single Subjects 
        #Extract Subjects 
        if pdd_hy_csvfile[pdd_hy_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 55:
            eo_s_subs_pd_hy.append(i)
        else:
            lo_s_subs_pd_hy.append(i)
        
        

#Controls

allsubs = ctrl_hy_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(ctrl_hy_csvfile[ctrl_hy_csvfile['Subject_ID']==i]['HY_Scores'])>1:
        #Extract Subjects 
        if ctrl_hy_csvfile[ctrl_hy_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55:
            eo_l_subs_matched_hy.append(i)
        
        else:
            lo_l_subs_matched_hy.append(i)
    else:
        #Extract Subjects 
        if ctrl_hy_csvfile[ctrl_hy_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 55:
            eo_s_subs_matched_hy.append(i)
        
        else:
            lo_s_subs_matched_hy.append(i)



#Separate databases by subject group
whole_eo_subs_hy=eo_l_subs_pd_hy + eo_l_subs_matched_hy + eo_s_subs_pd_hy + eo_s_subs_matched_hy
whole_lo_subs_hy=lo_l_subs_pd_hy + lo_l_subs_matched_hy + lo_s_subs_pd_hy + lo_s_subs_matched_hy

eo_db_hy = merged_db_hy.loc[merged_db_hy['Subject_ID'].isin(whole_eo_subs_hy)]
lo_db_hy = merged_db_hy.loc[merged_db_hy['Subject_ID'].isin(whole_lo_subs_hy)]


#----------Add Years Since Onset to PD Database

tmp = pdd_hy_corrected['Age_at_Test']-pdd_hy_corrected['Onset_Age']
pdd_hy_corrected['YSO']=tmp #Years Since Onset column

#----------Add Early-Late Flag

tmp = pd.Series(np.zeros(len(pdd_hy_corrected)))
pdd_hy_corrected['EoL']=tmp   #Early or Late column
pdd_hy_corrected['EoL']= pdd_hy_corrected['EoL'].astype(str) 
pdd_hy_corrected.loc[pdd_hy_corrected['Subject_ID'].isin(eo_s_subs_pd_hy+eo_l_subs_pd_hy), 'EoL'] = 'Early'
pdd_hy_corrected.loc[pdd_hy_corrected['Subject_ID'].isin(lo_s_subs_pd_hy+lo_l_subs_pd_hy), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(ctrl_hy_corrected)))
ctrl_hy_corrected['EoL']=tmp
ctrl_hy_corrected['EoL']= ctrl_hy_corrected['EoL'].astype(str) 
ctrl_hy_corrected.loc[ctrl_hy_corrected['Subject_ID'].isin(eo_s_subs_matched_hy+eo_l_subs_matched_hy), 'EoL'] = 'Early'
ctrl_hy_corrected.loc[ctrl_hy_corrected['Subject_ID'].isin(lo_s_subs_matched_hy+lo_l_subs_matched_hy), 'EoL'] = 'Late'

tmp = pd.Series(np.zeros(len(merged_db_hy)))
merged_db_hy['EoL']=tmp
merged_db_hy['EoL']= merged_db_hy['EoL'].astype(str) 
merged_db_hy.loc[merged_db_hy['Subject_ID'].isin(eo_s_subs_pd_hy+eo_l_subs_pd_hy+eo_s_subs_matched_hy+eo_l_subs_matched_hy), 'EoL'] = 'Early'
merged_db_hy.loc[merged_db_hy['Subject_ID'].isin(lo_s_subs_pd_hy+lo_l_subs_pd_hy+lo_s_subs_matched_hy+lo_l_subs_matched_hy), 'EoL'] = 'Late'

#--------------------Scaler

pd_db_hy_scaled = pdd_hy_corrected.copy()     #Parkinsons Database
ctrl_db_hy_scaled = ctrl_hy_corrected.copy() #Controls Database
merged_db_hy_scaled = merged_db_hy.copy() #Parkinsons + Controls Database 

var = ['Years_of_education','Age_at_Test']

scaler = StandardScaler()
pd_db_hy_scaled[var+['YSO','Onset_Age','Diagnosis_Age']] = scaler.fit_transform(pd_db_hy_scaled[var+['YSO','Onset_Age','Diagnosis_Age']])
ctrl_db_hy_scaled[var] = scaler.fit_transform(ctrl_db_hy_scaled[var])
merged_db_hy_scaled[var] = scaler.fit_transform(merged_db_hy_scaled[var])




#%%-----Early / Late Models + Interaction 

#Early Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education ", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model')
print(eo_lm.summary())

#Late Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model')
print(lo_lm.summary())


#Early Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model + interaction')
print(eo_lm.summary())

#Late Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model + interaction')
print(lo_lm.summary())

#--------Change ref levels

#Early Onset
eo_db2= eo_db.copy()
eo_db2['Group'] = (eo_db2['Group']=='Control').astype(int) 

lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education + Group*Age_at_Test", 
                 eo_db2, groups=eo_db2["Subject_ID"], re_formula='~Age_at_Test')
eo_lm_inv = lm.fit()
print('\n\n\nPD Ref Early Onset Model')
print(eo_lm_inv.summary())


#Late Onset
lo_db2 = lo_db.copy()
lo_db2['Group']= (lo_db2['Group']=='Control').astype(int)
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
                 lo_db2, groups=lo_db2["Subject_ID"], re_formula='~Age_at_Test')
lo_lm_inv = lm.fit()
print('\nPD Ref Late Onset Model')
print(lo_lm_inv.summary())



#%%-----Early / Late Models Residuals diagnosis


fig, ax = plt.subplots(1,2)
plt.suptitle('Early-Late Model Residuals_'+sname, fontsize=16)
fig.set_figheight(5)
fig.set_figwidth(12)

ax[0].set_title('Early Onset Model')
ax[0].scatter(eo_lm.fittedvalues, eo_lm.resid)
ax[0].set_xlabel('Fitted Values')
ax[0].set_ylabel('Residuals')

ax[1].set_title('Late Onset Model')
ax[1].scatter(lo_lm.fittedvalues, lo_lm.resid)
ax[1].set_xlabel('Fitted Values')
plt.savefig('EO-LO LM Residuals_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#Early-Late Models
graphics.gofplots.qqplot(eo_lm.resid, line='r')
plt.title('Early Onset Model Q-Q Plot')
plt.savefig('EO LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

graphics.gofplots.qqplot(lo_lm.resid, line='r')
plt.title('Late Onset Model Q-Q Plot')
plt.savefig('LO LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%-----PD / Ctrl Models + Interaction 

#PDD Model
lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
                 pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model')
print(pdd_lm.summary())

lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model 2')
print(pdd_lm.summary())

#Ctrl Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 ctrl_corrected, groups=ctrl_corrected["Subject_ID"], re_formula='~Age_at_Test')
ctrl_lm = lm.fit()
print('\nCtrl Model')
print(ctrl_lm.summary())

#Merge Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm = lm.fit()
print('\nMerged Model')
print(merged_lm.summary())

#Merge Model + interaction
merged_db = pd.concat([pdd_corrected, ctrl_corrected])
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group+ Age_at_Test*Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm_i = lm.fit()
print('\nMerged Model + interaction')
print(merged_lm_i.summary())

#%%-----PD / Ctrl / Merge Models Residuals diagnosis


fig, ax = plt.subplots(1,3)
plt.suptitle('PD - Ctrl - Merged Model Residuals_'+sname, fontsize=16)
fig.set_figheight(5)
fig.set_figwidth(15)

ax[0].set_title('PD Model')
ax[0].scatter(pdd_lm.fittedvalues, pdd_lm.resid)
ax[0].set_xlabel('Fitted Values')
ax[0].set_ylabel('Residuals')

ax[1].set_title('Ctrl Model')
ax[1].scatter(ctrl_lm.fittedvalues, ctrl_lm.resid)
ax[1].set_xlabel('Fitted Values')

ax[2].set_title('Merged Model')
ax[2].scatter(merged_lm.fittedvalues, merged_lm.resid)
ax[2].set_xlabel('Fitted Values')

plt.savefig('PD-Ctrl-Merged LM Residuals_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#QQ Plots
graphics.gofplots.qqplot(pdd_lm.resid, line='r')
plt.title('PD Model Q-Q Plot')
plt.savefig('PD LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

graphics.gofplots.qqplot(ctrl_lm.resid, line='r')
plt.title('Ctrl Model Q-Q Plot')
plt.savefig('Ctrl LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

graphics.gofplots.qqplot(merged_lm.resid, line='r')
plt.title('Merged Model Q-Q Plot')
plt.savefig('Merged LM QQPlot_'+(os.path.basename(sv_path)[:-4])+'_'+sname)

#%%-----Database Merge / Early-Late Onset selection MoCA (ONLY LONGITUDINALS) PD-Ctrl-Prod

merged_db = pd.concat([pdd_corrected, ctrl_corrected, prod_corrected], ignore_index=True)

#---------------Extract subjects 

eo_subs_pdd =[]
lo_subs_pdd =[]

eo_subs_matched =[]
lo_subs_matched =[]

eo_subs_prod =[]
lo_subs_prod =[]

#Parkinsons

allsubs = pdd_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(pdd_csvfile[pdd_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if pdd_csvfile[pdd_csvfile['Subject_ID']==i]['Onset_Age'].value_counts().index[0] < 50:
            eo_subs_pdd.append(i)
        
        else:
            lo_subs_pdd.append(i)


#Controls

allsubs = ctrl_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if ctrl_csvfile[ctrl_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 50:
            eo_subs_matched.append(i)
        
        else:
            lo_subs_matched.append(i)


#Prodromals

allsubs = prod_csvfile['Subject_ID'].value_counts()
allsubs= allsubs.sort_index()
allsubs=allsubs.index

for i in allsubs:
    #Only Subjects with more than 1 MoCA eval 
    if len(prod_csvfile[prod_csvfile['Subject_ID']==i]['MoCA_Scores'])>1:
        #Extract Subjects 
        if prod_csvfile[prod_csvfile['Subject_ID']==i]['Age_at_Test'].value_counts().index[0] < 50:
            eo_subs_prod.append(i)
        
        else:
            lo_subs_prod.append(i)

#Separate databases by subject group
whole_eo_subs=eo_subs_pdd + eo_subs_matched + eo_subs_prod
whole_lo_subs=lo_subs_pdd + lo_subs_matched + lo_subs_prod

eo_db = merged_db.loc[merged_db['Subject_ID'].isin(whole_eo_subs)]
lo_db = merged_db.loc[merged_db['Subject_ID'].isin(whole_lo_subs)]

#%%-----Prodomals Models----------------------------

#PDD Model
# lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
#                  pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
# pdd_lm = lm.fit()
# print('\n\n\nPDD Model')
# print(pdd_lm.summary())

lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model 2')
print(pdd_lm.summary())

#Ctrl Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 ctrl_corrected, groups=ctrl_corrected["Subject_ID"], re_formula='~Age_at_Test')
ctrl_lm = lm.fit()
print('\nCtrl Model')
print(ctrl_lm.summary())

#Prod Model
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 prod_corrected, groups=prod_corrected["Subject_ID"], re_formula='~Age_at_Test')
prod_lm = lm.fit()
print('\n\n\nprod Model 2')
print(prod_lm.summary())

#Merge Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm = lm.fit()
print('\nMerged Model')
print(merged_lm.summary())

#Merge Model + interaction
#merged_db = pd.concat([pdd_corrected, ctrl_corrected])
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group+ Age_at_Test*Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm_i = lm.fit()
print('\nMerged Model + interaction')
print(merged_lm_i.summary())




#%%-----------------------Plots------------------------------------------------
#%%-----First MoCA Score Early vs Late 

#Early onset first moca Scores
eo_fm_scores = eo_db[eo_db['Test_Number']==1]

#Late onset first moca Scores 
lo_fm_scores = lo_db[lo_db['Test_Number']==1] 


#------Group separation 

eo_fm_pd = np.array(eo_fm_scores[eo_fm_scores['Group']=='PD']['MoCA_Scores'])
eo_fm_ctrl= np.array(eo_fm_scores[eo_fm_scores['Group']=='Control']['MoCA_Scores'])

lo_fm_pd = np.array(lo_fm_scores[lo_fm_scores['Group']=='PD']['MoCA_Scores'])
lo_fm_ctrl= np.array(lo_fm_scores[lo_fm_scores['Group']=='Control']['MoCA_Scores'])


#-----Stats

#Normality 

n= 0
for i in [eo_fm_pd, lo_fm_pd, eo_fm_pd, eo_fm_ctrl]:
    normal = sp.shapiro(i)
    print(str(normal))
    if normal.pvalue < 0.05:
        n=1


#Between Groups
pvals_bg=[]

if n == 1: #Data not normal
    pvals_bg.append(sp.mannwhitneyu(eo_fm_pd,eo_fm_ctrl)[1]) #Early Onset PD vs Ctrl
    pvals_bg.append(sp.mannwhitneyu(lo_fm_pd,lo_fm_ctrl)[1]) #Late Onset PD vs Ctrl
    
#Within Groups
pvals_wg=[]  
if n == 1: #Data not normal
    pvals_wg.append(sp.mannwhitneyu(eo_fm_pd,lo_fm_pd)[1]) #Early Onset vs late onset PD
    pvals_wg.append(sp.mannwhitneyu(eo_fm_ctrl,lo_fm_ctrl)[1]) #Early Onset vs Late Onset Ctrl
    

#----Plot

fig, ax = plt.subplots()
fig.set_figheight(7)
fig.set_figwidth(8)
plt.suptitle('First MoCA Score by group', fontsize = 16)
if n==1:
    plt.title('U Mann-Whitney Test', fontsize=10, loc='right', pad=0)
    
##
#PDD Boxplot 
colors = ['steelblue']*2
bplot = ax.boxplot([eo_fm_pd,lo_fm_pd], positions=[1,2], notch=True, showfliers=False, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

#Controls Boxplot
colors = ['green']*2
bplot=ax.boxplot([eo_fm_ctrl,lo_fm_ctrl], positions=[1.2,2.2], notch = True, showfliers=False, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
##

plt.xticks([1,2],['Early Onset','Late Onset'])


plt.xlabel('Groups')
plt.ylabel('MoCA Score')

legends=[Line2D([0],[0], color = 'Steelblue',label='Parkinsons'),
         Line2D([0],[0], color = 'Green',label='Controls')]

#Tests between groups 
plt.text(1,20.1,'p=%.4f'%pvals_bg[0], fontsize = 7)
plt.text(2,20.1,'p=%.4f'%pvals_bg[1], fontsize = 7, color='red')
plt.plot([1,1.2],[20,20], color ='k')
plt.plot([2,2.2],[20,20], color ='k')

#Tests within groups
plt.text(1.4,19.6,'p=%.4f'%pvals_wg[0], fontsize = 7, color = 'red')
plt.text(1.6,19,'p=%.4f'%pvals_wg[1], fontsize = 7)
plt.plot([1,2],[19.5,19.5], color ='k')
plt.plot([1.2,2.2],[18.9,18.9], color ='k')

plt.legend(handles=legends)
plt.tight_layout()
plt.savefig('First MoCA Score by Group_'+(os.path.basename(sv_path)[:-4])+'_'+sname)



#%%---------MoCA Score vs Age Model Fitted values (EO-LO MODELS)
fig, ax = plt.subplots(3,1)
plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
fig.set_figheight(8)
fig.set_figwidth(12)


for i in whole_eo_subs:
    index = merged_db[merged_db['Subject_ID']==i].index
    scores = merged_db[merged_db['Subject_ID']==i]['MoCA_Scores']
    ages = merged_db[merged_db['Subject_ID']==i]['Age_at_Test']
    fitted = eo_lm.fittedvalues.loc[index]
    
    #ax[0,0].plot(ages, scores, color='k', alpha=0.1)
    if i in eo_subs_pdd:
        ax.plot(ages, fitted, color ='midnightblue')
        
    elif i in eo_subs_matched:
        ax.plot(ages, fitted, color ='gold')
    
    elif i in eo_subs_prod:
        ax.plot(ages, fitted, color ='mediumvioletred')
    

for i in whole_lo_subs:
    index = lo_db[lo_db['Subject_ID']==i].index
    scores = lo_db[lo_db['Subject_ID']==i]['MoCA_Scores']
    ages = lo_db[lo_db['Subject_ID']==i]['Age_at_Test']
    fitted = lo_lm.fittedvalues.loc[index]
    
    #ax[0,1].plot(ages, scores, color='k', alpha=0.1)
    if i in lo_subs_pdd:
        ax.plot(ages, fitted, color ='firebrick')
    
    elif i in lo_subs_matched:
        ax.plot(ages, fitted, color ='blueviolet')
        
    elif i in lo_subs_prod:
        ax.plot(ages, fitted, color ='forestgreen')

ax[0].set(ylabel='Parkinsons\n\n MoCA Score')
ax[0].set(xlabel='Age at Test')
ax[1].set(xlabel='Age at Test')

ax[0].set_ylim([16,30])
ax[1].set_ylim([16,30])
ax[0].set_ylim([16,30])
ax[1].set_ylim([16,30])
ax[0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 12)
ax[1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 12)


#------------


lo_matched_avg = [lo_matched_lm.params[0]+(lo_matched_lm.params[2]*x) for x in np.arange(50,90,1)]
ax[1,1].plot(np.arange(50,90,1), lo_matched_avg, color ='k', linewidth='3', label='Average LO Controls Slope= %.3f'%lo_matched_lm.params[2])

eo_pdd_ci=eo_pdd_lm.conf_int().loc['Age_at_Test']
lo_pdd_ci=lo_pdd_lm.conf_int().loc['Age_at_Test']
eo_matched_ci=eo_matched_lm.conf_int().loc['Age_at_Test']
lo_matched_ci=lo_matched_lm.conf_int().loc['Age_at_Test']

#----------Averages + Ci Intervals
#PDD Eo
eo_avg = [eo_pdd_lm.params[0]+(eo_pdd_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
ax[0,0].plot(np.arange(30,66,1), eo_avg, color ='k', linewidth='3', label='Average EO Parkinsons Slope= %.3f'%eo_pdd_lm.params[2])

eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[0]*x) for x in np.arange(30,66,1)]
ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

eo_avg_ci = [eo_pdd_lm.params[0]+(eo_pdd_ci.iloc[1]*x) for x in np.arange(30,66,1)]
ax[0,0].fill_between(np.arange(30,66,1),eo_avg,eo_avg_ci, color = 'k', alpha=0.2, linewidth=0)

#PDD Lo
lo_avg = [lo_pdd_lm.params[0]+(lo_pdd_lm.params[2]*x) for x in np.arange(50,90,1)]
ax[0,1].plot(np.arange(50,90,1), lo_avg, color ='k', linewidth='3', label='Average LO Parkinsons Slope= %.3f'%lo_pdd_lm.params[2])

lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[0]*x) for x in np.arange(50,90,1)]
ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

lo_avg_ci = [lo_pdd_lm.params[0]+(lo_pdd_ci.iloc[1]*x) for x in np.arange(50,90,1)]
ax[0,1].fill_between(np.arange(50,90,1),lo_avg, lo_avg_ci, color ='k', alpha=0.2, linewidth=0)

#Ctrl Eo
eo_matched_avg = [eo_matched_lm.params[0]+(eo_matched_lm.params[2]*x) for x in np.arange(30,66,1)] #Intercept + Age_at_Test slope (coef)
ax[1,0].plot(np.arange(30,66,1), eo_matched_avg, color ='k',linewidth='3', label='Average EO Controls Slope= %.3f'%eo_matched_lm.params[2])

eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[0]*x) for x in np.arange(30,66,1)]
ax[1,0].fill_between(np.arange(30,66,1),eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

eo_matched_avg_ci = [eo_matched_lm.params[0]+(eo_matched_ci.iloc[1]*x) for x in np.arange(30,66,1)]
ax[1,0].fill_between(np.arange(30,66,1), eo_matched_avg, eo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)

#Ctrl Lo
lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[0]*x) for x in np.arange(50,90,1)]
ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)
lo_matched_avg_ci = [lo_matched_lm.params[0]+(lo_matched_ci.iloc[1]*x) for x in np.arange(50,90,1)]
ax[1,1].fill_between(np.arange(50,90,1), lo_matched_avg, lo_matched_avg_ci, color ='k', alpha=0.2, linewidth=0)


#Labels
legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_pdd_lm.params[2]),
         Line2D([0],[0], color = 'midnightblue',label='Model fit by subject')]
ax[0,0].legend(handles=legends)

legends=[Line2D([0],[0], color = 'k',label='Model Slope= %.3f'%lo_pdd_lm.params[2]),
         Line2D([0],[0], color = 'firebrick',label='Model fit by subject')]
ax[0,1].legend(handles=legends)

legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%eo_matched_lm.params[2]),
         Line2D([0],[0], color = 'gold',label='Model fit by subject')]
ax[1,0].legend(handles=legends)

legends=[Line2D([0],[0], color = 'k', label='Model Slope= %.3f'%lo_matched_lm.params[2]),
         Line2D([0],[0], color = 'blueviolet',label='Model fit by subject')]
ax[1,1].legend(handles=legends)


    

# plt.savefig('E-L LM MoCA Score vs AGE GLM_'+(os.path.basename(sv_path)[:-4])+'_'+sname)
#%%---------MoCA Score vs Age Model Fitted values (PD-CTRL-PROD MODELS)
fig, ax = plt.subplots(3,1)
plt.suptitle('MoCA Score vs Age MLM '+sname, fontsize=16)
fig.set_figheight(8)
fig.set_figwidth(12)

for i in 


for i in whole_eo_subs:
    index = merged_db[merged_db['Subject_ID']==i].index
    scores = merged_db[merged_db['Subject_ID']==i]['MoCA_Scores']
    ages = merged_db[merged_db['Subject_ID']==i]['Age_at_Test']
    fitted = eo_lm.fittedvalues.loc[index]
    
    #ax[0,0].plot(ages, scores, color='k', alpha=0.1)
    if i in eo_subs_pdd:
        ax.plot(ages, fitted, color ='midnightblue')
        
    elif i in eo_subs_matched:
        ax.plot(ages, fitted, color ='gold')
    
    elif i in eo_subs_prod:
        ax.plot(ages, fitted, color ='mediumvioletred')
    

for i in whole_lo_subs:
    index = lo_db[lo_db['Subject_ID']==i].index
    scores = lo_db[lo_db['Subject_ID']==i]['MoCA_Scores']
    ages = lo_db[lo_db['Subject_ID']==i]['Age_at_Test']
    fitted = lo_lm.fittedvalues.loc[index]
    
    #ax[0,1].plot(ages, scores, color='k', alpha=0.1)
    if i in lo_subs_pdd:
        ax.plot(ages, fitted, color ='firebrick')
    
    elif i in lo_subs_matched:
        ax.plot(ages, fitted, color ='blueviolet')
        
    elif i in lo_subs_prod:
        ax.plot(ages, fitted, color ='forestgreen')

ax[0].set(ylabel='Parkinsons\n\n MoCA Score')
ax[0].set(xlabel='Age at Test')
ax[1].set(xlabel='Age at Test')

ax[0].set_ylim([16,30])
ax[1].set_ylim([16,30])
ax[0].set_ylim([16,30])
ax[1].set_ylim([16,30])
ax[0].set_title('Early Onset n='+str(len(eo_subs_pdd)), pad = 0, fontsize= 12)
ax[1].set_title('Late Onset n='+str(len(lo_subs_pdd)), pad = 0, fontsize= 12)
#%%-----MoCA Slope vs onset age + lin / exp / sqr adjust

pd_slopes= np.array(merged_db[((merged_db['Group']=='PD') & (merged_db['Test_Number']==1))]['Slope'])
pd_onset= np.array(merged_db[((merged_db['Group']=='PD') & (merged_db['Test_Number']==1))]['Onset_Age'])

ctrl_slopes= np.array(merged_db[((merged_db['Group']=='Control') & (merged_db['Test_Number']==1))]['Slope'])
ctrl_onset =  np.array(merged_db[((merged_db['Group']=='Control') & (merged_db['Test_Number']==1))]['Age_at_Test'])

#---Linear regression 

x_lr= pd_onset.reshape((-1,1))
pd_linear = LinearRegression().fit(x_lr,pd_slopes)
pd_l_x = np.arange(24,90,1)
pd_l_y = pd_linear.predict(pd_l_x.reshape((-1,1)))

x_lr = ctrl_onset.reshape((-1,1))
ctrl_linear= LinearRegression().fit(x_lr,ctrl_slopes)
ctrl_l_x = np.arange(24,90,1)
ctrl_l_y = ctrl_linear.predict(ctrl_l_x.reshape((-1,1)))


#-----Exponential regression 

pd_exponential = np.polyfit(pd_onset, np.log(pd_slopes),1)


#-----Quadratic regression 

pd_quadratic = np.poly1d(np.polyfit(pd_onset, pd_slopes,2))
pd_q_x=np.arange(24,90,1)
pd_q_y=pd_quadratic(pd_q_x)

ctrl_quadratic = np.poly1d(np.polyfit(ctrl_onset, ctrl_slopes,2))
ctrl_q_x=np.arange(24,90,1)
ctrl_q_y=pd_quadratic(ctrl_q_x)

#----Plots 

fig, ax = plt.subplots(2,1)
plt.suptitle('Onset age vs Slope Adjusts')

#Raw Data
ax[0].scatter(pd_onset,pd_slopes, alpha =0.5)
ax[1].scatter(ctrl_onset, ctrl_slopes, color = 'green', alpha =0.5)

#Linear Regression 
ax[0].plot(pd_l_x,pd_l_y, color='k', linewidth=2)
ax[1].plot(ctrl_l_x, ctrl_l_y, color='k', linewidth=2)

#Quadratic regression 

ax[0].plot(pd_q_x, pd_q_y, linestyle='--', color ='red', linewidth=2)
ax[1].plot(ctrl_q_x, ctrl_q_y, linestyle='--', color ='red', linewidth=2)



#%%-----Early / Late Models + Interaction 

#Early Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education ", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model (Long+Single)')
print(eo_lm.summary())

#Late Onset
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model (Long+Single)')
print(lo_lm.summary())


#Early Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 eo_db, groups=eo_db["Subject_ID"], re_formula='~Age_at_Test')
eo_lm = lm.fit()
print('\n\n\nEarly Onset Model + interaction (Long+Single)')
print(eo_lm.summary())

#Late Onset +interaction 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Age_at_Test + Group + Years_of_education +Group*Age_at_Test", 
                 lo_db, groups=lo_db["Subject_ID"], re_formula='~Age_at_Test')
lo_lm = lm.fit()
print('\nLate Onset Model + interaction (Long+Single)')
print(lo_lm.summary())

#%%-----PD / Ctrl Models + Interaction 

#PDD Model
lm = smf.mixedlm("MoCA_Scores ~ Sex + Onset_Age + Diagnosis_Age + Years_of_education + Age_at_Test", 
                 pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model (Long+Single)')
print(pdd_lm.summary())

lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 pdd_corrected, groups=pdd_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model 2 (Long+Single)')
print(pdd_lm.summary())

#Ctrl Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test", 
                 ctrl_corrected, groups=ctrl_corrected["Subject_ID"], re_formula='~Age_at_Test')
ctrl_lm = lm.fit()
print('\nCtrl Model (Long+Single)')
print(ctrl_lm.summary())

#Merge Model 
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm = lm.fit()
print('\nMerged Model')
print(merged_lm.summary())

#Merge Model + interaction
merged_db = pd.concat([pdd_corrected, ctrl_corrected])
lm = smf.mixedlm("MoCA_Scores ~ Sex + Years_of_education + Age_at_Test + Group+ Age_at_Test*Group", 
                 merged_db, groups=merged_db["Subject_ID"], re_formula='~Age_at_Test')
merged_lm_i = lm.fit()
print('\nMerged Model + interaction')
print(merged_lm_i.summary())


#%%////////////////////////////////HY\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#%%-----PD / Ctrl Models + Interaction 

#PDD Model
lm = smf.mixedlm("HY_Scores ~ Sex + Years_of_education + Age_at_Test + EoL + HY_Status +YSO", 
                 pd_db_hy_scaled, groups=pd_db_hy_scaled["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model Scaled (Long+Single)')
print(pdd_lm.summary())

lm = smf.mixedlm("HY_Scores ~ Sex + Years_of_education + Age_at_Test + EoL + HY_Status +YSO", 
                 pdd_hy_corrected, groups=pdd_hy_corrected["Subject_ID"], re_formula='~Age_at_Test')
pdd_lm = lm.fit()
print('\n\n\nPDD Model (Long+Single)')
print(pdd_lm.summary())

