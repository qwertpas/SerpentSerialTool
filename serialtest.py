import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial

def open_plot_window():
    # Create a new window
    plot_window = tk.Toplevel(root)
    plot_window.title("Serial Data Plot")
    plot_window.geometry("600x400")

    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Initialize empty lists for x and y data
    x_data = []
    y_data = []

    # Create an empty line object for the plot
    line, = ax.plot([], [], 'b-')

    # Function to update the plot
    def update_plot(i):
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            # Process the data as needed
            # Append the x and y data
            x_data.append(i)
            y_data.append(float(data))
            # Update the plot
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view()

    # Open the serial port
    ser = serial.Serial('COM1', 9600)  # Replace 'COM1' with the appropriate port and '9600' with the baud rate

    # Animation function to continuously update the plot
    anim = FuncAnimation(fig, update_plot, interval=100)

    # Start the animation
    plt.show()

root = tk.Tk()

# Create a button to open the plot window
button = ttk.Button(root, text="Open Plot Window", command=open_plot_window)
button.pack(pady=20)

root.mainloop()
