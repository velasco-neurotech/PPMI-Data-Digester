"""
Created on Tue Nov 26 11:31:18 2024

 ______     __         __     __   __     __        ______   ______     ______     __  __    
/\  ___\   /\ \       /\ \   /\ "-.\ \   /\ \      /\__  _\ /\  == \   /\  __ \   /\ \/ /    
\ \ \____  \ \ \____  \ \ \  \ \ \-.  \  \ \ \     \/_/\ \/ \ \  __<   \ \  __ \  \ \  _"-.  
 \ \_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_\       \ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_/        \/_/   \/_/ /_/   \/_/\/_/   \/_/\/_/ 
                                                                                          


@author: Miguel Velasco Orozco

Este programa obtiene los datos clínicos relevantes de los pacientes a partir de los diferentes archivos que se proveeen 
en la página PPMI


Requiere los siguientes archivos para funcionar:
    
    - INTERNAL (Proveniente de Metadata Refiner)
    
    - SUBJECTS_LIST (Proveniente de Metadata Refiner)
    
    - MDS-UPDRS_Part_III_####
        + Puntajes Hoehn-Yahr [CODE:NHY] 
        + Fechas Hoehn-Yahr [CODE: EXAMDT]
        + Estado ON-OFF Hoehn-Yahr [CODE:PDSTATE]
        
    - Demographics_###
        + Fecha de Nacimiento [CODE: BIRTHDT]
        
    - Socio-Economics_###
        + Número de años de escolaridad [CODE: EDUCYRS]
        
    - PD_Diagnosis_History_###
        + Edad de inicio de síntomas [CODE:SXDT]
        + Fecha de diagnóstico de Párkinson [CODE:PDDXDT]
        
Estructura de los datos Controles y Prodrómicos

Dict: {Subject_ID:[Int], Sex:[M/F], Birthdate:[Date], Group:[PD,Prod,Ctrl], Modality:[fMRI,T13D,DTI,NM],
       Years_of_education:[Int], HY_Scores:[Int], HY_Dates:[Date], MoCA_Scores:[Int], MoCA_Dates:[Date]}

Estructura de los datos Pacientes Parkinson

Dict: {Subject_ID:[Int], Sex:[M/F], Birthdate:[Date], Group:[PD,Prod,Ctrl], Modality:[fMRI,T13D,DTI,NM],Years_of_education:[Int], 
       HY_Scores:[Int], HY_Dates:[Date], MoCA_Scores:[Int], MoCA_Dates:[Date],Onset_Age:[Int], Diagnosis_Age:[Int], 
       HY_Status:[ON/OFF]}

Genera 2 Archivos principales 

-CLINI-TRAK_[SUBJECT TYPE] [SESSION NAME]_DATAFRAME
El cual contiene los datos de los diccionarios por sujeto. Las columnas que tiene son:
    + Subjec_ID (Int): Tiene el ID de sujeto
    + Sex (Str, M/F): Tiene el género del sujeto
    + Birthdate
    
-CLINI-TRAK_[SUBJECT TYPE] [SESSION NAME]_SUBJECTS

-LINMOD_MOCA_[SUBJECT TYPE] [SESSION NAME]

//////////////////////VER 2 Update//////////////////////////////////

Se añade módulo que genera los archivos para el análisis en modelo lineal; en este archivo se le asigna 
una fila a cada uno de los puntajes MoCA o H-Y (dependiendo del archivo). 
Este nuevo archivo añade 
las columnas:
    -'Test_Number' donde pone el número de examen al que corresponde ese puntaje. 
    -'Age_at_test' donde va la edad del paciente al momento de hacer el MoCA / HY
    -'Slope' Regresión lineal sobre los puntajes MoCA / HY contra la edad del paciente
A los controles y prodrómicos se les pone las columnas 'onset age' y 'diagnosis age' en cero.

///////////////////// VER 2.1 Update /////////////////////////////
01/4/25

Al momento de comparar las listas de sujetos y si los sujetos tenían los datos de los .csv
por alguna razón no estaba funcionando para los prodrómicos, por lo que se cambió la sintaxis 
de algunas funciones forzando a crear listas en vez de series de pandas. Se probó con los 
archivos.

///////////////////// VER 2.2 Update /////////////////////////////
07/4/26

Se cambia la forma en que se generan los archivos LINMOD_MOCA y LINMOD_HY, al implementar 
funciones en vez de hacer el proceso dividido según el tipo, se generaliza.
Función sorter()
    - Módulo para reordenar las fechas-puntajes MoCA/HY

Función linmod_df_filler
    - Módulo para generar el dataframe de puntajes MoCA/HY para los modelos lineales (archivo LINMOD_)
    está generalizado para poder llenar tanto de MoCA como HY dentro de la misma función 
    
Ahora genera el segundo archivo LINMOD_HY_ con los puntajes de Test Horen-Yahr

///////////////////// VER 2.3 Update /////////////////////////////
12/6/26

Se modifican funciones para integrar columna de estatus ON OFF Hoehn Yahr en los archivos LINMOD 

"""

