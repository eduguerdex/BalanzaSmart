from glob import glob
from tkinter import *
import tkinter as tk
import os
import webbrowser
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
import time
from time import   strftime
from datetime import datetime
import random
import sys
import cv2
import numpy as np
import tensorflow as tf
import array as arr
import qrcode
from pyzbar.pyzbar import decode
import pandas as pd
import collections
from mpl_toolkits.mplot3d import Axes3D
from IPython import display
import sklearn
import sklearn.manifold
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import itertools
import operator
import gspread

mail="guerdex@guerdex.com"
clave="be53409620026d7f570fe25fc2f3853d25f9eab"
credentials={
  "type": "service_account",
  "project_id": "proyectobalanzasmart",
  "private_key_id": "cbe53409620026d7f570fe25fc2f3853d25f9eab",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC4wE/wuZIo+I5p\neHWR5Kf3lwzHwClucdAQKojZUzbAwbiDeeVIDvXWKkB8b9iwy59jF6+hHdKim1VF\nTu6uhq7dWG7eqAuvgqgNzDGOBE4HPF+lO9t4vwBcXgVpGRn+jKiGfLOiYr7FJVvr\nK7x+IAj0jhIVa+Ea3SVVBoGKs8Rr356D4YZzvYTUV1vNJ9jA8p9ZfbQ8/zdjqD+v\nlDbYRzeEMB0+5smijhPAVavqPgf513R7GObKWdOB1uclO1v0H4U4XydQ36vv2K3Y\nRrXf3pOoWvqErhrr+26JpAPZAMPF5Jaq42ZfbkQL2LTs3yY3L/B/TVpBuktDqiLj\nFMTYMdpjAgMBAAECggEAPXQewyR/BSjUeinK9cn4wycX5bO6NFYgTthPJ/cBjfGC\nNh2MUkFDrcblJ18u1XQN4vDEh1O7tkH0BbdhNmVvcgoR6vc719genWRQEXzGFasT\n54r3EH18Gb1ekFx8pIrWHdIKEJhG+53XKu0j6FIwmGRPiJeXS4/G9LbSzTfJvNWW\n/3z2VaZmynejHymh/N7vlCQnJ2lIqwKBiMjMh44TuCX1GLvkqVKkIPTikYVWGakA\nfxhsX55xggqTN0U7DhR6FAT4RnmdZoQgFZpAJzecwyplNcAm+zrj21NNC12QXkLU\n2gv797QiXk9EGtMh6ToeD+czWKz8VWwUOjrkIp2QvQKBgQDin+JAiJpiaS82nMY2\nb4hXddv7mlMy7SGnq84Pjr/rRmp1h0sPhqD1ZxWIgs+OutOeBytQBcYCkicJag5Y\nMgwaRiJFvsVYehvmejluGJfunHvAI/Ttz7cPPtDuqNg6E1frGnyAoHUfWX7VZn4A\n74F8PVX40/R4/NcSislQ27GaHwKBgQDQsvCLCez2f/YJAdhgJNyUboMe0Fw+YMBg\nawqeno+mZ4YM0dZYaE07ni2eYcQ3b62rM2esbxZyuCDGmre9yxCmfDpaVCDeWPE8\nPaReKWUMcBISj2Yo01GTn8k+SzzB2zzs5NtAMn3iRtg6JcgM1/pfKpOHjJ5kki1M\nXJppTL2/PQKBgG78nnG8dN99ZAH7BZfjR4KN1g6Cpfxq5fCX03MLFjLDaZ/lgn04\nEdwdgA47AiuEk97w4+Vs7myT50pVBnFrEUJM1rwRkdSi+McHVNj2cnIJcRHIiktt\nTtnIicpYJo1Kq+QYNKFJ9BJGYjdg2pTaty+BWnliVHhsW2hZT/6pmXFBAoGASX87\nBzwvn3/g/bsQoItaw0tIEgn+8ljQZyRLUSE2Jbw/kTQ08F2LFXvXRPfZSkyiNLCd\nyjQ1C6GcqVTDcKua6YbGZhlKmgNosXZj9GVPmNm/A5pMuAPzrrGPBckpVHwJMMRI\nEou1mYKpk5DKqvtEyU8NNadoALMaENJr7rl/+WECgYANCbwACnOFF9KkrYE6kQ+p\nFD1tmfAvSp6xk7izLut83dbmxCiGiNQFfWza3J5OwrA+OBdOSctYweVZBCtUE+pi\nLpd+k2n6AckSGtcFnYLCdTrP7Vms4lqzVzZwA1rsSV9JdL2+bGvM3hhlMUL7VrXk\nzyYSpYRBtf0SxUMkhq8cdw==\n-----END PRIVATE KEY-----\n",
  "client_email": "proyectobalanzasmart@appspot.gserviceaccount.com",
  "client_id": "105104323822216977545",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/proyectobalanzasmart%40appspot.gserviceaccount.com"
}
gc = gspread.service_account_from_dict(credentials)
EMULATE_HX711=False
referenceUnit = 1
#Calibracion Balanza
# if not EMULATE_HX711:
#     import RPi.GPIO as GPIO
#     from hx711 import HX711
# else:
#     from emulated_hx711 import HX711
# hx = HX711(5, 6)
# hx.set_reading_format("MSB", "MSB")
# hx.set_reference_unit(215.793)
# hx.reset()
# hx.tare()

