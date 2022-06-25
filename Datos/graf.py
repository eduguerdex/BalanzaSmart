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
hx.set_reference_unit(225.2207)
hx.reset()
hx.tare()


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

print("Tare done! Add weight now...")

# Sample temperature every second for 10 seconds
start_time=time.time()
for t in range(0, 50):
    val=abs(round(hx.get_weight(5)/1000,3))
    output=open("cebolla.txt","a")
    output.write(str(round(time.time()-start_time))+","+str(val)+"\n")
    # Add x and y to lists
    xs.append(round(time.time()-start_time))
    ys.append(val)
    hx.power_down()
    hx.power_up()
    # Wait 1 second before sampling temperature again
    time.sleep(0.01)

# Draw plot
ax.plot(xs, ys)

# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Peso de producto respecto a tiempo')
plt.ylabel('Peso (Kg)')

# Draw the graph
plt.show()