VER='2.2'

import easygui as eg
import os                #Sirve para el Manejo de archivos
from datetime import datetime 
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


#%%---------PATH MANAGER-------------------------------------------------------

#-----Session Values Input
#Session Name
message = 'Please input Session Name or ID'
title = "Clini-Trak "+VER+" - Start"
sname = eg.enterbox(message, title) #Session Name

#Subject Type
message = 'Please select Subject Type'
title = "Clini-Trak "+VER+" - Start"
choices = ['Control','Prodromal','Parkinsons']
stype = eg.choicebox(message, title, choices) #Session Name

#Session Save path
message = 'Please input Session Save Folder'
title = "Clini-Trak "+VER+" - Start"
temp_path = eg.diropenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
sv_path = temp_path.replace(os.path.sep ,"/")

#Internal File path
message = 'Please Select Metadata Internal Refined File'
title = "Clini-Trak "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
fl_path = temp_path.replace(os.path.sep ,"/")

#MDS-UPDRS_Part_III File path 
message = 'Please Select MDS-UPDRS_Part_III File'
title = "Clini-Trak "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
updrs_path = temp_path.replace(os.path.sep ,"/")

#Demographics File path
message = 'Please Select Demographics File'
title = "Clini-Trak "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
dems_path = temp_path.replace(os.path.sep ,"/")

#Socio-Economics File path
message = 'Please Select Socio-Economics File'
title = "Clini-Trak "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
socec_path = temp_path.replace(os.path.sep ,"/")

#MoCA File path
message = 'Please Select Montreal_Cognitive_Assessment_MoCA File'
title = "Clini-Trak "+VER+" - "
temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") 
moca_path = temp_path.replace(os.path.sep ,"/")

#PDD_Diagnosis_History File path
if stype=='Parkinsons':
    message = 'Please Select PD_Diagnosis_History File'
    title = "Clini-Trak "+VER+" - "
    temp_path = eg.fileopenbox(message, title, default=r"C:/Users/Admin/Desktop/Maestría en Neurobiología/Proyecto") #Save Path
    pdiag_path = temp_path.replace(os.path.sep ,"/")


#-------Change working directory to save path 
os.chdir(sv_path)


#%%---------FILE OPEN----------------------------------------------------------

#Read Internal Refined File
intfile = pd.read_csv(fl_path)  

#Subjects Extraction 
unsorted_subjects=intfile['Subject'].value_counts()  #Extracts all subject numbers
unsorted_subjects=unsorted_subjects.sort_index()
subjects = unsorted_subjects.index

#Read Demographics File
demsfile = pd.read_csv(dems_path)

#Read Socioeconomics File
socecfile = pd.read_csv(socec_path)

#Read MDS-UPDRS_Part_III File
updrsfile = pd.read_csv(updrs_path)

#Read Montreal_Cognitive_Assessment_MoCA File
mocafile = pd.read_csv(moca_path)

#Read PDD_Diagnosis_History File
if stype=='Parkinsons':
    pdiagfile=pd.read_csv(pdiag_path)
    
