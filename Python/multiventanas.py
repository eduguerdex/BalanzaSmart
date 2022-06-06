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
from datetime import datetime
import random
import sys
import pandas as pd
from pandas import ExcelWriter

EMULATE_HX711=False

referenceUnit = 1

# if not EMULATE_HX711:
#     import RPi.GPIO as GPIO
#     from hx711 import HX711
# else:
#     from emulated_hx711 import HX711
def cleanAndExit():
    print("Cleaning...")
    print("Bye!")
    sys.exit()

#     if not EMULATE_HX711:
#         GPIO.cleanup()
        
#     print("Bye!")
#     sys.exit()

# hx = HX711(5, 6)
# hx.set_reading_format("MSB", "MSB")
# #-223.999
# hx.set_reference_unit(215.793)
# hx.reset()
# hx.tare()
print("Tare done! Add weight now...")

cap = None
INTERVALO_REFRESCO_RELOJ = 300  # En milisegundos

root = Tk()
root.title("Registro")
root.geometry('900x510+290+10')
root.resizable(0, 0)
root.config(bg='black')
root.state(newstate  = "normal")
correo1,producto1,peso1 = [],[],[]

def agregar_datos():
	global correo1, producto1, peso1
	correo1.append(ingresa_correo.get())
	#producto1.append(ingresa_producto.get())
	#peso1.append(ingresa_peso.get())
	ingresa_correo.delete(0,END)
	#ingresa_producto.delete(0,END)
	#ingresa_peso.delete(0,END)

def excel():
    global correo1, producto1, peso1
    datos = {'Correo':correo1} 
    df = pd.DataFrame(datos,columns =['Correo'])
    escritor=pd.ExcelWriter('C:/Users/Aprender Creando/Documents/BalanzaConection/Data_Balanza.xlsx',engine='xlsxwriter')
    df.to_excel(escritor,sheet_name="Usuarios",index=False)
    escritor.save()
    print("Data agregada")

def funcion():
    ws.state(newstate  = "normal")
    root.state(newstate  = "withdraw")
def funcion2():
    ws.state(newstate  = "withdraw")
    root.state(newstate  = "normal") 
absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
absolute_image_path = os.path.join(absolute_folder_path, 'Gris_balance.png')
bg = tk.PhotoImage(file = absolute_image_path)

absolute_folder_path1 = os.path.dirname(os.path.realpath(__file__))
absolute_image_path1 = os.path.join(absolute_folder_path1, 'ingresar.png')
ingresar = tk.PhotoImage(file = absolute_image_path1)

root.call('wm', 'iconphoto', root._w, bg)

