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
Finds closest date between MoCA evaluation and MRI imaging 

Creates Dataframe with only MRI Data and LINMOD file with clinical data 

//////////////UPDATE v1.1/////////////////////
- Data management to include HY Status ON-OFF on cols

//////////////UPDATE v1.2////////////////////
- Drop columns with repeated values coming from Clini-Trak v2.4

//////////////UPDATE v1.3////////////////////
- Bug correction

//////////////UPDATE v1.4////////////////////
- Se ELIMINA la comparativa con el examen HY (solo MoCA queda)
- Corrección de bugs que truncaban filas al aumentar el dataset:
  1. match_moca_to_mri reemplaza closest_dates: ordena por fecha y
     empareja 1:1 con máximo matching bipartito (algoritmo de Kuhn),
     respetando ventana temporal. Sin desalineamiento posicional.
  2. Se elimina el patrón isin(matcher) + concat(axis=1) que producía
     desalineación cuando un MoCA alimentaba varias resonancias.
  3. Conversión de fechas a datetime se mueve FUERA de la rama 'Parkinsons'
     (antes solo se ejecutaba si había PD, rompiendo Control/Prodromal).
  4. Merge con MRIQC ahora es how='inner': "solo conservar imágenes AN que
     estén en MRIQC FLTRD". MRIQC FLTRD ya aplicó el QC, por lo que la
     columna 'Quality control' de AssemblyNet NO se usa como filtro.
  5. Se ELIMINA el filtro redundante pd_validated_df['Quality control'] != 'C'.
  6. dropna() global eliminado: solo se aplica dropna sobre columnas
     clínicas críticas (MoCA_Scores, MoCA_Dates).
  7. Ventana temporal máxima ±3 meses (MAX_DELTA_DAYS = 90 días).
  8. PRIORIZACIÓN 1:1 — Primera pasada: máximo matching bipartito (Kuhn),
     asignando cada MoCA a lo sumo a una resonancia (1:1) y priorizando
     las parejas con menor Δt. Segunda pasada (solo si quedan resonancias
     sin pareja): duplica el MoCA más cercano. Así los MoCA disponibles
     se agotan ANTES de generar duplicados.
  9. Eliminado el PerformanceWarning de "highly fragmented DataFrame":
     match_moca_to_mri ya no hace inserciones sucesivas de columnas,
     sino que construye el output con pd.concat(axis=1).
