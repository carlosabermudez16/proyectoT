import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from server import app
from dash.exceptions import PreventUpdate

import face_recognition
from PIL import Image, ImageDraw, ImageFont
import os
import os.path
from os import path, remove
import numpy as np
from datetime import datetime
from pathlib import Path
import pandas as pd
import pyrebase
from firebase import firebase
import json 
import shutil
import itertools
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil
from database.config import Config


app.config.suppress_callback_exceptions = True  # hace parte de frontend

############# Hace parte de backend #############

config = Config.firebase_connetion

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

var0 = 'data1'
carpeta_datos = 'Archivo_JSON'
archivo = 'informacion.json'
destino = carpeta_datos + '/'

if os.path.exists(var0):
    print('carpeta de envio de datos ya existe')
else:
    os.makedirs(var0, exist_ok=True)

if os.path.exists(carpeta_datos):
    info = os.listdir(destino)
    if len(info) == 1:
        new_archivo = carpeta_datos + '/' + str(int(info[0][0]) + 1) + archivo
    else:
        new_archivo = carpeta_datos + '/' + str(int(info[1][0]) + 1) + archivo
    storageRef = storage.download(filename= new_archivo, token='gs://fir-tutorial-ff628.appspot.com/')
else:
    os.makedirs(carpeta_datos, exist_ok=True)
    storageRef = storage.download(filename= carpeta_datos + '/' + '1informacion.json', token='gs://fir-tutorial-ff628.appspot.com/')

new_info = os.listdir(destino)
print(new_info,type(new_info),len(new_info))

lista = []

n = 0

def filedownload(conteo,n):
    a = 0 
    sumador = 0
    m = []

    while n < conteo:
                    for i in lista[n]:
                        
                        if i == "/":
                            print(a)
                            sumador +=1
                            m.append(a)
                        a += 1

                    folder_name = lista[n][:m[sumador-1]]
                    print(folder_name) # muestra cada una de las carpetas obtenidas en la base de datos
                    contenido = os.listdir('.')
                    print(contenido)    # Muestra todo lo que hay en el directorio
                        
                    os.makedirs('Data_base_firebase2/'+folder_name, exist_ok=True)
                    name_file_download = lista[n][m[sumador-1]+1:]
                        
                    storage.child(lista[n]).download('Data_base_firebase2/'+folder_name+'/'+name_file_download)
                    
                    sumador = 0
                    a = 0
                    m = []
                    n +=1


if len(new_info) > 2:    
    os.remove(carpeta_datos + '/' + new_info[0])

    new_info2 = os.listdir(destino)

    sizefile1 = os.stat(carpeta_datos + '/' + new_info2[0]).st_size
    sizefile2 = os.stat(carpeta_datos + '/' + new_info2[1]).st_size
    peso_mayor = sizefile2 > sizefile1
    
    if peso_mayor == True:
        with open(carpeta_datos + '/' + new_info2[1]) as file:
                    conteo = 0
                    data = json.load(file)
                    for items in data['items']:
                        conteo += 1
                        lista.append(items['name'])
                    file.close()
        
        filedownload(conteo,n)

elif len(new_info) == 2:
    sizefile1 = os.stat(carpeta_datos + '/' + new_info[0]).st_size
    sizefile2 = os.stat(carpeta_datos + '/' + new_info[1]).st_size
    peso_mayor = sizefile2 > sizefile1
    
    if peso_mayor == True:
        with open(carpeta_datos + '/' + new_info[1]) as file:
                    conteo = 0
                    data = json.load(file)
                    for items in data['items']:
                        conteo += 1
                        lista.append(items['name'])
                    file.close()
        
        filedownload(conteo,n)
else:
    with open(carpeta_datos + '/' + new_info[0]) as file:
        conteo = 0
        data = json.load(file)
        for items in data['items']:
            conteo += 1
            lista.append(items['name'])
        file.close()
    
    filedownload(conteo,n)


materia = os.listdir('Data_base_firebase2/DOCENTES/107435720803934230443') # condición especifica de uso para este proyecto
print(materia)

materias = [i[-5:] for i in materia]

nombre = sorted(materias)
print(nombre)

