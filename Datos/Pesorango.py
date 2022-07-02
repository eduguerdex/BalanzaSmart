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


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

print("Tare done! Add weight now...")
memoria=[]
# Sample temperature every second for 10 seconds
start_time=time.time()
conteo=0
total=[]
for t in range(20):
    val=abs(hx.get_weight(5)/1000)
    output=open("conteo.txt","a")
    output.write(str(round(time.time()-start_time))+","+str(val)+"\n")
    memoria.append(val)
    hx.power_down()
    hx.power_up()
    n=len(memoria)
    if n>1:
        if round(memoria[t],2)==round(memoria[t-1],2):
            conteo+=1
            total.append(memoria[t])
            #print(conteo)
        else:
            conteo=0
            total=[]
            print("esperar unos segundos, calculando peso")
        if conteo>6:
            peso=round(sum(total)/len(total),3)
            print("peso del producto: ",peso,)
    # Add x and y to lists
    xs.append(round((time.time()-start_time),2))
    ys.append(val)
    #print(memoria)
    #print(t)    
    time.sleep(0.0001)

# Draw plot
ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Peso de producto respecto a tiempo')
plt.ylabel('Peso (Kg)')

# Draw the graph
plt.show()