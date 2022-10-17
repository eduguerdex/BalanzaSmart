import cv2
import uuid
n=0
def tomfoto(i):
    PATHA="/home/utec/Desktop/"
    cap = cv2.VideoCapture(i)
    leido, frame = cap.read()
    if leido == True:
        nombre_foto = PATHA+str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite(nombre_foto, frame)
        print("Foto tomada correctamente con el nombre {}".format(nombre_foto))
    else:
        print("Error al acceder a la cámara")
    cap.release()
while n<2:
    tomfoto(n)
    n=n+1
print("finalizado")