# CODIGO --> Para este proyecto debe de contener todas las asignaturas impartidas en la universidad
# para la realización del proyecto no se usó, lo que se hizo fue que se agrego una asinatura tipo par key/value que pertenece al
# docente que dió su concentimiento para la recolección de los daots.
CODIGO = {'FR001':'PEDAGOGÍA','EL441':'LAB DISEÑO','EL442':'TRA_TO DE SEÑALES','EL417':'CONTROL I','CL843':'','EL422':'CONTROL II','EL420':'COMUNICACIONES I','EL443':'TELEMATICA I','EL448':'PROYECTO II'}
Asignaturas = []
claves_asignaturas = []
for clave in nombre:
  if clave in CODIGO:
    #print (clave, ":", CODIGO[clave])
    Asignaturas.append(CODIGO[clave])
    claves_asignaturas.append(CODIGO[clave])
    claves_asignaturas.append(clave)

print(Asignaturas)
plain_list_iter = iter(claves_asignaturas)
plain_list_dict_object = itertools.zip_longest(plain_list_iter, plain_list_iter, fillvalue=None)
claves_asignaturas = dict(plain_list_dict_object)

print(f'estos son {claves_asignaturas}')

############# final de la parte del backend #############


#-----------botones, grupo, clases y tabla3 es frontend--------

clases = html.Div([
                                
            html.Div(
                    [
                    html.Button(
                                children=str(i),
                                #n_clicks=0,
                                
                                type='submit',
                                id= f'{claves_asignaturas.get(i)}-button',
                                value = claves_asignaturas.get(i),
                                className='btn9',
                                hidden= False,
                                ),
                    dcc.Store(id=claves_asignaturas.get(i)),
                    html.Div(id=claves_asignaturas.get(i)+'-clicks', children='')
                    
                    ],className='col-lg-5',style={'background':'transparent','margin-left':'20px'}
                                    
                ) for i in Asignaturas
                            
            ],className='col-lg-12',style={'display': 'flex',  
                'flex-wrap': 'wrap', 'background':'transparent','margin-top':'10px', 'margin-bottom':'20px'}
        )


grupos = ['G1','G2','G3','G4','G5','G6']

grupo = html.Div([
        
        dcc.RadioItems(
            id = 'grupos_clase',
            options=[{'value': i, 'label': i} for i in grupos],
            value='',
            labelStyle={'display':'inline-block','font-size':'14px',
                        'padding-left':'22px',
                        }     
        ),
    ],className='col-lg-12',style={'display': 'flex', 
                'flex-wrap': 'wrap', 'background':'transparent','margin-top':'20px', 'margin-bottom':'20px'}
                )

botones = html.Div([
        html.Div([
            html.Button(
                children='Procesar',
                n_clicks=0,
                type='submit',
                id='btn6',
                className='col-lg-3',
                        ),
            html.Div(id='salida1', children='')
            ]),
        
        html.Div([
            dcc.ConfirmDialog(
                id='confirm',
                message='Para enviar los archivos procesados, primero debe realizar los pasos siguientes: 1) Elegir un grupo, 2) Elegir Asignatura, 3) Click en Procesar',
            ),
            html.Button(
                children='Enviar reporte',
                n_clicks=0,
                type='submit',
                id='btn8',
                className='col-lg-5'
                ),
            html.Div(id='salida3', children='')
        ]),
        html.Br(),
    ],className='col-lg-12',style={'margin-top':'10px', 'margin-bottom':'20px'}
                        )

dfaa = pd.DataFrame(
                  columns=['Nombre', 'Total_As', 'Fallas']
                  )

def tabla_output(id_data,dataframe):
    dataframe = pd.DataFrame(dataframe)
    
    return html.Div([
            
            dash_table.DataTable(
                                    id= id_data,
                                    columns = [{'name':i, 'id':i, "hideable": True} for i in dataframe.columns],
                                    data = dataframe.to_dict('records'),
                                    selected_rows=[],
                                    export_columns="all",
                                    export_format="xlsx",
                                    export_headers ="names",
                                    filter_action = 'native',
                                    style_filter_conditional=[{
                                                
                                                'backgroundColor': 'rbga(165,177,205,.2)',
                                                
                                            }],
                                    #sort_action = 'native',
                                    sort_mode = 'multi',
                                    page_size = 12,
                                    row_selectable = 'multi', 
                                    style_cell = {
                                        #'whiteSpace': 'normal',
                                        #'height': 'auto',
                                        'textAlign': 'center',
                                         "backgroundColor": "#1f2c56",
                                         
                                         "border-bottom": "0.01rem solid #19aae1",
                                    },
                                    

                                    style_data_conditional=[{
                                                        'if': {'column_id': 'Nombre'},
                                                        'textDecoration': 'underline',
                                                        'textDecorationStyle': 'dotted',
                                                    }],
                                    #tooltip_delay=0,
                                    #tooltip_duration=None,
                                    
                                    style_header = {
                                        
                                        'fontWeight':'bold',
                                        #'backgroundColor': "paleturquoise",
                                        
                                        "font": "Lato, sans-serif",
                                        "color": "#00d970",
								        "border": "#1f2c56"
                                    },
                                    style_as_list_view = True,
							        style_data = {
                                                #'backgroundColor':"lavender",
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
								                "styleOverflow": "hidden",
								                "color": "#a5b1cd"
							        },

                                ),
                    ], className = "create_container col-lg-3",style={'font-size':'10px'}
                    )

