import tkinter as tk
from tkinter.messagebox import showinfo
import serial.tools.list_ports
import threading
import time



root = tk.Tk()
root.title("Serial tool")

# Create a frame to hold the checkbox, text display, and scrollbar
mainframe = tk.Frame(root)
mainframe.pack(fill=tk.BOTH, expand=True)


portframe = tk.Frame(mainframe)
portframe.pack()

# label for the port dropdown
portlabel = tk.Label(portframe, text = "Serial port:")
portlabel.pack(side=tk.LEFT)

def scan_serial_ports():
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    return port_names

# Create a dropdown menu for serial ports
ports = scan_serial_ports()
port_var = tk.StringVar()
port_dropdown = tk.OptionMenu(portframe, port_var, *ports)
port_dropdown.pack(side=tk.RIGHT)

baudframe = tk.Frame(mainframe)
baudframe.pack()
# label for the baudrate dropdown
baudlabel = tk.Label(baudframe, text = "   Baudrate:")
baudlabel.pack(side=tk.LEFT)


# Create a dropdown menu for serial ports
baudrates = [9600, 115200]
baudrate_var = tk.IntVar()
baudrate_var.set(baudrates[0])
baud_dropdown = tk.OptionMenu(baudframe, baudrate_var, *baudrates)
baud_dropdown.pack(side=tk.RIGHT)


serial_on = False
serial_thread = None
ser = None

def read_serial():
    port = port_var.get()

    print(f"Connecting to {port} at {baudrate_var.get()} baud")

    global ser
    if port:
        try:
            ser = serial.Serial(port, baudrate=baudrate_var.get(), timeout=1)
        except serial.SerialException:
            showinfo("Error", f"Failed to open serial port: {port}")
            return
    else:
        showinfo("Error", "Please select a port.")
        return
    
    while serial_on:
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            text_display.configure(state=tk.NORMAL)
            text_display.insert(tk.END, data + '\n')
            text_display.configure(state=tk.DISABLED)
            text_display.see(tk.END)
        time.sleep(0.1)
        
    ser.close()

def toggle_serial():
    global serial_on, serial_thread
    serial_on = not serial_on 
    if serial_on: #turning on
        
        serial_thread = threading.Thread(target=read_serial, daemon=True)
        serial_thread.start()

        runbutton.config(text="Pause")
    else: #turning off
        # if(serial_thread):
        #     serial_thread.join()
        runbutton.config(text="Run")

runbutton = tk.Button(mainframe, text="Run", command=toggle_serial)
runbutton.pack()




consoleframe = tk.Frame(mainframe)
consoleframe.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(consoleframe)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Create a text display widget
text_display = tk.Text(consoleframe, yscrollcommand=scrollbar.set)
text_display.configure(state=tk.DISABLED)
text_display.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar to work with the text display
scrollbar.config(command=text_display.yview)




# Create a checkbox for toggling autosend keystrokes
auto_send = tk.IntVar()
autosend_check = tk.Checkbutton(mainframe, text="Send keystrokes immediately", variable=auto_send)
autosend_check.pack()


entryframe = tk.Frame(mainframe)
entryframe.pack()

# label for the send textentry
entrylabel = tk.Label(entryframe, text = "Send:")
entrylabel.pack(side=tk.LEFT)

def add_text():
    text = entry.get()
    if text:
        global ser
        if(ser is not None):
            if(ser.is_open):
                ser.write(text.encode())

        text_display.configure(state=tk.NORMAL)
        text_display.insert(tk.END, text + '\n')
        text_display.configure(state=tk.DISABLED)
        entry.delete(0, tk.END)
        text_display.see(tk.END)

# Create a text entry widget
entry = tk.Entry(entryframe)
# Bind the Enter key to add_text function
entry.bind("<Return>", lambda event: add_text())

def on_keypress(event):
    if auto_send.get() == 1:
        key = event.char
        entry.delete(0, tk.END)
        entry.insert(0, key)
        add_text()

# Bind the KeyPress event to the on_keypress function
entry.bind("<KeyPress>", on_keypress)

entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)


# Start the tkinter event loop
root.mainloop()
