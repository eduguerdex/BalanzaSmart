from glob import glob
import serial, time
import screen_brightness_control as sbc 
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
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

mail="guerdex@guerdex.com"
credentials={
  "type": "service_account",
}
gc = gspread.service_account_from_dict(credentials)
EMULATE_HX711=False
worksheet=[]
user_user_sim_matrix=[]
customer_item_matrix=[]
referenceUnit = 1
fig11=''
datos=''
dist=0
arduino = serial.Serial('COM13',9600,timeout=1)
arduino.close()
arduino.open()

#Definiciones usadas
def capturadatos():
    global worksheet,gc,DNI1,recomendacion,var,user_user_sim_matrix,customer_item_matrix, datos
    gc = gspread.service_account_from_dict(credentials)
    worksheet = gc.open('Datos_Balanza').worksheet('Ordenado')
    # get_all_values gives a list of rows.
    data=worksheet.get('D2:N')
    DatosUsuar=pd.DataFrame.from_records(data)  
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

def evaluarcliente():
    global gc,user_user_sim_matrix,customer_item_matrix
    count=0
    dni=str(DNI1.pop())
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
                print(str(j))
                if str(j)=="platano":
                    lbl_recom=tk.Label(framerecom,image=platano,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                elif str(j)=="limon":
                    lbl_recom=tk.Label(framerecom,image=limon,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                elif str(j)=="cebolla":
                    lbl_recom=tk.Label(framerecom,image=cebolla,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                elif str(j)=="manzana":
                    lbl_recom=tk.Label(framerecom,image=manzana,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                elif str(j)=="camote":
                    lbl_recom=tk.Label(framerecom,image=camote,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                elif str(j)=="papa":
                    lbl_recom=tk.Label(framerecom,image=papa,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                else:
                    lbl_recom=tk.Label(framerecom,image=cebolla,bg='#FCFCFC',font=('Georgia', 20))
                    lbl_recom.grid(row=1,column=1,pady=0)
                break
        if count==cant_usuar:
            popular =worksheet.get('V11')
            recomendacion=[popular]
            recomendacion=str(recomendacion).replace("[['"," ")[1:-1]
            recomendacion=str(recomendacion).replace("']"," ")[1:-1]
            j=recomendacion
            print('\nProductos recomendados: ',j)
            lbl_recom=tk.Label(framerecom,image=manzana,bg='#FCFCFC',font=('Georgia', 20))
            lbl_recom.grid(row=1,column=1,pady=0)
    var.set(j)

def cleanAndExit():
    print("Cleaning...")
    #if not EMULATE_HX711:
        #GPIO.cleanup()      
    print("Bye!")
    sys.exit()
def agregar_usuar():
    global DNI1,producto1
    DNI1.append(ingresa_DNI.get())
    ingresa_DNI.delete(0,END)
    funcion()
def funcion():
    global DNI1
    print(DNI1)
    if len(DNI1[-1])==8:
        ws.state(newstate  = "normal")
        ws.focus()
        lbl_u.insert(0,DNI1[-1])
        root.state(newstate  = "withdraw")
        print("Data agregada")
        clear()
        evaluarcliente()
        iniciar()
    else: 
        print("Error: Colocar DNI con 8 digitos")
        messagebox.showinfo(message="Colocar los 8 dígitos del DNI", title="Error")
        clear()
def funcion2():
    global muestra, nivel
    ws.state(newstate  = "withdraw")
    root.state(newstate  = "normal") 
    frame2.grid_forget()
    muestra = 0
    move=150
    nivel=0
    print(muestra)
    val=0
    #############TEXTO ################
    texto = '0 Kg'
    print("valor: ",val)
    texbal = Label(	ws,text=' 0 Kg',    width=5,	height=0, font=('Arial',22, 'bold'), bg='gray22',fg ='deep sky blue')
    texbal_canva = canvas.create_window(485+move, 380,anchor = "center",	window = texbal	)
    canvas.create_oval(415+move,290,555+move,430, fill='gray22', outline='white', width=6)
    canvas.create_text(485+move, 380, text= texto, font=('Arial',22, 'bold'), fill ='deep sky blue')
    canvas.create_text(485+move, 335, text= 'PESO' , font=('Cambria Math',22, 'bold'), fill ='white')
    frame3.place_forget()
    delete()
    listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
    finalizar()
def agregarimage():
    global absolute_folder_path,QR, logo, ingresar, balanza, fond, grad,bg,home,settings,lista, iconhome,iconlogo, configuracion, iconlista, peso, platano,limon,manzana,cebolla,camote,papa

    absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
    absolute_image_path = os.path.join(absolute_folder_path, 'logo_balanza.png')
    logo = tk.PhotoImage(file = absolute_image_path)
    iconlogo1 = Image.open(absolute_image_path).resize((70,70),Image.ANTIALIAS)
    iconlogo= ImageTk.PhotoImage(iconlogo1)

    absolute_image_path1 = os.path.join(absolute_folder_path, 'ingresar.png')
    ingresar = tk.PhotoImage(file = absolute_image_path1)

    absolute_image_path2 = os.path.join(absolute_folder_path, 'balanza_cambio.png')
    balanza = tk.PhotoImage(file = absolute_image_path2)

    absolute_image_pathg = os.path.join(absolute_folder_path, 'gradiente.png')
    grad= tk.PhotoImage(file =absolute_image_pathg)

    absolute_image_pathi = os.path.join(absolute_folder_path, 'iconhome.png')
    iconhome1 = Image.open(absolute_image_pathi).resize((60,60),Image.ANTIALIAS)
    iconhome= ImageTk.PhotoImage(iconhome1)

    absolute_image_pathh = os.path.join(absolute_folder_path, 'home.png')
    home1 = Image.open(absolute_image_pathh).resize((210,60),Image.ANTIALIAS)
    home=ImageTk.PhotoImage(home1)

    absolute_image_paths = os.path.join(absolute_folder_path, 'iconsettings.png')
    settings1 = Image.open(absolute_image_paths).resize((60,60),Image.ANTIALIAS)
    settings=ImageTk.PhotoImage(settings1)

    absolute_image_pathc = os.path.join(absolute_folder_path, 'configuracion.png')
    configuracion1 = Image.open(absolute_image_pathc).resize((210,60),Image.ANTIALIAS)
    configuracion=ImageTk.PhotoImage(configuracion1)

    absolute_image_pathls = os.path.join(absolute_folder_path, 'lista.png')
    lista1 = Image.open(absolute_image_pathls).resize((210,60),Image.ANTIALIAS)
    lista=ImageTk.PhotoImage(lista1)

    absolute_image_pathil = os.path.join(absolute_folder_path, 'iconlista.png')
    iconlistal = Image.open(absolute_image_pathil).resize((60,60),Image.ANTIALIAS)
    iconlista=ImageTk.PhotoImage(iconlistal)

    absolute_image_pathpe = os.path.join(absolute_folder_path, 'peso.png')
    iconpeso1= Image.open(absolute_image_pathpe).resize((150,150),Image.ANTIALIAS)
    peso=ImageTk.PhotoImage(iconpeso1)

    absolute_image_pathb = os.path.join(absolute_folder_path, 'platano.png')
    incplatano= Image.open(absolute_image_pathb).resize((250,150),Image.ANTIALIAS)
    platano = ImageTk.PhotoImage(incplatano)
    absolute_image_pathlim = os.path.join(absolute_folder_path, 'limon.png')
    inclimin= Image.open(absolute_image_pathlim).resize((250,150),Image.ANTIALIAS)
    limon = ImageTk.PhotoImage(inclimin)
    absolute_image_pathman = os.path.join(absolute_folder_path, 'manzana.png')
    incmanzan= Image.open(absolute_image_pathman).resize((250,150),Image.ANTIALIAS)
    manzana = ImageTk.PhotoImage(incmanzan)
    absolute_image_pathcebo = os.path.join(absolute_folder_path, 'cebolla.png')
    incebo= Image.open(absolute_image_pathcebo).resize((250,150),Image.ANTIALIAS)
    cebolla = ImageTk.PhotoImage(incebo)
    absolute_image_pathcamo= os.path.join(absolute_folder_path, 'camote.png')
    incamo= Image.open(absolute_image_pathcamo).resize((250,150),Image.ANTIALIAS)
    camote = ImageTk.PhotoImage(incamo)
    absolute_image_pathpapa = os.path.join(absolute_folder_path, 'papa.png')
    inpapa= Image.open(absolute_image_pathpapa).resize((250,150),Image.ANTIALIAS)
    papa = ImageTk.PhotoImage(inpapa)
    absolute_image_pathqr= os.path.join(absolute_folder_path, 'qrcode.png')
    inqr= Image.open(absolute_image_pathqr).resize((250,250),Image.ANTIALIAS)
    QR = ImageTk.PhotoImage(inqr)
def arduinorecibe():
    global datos, dist
    print("dist: ",dist)
    if dist==0:
        cad = arduino.readline().decode('ascii')
        pos=cad.find(":")
        eti=cad[:pos]
        val=cad[pos+1:]
        flag=1
        if eti=='a':
            sbc.fade_brightness(val) 
        elif eti=='o':
            sbc.fade_brightness(val) 
        root.after(1000, arduinorecibe)
    
def obtener_hora_actual():
    global dia, fecha, hora
    hora =  strftime('%H:%M:%S')
    dia = strftime('%A')
    fecha = strftime('%d - %m - %y')
    if dia =='Monday':
	    dia = 'Lunes'
    elif dia =='Tuesday':
        dia = 'Martes'
    elif dia =='Wednesday':
        dia = 'Miercoles'
    elif dia =='Thursday':
        dia = 'Jueves'
    elif dia =='Friday':
        dia = 'Viernes'
    elif dia =='Saturday':
        dia = 'Sábado'
    elif dia =='Sunday':
        dia = 'Domingo'
    lbl_fd.config(text=fecha)
    return datetime.now().strftime("%H:%M:%S")
def refrescar_reloj():
    variable_hora_actual.set(obtener_hora_actual())
    ws.after(INTERVALO_REFRESCO_RELOJ, refrescar_reloj)
def iniciar():
    global cap, cap2, dist
    dist=1
    cap = cv2.VideoCapture(2)
    cap2= cv2.VideoCapture(0)
    if dist==1:
        sbc.fade_brightness(100)
    elif dist==0:
        sbc.fade_brightness(0)
    visualizar()
def visualizar():
    global cap, cap2, fig11
    if cap is not None:
        ret, frame = cap.read()
        ret2, fig2= cap2.read()
        if ret == True and ret2 == True:
            x240=500
            x0=x240-240
            fig11=frame[150:450,150:550]
            frame = imutils.resize(fig11, width=240,height=240)
            frame2 = imutils.resize(fig2, width=240,height=240)
            cv2image= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            cv2image2= cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img2 = Image.fromarray(cv2image2)
            imgtk = ImageTk.PhotoImage(image = img)
            imgtk2 = ImageTk.PhotoImage(image = img2)
            lblVideo.imgtk = imgtk
            lblVideo2.imgtk2 = imgtk2
            lblVideo.configure(image=imgtk)
            lblVideo2.configure(image=imgtk2)
            lblVideo.after(15, visualizar)
        else:
            lblVideo.image = ""
            lblVideo2.image = ""
            cap.release()
            cap2.release()
def finalizar():
    global cap, cap2, dist
    dist=0
    cap.release()
    cap2.release()
    arduinorecibe()
def progressBar():
    global nivel, move,val
    muestra=1
    arduino.write(b'i')
    ws.after(1000,get_data())    	
def get_data():
    global val_anterior, nivel, move,val,flag, arduino, cod,pasaje
    try:
        cad = arduino.readline().decode('ascii').strip()
        print(cad)
        pos=cad.find(":")
        eti=cad[:pos]
        val=cad[pos+1:]
        flag=1
        if cad!=val_anterior:
            if eti=='pes':
                val_anterior=cad
                pesaje=val
                move=150
                texbal = Label(	ws,    text=pesaje+ ' Kg',    width=6,	height=0, font=('Arial',16, 'bold'), bg='gray22',fg ='deep sky blue')
                texbal_canva = canvas.create_window(485+move, 380,anchor = "center",	window = texbal	)
                #############TEXTO ################
                pesaje=float(pesaje)
                print("pesaje: ",pesaje," kg")
                canvas.create_oval(415+move,290,555+move,430, fill='gray22', outline='white', width=6)
                #canvas.create_text(485+move, 380, text= texto, font=('Arial',22, 'bold'), fill ='deep sky blue')
                canvas.create_text(485+move, 335, text= 'PESO' , font=('Cambria Math',22, 'bold'), fill ='white')
            else:
                print("NO PESO")
                ws.after(1000,progressBar())
        else:
            print("repetido")
            ws.after(1000,progressBar())
    except:
        pass
def expand():
    global cur_width, expanded,move
    move=0
    cur_width += 10 # Increase the width by 10
    rep = ws.after(5,expand) # Repeat this func every 5 ms
    frame.config(width=cur_width) # Change the width to new increase width
    if cur_width >= max_w: # If width is greater than maximum width 
        expanded = True # Frame is expended
        ws.after_cancel(rep) # Stop repeating the func
        fill()
def contract():
    global cur_width, expanded, move
    cur_width -= 10 # Reduce the width by 10 
    move=0
    rep = ws.after(5,contract) # Call this func every 5 ms
    frame.config(width=cur_width) # Change the width to new reduced width
    if cur_width <= min_w: # If it is back to normal width
        expanded = False # Frame is not expanded
        ws.after_cancel(rep) # Stop repeating the func
        fill()
def fill():
    if expanded: # If the frame is exanded
        # Show a text, and remove the image
        home_b.config(image=home,command=funcion2,font=(0,21))
        set_b.config(image=configuracion,font=(0,21))
        lista_b.config(image=lista,font=(0,21))
        logo_b.config(image=logo,font=(0,21))
    else:
        # Blista the image back
        logo_b.config(image=iconlogo,font=(0,21))
        home_b.config(image=iconhome,font=(0,21))
        set_b.config(image=settings,font=(0,21))
        lista_b.config(image=iconlista,font=(0,21))
def borrarOmostrar():
    if frame2.grid_info() != {}:
        frame2.grid_remove()
        pagar.place_forget()
        eliminar.place_forget()
    else:
        width=1020
        height=720
        frame2.grid(padx=1,column = 0, row = 0,sticky=E,columnspan=3)
        pagar.place(x=(width*9/12)+20, y=495.0)
        eliminar.place(x=(width*10/12)+65, y=495.0)
        frame.after(5000, borrarOmostrar)
def retrievedata():
    ''' get data stored '''
    global list_data
    list_data = []
    try:
      with open("save.txt", "r", encoding="utf-8") as file:
       for f in file:
        listbox.insert(END, f.strip())
        list_data.append(f.strip())
        print(list_data)
    except:
        pass
def delete():
    global list_data
    listbox.delete(0, tk.END)
    lbl_u.delete(tk.END, tk.END)
    list_data = []
def calc_costos(producto):
    global alimentos,val, costos,deteccion,deteccion2,deteccion3,precioreal
    seleccionado=producto
    precio=costos[str(seleccionado)]
    print("precio: ",precio,"pesaje: ",val)
    pesaje=float(val)
    precioreal=precio*pesaje/1#tomando 1kg como valor base de costos
def add_item():
    global list_data,flag,fixedlen, precioreal,val, pesaje
    calc_costos(producto1.get())
    pesaje=float(val)
    if producto1 != "" and flag==1:
        item = ("{:<20s}"+(fixedlen-len(str(producto1.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(pesaje)))*" " +"{:<10.1f}"+(fixedlen-len(str(precioreal)))*"").format(producto1.get(),pesaje,precioreal)
        listbox.insert(END,item)
        list_data.append(producto1.get())
        producto1.set("")
        flag=0
    borrarOmostrar()     
def add_item2():
    global list_data,flag,fixedlen,precioreal, pesaje,val
    calc_costos(producto2.get())
    pesaje=float(val)
    if producto2 != "" and flag==1:
        #listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
        item = ("{:<20s}"+(fixedlen-len(str(producto2.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(pesaje)))*" " +"{:<10.1f}"+(fixedlen-len(str(precioreal)))*"").format(producto2.get(),pesaje,precioreal)
        listbox.insert(END,item)
        list_data.append(producto2.get())
        producto2.set("")
        flag=0
    borrarOmostrar()
def add_item3():
    global list_data,flag,fixedlen,precioreal, pesaje,val
    calc_costos(producto3.get())
    pesaje=float(val)
    if producto3 != "" and flag==1:
        #listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
        item = ("{:<20s}"+(fixedlen-len(str(producto3.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(pesaje)))*" " +"{:<10.1f}"+(fixedlen-len(str(precioreal)))*"").format(producto3.get(),pesaje,precioreal)
        listbox.insert(END,item)
        list_data.append(producto2.get())
        producto3.set("")
        flag=0
    borrarOmostrar()
def vision():
    global alimentos,deteccion,deteccion2, deteccion3,producto1, producto2, producto3, val
    frame3.place(	x=(width*5/24)+70, y=height*12/15,	anchor = "center")
    producto1 = StringVar(value=alimentos[deteccion])
    producto2 = StringVar(value=alimentos[deteccion2])
    producto3 = StringVar(value=alimentos[deteccion3])
    lbl_pc1.config(text = producto1.get())
    lbl_pc2.config(text = producto2.get())
    lbl_pc3.config(text = producto3.get())
    lbl_pc1.grid(row=0,column=0)
    lbl_pc2.grid(row=1,column=0)
    lbl_pc3.grid(row=2,column=0)
def detectar():
    global cap,cap2,model,deteccion,deteccion2,deteccion3
    ret,frame = cap.read()
    ret2,frame2 = cap2.read()
    #Extraccion de cada frame de video
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
    for i in B1:
        if P1==i:
            deteccion=B1.index(i)
            print(deteccion)
        if P2==i:
            deteccion2=B1.index(i)
            print(deteccion2)
        if P3==i:
            deteccion3=B1.index(i)
            print(deteccion3)
    #if cv2.waitKey(1) == ord('q'):
    vision()
def delete_selected():
    try:
        selected = listbox.get(listbox.curselection())
        listbox.delete(listbox.curselection())
        list_data.pop(list_data.index(selected))
        # reload_data()
        # # listbox.selection_clear(0, END)
        listbox.selection_set(0)
        listbox.activate(0)
        listbox.event_generate("&lt;&lt;ListboxSelect>>")
        print(listbox.curselection())
    except:
        pass
def qrfun():
    print(list_data)
    if len(list_data)!=0 :
        global qr,img
        datos = ('https://www.kushki.com/products/')
        qr = pyqrcode.create(datos)
        img = BitmapImage(data = qr.xbm(scale=7))
    else:
        messagebox.showwarning('Atención', 'No se ha detectado producto')
    try:
        display_code()
    except:
        pass

def display_code():
    global iconlqr
    iconlqr=Label(frameqr,image=img,bg='white',relief='flat')
    iconlqr.grid(row=0,column=0,pady=0)
    iconlqr.config(image = img)
def borrarOmostrarqr():
    if frameqr.grid_info() != {}:
        frameqr.grid_remove()
    else:
        frameqr.grid(padx=0,column = 0, row = 0,sticky=E,columnspan=1)
        #frameqr.place(	x=(width*20/24)+30, y=height*7/15,	anchor = "center")
        qrfun()
        frameqr.after(10000, borrarOmostrarqr)
def btnClik(num):
    global operador
    operador=operador+str(num)
    input_text.set(operador)
def clear():
    global operador
    operador=("")
    input_text.set("")

#Variables usadas
ced=[0,1]
pesaje=0.0
val_anterior=0
cap = None
cap2 = None
fixedlen = 10
list_data=[]
isRun=False
INTERVALO_REFRESCO_RELOJ = 300  # En milisegundos
width=1020
height=720
deteccion=0
deteccion2=0
deteccion3=0
producto1,producto2,producto3=[],[],[]
DNI1,producto,peso1 = [],[],[]
nivel = 0
min_w = 70
max_w = 220
cur_width = min_w 
expanded = False 
move=150
hora=0
val=0
muestra=0
flag=0
model = tf.keras.models.load_model("C:/Users/Aprender Creando/Documents/modeloproduct.h5")
alimentos=["manzana","platano","beterraga","zanahoria","maiz","limon","cebolla","papa","camote","tomate"]
costos={"manzana":5.29,"platano":2.29,"beterraga":2.99,"zanahoria":3.49,"maiz":2.89,"limon":3.69,"cebolla":3.99,"papa":2.69,"camote":2.39,"tomate":3.29}
precioreal=0



#Primera Ventana
root = Tk()
root.title("Registro")
root.geometry('1020x720+15+10')
root.resizable(0, 0)
root.config(bg='black')
root.state(newstate  = "normal")

arduinorecibe()

#Agregar Imagenes
agregarimage()
capturadatos()

root.call('wm', 'iconphoto', root._w, logo)
#Primera Ventana
canvas = tk.Canvas(
    root, bg="RoyalBlue1", height=720, width=1020,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(560, 0, 1020, 720, fill="#FCFCFC", outline="")
canvas.create_text(
    590.0, 266.0, text="DNI: ", fill="black",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    659, 210.0, text="Bienvenid@",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))
title = tk.Label(
    text="Balanza Smart", bg="RoyalBlue1",
    fg="white", font=("Arial-BoldMT", int(30.0)))
title.place(x=27.0, y=110.0)

input_text=StringVar()
ingresa_DNI = tk.Entry(bd=0, bg="black", highlightthickness=0, fg='white',textvariable=input_text,font=('arial',20,'bold'))
ingresa_DNI.place(x=630.0, y=280, width=321.0, height=35)
usuario_actual = StringVar(value=input_text)

color_boton=("gray77")
ancho_boton=5
alto_boton=1
operador=""
nume=640
numy=150
Button(canvas,text="9",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(9)).place(x=17+nume,y=180+numy)
Button(canvas,text="8",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(8)).place(x=107+nume,y=180+numy)
Button(canvas,text="7",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(7)).place(x=197+nume,y=180+numy)
Button(canvas,text="6",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(6)).place(x=17+nume,y=240+numy)
Button(canvas,text="5",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(5)).place(x=107+nume,y=240+numy)
Button(canvas,text="4",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(4)).place(x=197+nume,y=240+numy)
Button(canvas,text="3",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(3)).place(x=17+nume,y=300+numy)
Button(canvas,text="2",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(2)).place(x=107+nume,y=300+numy)
Button(canvas,text="1",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(1)).place(x=197+nume,y=300+numy)
Button(canvas,text="0",font = ("Helvetica", 20),bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(0)).place(x=107+nume,y=360+numy)
Button(canvas,text="C",font = ("Helvetica", 20),bg="Skyblue1",width=ancho_boton,height=alto_boton,command=clear).place(x=17+nume,y=360+numy)

path_picker_button = tk.Button(
    image=ingresar,
    compound = 'center',
    fg = 'white',
    bg='#FCFCFC',
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda:[agregar_usuar()],relief = 'flat')
path_picker_button.place(
    x = 760, y = 600,
    width = 300,
    height = 60)
info_text = tk.Label(
    text="Esta es la nueva balanza inteligente\n"
    "\n"
    "Coloca tu DNI y pulsa INGRESAR \n\n"
    "Encima de la bandeja situa el producto\n"
    "que deseas pesar.\n\n"
    "Selecciona el producto que has pesado\n\n"
    "Puedes pagar usando el QR de la pantalla",
    bg="RoyalBlue1", fg="white", justify="left",
    font=("Georgia", int(16.0)))
info_text.place(x=27.0, y=200.0)
lbl_balanza=tk.Label(canvas,image=balanza,bg='RoyalBlue1')
lbl_balanza.place(x=50.0, y=475.0)
lbl_logo=tk.Label(canvas,image=logo,bg='#FCFCFC')
lbl_logo.place(x=805.0, y=0.0)

#Segunda Ventana
ws = Toplevel()
var=StringVar()
ws.state(newstate  = "withdraw")
ws.title("Balanza Smart")
ws.geometry('1020x720+15+10')
ws.config(bg='black')
ws.overrideredirect(True)

canvas = Canvas(ws, height=720, width=1020,
    bd=0, highlightthickness=0, relief="ridge")
canvas.create_image(width/2, height/2,image=grad,anchor = "center")
ws.resizable(width=False, height=False)
canvas.grid(row=0,column=0) 
canvas.create_text((width/2)+70, height/15, text = 'Balanza Smart', fill='white',font=('Georgia', 40,"bold"))
 
canvas.create_oval(390+move,265,575+move,430, fill="", outline ='',width=5)
canvas.create_oval(392+move,270,578+move,450, fill= '', outline='white', width= 6)

btn = Button(ws,image=peso,command=lambda:[progressBar(),detectar()] ,bg='#2989cc',relief='flat')
btn_canvas = canvas.create_window((width*15/24), height*12/15,anchor = "center",window = btn)

lblVideo = Label(ws)
lblVideo_canvas3 = canvas.create_window((width*4/24)-10, height*3/15,anchor = "nw",window = lblVideo)
lblVideo2 = Label(ws)
lblVideo2_canvas3 = canvas.create_window((width*4/24)-10, (height*3/15)+170,anchor = "nw",window = lblVideo2)

lbl_u = Listbox(ws,height=1, width=10,bg='#2989cc',fg='black',font=('Georgia', 15,"bold"),justify='center')
lblu_canvas = canvas.create_window(	(width*5/24)+70, height*2/15,	anchor = "center",	window = lbl_u	)

variable_hora_actual = StringVar(ws, value=obtener_hora_actual)
lbl_fh = Label(	ws,    textvariable=variable_hora_actual ,    width=10,	height=0, font =('Fixedsys', 20,"bold"), bg='#2989cc')
lblfh_canvas = canvas.create_window((width*21/24)-30, height*2/15,	anchor = "center",	window = lbl_fh	)

lbl_fd = Label(	ws, width=9,	height=0, font =('Georgia', 21,"bold"), bg='black', fg='#2989cc')
lblfd_canvas = canvas.create_window((width*21/24)-30, height*2/15+30,	anchor = "center",	window = lbl_fd	)
refrescar_reloj()


#Menu desplegable lateral
ws.update() # For the width to get updated

frame = Frame(ws, bg='black', width=70, height=720)
frame.grid(column = 0, row = 0,sticky=W)
# Iconos
logo_b=Label(frame,image=iconlogo,bg='white',relief='flat')
home_b = Button(frame,image=iconhome,command=funcion2,bg='black',relief='flat')
set_b = Button(frame,image=settings,bg='black',relief='flat')
lista_b = Button(frame,image=iconlista,command=borrarOmostrar,bg='black',relief='flat')

# Colocar elementos
logo_b.grid(row=0,column=0,pady=50)
set_b.grid(row=1,column=0,pady=20)
lista_b.grid(row=2,column=0,pady=20)
home_b.grid(row=3,column=0,pady=100)

# Bind to the frame, if entered or left
frame.bind('<Enter>',lambda e: expand())
frame.bind('<Leave>',lambda e: contract())

# So that it does not depend on the widgets inside the frame
frame.grid_propagate(False)

frame2 = Frame(ws, bg='white', width=250, height=350)
frame2.grid_propagate(False)

frameqr = Frame(ws, bg='white', width=300, height=280)
frameqr.grid_propagate(False)


framerecom = Frame(ws, bg='white', width=250, height=150)
framerecom.grid_propagate(False)
framerecom.place(	x=(width*20/24)+30, y=height*13/15,	anchor = "center")
#lbl_oferta=tk.Label(framerecom,textvariable=var,bg='#FCFCFC',font=('Georgia', 20))
#lbl_oferta.grid(row=2,column=1,pady=0)

listbox = Listbox(frame2,height=400, width=250,font=('Georgia', 10))
listbox.grid(row=1,column=1,pady=0)
listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
eliminar = Button(	ws,   text="Eliminar\nseleccionado",    width=10,	height=2,command=delete_selected,font=('Georgia', 9,"bold"))
pagar = Button(	ws,    text="Pagar\nproductos",    width=10,	height=2,command=borrarOmostrarqr,font=('Georgia', 9,"bold"))

#barra=Scrollbar(ws, command=listbox.yview)
#barra.grid(row=2,column=1,pady=0)
#listbox.config(yscrollcommand=barra)

frame3 = Frame(ws, bg='#2989cc', width=150, height=100)
lbl_pc1 = Button(	frame3,   textvariable=producto1,    width=10,	height=1,command=add_item,font=('Georgia', 15,"bold"))
lbl_pc2 = Button(	frame3,    textvariable=producto2,    width=10,	height=0,command=add_item2,font=('Georgia', 13,"bold"))
lbl_pc3 = Button(	frame3,    textvariable=producto3,    width=10,	height=0,command=add_item3,font=('Georgia', 12,"bold"))
ws.mainloop()
root.mainloop()

if (SystemExit):
    cleanAndExit()