#Definiciones usadas

def tomardatos():
    global gc,DNI1,recomendacion,var
    worksheet = gc.open('Datos_Balanza').worksheet('Ordenado')
    # get_all_values gives a list of rows.
    data=worksheet.get('D2:N')
    DatosUsuar=pd.DataFrame.from_records(data)  
    ratings=worksheet.get('Q2:T11')
    # Convert to a DataFrame and render.      
    DatosUsuar=DatosUsuar.set_axis(['Documento', 'manzana', 'platano', 'beterraga','zanahoria', 'maiz', 'limon', 'cebolla', 'papa', 'camote', 'tomate'], axis=1)
    DatosUsuar.head(10)
    rating=pd.DataFrame.from_records(ratings)
    rating=rating.set_axis(['Producto ID', 'Producto', 'Veces comprado', 'Usuarios compradores'], axis=1)
    rating=rating.sort_values('Veces comprado')
    comprado = rating["Veces comprado"].astype(int)
    comprado = comprado.tolist()
    product = rating["Producto"].tolist()
    Documento=worksheet.col_values(4)
    Productos=worksheet.get('E1:N1')
    Productos = str(Productos)[1:-1]
    usuario_un=[{'Documento':'18978998','manzana':'1', 'platano':'0', 'beterraga':'1', 'zanahoria':'0', 'maiz':'0', 'limon':'0', 'cebolla':'1', 'papa':'0', 'camote':'0', 'tomate':'1'}]
    entrada_food=pd.DataFrame(usuario_un)
    data1=worksheet.get('E2:N')
    DatosUsuar1=pd.DataFrame.from_records(data1)
    ratings_train, ratings_test = train_test_split(DatosUsuar1, test_size = 0.2, random_state=42)
    sim_matrix = 1 - sklearn.metrics.pairwise.cosine_distances(DatosUsuar1)
    sim_matrix_train = sim_matrix[0:8,0:8]
    sim_matrix_test = sim_matrix[8:10,8:10]
    sim_train=pd.DataFrame(sim_matrix_train)
    derived_df = ratings_train.drop([8,9], axis=1)
    derived_df = derived_df.astype(float)
    derived_df= derived_df.sort_values(0)
    users_predictions =derived_df.dot(sim_train)/np.array([np.abs(sim_matrix_train).sum(axis=1)]).T
    pd.DataFrame(data=users_predictions, index=['a','b','c','d','e','f','g'])
    USUARIO_EJEMPLO =DNI1.pop()
    USUARIO_EJEMPLO=str(USUARIO_EJEMPLO)
    USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip('[[')
    USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip(']]')
    USUARIO_EJEMPLO=USUARIO_EJEMPLO.strip("'")
    print("Para usuario: ",USUARIO_EJEMPLO) # debe existir en nuestro dataset de train!
    datas = DatosUsuar[DatosUsuar['Documento'] == USUARIO_EJEMPLO]
    usuario_ver=datas.index[datas['Documento'] == USUARIO_EJEMPLO]
    z=usuario_ver.tolist()
    def red():
        global recomendacion,var
        user0=users_predictions.index.argsort()[usuario_ver]
        compara=[]
        # Veamos los tres recomendados con mayor puntaje en la predic para este usuario
        for i, aRepo in enumerate(user0[-3:]):
            selRepo = DatosUsuar[DatosUsuar['Documento']==(aRepo+1)]
            compara.append(users_predictions[usuario_ver])
            #print(selRepo['Documento'] , 'puntaje:\n', users_predictions[usuario_ver][aRepo])
        compara=(str(compara)[13:-1].replace("  ",","))
        compara=compara.replace("\n",",")
        compara=compara.split(',')
        plain_list_iter = iter(compara)
        plain_list_dict_object = itertools.zip_longest(plain_list_iter, plain_list_iter, fillvalue=None)
        comparacion = dict(plain_list_dict_object)
        comparacion_sort= sorted(comparacion.items(), key=operator.itemgetter(1), reverse=True)
        user =str(user0)[1:-1]
        for name in enumerate(comparacion_sort):
            if user in name[1][0]:
                print('detect')
            else:
            #print(name[1][0], ':', comparacion[name[1][0]])
                similar=name[1][0]
                break
        first = users_predictions.loc[[int(similar)]]
        maxi=(str(first.max(axis = 1))[5:-15])
        maxi=float(maxi)
        rating_orden=rating.sort_index()
        #print("Datos:\n",datas)
        print("Similar:\n",first)
        recomendacion=[]
        for index in range(first.shape[1]):
            valor=float(first.iloc[: , index].values)
            valor=("{:.6f}".format(valor))
            if float(valor)==maxi:    
                recomendacion.append(rating_orden.iloc[index, 1])
        print('\nProductos recomendados: ',str(recomendacion).replace("'","")[1:-1])
        return recomendacion
    if len(z) == 0:
        popular =worksheet.get('V11')
        recomendacion=[popular]
        recomendacion=str(recomendacion).replace("[['"," ")[1:-1]
        recomendacion=str(recomendacion).replace("']"," ")[1:-1]
        print('\nProductos recomendados: ',recomendacion)
        var.set(recomendacion)
    else:
        recomendacion=[]
        red()
        var.set(recomendacion)
