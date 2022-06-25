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
#import tensorflow as tf
import array as arr

#import pandas as pd
#from pandas import ExcelWriter

EMULATE_HX711=False

referenceUnit = 1

#Calibracion Balanza
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
#-223.999
hx.set_reference_unit(226.2207)
hx.reset()
hx.tare()

#Definiciones usadas
def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()      
    print("Bye!")
    sys.exit()
def agregar_datos():
	global correo1, producto1, peso1
	correo1.append(ingresa_correo.get())
	#producto1.append(ingresa_producto.get())
	#peso1.append(ingresa_peso.get())
	ingresa_correo.delete(0,END)
	#ingresa_producto.delete(0,END)
	#ingresa_peso.delete(0,END)
def excel():
    global correo1, producto1, peso1, balanza
    datos = {'Correo':correo1} 
    #df = pd.DataFrame(datos,columns =['Correo'])
    #escritor=pd.ExcelWriter('C:/Users/Aprender Creando/Documents/BalanzaConection/Data_Balanza.xlsx',engine='xlsxwriter')
    #df.to_excel(escritor,sheet_name="Usuarios",index=False)
    #escritor.save()
    lbl_u.insert(0,correo1.pop())
    print("Data agregada")
def funcion():
    ws.state(newstate  = "normal")
    root.state(newstate  = "withdraw")
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
def agregarimage():
    global logo, ingresar, balanza, fond, grad,bg,home,settings,lista, iconhome,iconlogo, configuracion, iconlista, peso

    absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
    absolute_image_path = os.path.join(absolute_folder_path, 'logo_balanza.png')
    logo = tk.PhotoImage(file = absolute_image_path)
    iconlogo1 = Image.open(absolute_image_path).resize((70,70),Image.ANTIALIAS)
    iconlogo= ImageTk.PhotoImage(iconlogo1)

    absolute_image_path1 = os.path.join(absolute_folder_path, 'ingresar.png')
    ingresar = tk.PhotoImage(file = absolute_image_path1)

    absolute_image_path2 = os.path.join(absolute_folder_path, 'balanza_modern.png')
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
    cap = cv2.VideoCapture(0)
    visualizar()
def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
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
        val=abs(round(hx.get_weight(5)/1000,2))
        #val=random.randrange(20)
        nivel = int(val)
        flag=1
        hx.power_down()
        hx.power_up()
        #x0,y0,x1,y1
        texbal = Label(	ws,    text=str(val) + ' Kg',    width=6,	height=0, font=('Arial',18, 'bold'), bg='gray22',fg ='deep sky blue')
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
def borarOmostrar():
    if frame2.grid_info() != {}:
        frame2.grid_remove()
    else:
        frame2.grid(padx=1,column = 0, row = 0,sticky=E,columnspan=3)
        frame.after(5000, borarOmostrar)
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
    frame2.grid(padx=1,column = 0, row = 0,sticky=E,columnspan=3)
    frame.after(2000, borarOmostrar)      
def add_item2():
    global list_data,flag,fixedlen
    if producto2 != "" and flag==1:
        #listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )
        item = ("{:<20s}"+(fixedlen-len(str(producto2.get())))*" " +"{:<10.2f}"+(fixedlen-len(str(val)))*" " +"{:<10s}"+(fixedlen-len(str("Costo")))*"").format(producto2.get(),val,"Costo")
        listbox.insert(END,item)
        list_data.append(producto2.get())
        producto2.set("")
        flag=0
    frame2.grid(padx=10,column = 0, row = 0,sticky=E,columnspan=3)
    frame.after(2000, borarOmostrar)
def vision():
    global alimentos,detectado, producto1, producto2, val
    frame3.place(	x=(width*5/24)+70, y=height*12/15,	anchor = "center")
    producto1 = StringVar(value=alimentos[nivel])
    producto2 = StringVar(value=alimentos[nivel-1])
    lbl_pc1.config(text = producto1.get())
    lbl_pc3.config(text = producto2.get())
    lbl_pc1.grid(row=0,column=0)
    lbl_pc3.grid(row=1,column=0)
 
#Variables usadas
cap = None
fixedlen = 10
list_data=[]
INTERVALO_REFRESCO_RELOJ = 300  # En milisegundos
width=1020
height=720
producto1,producto2=[],[]
correo1,producto,peso1 = [],[],[]
nivel = 0
min_w = 70 # Minimum width of the frame
max_w = 220 # Maximum width of the frame
cur_width = min_w # Increasing width of the frame
expanded = False # Check if it is completely exanded
move=150
hora=0
val=0
muestra=0
flag=0
alimentos=["manzana","platano","beterraga","zanahoria","maiz","limon","cebolla","papa","camote ","tomate "]
#Primera Ventana
root = Tk()
root.title("Registro")
root.geometry('1020x720+0+0')
root.resizable(0, 0)
root.config(bg='black')
root.state(newstate  = "normal")
#Agregar Imagenes
agregarimage()

