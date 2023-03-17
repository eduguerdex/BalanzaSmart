from flask import Flask,render_template,Response
from flask import request,send_file,redirect, url_for, jsonify
import cv2
import json
import mediapipe as mp
import imutils
from glob import glob
import serial, time
import screen_brightness_control as sbc 
import os
import webbrowser
import cv2
import imutils
import os
from time import   strftime
from datetime import datetime
import random
import sys
import cv2
import numpy as np
import tensorflow as tf
import array as arr
import pyqrcode
from pyzbar.pyzbar import decode
import pandas as pd
import collections
from IPython import display
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import itertools
import operator
import gspread
from mpl_toolkits.mplot3d import Axes3D
from IPython import display
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import seaborn as sb
import sys

# Credenciales Google
credentials={
  
}
#Variables usadas
gc = gspread.service_account_from_dict(credentials)
EMULATE_HX711=False
worksheet=[]
user_user_sim_matrix=[]
customer_item_matrix=[]
referenceUnit = 1
fig11=''
datos=''
dist=0
var=0
# arduino = serial.Serial('COM4',9600,timeout=1)
# arduino.close()
# arduino.open()
ced=[0,1]
pesaje=0.0
val_anterior=0
cap = None
cap2 = None
fixedlen = 10
list_data=[]
isRun=False
deteccion=0
deteccion2=0
deteccion3=0
producto1,producto2,producto3=[],[],[]
DNI1,producto,peso1 = [],[],[]
model = tf.keras.models.load_model("C:/Users/guerd/Downloads/modeloproduct.h5")
alimentos=["manzana","platano","beterraga","zanahoria","maiz","limon","cebolla","papa","camote","tomate"]
costos={"manzana":5.29,"platano":2.29,"beterraga":2.99,"zanahoria":3.49,"maiz":2.89,"limon":3.69,"cebolla":3.99,"papa":2.69,"camote":2.39,"tomate":3.29}
precioreal=0


path = os.path.dirname(os.path.realpath(__file__))
path= path+ '\static\css\images\\'

app = Flask(__name__, template_folder='templates')
#Funciones
def capturadatos():
    global worksheet,gc,DNI1,recomendacion,var,user_user_sim_matrix,customer_item_matrix, datos
    gc = gspread.service_account_from_dict(credentials)
    worksheet = gc.open('Datos_Balanza').worksheet('Ordenado')
    # get_all_values gives a list of rows.
    data=worksheet.get('D2:N')
    DatosUsuar=pd.DataFrame.from_records(data) 
    print(data) 
    # Convert to a DataFrame and render.      
    DatosUsuar=DatosUsuar.set_axis(['Documento', 'manzana', 'platano', 'beterraga','zanahoria', 'maiz', 'limon', 'cebolla', 'papa', 'camote', 'tomate'], axis=1)
    descridata=DatosUsuar.describe()
    customer_item_matrix = DatosUsuar.pivot_table(
        index='Documento'
    )
    customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0)
    user_user_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix))
    user_user_sim_matrix.columns = customer_item_matrix.index
    user_user_sim_matrix['Documento'] = customer_item_matrix.index
    user_user_sim_matrix = user_user_sim_matrix.set_index('Documento')
    user_user_sim_matrix.columns = customer_item_matrix.index

