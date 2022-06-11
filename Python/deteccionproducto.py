import cv2
import numpy as np
import tensorflow as tf
import array as arr

model = tf.keras.models.load_model("modeloproduct.h5") #model.summary()
cap2 = cv2.VideoCapture('projectBanana.mp4')
while True:
    ret, frame = cap2.read()
    cv2.imshow('frame', frame)
    image = cv2.resize(frame, (255, 255))
    X = tf.keras.utils.img_to_array(image)
    X = np.expand_dims(X, axis=0)
    X = X/255
    Class = model.predict(X)
    if Class[0,0] >= 0.5:
        print('apple')
    elif Class[0,1] >= 0.5:
        print('banana')
    elif Class[0,2] >= 0.5:
        print('beetroot')
    elif Class[0,3] >= 0.5:
        print('carrot')
    elif Class[0,4] >= 0.5:
        print('corn')
    elif Class[0,5] >= 0.5:
        print('lemon')
    elif Class[0,6] >= 0.5:
        print('onion')
    elif Class[0,7] >= 0.5:
        print('potato')
    elif Class[0,8] >= 0.5:
        print('sweetpotato')
    elif Class[0,9] >= 0.5:
        print('tomato')
    if cv2.waitKey(1) == ord('q'):
        break
cap2.release()
cv2.destroyAllWindows()