#Create Log File 
with open (sname+' - Clini-Trak Log File.txt', 'w') as savefile:
    savefile.write(' ______     __         __     __   __     __        ______   ______     ______     __  __  \n')  
    savefile.write('/\  ___\   /\ \       /\ \   /\ "-.\ \   /\ \      /\__  _\ /\  == \   /\  __ \   /\ \/ /  \n' ) 
    savefile.write('\ \ \____  \ \ \____  \ \ \  \ \ \-.  \  \ \ \     \/_/\ \/ \ \  __<   \ \  __ \  \ \  _"-. \n' )
    savefile.write(' \ \_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_\       \ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\ \n')
    savefile.write('  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_/        \/_/   \/_/ /_/   \/_/\/_/   \/_/\/_/ \n\n')                                                                                        
    savefile.write('Created By: NeuroSc Miguel Velasco-Orozco \u00A9 2025\nVersion Control: '+VER+'\n\n\n')
    savefile.write('Session Name: '+sname+'\n')
    savefile.write('Subject Type: '+stype+'\n\n')
    savefile.write('Metadata Internal Refined File Route: \n'+fl_path+'\n\n')
    savefile.write('MDS-UPDRS_Part_III File Route: \n'+updrs_path+'\n\n')
    savefile.write('Demographics File Route: \n'+dems_path+'\n\n')
    savefile.write('Socio-Economics File Route: \n'+socec_path+'\n\n')
    savefile.write('MoCA File Route: \n'+moca_path+'\n\n')
    if stype=='Parkinsons':
        savefile.write('PDD_Diagnosis_History: \n'+pdiag_path+'\n\n')
    savefile.write('Save Folder Route: \n'+sv_path+'\n\n\n')
    savefile.write('Session Timestamp: '+str(datetime.now())+'\n\n')

#%%---------MAIN DATA MINER----------------------------------------------------

#Patients not in other files 
dems_exclusions=[]
socec_exclusions=[]
updrs_exclusions=[]
moca_exclusions=[]