@app.route('/', methods=['POST'])
def evaluarcliente(documenton):
    global gc,user_user_sim_matrix,customer_item_matrix,path
    count=0
    dni=documenton
    documents=user_user_sim_matrix.index.tolist()
    cant_usuar=len(documents)
    for u in documents:
        count=count+1
        if dni==u:
            f=user_user_sim_matrix.loc[dni].sort_values(ascending=False)
            items_bought_by_A = set(customer_item_matrix.loc[dni].iloc[
                customer_item_matrix.loc[dni].to_numpy().nonzero()
            ].index)
            for i in range(1,5):
                usuar_similar=f.index.tolist()[i]
                print("usuario similar: "+usuar_similar)
                items_bought_by_B = set(customer_item_matrix.loc[usuar_similar].iloc[
                    customer_item_matrix.loc[usuar_similar].to_numpy().nonzero()
                ].index)
                items_to_recommend_to_A = set(items_bought_by_B) - set(items_bought_by_A)
                if items_to_recommend_to_A!=[]:
                    break
            if len(items_to_recommend_to_A) == 0:
                    popular =worksheet.get('V11')
                    recomendacion=[popular]
                    recomendacion=str(recomendacion).replace("[['"," ")[1:-1]
                    recomendacion=str(recomendacion).replace("']"," ")[1:-1]
                    print('\nProductos recomendados: ',recomendacion)
            for j in items_to_recommend_to_A:
                count=0
                if str(j)=="platano":
                    ruta_imagen = path+'platano.png'
                    print(ruta_imagen)
                elif str(j)=="limon":
                    ruta_imagen =  path+'limon.png'
                    print(ruta_imagen)
                elif str(j)=="cebolla":
                    ruta_imagen =  path+'cebolla.png'
                    print(ruta_imagen)
                elif str(j)=="manzana":
                    ruta_imagen =  path+'manzana.png'
                    print(ruta_imagen)
                elif str(j)=="camote":
                    ruta_imagen =  path+'camote.png'
                    print(ruta_imagen)
                elif str(j)=="papa":
                    ruta_imagen = path+'papa.png'
                    print(ruta_imagen)
                else:
                    print(str(j))
                valor = {
                        'imagen': str(j)
                }
                return jsonify(valor)
        if count==cant_usuar:
            popular =worksheet.get('V11')
            recomendacion=[popular]
            recomendacion=str(recomendacion).replace("[['"," ")[1:-1]
            recomendacion=str(recomendacion).replace("']"," ")[1:-1]
            j=recomendacion
            ruta_imagen = path+'papa.png'
            print('\nProductos recomendados: ',j)
            print(j)
            valor = {
                        'imagen': str(j)
                }
            return jsonify(valor)

def cleanAndExit():
    print("Cleaning...")
    # arduino.close()     
    print("Bye!")
    sys.exit()

# Creamos nuestra funcion de dibujo
app = Flask(__name__, template_folder='templates')

frame,frame2,ret2,ret=[],[],[],[]