"""

VER='1.4'

import easygui as eg
import os                #Sirve para el Manejo de archivos
import pandas as pd

#%%----------------------PARÁMETROS GLOBALES------------------------------------

# Ventana temporal máxima entre resonancia y evaluación MoCA.
# "No más de 3 meses" ≈ 90 días. Ajustar aquí si se requiere otro umbral.
MAX_DELTA_DAYS = 90

# Columnas clínicas redundantes (ya presentes en BrAiN-Trak o no relevantes
# para el modelo) que se eliminan del DataFrame clínico antes de concatenar.
# 'errors=ignore' evita KeyError si algún CSV de un grupo no las trae.
MOCA_COLS_TO_DROP = [
    'Subject_ID','Sex','Birthdate','Group','Modality','Years_of_education',
    'Onset_Age','Diagnosis_Age','Handedness','Test_Number','Sympt_Laterality'
]

#%%----------------------FUNCTION MANAGER--------------------------------------

def _kuhn_matching(adj, n_left, n_right):
    """
    Algoritmo de Kuhn (augmenting paths) para máximo emparejamiento
    bipartito. Garantiza el mayor número de parejas 1:1 posible.

    Parámetros
    ----------
    adj : list[list[int]]
        adj[u] = lista de índices (en el lado derecho) a los que el nodo
        izquierdo 'u' puede emparejarse, ORDENADA por preferencia (en este
        caso, por Δt ascendente: primero las parejas con menor Δt).
    n_left : int
        Número de nodos en el lado izquierdo (resonancias).
    n_right : int
        Número de nodos en el lado derecho (evaluaciones MoCA).

    Returns
    -------
    match_left : list[int]
        match_left[u] = índice de MoCA asignado a la resonancia u, o -1.
        Garantiza máximo cardinalidad.
    """
    match_right = [-1] * n_right
    match_left = [-1] * n_left

    def try_augment(u, visited):
        # Recorre los candidatos del nodo izquierdo u en orden de preferencia.
        for v in adj[u]:
            if visited[v]:
                continue
            visited[v] = True
            # Si v está libre o su ocupante puede reubicarse en otro lado,
            # reasignamos: u se queda con v.
            if match_right[v] == -1 or try_augment(match_right[v], visited):
                match_right[v] = u
                match_left[u] = v
                return True
        return False

    for u in range(n_left):
        visited = [False] * n_right
        try_augment(u, visited)

    return match_left


def match_moca_to_mri(bt_tmp, ct_tmp, max_delta_days=MAX_DELTA_DAYS):
    """
    Empareja cada resonancia (bt_tmp) con su evaluación MoCA más cercana
    en el tiempo (ct_tmp) dentro de una ventana temporal de max_delta_days.

    Estrategia 1:1 con duplicación como fallback
    --------------------------------------------
    PASO 1 (1:1 preferente):
        Se construye un grafo bipartito resonancia↔MoCA con las parejas
        cuyo Δt ≤ max_delta_days. Se corre máximo emparejamiento bipartito
        (Kuhn). Resultado: cada MoCA se usa A LO SUMO UNA VEZ, agotando los
        MoCA disponibles. En empates de Δt, el orden de preferencia de
        'adj' (por Δt ascendente) hace que se prioricen las parejas más
        cercanas temporalmente.

    PASO 2 (duplicación como fallback):
        Solo las resonancias que NO obtuvieron un MoCA único (porque había
        más resonancias que MoCA dentro de la ventana) se asignan a su MoCA
        MÁS CERCANO, aunque ya esté usado. La columna 'MoCA_delta_days'
        documenta la distancia temporal para que la duplicación sea auditable.

    Parámetros
    ----------
    bt_tmp : pd.DataFrame
        Sub-DataFrame BrAiN-Trak de un solo sujeto. Debe contener 'Date'.
    ct_tmp : pd.DataFrame
        Sub-DataFrame Clini-Trak (MoCA) del mismo sujeto. Debe contener
        'MoCA_Dates' y ya debe tener eliminadas las columnas clínicas
        redundantes.
    max_delta_days : int
        Ventana temporal máxima en días (por defecto 90 ≈ 3 meses).

    Returns
    -------
    pd.DataFrame
        Concatenado lado a lado: una fila por resonancia emparejada.
        DataFrame vacío si no hubo emparejamiento válido.
    """
    # Limpieza inicial: filas sin fecha no se pueden emparejar.
    bt_tmp = bt_tmp.dropna(subset=['Date']).reset_index(drop=True).copy()
    ct_tmp = ct_tmp.dropna(subset=['MoCA_Dates']).reset_index(drop=True).copy()

    if bt_tmp.empty or ct_tmp.empty:
        return pd.DataFrame()

    # Ordenar por fecha (determinista y con salida cronológica).
    bt_tmp = bt_tmp.sort_values('Date').reset_index(drop=True)
    ct_tmp = ct_tmp.sort_values('MoCA_Dates').reset_index(drop=True)

    bt_dates = bt_tmp['Date'].tolist()
    ct_dates = ct_tmp['MoCA_Dates'].tolist()

    # Construcción del grafo bipartito: adj[u] = MoCAs elegibles para
    # la resonancia u, ordenados por Δt ascendente (preferencia).
    # También guardamos el Δt de cada pareja en un dict auxiliar.
    adj = []
    pair_delta = {}   # (bt_idx, ct_idx) -> delta_days
    for bt_idx, bt_date in enumerate(bt_dates):
        options = []
        for ct_idx, ct_date in enumerate(ct_dates):
            delta_days = abs((bt_date - ct_date).days)
            if delta_days <= max_delta_days:
                options.append((ct_idx, delta_days))
                pair_delta[(bt_idx, ct_idx)] = delta_days
        options.sort(key=lambda x: x[1])      # menor Δt primero
        adj.append([ct_idx for ct_idx, _ in options])

    # Sin ninguna pareja válida dentro de la ventana: nada que emparejar.
    if not any(adj):
        return pd.DataFrame()

    # ---- PASO 1: máximo emparejamiento bipartito 1:1 (Kuhn) ----
    match_left = _kuhn_matching(adj, n_left=len(bt_dates), n_right=len(ct_dates))

    assignment = {}   # bt_idx -> (ct_idx, delta_days)
    for bt_idx, ct_idx in enumerate(match_left):
        if ct_idx != -1:
            assignment[bt_idx] = (ct_idx, pair_delta[(bt_idx, ct_idx)])

    # ---- PASO 2: duplicación SOLO para resonancias aún sin MoCA ----
    # Todas las parejas ya están dentro de la ventana; adj[u] está
    # ordenado por Δt ascendente, así que adj[u][0] es el MoCA más cercano.
    for bt_idx in range(len(bt_dates)):
        if bt_idx in assignment:
            continue
        if not adj[bt_idx]:
            continue   # sin MoCA en ventana → resonancia descartada
        closest_ct_idx = adj[bt_idx][0]
        assignment[bt_idx] = (closest_ct_idx, pair_delta[(bt_idx, closest_ct_idx)])

    if not assignment:
        return pd.DataFrame()

    # Construcción del output. Se ensambla TODO con pd.concat(axis=1) en
    # lugar de insertar columnas una a una → evita PerformanceWarning de
    # "highly fragmented DataFrame".
    mri_indices  = sorted(assignment.keys())
    moca_indices = [assignment[i][0] for i in mri_indices]
    delta_days   = [assignment[i][1] for i in mri_indices]

    bt_matched = pd.concat(
        [
            bt_tmp.iloc[mri_indices].reset_index(drop=True),
            pd.Series(delta_days, name='MoCA_delta_days'),
        ],
        axis=1,
    )
    ct_matched = ct_tmp.iloc[moca_indices].reset_index(drop=True)

    # Defragmentación final con copy() (belt-and-suspenders).
    out = pd.concat([ct_matched, bt_matched], axis=1).copy()
    return out


def summarize_duplication(df, label):
    """
    Imprime un resumen de auditoría de duplicación de MoCA:
    número de resonancias, número de MoCA únicos y cuántas resonancias
    compartieron MoCA con otra resonancia.
    """
    if df is None or df.empty:
        print(f"[{label}] Sin datos (0 resonancias emparejadas).")
        return
    n_res = len(df)
    n_uniq = df['MoCA_Dates'].nunique() if 'MoCA_Dates' in df.columns else 0
    print(f"[{label}] Resonancias: {n_res} | MoCA únicos: {n_uniq} "
          f"| duplicadas: {n_res - n_uniq} "
          f"({100 * (n_res - n_uniq) / n_res:.1f}%)")
    if 'MoCA_delta_days' in df.columns:
        print(f"[{label}] Δt (días) resonancia-MoCA: "
              f"media={df['MoCA_delta_days'].mean():.1f}, "
              f"máx={df['MoCA_delta_days'].max()}")


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
    # (HY input eliminado en v1.4)
    
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
    # (HY input eliminado en v1.4)
   
    
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
    # (HY input eliminado en v1.4)
    
#-------Change working directory to save path 
os.chdir(sv_path)

#%%----------------------FILE OPEN AND CONCAT----------------------------------

if 'Parkinsons' in stype:
    
    #PDD
    #Read Clini-Trak MoCA File y conversión de fechas a datetime
    pd_moca_file = pd.read_csv(pd_moca_path)
    pd_moca_file['MoCA_Dates'] = pd.to_datetime(pd_moca_file['MoCA_Dates'], format='%m/%Y')
    # (HY read eliminado en v1.4)
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
    pd_AN_dataframe.drop(columns=['Age','Sex'], inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in pd_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    pd_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    # v1.4: inner join = "solo conservar imágenes AN que estén en MRIQC FLTRD".
    # MRIQC FLTRD ya aplicó el QC; NO se filtra por 'Quality control' de AN.
    pd_dataframe= pd.merge(pd_AN_dataframe, pd_fltrd_file, on='Filename', how='inner')
    # v1.4: conversión de fecha de imagen movida AQUÍ (antes solo en rama PD,
    # lo que rompía Control/Prodromal).
    pd_dataframe['Date'] = pd.to_datetime(pd_dataframe['Date'], format='%Y-%m-%d')

if 'Control' in stype:
    #Ctrl
    #Read Clini-Trak MoCA File y conversión de fechas
    ctrl_moca_file = pd.read_csv(ctrl_moca_path)
    ctrl_moca_file['MoCA_Dates'] = pd.to_datetime(ctrl_moca_file['MoCA_Dates'], format='%m/%Y')
    # (HY read eliminado en v1.4)
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
    ctrl_AN_dataframe.drop(columns=['Age','Sex'], inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in ctrl_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    ctrl_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    # v1.4: inner join — MRIQC FLTRD es el filtro de calidad real.
    ctrl_dataframe= pd.merge(ctrl_AN_dataframe, ctrl_fltrd_file, on='Filename', how='inner')
    ctrl_dataframe['Date'] = pd.to_datetime(ctrl_dataframe['Date'], format='%Y-%m-%d')

if 'Prodromal' in stype:
    
    #Prod
    #Read Clini-Trak MoCA File y conversión de fechas
    prod_moca_file = pd.read_csv(prod_moca_path)
    prod_moca_file['MoCA_Dates'] = pd.to_datetime(prod_moca_file['MoCA_Dates'], format='%m/%Y')
    # (HY read eliminado en v1.4)
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
    prod_AN_dataframe.drop(columns=['Age','Sex'], inplace=True)
    #Extract filename from Subject col as series
    filename=[]
    for i in prod_AN_dataframe['Subject']:
        fn = i.split('/')[-1]
        filename.append(fn)
    #Add Filename column to dataframe
    prod_AN_dataframe['Filename']=filename
    #-----DATAFRAMES MERGE
    # v1.4: inner join — MRIQC FLTRD es el filtro de calidad real.
    prod_dataframe= pd.merge(prod_AN_dataframe, prod_fltrd_file, on='Filename', how='inner')
    prod_dataframe['Date'] = pd.to_datetime(prod_dataframe['Date'], format='%Y-%m-%d')

#%%----------------------Dataframes to Master CSV------------------------------

if 'Parkinsons' in stype:
    pd_dataframe.to_csv('PD_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)

if 'Control' in stype:
    ctrl_dataframe.to_csv('CTRL_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
elif 'Prodromal' in stype:
    prod_dataframe.to_csv('PROD_'+sname+'_BRAIN-TRAK_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
    
#%%----------------------Clini-Trak MoCA Validation---------------------------------

if 'Parkinsons' in stype:

    #-----Cast Subject ID as Integer
    pd_dataframe['SubjectID']= pd_dataframe['SubjectID'].astype(int)
    pd_moca_file['Subject_ID']= pd_moca_file['Subject_ID'].astype(int)
    pd_sub_id = list(set(pd_dataframe['SubjectID'])) #List of subject ids
    pd_sub_id.sort()
    
    #-----MoCA Validation Loop (v1.4)
    # Para cada sujeto: se emparejan sus resonancias con sus MoCA usando
    # match_moca_to_mri. Primero se agotan los MoCA 1:1 (Kuhn), luego
    # se duplica solo si sobran resonancias.
    pd_frames = []
    for i in pd_sub_id:
        print(i)
        ct_tmp = pd_moca_file[pd_moca_file['Subject_ID']==i].copy()
        bt_tmp = pd_dataframe[pd_dataframe['SubjectID']==i]
        ct_tmp = ct_tmp.drop(columns=MOCA_COLS_TO_DROP, errors='ignore')
        tmp_df = match_moca_to_mri(bt_tmp, ct_tmp)
        if not tmp_df.empty:
            pd_frames.append(tmp_df)
    pd_validated_df = (pd.concat(pd_frames, axis=0, ignore_index=True)
                       if pd_frames else pd.DataFrame())

    # v1.4: dropna() solo sobre columnas clínicas críticas. Antes era global
    # y mataba resonancias con algún NaN en columnas no críticas.
    essential = [c for c in ['MoCA_Scores', 'MoCA_Dates'] if c in pd_validated_df.columns]
    if essential:
        pd_validated_df = pd_validated_df.dropna(subset=essential)
    # v1.4: NO se filtra por 'Quality control' de AssemblyNet.
    # El filtro de calidad es la presencia en MRIQC FLTRD (aplicado en el merge).
    pd_validated_df = pd_validated_df.reset_index(drop=True) #Reset indexes 
    # Auditoría de duplicación
    summarize_duplication(pd_validated_df, 'PD')
    
if 'Control' in stype:
    print('starting ctrls')
    #-----Cast Subject ID as Integer
    ctrl_dataframe['SubjectID']= ctrl_dataframe['SubjectID'].astype(int)
    ctrl_moca_file['Subject_ID']= ctrl_moca_file['Subject_ID'].astype(int)
    ctrl_sub_id = list(set(ctrl_dataframe['SubjectID'])) #List of subject ids
    ctrl_sub_id.sort()
    
    #-----MoCA Validation Loop (v1.4)
    ctrl_frames = []
    for i in ctrl_sub_id:
        print(i)
        ct_tmp = ctrl_moca_file[ctrl_moca_file['Subject_ID']==i].copy()
        bt_tmp = ctrl_dataframe[ctrl_dataframe['SubjectID']==i]
        ct_tmp = ct_tmp.drop(columns=MOCA_COLS_TO_DROP, errors='ignore')
        tmp_df = match_moca_to_mri(bt_tmp, ct_tmp)
        if not tmp_df.empty:
            ctrl_frames.append(tmp_df)
    ctrl_validated_df = (pd.concat(ctrl_frames, axis=0, ignore_index=True)
                         if ctrl_frames else pd.DataFrame())

    essential = [c for c in ['MoCA_Scores', 'MoCA_Dates'] if c in ctrl_validated_df.columns]
    if essential:
        ctrl_validated_df = ctrl_validated_df.dropna(subset=essential)
    ctrl_validated_df = ctrl_validated_df.reset_index(drop=True) #Reset indexes 
    summarize_duplication(ctrl_validated_df, 'CTRL')
    
    
if 'Prodromal' in stype:
    #-----Cast Subject ID as Integer
    prod_dataframe['SubjectID']= prod_dataframe['SubjectID'].astype(int)
    prod_moca_file['Subject_ID']= prod_moca_file['Subject_ID'].astype(int)
    prod_sub_id = list(set(prod_dataframe['SubjectID'])) #List of subject ids
    prod_sub_id.sort()
    
    #-----MoCA Validation Loop (v1.4)
    prod_frames = []
    for i in prod_sub_id:
        print(i)
        ct_tmp = prod_moca_file[prod_moca_file['Subject_ID']==i].copy()
        bt_tmp = prod_dataframe[prod_dataframe['SubjectID']==i]
        ct_tmp = ct_tmp.drop(columns=MOCA_COLS_TO_DROP, errors='ignore')
        tmp_df = match_moca_to_mri(bt_tmp, ct_tmp)
        if not tmp_df.empty:
            prod_frames.append(tmp_df)
    prod_validated_df = (pd.concat(prod_frames, axis=0, ignore_index=True)
                         if prod_frames else pd.DataFrame())

    essential = [c for c in ['MoCA_Scores', 'MoCA_Dates'] if c in prod_validated_df.columns]
    if essential:
        prod_validated_df = prod_validated_df.dropna(subset=essential)
    prod_validated_df = prod_validated_df.reset_index(drop=True) #Reset indexes 
    summarize_duplication(prod_validated_df, 'PROD')


#%%----------------------Validated Dataframes to Linear Model CSV--------------

if 'Control-Parkinsons' in stype:
    pd_validated_df.to_csv('PD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    ctrl_validated_df.to_csv('CTRL_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    
elif 'Control-Prodromal-Parkinsons' in stype:
    pd_validated_df.to_csv('PD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    ctrl_validated_df.to_csv('CTRL_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)
    prod_validated_df.to_csv('PROD_'+sname+'_VALIDATED_BRAIN-TRAK_LINMOD_DATAFRAME_'+(os.path.basename(sv_path)[:-4])+'.csv', index=False)