#Iterator by subject type
if stype == 'Parkinsons':     #If subject type is Parkinsons 
    pdiag_exclusions=[]
    print('Subject Type: Parkinsons\n')
    
    dict_list=[]   #Initialize list of data dictionaries
    
    for i in subjects:
        #print('\n')
        #------Extract Sex from Internal file
        sex = intfile[(intfile['Subject']==i)]['Sex'].value_counts().index[0]
        
        #------Extract Birthdate from Demographics file 
        if i in demsfile['PATNO']:
            birthdate = demsfile[(demsfile['PATNO']==i)]['BIRTHDT'].value_counts().index[0]   
        else:
            print('Patient '+str(i)+' not in Demographics file, Birth Year inferred')
            dems_exclusions.append(i)
            birthdate =str(int(datetime.strptime(intfile[(intfile['Subject']==i)]['Acq Date'].value_counts().index[0], '%m/%d/%Y').strftime('%Y'))-int(intfile[(intfile['Subject']==i)]['Age'].value_counts().index[0]))
            birthdate = datetime.strptime(birthdate, '%Y').strftime('%m/%Y')
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in Demographics file, Birth Year inferred\n')
       
        #------Extract Modalities from Internal file
        ni_check=0 #Checks if patient has useful mri sequences
        modality=[]
        if 'T13D' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('T13D')
            ni_check=1
        if 'fMRI' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('fMRI')
            ni_check=1
        if 'DTI' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('DTI')
            ni_check=1
        if 'NM' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('NM')
            ni_check=1
        
        if not ni_check:
            print('Patient '+str(i)+' has no useful MRI sequences')
            modality='NO DATA'
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' has no useful MRI sequences\n')

        #------Extract education years from socioeconomics file
        if i in socecfile['PATNO']:
            yoe = socecfile[(socecfile['PATNO']==i)]['EDUCYRS'].value_counts().index[0] 
        else:
            print('Patient '+str(i)+' not in Socioeconomics file')
            yoe='NO DATA'
            socec_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in Socioeconomics file\n')
            
        #-----Extract Hoehn-Yahr Scores from MDS-UPDRS_Part_III
        if i in updrsfile['PATNO']:
            hy= updrsfile[(updrsfile['PATNO']==i)][['NHY','INFODT','PDSTATE']]
            #There are NaN values in HY status corresponding to before treatment was started (Col PDTRTMNT)
            #so they correspond to a 'OFF State', NaN Values are replaced to 'NoTrtOFF' to indicate this
            hy['PDSTATE'] = hy['PDSTATE'].fillna('NoTrtOFF')
            #Remove rows with NaN values in score col
            hy.dropna(inplace=True)
            #Sort by date 
            hy['INFODT']=pd.to_datetime(hy['INFODT'], format='%m/%Y')
            hy.sort_values(by='INFODT', inplace=True)
            hy.reset_index(inplace=True, drop = True)
            #Create lists of values 
            hyscores = list(hy['NHY'])
            hydates = list(hy['INFODT'].dt.strftime('%m/%Y'))
            hystatus = list(hy['PDSTATE'])
            
        else:
            print('Patient '+str(i)+' not in MDS-UPDRS file')
            hyscores='NO DATA'
            hydates='NO DATA'
            hystatus='NO DATA'
            updrs_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in MDS-UPDRS file\n')
        
        #------Extract MoCA scores from Montreal_Cognitive_Assessment_MoCA File
        if i in mocafile['PATNO']:
            moca = mocafile[(mocafile['PATNO']==i)][['MCATOT','INFODT']]
            #Sort by date 
            moca['INFODT']=pd.to_datetime(moca['INFODT'], format='%m/%Y')
            moca.sort_values(by='INFODT', inplace=True)
            moca.reset_index(inplace=True, drop = True)
            #Create lists of values 
            mocascore = list(moca['MCATOT'])
            mocadates = list(moca['INFODT'].dt.strftime('%m/%Y'))
        else:
            print('Patient '+str(i)+' not in MoCA file')
            mocascore='NO DATA'
            mocadates='NO DATA'
            moca_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in MoCA file\n')
            
        #------Extract Age of onset and diagnosis from PD_Diagnosis_History
        if i in list(pdiagfile['PATNO']):
            
            onsetdate= list(pdiagfile[list(pdiagfile['PATNO']==i)]['SXDT'])[0]
            diagdate= list(pdiagfile[list(pdiagfile['PATNO']==i)]['PDDXDT'])[0]

            #Check Values in cell
            if isinstance(onsetdate, str):
                onsetage= int(int(datetime.strptime(onsetdate,'%m/%Y').strftime('%Y'))-int(datetime.strptime(birthdate,'%m/%Y').strftime('%Y')))
            else:
                print('Patient '+str(i)+' does not have Onset Date Data')
                onsetdate = 'NO DATA'
                onsetage = 'NO DATA'
                pdiag_exclusions.append(i)
                with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                    savefile.write('Patient '+str(i)+' does not have Onset Date Data\n')

            if isinstance(diagdate, str):
                diagage= int(int(datetime.strptime(diagdate,'%m/%Y').strftime('%Y'))-int(datetime.strptime(birthdate,'%m/%Y').strftime('%Y')))  
            else:
                print('Patient '+str(i)+' does not have Onset Date Data')
                diagdate = 'NO DATA'
                diagage = 'NO DATA'
                pdiag_exclusions.append(i)
                with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                    savefile.write('Patient '+str(i)+' does not have Onset Date Data\n')
            
        else:
            print('Patient '+str(i)+' not in PD_Diagnosis_History file')
            onsetdate='NO DATA'
            diagdate='NO DATA'
            onsetage= 'NO DATA'
            diagage= 'NO DATA'
            pdiag_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in PD_Diagnosis_History file\n')
        
        
        
        #Creating dictionary 
        pdd_temp_dict={'Subject_ID':int(i), 
                      'Sex':sex, 
                      'Birthdate':birthdate, 
                      'Group':intfile[(intfile['Subject']==i)]['Group'].value_counts().index[0], 
                      'Modality':modality,  
                      'Years_of_education':yoe, 
                      'HY_Scores':hyscores, 
                      'HY_Dates':hydates, 
                      'MoCA_Scores':mocascore, 
                      'MoCA_Dates':mocadates,
                      'Onset_Date':onsetdate,
                      'Onset_Age':onsetage,
                      'Diagnosis_Date':diagdate,
                      'Diagnosis_Age':diagage,
                      'HY_Status':hystatus}

        dict_list.append(pdd_temp_dict)
        
    print('All Clinical data has been recovered from patients index')

