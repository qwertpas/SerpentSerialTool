import tkinter as tk
import serial.tools.list_ports



root = tk.Tk()
root.title("Text Entry and Display")

# Create a frame to hold the checkbox, text display, and scrollbar
mainframe = tk.Frame(root)
mainframe.pack(fill=tk.BOTH, expand=True)


portframe = tk.Frame(mainframe)
portframe.pack()

# label for the port dropdown
portlabel = tk.Label(portframe, text = "Select a serial port:")
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

def stream_data():
    selected_port = port_var.get()
    if selected_port:
        try:
            ser = serial.Serial(selected_port, baudrate=baudrate_var.get(), timeout=1)
            while True:
                data = ser.readline().decode().strip()
                text_display.configure(state=tk.NORMAL)
                text_display.insert(tk.END, data + '\n')
                text_display.configure(state=tk.DISABLED)
                text_display.see(tk.END)
        except serial.SerialException:
            print(f"Failed to open serial port: {selected_port}")

doprint = False
def toggleprint():
    global doprint
    doprint = not doprint 
    if doprint:
        print(f"Connecting to {port_var.get()} at {baudrate_var.get()} baud")
        stream_data()
        runbutton.config(text="Pause")
    else:
        runbutton.config(text="Run")
runbutton = tk.Button(mainframe, text="Run", command=toggleprint)
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
        add_text()
        print("Key pressed:", key)

# Bind the KeyPress event to the on_keypress function
entry.bind("<KeyPress>", on_keypress)

entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)


# Start the tkinter event loop
root.mainloop()