datatable = tabla_output('table',dfaa)
aside =   html.Div([
                        html.H2('Tablero de clases',
                                style={'text-align':'center'}),
                        html.P('En este espacio puede ver y actualizar las materias impartidas.',
                                style={'text-align':'center','font-size':'14px','padding-top':'10px'}),

                        html.Br(),html.Hr(),
                        botones,
                        html.Hr(),
                        grupo,
                        html.Hr(),
                        clases,
                        html.Hr(),
                        
                        

                    ], className = "sidebar col-lg-12"
                    )


layout = html.Div([
    aside,
    datatable,

])



for store in nombre:

    # adiciona click a la propiedad alamenamiento.
    @app.callback(Output(store, 'data'),
                  Input('{}-button'.format(store), 'n_clicks'),
                  Input('{}-button'.format(store), 'value'),
                  State(store, 'data'),
                  )
    def on_click(n_clicks, valor2,data):

        if n_clicks is None:
            # Evitar las devoluciones de llamada None es importante con 
            # el componente de almacenamiento. no quieres actualizar la tienda por nada.
            raise PreventUpdate

        
        # Proporcione un dictado de datos predeterminado con 0 clics si no hay datos.
        data = data or {'clicks': 0,'value':valor2}
        
        data['clicks'] = data['clicks'] + 1
        

        return data

    # generar los clics almacenados en la celda de la tabla.
    @app.callback(Output('{}-clicks'.format(store), 'children'),
                  
                  Input(store, 'modified_timestamp'),
                  Input(store, 'data'))
    def on_data(ts, data):
        
        if ts is None:
            raise PreventUpdate

        data = data or {}
        
        #print(f'\n{data}',ts)

        return 


@app.callback([Output('table', 'data'),
              Output("table", "tooltip_data")],
              Input('grupos_clase', 'value'),
              Input('btn6', 'n_clicks'),
              [Input(store, 'data') for store in nombre],
              [Input(store, 'modified_timestamp') for store in nombre]
              )