else:
    print('Subject Type: Prodromal/Control \n')
    dict_list=[]   #Initialize list of data dictionaries
    
    for i in subjects:
        #------Extract Sex from Internal file
        sex = intfile[(intfile['Subject']==i)]['Sex'].value_counts().index[0]
        
        #------Extract Birthdate from Demographics file 
        if i in list(demsfile['PATNO']):
            birthdate = demsfile[(demsfile['PATNO']==i)]['BIRTHDT'].value_counts().index[0]   
        else:
            print('Patient '+str(i)+' not in Demographics file, Birth Year inferred')
            dems_exclusions.append(i)
            birthdate =str(int(datetime.strptime(intfile[(intfile['Subject']==i)]['Acq Date'].value_counts().index[0], '%m/%d/%Y').strftime('%Y'))-int(intfile[(intfile['Subject']==i)]['Age'].value_counts().index[0]))
            birthdate = datetime.strptime(birthdate, '%Y').strftime('%m/%Y')
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in Demographics file, Birth Year inferred\n')
       
        #------Extract Modalities from Internal file
        ni_check=0 #Checks if patient has useful mri sequences
        modality=[]
        if 'T13D' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('T13D')
            ni_check=1
        if 'fMRI' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('fMRI')
            ni_check=1
        if 'DTI' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('DTI')
            ni_check=1
        if 'NM' in intfile[(intfile['Subject']==i)]['Modality'].value_counts().index:
            modality.append('NM')
            ni_check=1
        
        if not ni_check:
            print('Patient '+str(i)+' has no useful MRI sequences')
            modality='NO DATA'
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' has no useful MRI sequences\n')

        #------Extract education years from socioeconomics file
        if i in list(socecfile['PATNO']):
            yoe = socecfile[(socecfile['PATNO']==i)]['EDUCYRS'].value_counts().index[0] 
        else:
            print('Patient '+str(i)+' not in Socioeconomics file')
            yoe='NO DATA'
            socec_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in Socioeconomics file\n')
            
        #-----Extract Hoehn-Yahr Scores from MDS-UPDRS_Part_III
        if i in list(updrsfile['PATNO']):
            hy= updrsfile[(updrsfile['PATNO']==i)][['NHY','INFODT','PDSTATE']]
            #There are NaN values in HY status corresponding to before treatment was started (Col PDTRTMNT)
            #so they correspond to a 'OFF State', NaN Values are replaced to 'NoTrtOFF' to indicate this
            hy['PDSTATE'] = hy['PDSTATE'].fillna('NoTrtOFF')
            #Remove rows with NaN values in score col
            hy.dropna(inplace=True)
            #Sort by date 
            hy['INFODT']=pd.to_datetime(hy['INFODT'], format='%m/%Y')
            hy.sort_values(by='INFODT', inplace=True)
            hy.reset_index(inplace=True, drop = True)
            #Create lists of values 
            hyscores = list(hy['NHY'])
            hydates = list(hy['INFODT'].dt.strftime('%m/%Y'))
            hystatus = list(hy['PDSTATE'])
            
        else:
            print('Patient '+str(i)+' not in MDS-UPDRS file')
            hyscores='NO DATA'
            hydates='NO DATA'
            hystats='NO DATA'
            updrs_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in MDS-UPDRS file\n')
        
        #------Extract MoCA scores from Montreal_Cognitive_Assessment_MoCA File
        if i in list(mocafile['PATNO']):
            moca = mocafile[(mocafile['PATNO']==i)][['MCATOT','INFODT']]
            #Sort by date 
            moca['INFODT']=pd.to_datetime(moca['INFODT'], format='%m/%Y')
            moca.sort_values(by='INFODT', inplace=True)
            moca.reset_index(inplace=True, drop = True)
            moca.dropna(inplace=True)
            #Create lists of values 
            mocascore = list(moca['MCATOT'])
            mocadates = list(moca['INFODT'].dt.strftime('%m/%Y'))
        else:
            print('Patient '+str(i)+' not in MoCA file')
            mocascore='NO DATA'
            mocadates='NO DATA'
            moca_exclusions.append(i)
            with open (sname+' - Clini-Trak Log File.txt', 'a') as savefile:
                savefile.write('Patient '+str(i)+' not in MoCA file\n')
            
        
        #Creating dictionary 
        pdd_temp_dict={'Subject_ID':int(i), 
                      'Sex':sex, 
                      'Birthdate':birthdate, 
                      'Group':intfile[(intfile['Subject']==i)]['Group'].value_counts().index[0], 
                      'Modality':modality,  
                      'Years_of_education':yoe, 
                      'HY_Scores':hyscores, 
                      'HY_Dates':hydates, 
                      'MoCA_Scores':mocascore, 
                      'MoCA_Dates':mocadates,
                      'HY_Status':hystatus}

        dict_list.append(pdd_temp_dict)
        
    print('\n\nAll Clinical data has been recovered from patients index')
    