@app.route("/detectar", methods=['POST'])
def detectar():
    global model,deteccion,deteccion2,deteccion3,cap2,cap,P1,P2,P3
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    #Extraccion de cada frame de video
    for i in range(5):
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
    print("imagen tomada")
    if ret and ret2 is True:
        image = cv2.resize(frame,(255,255),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        image2 = cv2.resize(frame2,(255,255),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)    
        cv2.imwrite(os.path.join(path , 'temp1.jpg'), image)
        cv2.imwrite(os.path.join(path , 'temp2.jpg'), image2)
        # cv2.imshow("cam1",image) 
        # cv2.imshow("cam2",image2)
        try:
            X = np.asarray(image)
            X2 = np.asarray(image2)
            X = np.expand_dims(X,axis=0)
            X2 = np.expand_dims(X2,axis=0)
            X = X/255
            X2 = X2/255
            #print(X)
            print("------")
            #print(X2)
            # #Prediccion del modelo
            Class = model.predict(X)
            Class2 = model.predict(X2)
            #Rxeajuste de la imagen a los parametros de entrada de la red
          # #Algoritmo para elegir los tres productos con mayor exactitud
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
            NM1 = [[]]
            NM2 = [[]]
            E = [[]]
            for i in B1:
                if P1==i:
                    deteccion=B1.index(i)
                if P2==i:
                    deteccion2=B1.index(i)
                if P3==i:
                    deteccion3=B1.index(i)
            return jsonify({"P1": P1, "P2": P2, "P3": P3})
            #render_template("Balanzaindex.html",producto1=P1,producto2=P2,producto3=P3)
        except ValueError:
           return redirect(url_for('detectar'))
    else:
        peso()
        cap.release()
        cap2.release()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

@app.route("/")
def index():
    global cap,cap2
    #return 'Hola Mundo'
    title='Balanza Smart'
    cap.release()
    cap2.release()
    capturadatos()
    return render_template("Home_forms.html",title=title)

documenton=0
@app.route('/', methods=['POST'])
def getvalue():
    global cap,cap2, documenton
    if request.method=='POST':
        documenton = request.form['ndocumento']
        print(documenton)
        if len(str(documenton))==8:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
            for i in range(5):
                ret, frame = cap.read()
                ret2, frame2 = cap2.read()
            if ret and ret2 is True:
                image = imutils.resize(frame, width=300,height=300)
                image2 = imutils.resize(frame2, width=300,height=300)
                cv2.imwrite(os.path.join(path , 'temp1.jpg'), image)
                cv2.imwrite(os.path.join(path , 'temp2.jpg'), image2)
            print("imagen tomada")
            take_photo()
            return render_template("Balanzaindex.html",documento1=documenton)
        else:
            return redirect('/')

@app.route('/obtener_imagen')
def obtener_imagen():
    global documenton
    # Lógica para obtener la imagen
    print(documenton)
    imagen = evaluarcliente(documenton)
    return imagen

@app.route("/video_feed")
def video_feed():
    return Response(gen_frame(),mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video2_feed")
def video2_feed():
    return Response(generate2(),mimetype = "multipart/x-mixed-replace; boundary=frame2")

@app.route("/cambiarImagen")
def take_photo():
    global path
    isExist = os.path.exists(path+'temp1.jpg')
    print(path+'temp1.jpg')
    if isExist:
        img = cv2.imread(path+'temp1.jpg')
        print("Listo para cargar")
        return send_file('static/css/images/temp1.jpg', mimetype="image/jpg")
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        #Extraccion de cada frame de video
        for i in range(5):
            ret, frame = cap.read()
            ret2, frame2 = cap2.read()
        print("imagen tomada")
        if ret and ret2 is True:
            image = imutils.resize(frame, width=300,height=300)
            image2 = imutils.resize(frame2, width=300,height=300)
            cv2.imwrite(os.path.join(path , 'temp1.jpg'), image)
            cv2.imwrite(os.path.join(path , 'temp2.jpg'), image2)
        return send_file('static/css/images/temp1.jpg', mimetype="image/jpg")

@app.route('/update_image')
def update_image():
    # Toma una fotografía y devuelve la URL de la imagen
    image_url = take_photo()
    if image_url:
        return

@app.route("/peso", methods = ['POST'])
def peso():
    global cap, cap2,P1,P2,P3
    pesaje = round(random.uniform(0.50, 5.50), 2)
    cap.release()
    cap2.release()
    detectar()
    while True:
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        print("El producto puede ser", P1, "o", P2, "o", P3)
        values = {
            'Peso': pesaje,
            'P1': P1,
            'P2': P2,
            'P3': P3
        }
        return jsonify(values)
     #global val_anterior, nivel, move,val,flag, arduino, cod,pasaje
     # try:
     #    cad = arduino.readline().decode('ascii').strip()
     #    print(cad)
     #    pos=cad.find("-:")
     #    eti=cad[:pos]
     #    val=cad[pos+1:]
     #    flag=1
          # if cad!=val_anterior:
          #      if eti=='pes':
          #       val_anterior=cad
          #       pesaje=val
          #       move=150
          #       texbal = Label(	ws,    text=pesaje+ ' Kg',    width=6,	height=0, font=('Arial',16, 'bold'), bg='gray22',fg ='deep sky blue')
          #       texbal_canva = canvas.create_window(485+move, 380,anchor = "center",	window = texbal	)
          #       #############TEXTO ################
          #       pesaje=float(pesaje)
          #       print("pesaje: ",pesaje," kg")
          #       arduino.write(b't')
          #      else:
          #       print("NO PESO")
          # else:
          #   print("repetido")
     #return 'Hola Mundo'
     
@app.route('/update-content')
def update_content():
  global cap, cap2
  # Obtener la información necesaria para actualizar el contenido de la página
  data = peso()
  return data

def gen_frame():
    global cap
    while True:
        ret, frame = cap.read()
        if ret==False:
            cap = cv2.VideoCapture(2, cv2.CAP_PROP_FPS,30)
            gen_frame()
        else:
            # Leemos la VideoCaptura
            frame = imutils.resize(frame, width=300,height=300)
        # Si tenemos un error
        if not ret:
            break
        else:
            # Observamos los resultados
            suc, encode = cv2.imencode('.jpg', frame)
            frame = encode.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def generate2():
    global cap2
    while True:
        ret2, frame2 = cap2.read()
        if ret2==False:
            cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
            generate2()
        else:
            # Leemos la VideoCaptura
            frame2 = imutils.resize(frame2, width=300,height=300)
        # Si tenemos un error
        if not ret2:
            break
        else:
            (flag, encodedImage) = cv2.imencode(".jpg", frame2)
            frame2 = encodedImage.tobytes()
        yield(b'--frame2\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

if __name__ == "__main__":
    #app.run(debug=False)
    app.run(host='0.0.0.0', port=5000, debug=False)
