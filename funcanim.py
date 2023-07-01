# live_plot_sensor.py

import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# animation function
def animate(i, data_lst, ser):  # ser is the serial object
    # b = ser.readline()
    # string_n = b.decode()
    # string = string_n.rstrip()
    
    data_lst.append(2)
    data_lst.append(3)

    # Add x and y to lists

    # Limit the data list to 100 values
    data_lst = data_lst[-100:]
    # clear the last frame and draw the next frame
    ax.clear()
    ax.plot(data_lst)
    # Format plot
    ax.set_ylim([0, 1050])
    ax.set_title("Potentiometer Reading Live Plot")
    ax.set_ylabel("Potentiometer Reading")
    print(time.time())


# create empty list to store data
# create figure and axes objects
data_lst = []
fig, ax = plt.subplots()

# set up the serial line
ser = serial.Serial("/dev/cu.usbmodem109297901", 9600)  # change COM# if necessary
time.sleep(2)
print(ser.name)

# run the animation and show the figure
ani = animation.FuncAnimation(
    fig, animate, frames=100, fargs=(data_lst, ser), interval=100
)
plt.show()

# after the window is closed, close the serial line
ser.close()
print("Serial line closed")