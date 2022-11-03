import cv2
import tensorflow as tf
import numpy as np
import time
import array as arr
import h5py
model = tf.keras.models.load_model("modeloproduct.h5")
#model = h5py.File('modelAlex.h5','r')
cap2 = cv2.VideoCapture('projectApple1.mp4')

while True:
    #Visualizacion del video
    ret,frame = cap2.read()
    ret2,frame2 = cap2.read()
    #Extraccion de cada frame de video
    cv2.imshow('frame',frame)
    cv2.imshow('frame', frame2)
    #Reajuste de la imagen a los parametros de entrada de la red
    image = cv2.resize(frame,(255,255))
    image2 = cv2.resize(frame2,(255,255))
    X = np.asarray(image)
    X2 = np.asarray(image2)
    X = np.expand_dims(X,axis=0)
    X2 = np.expand_dims(X2,axis=0)
    X = X/255
    X2 = X2/255
    #Prediccion del modelo
    Class = model.predict(X)
    Class2 = model.predict(X2)
    #Algoritmo para elegir los tres productos con mayor exactitud
    B1 = ['Manzana', 'Banana','Beterraga', 'Zanahoria', 'Maiz', 'Limon', 'Cebolla', 'Papa', 'Camote','Tomate']

    A2 = [Class[0][0], Class[0][1], Class[0][2], Class[0][3], Class[0][4], Class[0][5], Class[0][6], Class[0][7], Class[0][8], Class[0][9]]
    A3 = [Class2[0][0], Class2[0][1], Class2[0][2], Class2[0][3], Class2[0][4], Class2[0][5], Class2[0][6], Class2[0][7], Class2[0][8], Class[0][9]]

    NM1 = np.sort(Class)
    NM2 = np.sort(Class2)

    E11 = NM1[0][9]
    E12 = NM1[0][8]
    E13 = NM1[0][7]

    E21 = NM2[0][9]
    E22 = NM2[0][8]
    E23 = NM2[0][7]

    E = [[E11, E12, E13, E21, E22, E23]]
    NME = np.sort(E)
    EF1 = NME[0][5]
    EF2 = NME[0][4]
    EF3 = NME[0][3]

    try:
        O1 = A2.index(EF1)
    except ValueError:
        O1 = A3.index(EF1)

    try:
        O2 = A2.index(EF2)
    except ValueError:
        O2 = A3.index(EF2)

    try:
        O3 = A2.index(EF3)
    except ValueError:
        O3 = A3.index(EF3)

    P1 = B1[O1]
    P2 = B1[O2]
    P3 = B1[O3]

    print("El producto puede ser", P1, "o", P2, "o", P3)

    NM1 = [[]]
    NM2 = [[]]
    E = [[]]

    if cv2.waitKey(1) == ord('q'):
        break

cap2.release()
cv2.destroyAllWindows()