def cleanAndExit():
    print("Cleaning...")
    #if not EMULATE_HX711:
        #GPIO.cleanup()      
    print("Bye!")
    sys.exit()
def agregar_datos():
	global DNI1, producto1, peso1
	DNI1.append(ingresa_DNI.get())
	ingresa_DNI.delete(0,END)
def funcion():
    global DNI1
    ws.state(newstate  = "normal")
    lbl_u.insert(0,DNI1[-1])
    tomardatos()
    root.state(newstate  = "withdraw")
    print("Data agregada")
    clear()
    iniciar()
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
    print("valor",val)
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
    global logo, ingresar, balanza, fond, grad,bg,home,settings,lista, iconhome,iconlogo, configuracion, iconlista, peso

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

    absolute_image_pathi = os.path.join(absolute_folder_path, 'iconHome.png')
    iconhome1 = Image.open(absolute_image_pathi).resize((60,60),Image.ANTIALIAS)
    iconhome= ImageTk.PhotoImage(iconhome1)

    absolute_image_pathh = os.path.join(absolute_folder_path, 'home.png')
    home1 = Image.open(absolute_image_pathh).resize((210,60),Image.ANTIALIAS)
    home=ImageTk.PhotoImage(home1)

    absolute_image_paths = os.path.join(absolute_folder_path, 'iconsettings.png')
    settings1 = Image.open(absolute_image_paths).resize((60,60),Image.ANTIALIAS)
    settings=ImageTk.PhotoImage(settings1)

    absolute_image_pathc = os.path.join(absolute_folder_path, 'Configuracion.png')
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
    global cap
    cap = cv2.VideoCapture(1)
    visualizar()
