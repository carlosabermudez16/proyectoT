from server import app


app.config.suppress_callback_exceptions = True
########################################################## Se trabaja con la información de firebase ##########################################################

import shutil
"""
test_image = face_recognition.load_image_file(f'./data/IMG_20211002_082238.jpg')
pil_image = Image.fromarray(test_image)
img = pil_image
ancho, alto = img.size
img = img.resize((ancho,alto),Image.ANTIALIAS)

img.save(f'./data/image.jpg') # finalmente se guarda la imagen 

"""

""" 
Precision nos da la calidad de la predicción: ¿qué porcentaje de los que hemos dicho que son la clase positiva, en realidad lo son?
Recall nos da la cantidad: ¿qué porcentaje de la clase positiva hemos sido capaces de identificar?
F1 combina Precision y Recall en una sola medida
La Matriz de Confusión indica qué tipos de errores se cometen
"""

from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from mlxtend.plotting import plot_confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt


#y_true = np.array(['YAMILETH GARCIA','KATTY CHAVEZ','ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS','EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO'])

#y_pred = np.array(['YAMILETH GARCIA','KATTY CHAVEZ','ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS','EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO']) # clase 1

#y_pred = np.array(['YAMILETH GARCIA','KATTY CHAVEZ','ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS','EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO']) # clase 2

#y_pred = np.array(['YAMILETH GARCIA','KATTY CHAVEZ','ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS','EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO']) # clase 3

y_true = ['ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS','EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO']
#y_pred = ['ROSSANA PUELLO','MARLY PEDROZO','YAMILETH GARCIA' ,'EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO'] # clase 4

y_pred = ['ROSSANA PUELLO','MARLY PEDROZO','CINDY MONTECINOS' ,'EVA CRESPO','LIZETH TRESPALACIOS','LINDA MONTERO'] # clase 5

# Confusion Matrix
mc = confusion_matrix(y_true=y_true,y_pred=y_pred,labels=None)
confusionMatrixDisplay = ConfusionMatrixDisplay(confusion_matrix=mc, display_labels=None)

confusionMatrixDisplay.plot(cmap="Blues")
plt.show()

print('\n')
print(metrics.classification_report(y_true=y_true,y_pred=y_pred,digits=4))
print('\n')


"""
# Presición
clases = 12
estudiantes = 8

asistencia_total = clases*estudiantes

asistencia_real = 74

TP = 8
FP = 1
precision = TP + FP*TP
precision_real = 100 - precision

print(f'La metrica de precisión es de un : {precision_real}% '  )
FN = 0
recall = TP + FN*TP
recall_real = 100 - recall

print(f'La metrica de recall es de un : {recall_real}% '  )

F1 = 2*precision_real + recall_real*precision_real*recall_real
print(f'La metrica de F1 es de un : {F1}% '  )

TN = 0

accuracy = TP + TN + FP + FN*TP + TN
print(f'La metrica de exactitud es de un : {accuracy}% '  )

"""


