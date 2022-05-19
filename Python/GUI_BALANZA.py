from tkinter import *
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


cap = None
INTERVALO_REFRESCO_RELOJ = 300  # En milisegundos

ws = Tk()
ws.title("Balanza Smart")
ws.geometry('900x510')


new = 1
url = "https://www.pythonguides.com"

def obtener_hora_actual():
    return datetime.now().strftime("%H:%M:%S")

def refrescar_reloj():
    variable_hora_actual.set(obtener_hora_actual())
    ws.after(INTERVALO_REFRESCO_RELOJ, refrescar_reloj)

def obtener_peso_actual():
    time.sleep(0.01)
    return random.randrange(10)
def refrescar_peso():
    peso_actual.set(obtener_peso_actual())
    ws.after(INTERVALO_REFRESCO_RELOJ, refrescar_peso)

def openbrowser():
    webbrowser.open(url,new=new)

def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

canvas = Canvas(
	ws, 
	width = 100,
	height = 00
	)

canvas.pack(fill='both', expand = True)

canvas.create_image(
	0, 
	0, 
	image=bg,
	anchor = "nw"
	)

canvas.create_text(
	450, 
	45, 
	text = 'Balanza Smart', fill='white',
	font=('Arial', 30),
	)

btn = Button(
	ws, 
	text = "Nuevo \n Producto",
	command=finalizar,
	width=10,
	height=2,
	relief=SOLID,
	font=('arial', 13)
	)

btn_canvas = canvas.create_window(
	70, 
	430,
	anchor = "nw",
	window = btn,
	)
btn2= Button(
	ws, 
	text = "Aumentar\n Cantidad",
	command=iniciar,
	width=10,
	height=2,
	relief=SOLID,
	font=('arial', 13)
	)

btn2_canvas2 = canvas.create_window(
	190, 
	430,
	anchor = "nw",
	window = btn2,
	)

lblVideo = Label(
	ws,
    width=280,
	height=300,
	)
lblVideo_canvas3 = canvas.create_window(
	25, 
	100,
	anchor = "nw",
	window = lblVideo,
	)

lbl_u = Label(	ws,    text=f'Eduardo Guerrero Dextre',    width=25,	height=2	)
lblu_canvas = canvas.create_window(	45, 	30,	anchor = "nw",	window = lbl_u	)

peso_actual = StringVar(ws, value=obtener_peso_actual())
lbl_p = Label(	ws,    textvariable=peso_actual,    width=30,	height=3)

lblp_canvas = canvas.create_window(	380, 	340,	anchor = "nw",	window = lbl_p	)

lbl_pc1 = Button(	ws,    text=f'Producto 1',    width=30,	height=3)
lblpc1_canvas = canvas.create_window(	375, 	150,	anchor = "nw",	window = lbl_pc1	)


lbl_pc3 = Button(	ws,    text=f'Producto 2',    width=30,	height=3)
lblpc3_canvas = canvas.create_window(	375, 	225,	anchor = "nw",	window = lbl_pc3	)

btns= Button(
	ws, 
	text = "Salir",
	command=iniciar,
	width=10,
	height=2,
	relief=SOLID,
	font=('arial', 13)
	)
btns_canvas = canvas.create_window(
	710, 
	430,
	anchor = "nw",
	window = btns,
	)

variable_hora_actual = StringVar(ws, value=obtener_hora_actual())
lbl_fh = Label(	ws,    textvariable=variable_hora_actual,    width=25,	height=2	)
lblfh_canvas = canvas.create_window(	665, 	30,	anchor = "nw",	window = lbl_fh	)
refrescar_reloj()

lbl_l = Label(	ws,    text=f'Lista de elementos',    width=25,	height=20	)
lbll_canvas = canvas.create_window(	660, 	100,	anchor = "nw",	window = lbl_l	)


iniciar()
ws.mainloop()
