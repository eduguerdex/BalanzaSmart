from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
import time

def load_labels(path): #Read the labels from the python list
    with open(path, 'r') as f:
        return [line.strip() for i, line in enumerate(f.readlines())]

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)
    
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
    
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)
    
    ordered = np.argpartition(-output, 1)
    return [(i, output[i]) for i in ordered[:top_k]][0]

data_folder = "/home/raspberry/Desktop/BalanzaSmart/Python"

model_path = data_folder + "/modelofinal.tflite"
label_path = data_folder + "/Labels.txt"

interpreter = Interpreter(model_path)
print("Modelo cargado exitosamente")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Image shape (", width, ",", height, ")")
dim = (width, height)
#Cargar una imagen
image = cv2.imread('/home/raspberry/Desktop/BalanzaSmart/Python/Appletest')
imager = cv2.resize(image, dim)

#Clasificar la imagen
time1 = time.time()
label_id, prob = classify_image(interpreter, imager)
time2 = time.time()
classification_time = np.round(time2-time1, 3)
print("Tiempo de clasificacion =",  classification_time, "Seconds.")

#Read class labels
labels = load_labels(label_path)

#Return the classifcation label of the image
classification_label = labels[label_id]
print("La imagen es :", classification_label, ",con un accuracy de", np.round(prob*100, 2), "%.")