def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640,height=480)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()
def finalizar():
    global cap
    cap.release()
def progressBar():
    global nivel, move,val,flag
    muestra=1
    print(muestra)
    move=150
    if muestra==1:
        #val=round(hx.get_weight(5)/1000,2)
        val=random.randrange(20)
        nivel = 1.961
        flag=1
        #hx.power_down()
        #hx.power_up()
        #x0,y0,x1,y1
        texbal = Label(	ws,    text=str(nivel) + ' Kg',    width=6,	height=0, font=('Arial',16, 'bold'), bg='gray22',fg ='deep sky blue')
        texbal_canva = canvas.create_window(485+move, 380,anchor = "center",	window = texbal	)
        #############TEXTO ################
        texto = str(nivel) + ' Kg'
        canvas.create_oval(415+move,290,555+move,430, fill='gray22', outline='white', width=6)
        #canvas.create_text(485+move, 380, text= texto, font=('Arial',22, 'bold'), fill ='deep sky blue')
        canvas.create_text(485+move, 335, text= 'PESO' , font=('Cambria Math',22, 'bold'), fill ='white')  	
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
def add_item():
    global list_data,flag,fixedlen
    if producto1 != "" and flag==1:
        item = ("{:<20s}"+(fixedlen-len(str(producto1.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(val)))*" " +"{:<10s}"+(fixedlen-len(str("Costo")))*"").format(producto1.get(),val,"Costo")
        listbox.insert(END,item)
        list_data.append(producto1.get())
        producto1.set("")
        flag=0
    borrarOmostrar()     
def add_item2():
    global list_data,flag,fixedlen
    if producto2 != "" and flag==1:
        #listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
        item = ("{:<20s}"+(fixedlen-len(str(producto2.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(val)))*" " +"{:<10s}"+(fixedlen-len(str("Costo")))*"").format(producto2.get(),val,"Costo")
        listbox.insert(END,item)
        list_data.append(producto2.get())
        producto2.set("")
        flag=0
    borrarOmostrar()
def vision():
    global alimentos,deteccion, producto1, producto2, val
    frame3.place(	x=(width*5/24)+70, y=height*12/15,	anchor = "center")
    producto1 = StringVar(value=alimentos[deteccion])
    producto2 = StringVar(value=alimentos[deteccion-1])
    lbl_pc1.config(text = producto1.get())
    lbl_pc3.config(text = producto2.get())
    lbl_pc1.grid(row=0,column=0)
    lbl_pc3.grid(row=1,column=0)
def detectar():
    global cap,model,deteccion
    ret, frame = cap.read()
    #cv2.imshow('frame', frame)
    image = cv2.resize(frame, (255, 255))
    X = tf.keras.utils.img_to_array(image)
    X = np.expand_dims(X, axis=0)
    X = X/255
    Class = model.predict(X)
    if Class[0,0] >= 0.5:
        deteccion=0
        print('apple')
    elif Class[0,1] >= 0.5:
        deteccion=1
        print('banana')
    elif Class[0,2] >= 0.5:
        deteccion=2
        print('beetroot')
    elif Class[0,3] >= 0.5:
        deteccion=3
        print('carrot')
    elif Class[0,4] >= 0.5:
        deteccion=4
        print('corn')
    elif Class[0,5] >= 0.5:
        deteccion=5
        print('lemon')
    elif Class[0,6] >= 0.5:
        deteccion=6
        print('onion')
    elif Class[0,7] >= 0.5:
        deteccion=7
        print('potato')
    elif Class[0,8] >= 0.5:
        deteccion=8
        print('sweetpotato')
    elif Class[0,9] >= 0.5:
        deteccion=9
        print('tomato')
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
    global iconlqr
    qr = qrcode.QRCode(
        version= 1,
        box_size=10,
        border = 2
    )
    datos = ('https://www.kushki.com/products/')
    qr.add_data(datos)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black',back_color='#2989cc')
    img.save('C:/Users/Aprender Creando/Documents/qrcode.png')
    absolute_folder_pathqr = os.path.dirname(os.path.realpath(__file__))
    absolute_image_pathqr = os.path.join(absolute_folder_path, 'qrcode.png')
    logo = tk.PhotoImage(file = absolute_image_pathqr)
    iconqr = Image.open(absolute_image_pathqr).resize((70,70),Image.ANTIALIAS)
    iconlqr= ImageTk.PhotoImage(iconqr)
    iconlqr=Label(frameqr,image=iconlqr,bg='white',relief='flat')
    iconlqr.grid(row=0,column=0,pady=50)
def borrarOmostrarqr():
    if frameqr.grid_info() != {}:
        frameqr.grid_remove()
    else:
        frameqr.grid(padx=1,column = 0, row = 0,sticky=E,columnspan=3)
        qrfun()
        frameqr.after(5000, borrarOmostrarqr)
def btnClik(num):
    global operador
    operador=operador+str(num)
    input_text.set(operador)
def clear():
    global operador
    operador=("")
    input_text.set("")

#Variables usadas
cap = None
fixedlen = 10
list_data=[]
INTERVALO_REFRESCO_RELOJ = 300  # En milisegundos
width=1020
height=720
deteccion=0
producto1,producto2=[],[]
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
alimentos=["manzana","platano","beterraga","zanahoria","maiz","limon","cebolla","papa","camote ","tomate "]

#Primera Ventana
root = Tk()
root.title("Registro")
root.geometry('1020x720+5+0')
root.resizable(0, 0)
root.config(bg='black')
root.state(newstate  = "normal")
#Agregar Imagenes
agregarimage()

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
ancho_boton=11
alto_boton=3
operador=""
nume=640
numy=150

Button(canvas,text="0",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(0)).place(x=17+nume,y=180+numy)
Button(canvas,text="1",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(1)).place(x=107+nume,y=180+numy)
Button(canvas,text="2",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(2)).place(x=197+nume,y=180+numy)
Button(canvas,text="3",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(3)).place(x=17+nume,y=240+numy)
Button(canvas,text="4",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(4)).place(x=107+nume,y=240+numy)
Button(canvas,text="5",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(5)).place(x=197+nume,y=240+numy)
Button(canvas,text="6",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(6)).place(x=17+nume,y=300+numy)
Button(canvas,text="7",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(7)).place(x=107+nume,y=300+numy)
Button(canvas,text="8",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(8)).place(x=197+nume,y=300+numy)
Button(canvas,text="9",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(9)).place(x=107+nume,y=360+numy)
Button(canvas,text="C",bg="Skyblue1",width=ancho_boton,height=alto_boton,command=clear).place(x=17+nume,y=360+numy)

path_picker_button = tk.Button(
    image=ingresar,
    compound = 'center',
    fg = 'white',
    bg='#FCFCFC',
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda:[agregar_datos(), funcion()],relief = 'flat')
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
ws.geometry('1020x720+10+0')
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
lblVideo = Label(ws,width=320,height=350)
lblVideo_canvas3 = canvas.create_window((width*2/24)+50, height*3/15,anchor = "nw",window = lblVideo)

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
frame = Frame(ws, bg='black', width=70, height=ws.winfo_height())
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

frameqr = Frame(ws, bg='white', width=250, height=350)
frameqr.grid_propagate(False)

framerecom = Frame(ws, bg='white', width=250, height=150)
framerecom.grid_propagate(False)
framerecom.place(	x=(width*20/24)+30, y=height*13/15,	anchor = "center")
lbl_recom=tk.Label(framerecom,text="Recomendación",bg='#FCFCFC',font=('Georgia', 20))
lbl_recom.grid(row=1,column=1,pady=0)
lbl_oferta=tk.Label(framerecom,textvariable=var,bg='#FCFCFC',font=('Georgia', 20))
lbl_oferta.grid(row=2,column=1,pady=0)

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
lbl_pc3 = Button(	frame3,    textvariable=producto2,    width=10,	height=0,command=add_item2,font=('Georgia', 13,"bold"))
ws.mainloop()
root.mainloop()

if (SystemExit):
    cleanAndExit()