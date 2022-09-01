# -*- coding: utf-8 -*-

"""
import numpy as np

import numpy as np

a = np.array([
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 8, 9]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18], [7, 8, 9]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18], [7, 8, 9]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18], [7, 8, 9]],
    [[10, 11, 12], [13, 14, 15], [16, 17, 18], [7, 8, 9]],
    ])
print(a)
print(a.shape) # shape(fila,columna,profundidad)
print(len(a.shape))

print(f'El arreglo está compuesto por {a.shape[0]} fila, {a.shape[1]} columnas y profundidad de {a.shape[2]}')

b = np.array([[1],[2],[3],[1],[2],[3],[1],[2],[3]])
print(b.shape) # shape(fila,columna,profundidad)
print(len(b.shape))
"""
#############################################################
import pandas as pd
import os
import os.path
from os import path

dfa = pd.read_csv('./data/Asistencia.csv')
print(dfa)

list_chosen_countries=dfa['Nombre estudiante'].tolist()
list_chosen_clase=dfa['dateRep'].tolist()
columna_1 = []
columna_2 = []
columna_3 = []
columna_4 = []
columna_5 = []

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

print(dfa)

g = os.listdir(f"Data_base_firebase2/DOCENTES/103354351174864699319/103354351174864699319_RUSVEL ENRIQUE PASOS LEYVA_CLASE DE PRUEBA.EL441/FOTO_CLASE")
horas_clase = 2
clases = len(g)

var = "Resultados2/fotos de clases/LAB DISEÑO/G1/Asistencia_cm.csv"
if not path.exists(var):
    print('No existe')
else:
    print('Existe')

