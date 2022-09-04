import numpy as np
import cv2
import uuid
import time
dataPath = 'C:/Users/Aprender Creando/Pictures/pruebasmano'
captures = [
    cv2.VideoCapture(0, cv2.CAP_DSHOW),
    cv2.VideoCapture(1, cv2.CAP_DSHOW),
]
num_cam=len(captures)
n=0
while True:  # while true, read the camera
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        frames.append((frame if ret else None))

    for i, frame in enumerate(frames):
        if frame is not None:  # None if not captured
            cv2.imshow(f"camera{i}", frame)
        if ret==True:
            time.sleep(1)
            nombre_foto = dataPath + '/'+str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
            cv2.imwrite(nombre_foto, frame)
            print("Foto tomada correctamente")
            n=n+1

    # to break the loop and terminate the program
    if cv2.waitKey(1) & 0xFF == ord("q") or n==num_cam:
        break

for cap in captures:
    cap.release()