#%%---------CLINI-TRAK FILES GENERATION----------------------------------------

subs = set((list(subjects)))
if stype=='Parkinsons':
    #Generate list of subjects with all data 
    missingdata_subjects=set((dems_exclusions+socec_exclusions+updrs_exclusions+moca_exclusions+pdiag_exclusions))
    alldata_subjects =sorted(subs-missingdata_subjects)

    subs_ls=pd.DataFrame([alldata_subjects, dems_exclusions, socec_exclusions, updrs_exclusions, moca_exclusions, pdiag_exclusions])
    subs_ls=subs_ls.transpose()
    subs_ls.columns=['Subjects With All Data','Demographics Exclusions','Socioeconomics Exclusions','UPDRS Exclusions','MoCA Exclusions','PDD Exclusions']
    
    dataframe= pd.DataFrame.from_dict(dict_list)
    dataframe.to_csv('CLINI-TRAK_'+stype+' '+sname+'_DATAFRAME.csv', index=False)
    subs_ls.to_csv('CLINI-TRAK_'+stype+' '+sname+'_SUBJECTS.csv', index=False)
    
else:
    #Generate list of subjects with all data 
    missingdata_subjects=set((dems_exclusions+socec_exclusions+updrs_exclusions+moca_exclusions))
    alldata_subjects =sorted(subs-missingdata_subjects)
    
    subs_ls=pd.DataFrame([alldata_subjects, dems_exclusions, socec_exclusions, updrs_exclusions, moca_exclusions])
    subs_ls=subs_ls.transpose()
    subs_ls.columns=['Subjects With All Data','Demographics Exclusions','Socioeconomics Exclusions','UPDRS Exclusions','MoCA Exclusions']
    
    dataframe= pd.DataFrame.from_dict(dict_list)
    dataframe.to_csv('CLINI-TRAK_'+stype+'_'+sname+'_DATAFRAME.csv', index=False)
    subs_ls.to_csv('CLINI-TRAK_'+stype+'_'+sname+'_SUBJECTS.csv', index=False)

#%%---------DEFINE FUNCTIONS---------------------------------------------------