root.call('wm', 'iconphoto', root._w, logo)
#Primera Ventana
canvas = tk.Canvas(
    root, bg="#3A7FF6", height=720, width=1020,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(560, 0, 1020, 720, fill="#FCFCFC", outline="")
canvas.create_text(
    590.0, 266.0, text="Correo electrónico", fill="black",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    659, 210.0, text="Bienvenid@",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))
title = tk.Label(
    text="Balanza Smart", bg="#3A7FF6",
    fg="white", font=("Arial-BoldMT", int(30.0)))
title.place(x=27.0, y=110.0)

ingresa_correo = tk.Entry(bd=0, bg="black", highlightthickness=0, fg='white')
ingresa_correo.place(x=590.0, y=280, width=321.0, height=35)
usuario_actual = StringVar(value=ingresa_correo)

path_picker_button = tk.Button(
    image=ingresar,
    compound = 'center',
    fg = 'white',
    bg='#FCFCFC',
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda:[agregar_datos(), funcion(),excel()],
    relief = 'flat')
path_picker_button.place(
    x = 760, y = 400,
    width = 300,
    height = 60)
info_text = tk.Label(
    text="Esta es la nueva balanza inteligente\n"
    "\n"
    "Coloca tu correo y pulsa INGRESAR \n\n"
    "Encima de la bandeja situa el producto\n"
    "que deseas pesar.\n\n"
    "Selecciona el producto que has pesado\n\n"
    "Puedes pagar usando el QR de la pantalla",
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))
info_text.place(x=27.0, y=200.0)
lbl_balanza=tk.Label(canvas,image=balanza,bg='#3A7FF6')
lbl_balanza.place(x=0.0, y=475.0)
lbl_logo=tk.Label(canvas,image=logo,bg='#FCFCFC')
lbl_logo.place(x=805.0, y=0.0)

#Segunda Ventana
ws = Toplevel()
ws.state(newstate  = "withdraw")
ws.title("Balanza Smart")
ws.geometry('1020x720+0+0')
ws.config(bg='black')
#ws.call('wm', 'iconphoto', root._w, logo)
canvas = Canvas(ws, height=720, width=1020,
    bd=0, highlightthickness=0, relief="ridge")
canvas.create_image(width/2, height/2,image=grad,anchor = "center")
ws.resizable(width=False, height=False)
canvas.grid(row=0,column=0) 
canvas.create_text((width/2)+70, height/15, text = 'Balanza Smart', fill='white',font=('Georgia', 40,"bold"))

canvas.create_oval(390+move,265,575+move,430, fill="", outline ='',width=5)
canvas.create_oval(392+move,270,578+move,450, fill= '', outline='white', width= 6)

btn = Button(ws,image=peso,command=lambda:[progressBar(),vision()] ,bg='#2989cc',relief='flat')
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
iniciar()

#Menu desplegable lateral
ws.update() # For the width to get updated

frame = Frame(ws, bg='black', width=70, height=720)
frame.grid(column = 0, row = 0,sticky=W)
# Make the buttons with the icons to be shown 
logo_b=Label(frame,image=iconlogo,bg='white',relief='flat')
home_b = Button(frame,image=iconhome,command=funcion2,bg='black',relief='flat')
set_b = Button(frame,image=settings,bg='black',relief='flat')
lista_b = Button(frame,image=iconlista,command=borarOmostrar,bg='black',relief='flat')

# Put them on the frame
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

listbox = Listbox(frame2,height=400, width=250,font=('Georgia', 10))
listbox.grid(row=2,column=1,pady=0)
listbox.insert(END, "{:<15s}  {:<10s} {:>15s}".format("Producto","Peso (Kg)","Costo (S/.)") )

#barra=Scrollbar(ws, command=listbox.yview)
#barra.grid(row=2,column=1,pady=0)
#listbox.config(yscrollcommand=barra)

frame3 = Frame(ws, bg='#2989cc', width=150, height=100)
#frame3.grid_propagate(False)
lbl_pc1 = Button(	frame3,   textvariable=producto1,    width=10,	height=1,command=add_item,font=('Georgia', 15,"bold"))
lbl_pc3 = Button(	frame3,    textvariable=producto2,    width=10,	height=0,command=add_item2,font=('Georgia', 13,"bold"))

ws.mainloop()
root.mainloop()
if (SystemExit):
    cleanAndExit()