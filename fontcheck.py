import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading

# Global flag to indicate whether the thread should continue running or terminate
is_running = False

def read_serial():
    global is_running
    while is_running:
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            # Process the received data
            # Update the plot with the new data
            # ...

def open_plot_window():
    global is_running
    # Create a new window
    plot_window = tk.Toplevel(root)
    plot_window.title("Serial Data Plot")

    # Create a frame to hold the Matplotlib plot
    frame = tk.Frame(plot_window)
    frame.pack(padx=10, pady=10)

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots()

    # Create a Matplotlib canvas within the frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

    # Create a text entry for adjusting x and y limits
    limits_frame = tk.Frame(plot_window)
    limits_frame.pack(pady=10)
    x_limit_entry = tk.Entry(limits_frame, width=10)
    x_limit_entry.pack(side=tk.LEFT, padx=5)
    y_limit_entry = tk.Entry(limits_frame, width=10)
    y_limit_entry.pack(side=tk.LEFT, padx=5)

    def update_plot_limits():
        try:
            x_limit = float(x_limit_entry.get())
            y_limit = float(y_limit_entry.get())
            ax.set_xlim(0, x_limit)
            ax.set_ylim(0, y_limit)
            canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid limit value!")

    # Create a button to update plot limits
    update_button = tk.Button(plot_window, text="Update Limits", command=update_plot_limits)
    update_button.pack(pady=10)

    # Open the serial port
    ser = serial.Serial('/dev/cu.usbmodem109297901', 9600)  # Replace 'COM1' with the appropriate port and '9600' with the baud rate

    # Start reading serial data in a separate thread
    is_running = True
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.start()

    def close_plot_window():
        global is_running
        is_running = False  # Stop the serial thread
        plot_window.destroy()  # Close the plot window

    # Set the close event handler for the plot window
    plot_window.protocol("WM_DELETE_WINDOW", close_plot_window)

root = tk.Tk()

plot_button = tk.Button(root, text="Open Plot Window", command=open_plot_window)
plot_button.pack(pady=20)

root.mainloop()