def sorter(dates, scores, testname, hyStatus=0):
    """
    Sorts MoCA/HY scores by date

    Parameters
    ----------
    dates : Array 
        Initial subject test Dates.
    scores : Array
        Initial subject Scores.
    testname : String
        'HY' or 'MoCA'
    hyStatus : Array
        Initial subject treatment status.

    Returns
    -------
    skip : Bool
        If subject has no valid scores returns True so that subject can be skipped without adding it to
        the final file.
        
    datesRes: Array 
        Array with ordered Test Dates.
    
    scoresRes: Array
        Array with ordered Scores.

    """
    
    if testname == 'MoCA':
        tmp = {'Dates':dates, 'Scores':scores}
        tmp_dataframe = pd.DataFrame.from_dict(tmp)
        tmp_dataframe.dropna(inplace=True)
        tmp_dataframe = tmp_dataframe[tmp_dataframe['Scores'] != 101] #Drops 'Unable to evaluate' rows, codemark 101 (see: Code_List_Harmoonized, ITM_NAME: NHY, CODE: 101)
        
        if len(tmp_dataframe)== 0:
            skip = True
            datesRes=[]
            scoresRes=[]
            return skip, datesRes, scoresRes 
        
        else:
            
            tmp_dataframe['Dates'] = pd.to_datetime(tmp_dataframe['Dates'], format='%m/%Y')
            tmp_dataframe.sort_values(by='Dates', inplace=True)
            tmp_dataframe.reset_index(inplace=True, drop=True)
            #tmp_dataframe.drop_duplicates(subset = 'Dates', inplace =True) #Drops Duplicated evals (done on same day)
            tmp_dataframe['Dates']= tmp_dataframe['Dates'].dt.strftime('%m/%Y')
            datesRes = np.array(tmp_dataframe['Dates'])
            scoresRes = np.array(tmp_dataframe['Scores'])
            skip = False 
            
            return skip, datesRes, scoresRes
    
    elif testname == 'HY':
        tmp = {'Dates':dates, 'Scores':scores, 'Status': hyStatus}
        tmp_dataframe = pd.DataFrame.from_dict(tmp)
        tmp_dataframe.dropna(inplace=True)
        tmp_dataframe = tmp_dataframe[tmp_dataframe['Scores'] != 101] #Drops 'Unable to evaluate' rows, codemark 101 (see: Code_List_Harmoonized, ITM_NAME: NHY, CODE: 101)
        
        if len(tmp_dataframe)== 0:
            skip = True
            datesRes=[]
            scoresRes=[]
            return skip, datesRes, scoresRes 
        
        else:
            
            tmp_dataframe['Dates'] = pd.to_datetime(tmp_dataframe['Dates'], format='%m/%Y')
            tmp_dataframe.sort_values(by='Dates', inplace=True)
            tmp_dataframe.reset_index(inplace=True, drop=True)
            #tmp_dataframe.drop_duplicates(subset = 'Dates', inplace =True) #Drops Duplicated evals (done on same day)
            tmp_dataframe['Dates']= tmp_dataframe['Dates'].dt.strftime('%m/%Y')
            datesRes = np.array(tmp_dataframe['Dates'])
            scoresRes = np.array(tmp_dataframe['Scores'])
            statusRes = np.array(tmp_dataframe['Status'])
            skip = False 
            
            return skip, datesRes, scoresRes, statusRes
    
    else:
        print('ERROR: Wrong Test Name, Chose HY or MoCA')
        