def filter(grupos_clase,procesar,data,ts1):#data1,data2,ts1,ts2,ts3):
    
    if ts1 is None:
        ts1 = 0
    numeros = [ts1]
    mayor = max(numeros)

    if data == None:
        raise PreventUpdate
    else:
        n_clicks1 = data.get('clicks')
    
    valor2 = data.get('value')

    valor1 = grupos_clase
    print(f'{n_clicks1}:{valor1}:{valor2}:{procesar}')
    print(f'{type(n_clicks1)}:{type(valor1)}:{type(valor2)}:{type(procesar)}')
    
    lista1 = []
    if len(lista1) == 0: 
        
        aux1 = 1 if n_clicks1 != 0 else 0
        aux2 = valor1 if valor1 != '' else ''
        aux3 = valor2 if valor2 != '' else ''
        aux4 = 1 if procesar != 0 else 0
        lista1.append(aux1)
        lista1.append(aux2)
        lista1.append(aux3)
        lista1.append(aux4)
    else:
         lista1.clear()
         aux1 = 0
         aux2 = ''
         aux3 = ''
         aux4 = 0
         lista1.append(aux1)
         lista1.append(aux2)
         lista1.append(aux3)
         lista1.append(aux4)
            
    print(f'aux1 --> {lista1[0]} aux2 --> {lista1[1]} aux3 --> {lista1[2]} aux4 --> {lista1[3]}')
    
    if (lista1[1] in grupos and lista1[2] in nombre and lista1[0] != 0):
        # las lineas 54-57 se pregunta el nombre del grupo y se crea una carpeta llamada "fotos de clases"
        # que contiene adentro las subcarpeta de cada grupo
        nombre_materia = CODIGO.get(lista1[2])
        

        Path("Resultados2/fotos de clases/{}/{}".format(nombre_materia,lista1[1])).mkdir(parents=True, exist_ok=True)

        
        folder_name = f"Resultados2/fotos de clases/{nombre_materia}/{lista1[1]}"
       
        # creamos el archivo csv
        if 'Asistencia.csv' in os.listdir(folder_name):
            print('Archivo existente en carpeta')
        else:
           with open(f'./{folder_name}/Asistencia.csv','w') as f:      
               f.writelines('Nombre estudiante,Hora de entrada,dateRep\n')
           f.close()

        print(f'Ahora preciona procesar')

        def validacion_name(caras_seleccionadas,distancia):
            minima_distancia = min(distancia)
            first_match_index = np.where(distancia==minima_distancia)[0][0]
            name = known_face_names[first_match_index]
            print(f'{name} con distancia de {minima_distancia}')

            if not name in caras_seleccionadas:
                caras_seleccionadas.append(name)
                return name
            else:
                distancia = np.delete(distancia,first_match_index)
                return validacion_name(caras_seleccionadas,distancia)


        if lista1[3] != 0:

            known_face_names = []   # listas que contienen "nombre de rostros conocidos"
            known_face_encodings = []   # "codificación de rostros conocidos"
            datos_face_conocidos = {}

            train_dir = os.listdir('Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/ESTUDIANTES/')  # se accede a la carpeta de base datos para saber que contiene
            print('\n',train_dir, len(train_dir))

            carpeta_datos_face_conocidos = 'Archivo_JSON_dataface'

            if os.path.exists(carpeta_datos_face_conocidos):
                print('La carpeta de vector de estudiantes ya existe')
            else:
                os.makedirs(carpeta_datos_face_conocidos, exist_ok=True)

                # se hace un recorrido en cada carpeta que contiene la base de datos
                for person in train_dir:
                        pix = os.listdir("Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/ESTUDIANTES/" + person) # muestra lo que contiene cada subcarpeta de la base de datos
                        # se hace un recorrido por cada archivo que contienen las subcarpeta
                        for person_img in pix:
                            
                            print('\n',"Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/ESTUDIANTES/" + person + "/" + person_img)
                            # se cargan las imagenes contenida en cada subcarpeta
                            face = face_recognition.load_image_file("Data_base_firebase2/DOCENTES/107435720803934230443/107435720803934230443_Yolfanis Vides Uribe_FORMACION PEDAGOGICA .FR001/ESTUDIANTES/" + person + "/" + person_img)
                            face_locations1 = face_recognition.face_locations(face)
                            # genera una lista con la codificaión de cada rostro
                            face_encoding = face_recognition.face_encodings(face,face_locations1)[0]
                            
                            datos_face_conocidos[f'{person_img[:-4]}'] = face_encoding

                dataframe_datos_rostros_conocidos = pd.DataFrame(list(datos_face_conocidos.items()),
                                columns=['names', 'encodings'])

                print(dataframe_datos_rostros_conocidos)

                dataframe_datos_rostros_conocidos.to_json(f"{carpeta_datos_face_conocidos}" + '/vector_face_estudiantes.json', orient = 'table')


            with open('./Archivo_JSON_dataface/vector_face_estudiantes.json') as file:
                                conteo = 0
                                data = json.load(file)
                                for items in data['data']:
                                    conteo += 1
                                    known_face_names.append(items['names'])
                                    known_face_encodings.append(items['encodings'])
                                    
                                file.close()

            known_face_encodings = np.array(known_face_encodings)

            # Encontramos la carpeta del docente para seleccionar la subcarpeta Foto clase
            for i in materia:
                
                if lista1[2] in i:
                    result = i
                
                g = os.listdir(f"Data_base_firebase2/DOCENTES/107435720803934230443/{result}/FOTO_CLASE")
                #print(g)    
                for im in g:
                    
                    
                    # se agrega la imagen con la que se realizará el test para el reconocimiento facial
                    test_image = face_recognition.load_image_file(f'./Data_base_firebase2/DOCENTES/107435720803934230443/{result}/FOTO_CLASE/{im}')
                    
                    # localiza las coordenadas de los rostros que aparecen en la imagen de test
                    face_locations = face_recognition.face_locations(test_image)
                    # se obtienen las codificaciones de en cada uno de los rostros de la imagen de test
                    face_encodings = face_recognition.face_encodings(test_image, face_locations)

                    # Convierte la imagen a un formato de matriz de PIL
                    pil_image = Image.fromarray(test_image)

                    # se usa para crear nuevas imagenes, anotar o retocar imagenes existentes
                    draw = ImageDraw.Draw(pil_image)

                    contador_face_true = []
                    caras_seleccionadas = []
                    # se recorre a traves de las variables que contiene la localizaciones y
                    # las codificaciones de cada rostros en la imagen de test.
                    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        distancia = face_recognition.face_distance(known_face_encodings,face_encoding)
                        print(distancia)
                        # se compara cada una de las codificaiones de los rostros conocidos con las codificaciones
                        # de los rostros de test, el resultados es (True) or False.
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                        
                        # si es True la comparción entra en la condición para dibujar el rectangulo con el nombre de la persona
                        if True in matches:
                            contador_face_true.append(True)
                            name = validacion_name(caras_seleccionadas,distancia)
                            print(name)
                        else:
                            name = "Desconocido"  # texto que se le coloca a los rostros que no están en la base de datos


                        # dibuja el rectangulo
                        draw.rectangle(((left, top), (right, bottom)), outline=(255,255,0))

                        # escribe la etiqueta
                        text_width, text_height = draw.textsize(name)
                        draw.rectangle(((left,bottom - text_height - 10), (right, bottom)), fill=(255,255,0), outline=(255,255,0))
                        draw.text((left + 6, bottom - text_height - 5), name, fill=(0,0,0))

                        # En las lineas 89-97, es el proceso donde se registra la asistencia con el nombre y la fecha 
                        
                        with open(f'./{folder_name}/Asistencia.csv','r+') as f:
                            myDataList = f.readlines()
                            nameList = []   
                            today = datetime.today()
                            conv = today.strftime("%m/%d/%Y")
                            for line in myDataList:
                                entry = line.split(',')
                                nameList.append(entry[0])
                            now = datetime.now()
                            dtString = now.strftime('%H:%M:%S')

                            f.writelines(f'{name},{dtString},{conv}\n')

                        
                    # Guardamos la imagen
                    

                    nombre_img = f"{g.index(im)}_IG{im[10:-4]}.jpg" # nombre que tendrá la imagen con el reconocimiento facial aplicado
                    fecha = str(datetime.now()) # se convierte la fecha a un string


                    font = ImageFont.truetype("arial.ttf",40) # tamaño de letra en el texto que se adiciona en la foto
                    x, y = pil_image.size # tamaño de la imagen
                    draw.text((10,y/1.1),fecha,fill = "black",font = font, align = "down") # lugar donde se coloca la fecha en la imagen


                    # debemos eliminar la instancia de dibujo de la memoria, se realiza por recomendación según la documentación 
                    del draw 

                    img = pil_image
                    ancho, alto = img.size
                    img = img.resize((ancho,alto),Image.ANTIALIAS)


                    img.save(f'./{folder_name}/{nombre_img}') # finalmente se guarda la imagen 


                    img.save(f'./{var0}/{nombre_img}') # se guarda una copia

                    # se convierte el archivo csv a excel
                    df = pd.read_csv(f'./{folder_name}/Asistencia.csv')
                    df.to_csv(f'./{var0}/Asistencia.csv', index = False)
                    df.to_excel(f"./{folder_name}/Asistencia.xlsx", "Asistencia")

                    

                    ################# tratamiento de datos para la tabla #################
                    dfa = df#pd.read_csv('./data/Asistencia_2.csv')
                    list_chosen_countries=dfa['Nombre estudiante'].tolist()
                    list_chosen_clase=dfa['dateRep'].tolist()
                    columna_1 = []
                    columna_2 = []
                    columna_3 = []
                    columna_4 = []
                    columna_5 = []
                    columna_6 = [] 

                    for i in list_chosen_countries:
                        if i not in columna_1:
                            cantidad = list_chosen_countries.count(i)
                            columna_1.append(i)
                            columna_2.append(cantidad)
                        else:
                            columna_1.append(None)
                            columna_2.append(None)
                    for i in list_chosen_clase:
                        columna_5.append(64)
                        if i not in columna_3:
                            cantidad = list_chosen_clase.count(i)
                            columna_3.append(i)
                            columna_4.append(2)
                        else:
                            columna_3.append(None)
                            columna_4.append(0)

                    dfa['Total_Es'] = columna_1
                    dfa['Total_As'] = columna_2
                    dfa['Fechas clase'] = columna_3
                    dfa['Horas realizadas'] = columna_4
                    dfa['Horas semestre'] = columna_5

                    df2 = pd.DataFrame()
                    df2['Nombre'] = dfa['Nombre estudiante'].unique()
                    df2['Total_As'] = list(dfa['Total_As'].dropna())
                    

                    indice=0
                    for i in df2['Nombre']:
                        valor = len(g)- df2['Total_As'][indice]
                        columna_6.append(valor)
                        indice+=1 

                    df2['Fallas'] = columna_6

                    df2 = df2
                    #print('\n',df2)
                    
                    tooltip_data= [{'Nombre': 
                                        {'value': 'Estudiante: \n\n\n![foto]({})'.format(
                                                                    app.get_asset_url('images/'+str(value).replace(' ','_')+'.PNG')), 
                                        'type': 'markdown'
                                            } 
                                    } for value in df2['Nombre']],

                    #print(df2, type(df2))
                    var = f"{var0}/asistencia_cm.csv"
                    if not path.exists(var):
                        df2.to_csv(f'./{var0}/asistencia_cm.csv', index = False)
                    else:
                        remove(f'{var0}/asistencia_cm.csv')
                        df2.to_csv(f'./{var0}/asistencia_cm.csv', index = False)

            

            return df2.to_dict('records'),tooltip_data[0]

    else:
        #dfa = pd.read_csv('./data/Asistencia_3.csv')

        tooltip_data= [{'Nombre': 
                                {'value': 'Estudiante: \n\n\n![foto]({})'.format(
                                                            app.get_asset_url('images/'+str(value).replace(' ','_')+'.PNG')), 
                                 'type': 'markdown'
                                    } 
                            } for value in dfaa['Nombre']],
        # Return all the rows on initial load/no country selected.
        return dfaa.to_dict('records'),tooltip_data[0]

        
    raise PreventUpdate
    

