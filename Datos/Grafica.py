import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
hx.set_reference_unit(226.2207)
hx.reset()
hx.tare()

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    val=abs(round(hx.get_weight(5)/1000,2))

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%M:%S'))
    ys.append(val)
    hx.power_down()
    hx.power_up()
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Peso de producto respecto a tiempo')
    plt.ylabel('Peso (Kg)')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()