def linmod_df_filler(stype, c, dates, scores, sub_dict, testname, hystatus=0):
    '''
    Creates Linear Model file dataframe, can be used with MoCA scores or HY scores

    Parameters
    ----------
    stype : Str
        Session type, valid only if contains 'Parkinsons','Control' or 'Prodromal'.
    c : Int
        Counter, to indicate if first iteration, only works if contains 0 or 1.
    dates : Array 
        Array of test dates.
    scores : Array
        Array of test scores.
    sub_dict : Dict
        Subject dictionary containing all subject data.
    testname : Str
        Name of test to evaluate, only works if contains 'MoCA' or 'HY'.
    hystatus : Array
        Array of HY treatment status.

    Returns
    -------
    
    if c == 0:
        df : Dataframe
            Contains dataframe of subject data with repeated rows according to test dates/scores.
        c2 : Int
            Counter = 1 to indicate first iterartion was completed
    
    if c == 1:
        tmp_df : Dataframe
            Contains dataframe of subject data with repeated rows according to test dates/scores.

    '''
    #-----Obtain number of repetitions
    rownum = len(scores) #Obtain number of rows per subjects 
    tstnum=np.arange(1,rownum+1,1) #Obtain test number 
    
    #------List of repeated items 
    subid=[sub_dict.get('Subject_ID')]*rownum
    sex=[sub_dict.get('Sex')]*rownum
    birthdate = [sub_dict.get('Birthdate')]*rownum
    group=[sub_dict.get('Group')]*rownum
    modality=[sub_dict.get('Modality')]*rownum
    yoe=[sub_dict.get('Years_of_education')]*rownum
    
    #------Lists of calculated items 
    
    #Obtain Age at Test 
    ageAtTest =np.array([(datetime.strptime(a, '%m/%Y')-datetime.strptime(birthdate[0],'%m/%Y')).days/365 for a in dates]) #Test date minus birthdate in years 
    
    #Obtain Days between tests
    daysBetween = np.array([(datetime.strptime(a, '%m/%Y')-datetime.strptime(dates[0],'%m/%Y')).days for a in dates])
    
    #Obtain General Slope
    ageAtTest_lr= ageAtTest.reshape((-1,1)) #Reshape x
    model=LinearRegression().fit(ageAtTest_lr,scores)
    slope=[(model.coef_[0])]*rownum
    
    
    #Dataframe Fill
    if stype == 'Parkinsons':
        
        if testname == 'MoCA':
            onsetage=[i.get('Onset_Age')]*rownum
            diagnosisage=[i.get('Diagnosis_Age')]*rownum
            if c ==0:
                df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':onsetage,
                'Diagnosis_Age':diagnosisage
                })
                
                c2=1
                return df, c2
            else:
                tmp_df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':onsetage,
                'Diagnosis_Age':diagnosisage
                })
                
                return tmp_df
        
        elif testname == 'HY':
            onsetage=[i.get('Onset_Age')]*rownum
            diagnosisage=[i.get('Diagnosis_Age')]*rownum
            if c ==0:
                df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':onsetage,
                'Diagnosis_Age':diagnosisage,
                'HY_Status':hystatus
                })
                
                c2=1
                return df, c2
            else:
                tmp_df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':onsetage,
                'Diagnosis_Age':diagnosisage,
                'HY_Status':hystatus
                })
                
                return tmp_df
        
    
    elif (stype == 'Prodromal') or (stype == 'Control'):
        if testname == 'MoCA':
            if c ==0:
                df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':np.zeros((rownum)),
                'Diagnosis_Age':np.zeros((rownum))
                })
                
                c2=1
                return df, c2
            else:
                tmp_df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':np.zeros((rownum)),
                'Diagnosis_Age':np.zeros((rownum))
                })
                
                return tmp_df
        
        elif testname == 'HY':
            if c ==0:
                df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':np.zeros((rownum)),
                'Diagnosis_Age':np.zeros((rownum)),
                'HY_Status':hystatus
                })
                
                c2=1
                return df, c2
            else:
                tmp_df=pd.DataFrame({
                'Subject_ID': subid,
                'Test_Number':tstnum,
                'Sex':sex,
                'Birthdate':birthdate,
                'Group':group,
                'Modality':modality,
                'Years_of_education':yoe,
                testname+'_Scores': scores,
                testname+'_Dates':dates,
                'Age_at_Test': ageAtTest,
                'Days_between_Tests':np.abs(daysBetween),
                'Slope': slope,
                'Onset_Age':np.zeros((rownum)),
                'Diagnosis_Age':np.zeros((rownum)),
                'HY_Status':hystatus
                })
                
                return tmp_df

    
#%%---------CLINI-TRAK LINEAR MODEL MOCA FILES GENERATION----------------------   

#File 1 MoCA
c=0
for i in dict_list: 
    if i.get('Subject_ID') in alldata_subjects:
        #-----Sort dates/scores 
        skip, mocaDates, mocaScores= sorter(np.array(i.get('MoCA_Dates')),np.array(i.get('MoCA_Scores')),'MoCA')
        #-----Obtain dataframe
        if not skip:
            print(i.get('Subject_ID'))
            if c==0:
                df,c = linmod_df_filler(stype,c,mocaDates,mocaScores,i,'MoCA')
            else:
                tmp_df = linmod_df_filler(stype,c,mocaDates,mocaScores,i,'MoCA')
                df = pd.concat([df, tmp_df])
            
df.to_csv('LINMOD_MOCA_'+stype+'_'+sname+'.csv', index=False)


#%%---------CLINI-TRAK LINEAR MODEL HY FILES GENERATION------------------------

#File 2 H-Y
c=0
for i in dict_list: 
    if i.get('Subject_ID') in alldata_subjects:
        #-----Sort dates/scores 
        skip, hyDates, hyScores, hyStatus= sorter(np.array(i.get('HY_Dates')),np.array(i.get('HY_Scores')),'HY',np.array(i.get('HY_Status')))
        #-----Obtain dataframe
        if not skip:
            print(i.get('Subject_ID'))
            if c==0:
                df,c = linmod_df_filler(stype,c,hyDates,hyScores,i,'HY',hyStatus)
            else:
                tmp_df = linmod_df_filler(stype,c,hyDates,hyScores,i,'HY',hyStatus)
                df = pd.concat([df, tmp_df])
            
df.to_csv('LINMOD_HY_'+stype+'_'+sname+'.csv', index=False)


    