canvas = tk.Canvas(
    root, bg="#3A7FF6", height=560, width=900,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(461, 0, 461 + 461, 0 + 560, fill="#FCFCFC", outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")
canvas.create_text(
    490.0, 186.0, text="Correo electrónico", fill="black",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    565, 140.0, text="Bienvenid@",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))
title = tk.Label(
    text="Balanza Smart", bg="#3A7FF6",
    fg="white", font=("Arial-BoldMT", int(30.0)))
title.place(x=27.0, y=110.0)

token_entry_img = canvas.create_image(650.5, 167.5, image=bg)
URL_entry_img = canvas.create_image(650.5, 248.5, image=bg)
filePath_entry_img = canvas.create_image(650.5, 329.5, image=bg)

ingresa_correo = tk.Entry(bd=0, bg="white", highlightthickness=0)
ingresa_correo.place(x=490.0, y=200, width=321.0, height=35)
ingresa_correo.focus()
path_picker_button = tk.Button(
    image=ingresar,
    compound = 'center',
    fg = 'white',
    bg='white',
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda:[agregar_datos(), funcion(),excel()],
    relief = 'flat')
path_picker_button.place(
    x = 550, y = 300,
    width = 300,
    height = 60)
info_text = tk.Label(
    text="Esta es la nueva balanza Inteligente\n"
    "\n"
    "Coloca tu correo y pulsa INGRESAR \n\n"
    "Encima de la bandeja situa el producto\n"
    "que deseas pesar.\n\n"
    "Selecciona el producto que has pesado\n"
    "Puedes pagar usando el QR de la pantalla",
    bg="#3A7FF6", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=200.0)

ws = Toplevel()
ws.state(newstate  = "withdraw")
ws.title("Balanza Smart")
ws.geometry('900x510+290+10')
ws.config(bg='black')

def obtener_hora_actual():
    return datetime.now().strftime("%H:%M:%S")

def refrescar_reloj():
    variable_hora_actual.set(obtener_hora_actual())
    progressBar()
    ws.after(INTERVALO_REFRESCO_RELOJ, refrescar_reloj)

def iniciar():
    global cap
    cap = cv2.VideoCapture(2)
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

absolute_folder_path = os.path.dirname(os.path.realpath(__file__))
absolute_image_path = os.path.join(absolute_folder_path, 'Gris_balance.png')
bg = PhotoImage(file = absolute_image_path)
canvas = Canvas(ws, width = 100,height = 00)
canvas.pack(fill='both', expand = True)
canvas.create_image(0, 0,image=bg,anchor = "nw")
canvas.create_text(450, 45, text = 'Balanza Smart', fill='white',font=('Arial', 30),)
btn = Button(ws, text = "Nuevo \n Producto",command=finalizar,width=10,height=2,relief=SOLID,font=('arial', 13))
btn_canvas = canvas.create_window(70, 430,anchor = "nw",window = btn)
btn2= Button(ws, text = "Aumentar\n Cantidad",command=iniciar,width=10,height=2,relief=SOLID,font=('arial', 13))
btn2_canvas2 = canvas.create_window(190, 430,anchor = "nw",window = btn2)

lblVideo = Label(ws,width=280,height=300)
lblVideo_canvas3 = canvas.create_window(25, 100,anchor = "nw",window = lblVideo)

usuario_actual = StringVar(ws, value=ingresa_correo.get())
lbl_u = Label(	ws,    textvariable=usuario_actual,    width=25,	height=2	)
lblu_canvas = canvas.create_window(	45, 	30,	anchor = "nw",	window = lbl_u	)

def sensor():
    try:
        #val=round(hx.get_weight(5)/1000,2)
        val=random.randrange(10)
        #hx.power_down()
        #hx.power_up()
        peso_actual = StringVar(ws, value=val)
        lbl_p = Label(	ws,    textvariable=peso_actual,    width=30,	height=3)
        lblp_canvas = canvas.create_window(	380, 	340,	anchor = "nw",	window = lbl_p	)
    except:
        pass
#ws.after(100,sensor)
nivel = 0


def progressBar():
    global nivel
    try:
        #val=round(hx.get_weight(5)/1000,2)
        val=random.randrange(20)
        nivel = int(val) 
        #hx.power_down()
        #hx.power_up()
        peso_actual = StringVar(ws, value=val)
        #x0,y0,x1,y1
        canvas.create_oval(415,290,555,435, fill="", outline ='',width=5)
        canvas.create_oval(410,285,560,440, fill= '', outline='white', width= 6)
        canvas.create_oval(425,300,545,420, fill='gray22', outline='white', width=6)
        #############TEXTO ################
        texto = str(nivel) + ' Kg'
        canvas.create_text(485, 380, text= texto, font=('Arial',22, 'bold'), fill ='deep sky blue')
        canvas.create_text(485, 335, text= 'PESO' , font=('Cambria Math',22, 'bold'), fill ='white')
    except:
        pass	
ws.after(100,progressBar)

lbl_pc1 = Button(	ws,    text=f'Producto 1',    width=30,	height=3)
lblpc1_canvas = canvas.create_window(	375, 	150,	anchor = "nw",	window = lbl_pc1	)

lbl_pc3 = Button(	ws,    text=f'Producto 2',    width=30,	height=1)
lblpc3_canvas = canvas.create_window(	375, 	210,	anchor = "nw",	window = lbl_pc3	)

btns= Button(ws, text = "Salir",command=funcion2,width=10,height=2,relief=SOLID,font=('arial', 13))
btns_canvas = canvas.create_window(710,430,anchor = "nw",window = btns)

variable_hora_actual = StringVar(ws, value=obtener_hora_actual())
lbl_fh = Label(	ws,    textvariable=variable_hora_actual,    width=25,	height=2	)
lblfh_canvas = canvas.create_window(	665, 	30,	anchor = "nw",	window = lbl_fh	)
refrescar_reloj()

lbl_l = Label(	ws,    text=f'Lista de elementos',    width=25,	height=15	)
lbll_canvas = canvas.create_window(	660, 	100,	anchor = "nw",	window = lbl_l	)
iniciar()
ws.mainloop()
root.mainloop()

if (KeyboardInterrupt, SystemExit):
    cleanAndExit()