@app.callback(Output('confirm', 'displayed'),
              Input('btn8', 'n_clicks'))
def display_confirm(value):

    #p = header.children
    #print(p)
    #p = p.children
    #p = p[0].children
    #p = p[0].id
    #print(p,type(p))

    var1 = "Envio_Reporte.zip"  # archivo de clase
    


    if value != 0 :
        print(value)
        if len(os.listdir(var0+'/')) >= 2:
            
                from database.config import Config
            
                archivo_zip = shutil.make_archive("Envio_Reporte", "zip", "data1")
                print("Creado el archivo:", archivo_zip)

                # pedimos datos para iniciar sesión
                usuario = Config.email
                #clave = getpass.getpass("Ingrese su clave:  ")
                clave = Config.password_email

                destinatario = "carlosabermudez@unicesar.edu.co"
                asunto = "Asistencia de clase"


                # crear mensaje
                mensaje = MIMEMultipart("alternative")   # estandar
                mensaje["Subject"] = asunto
                mensaje["From"] = usuario
                mensaje["To"] = destinatario

                html = f"""
                <html>
                <body>
                    Hola <i>{destinatario}</i><br>
                    Se adjunta el archivo de <b>asistencia</b>
                </body>
                </html>

                """

                # el contenido del mensaje como html
                parte_html = MIMEText(html,"html")
                # agregar ese contenido al mensaje
                mensaje.attach(parte_html)

                archivo =   var1 # archivo de clase

                # se adjunta a un mensaje de correo
                with  open(archivo, "rb") as adjunto:
                    contenido_adjunto = MIMEBase("application","octet-stream")
                    contenido_adjunto.set_payload(adjunto.read())

                encoders.encode_base64(contenido_adjunto)   # los bytes a enviar estan en base 64
                contenido_adjunto.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {archivo}",
                )

                mensaje.attach(contenido_adjunto)
                mensaje_final = mensaje.as_string

                # enviar el mensaje
                context = ssl.create_default_context()

                with smtplib.SMTP_SSL("smtp.gmail.com",465, context=context) as server:
                    server.login(usuario, clave)
                    print("Inició sesión")
                    server.sendmail(usuario,destinatario, mensaje.as_string())
                    server.close()
                    print('\nMensaje enviado')
                
            
                return False
        else:
            print('Los archivos aun no existen')
            return True
    
    
    return False


#if __name__ == '__main__':
#    app.run_server(debug=False)