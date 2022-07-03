import time
import datetime as dt
import matplotlib.pyplot as plt
EMULATE_HX711=False

referenceUnit = 1

#Calibracion Balanza
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB") #-223.999
hx.set_reference_unit(223.2207)
hx.reset()
hx.tare()
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def pesaje():
    memoria=[]
    start_time=time.time()
    nuevo_time=time.time()
    conteo=0
    total=[]
    for t in range(30):
        val=round(abs(hx.get_weight(5)/1000),4)
        memoria.append(val)
        hx.power_down()
        hx.power_up()
        n=len(memoria)
        if n>1:
            if round(memoria[t],2)==round(memoria[t-1],2):
                conteo+=1
                total.append(memoria[t])
                #print(conteo)
            elif round(memoria[t])<0.1:
                nuevo_time=time.time()-start_time
                #print(nuevo_time)
                conteo=0
                total=[]
            else:
                conteo=0
                total=[]
                print("Producto detectado, calculando peso")
            if conteo>6:
                pesado=round(sum(total)/len(total),3)
                print("peso del producto: ",pesado,"detectado al segundo",round(((time.time()-start_time)-nuevo_time),2))
                return(pesado)
        time.sleep(0.0001)
def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    time.sleep(0.01)
    if distance<20:
        print ("Measured Distance = %.1f cm" % distance)
        pesaje()
    else:
        print("No detectado")
while True:
    distance()