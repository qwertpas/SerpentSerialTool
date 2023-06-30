import tkinter as tk
from tkinter.messagebox import showinfo
import serial.tools.list_ports
import threading
import time



root = tk.Tk()
root.title("Serpent Serial Tool")

# Top level frame that stacks everything vertically
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

def refresh_ports():
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    menu = port_dropdown['menu']
    menu.delete(0, 'end')
    for port_name in port_names:
        menu.add_command(label=port_name, command=tk._setit(port_var, port_name))
    port_var.set(port_names[-1])

# Create a dropdown menu for serial ports
ports = scan_serial_ports()
port_var = tk.StringVar()
port_dropdown = tk.OptionMenu(portframe, port_var, *ports)
port_dropdown.pack(side=tk.RIGHT)

refresh_ports()


port_button = tk.Button(portframe, text="Refresh", command=refresh_ports)
port_button.pack(side=tk.RIGHT, before=port_dropdown)

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
            # ser.set_buffer_size(rx_size = 128000, tx_size = 128000)

        except serial.SerialException:
            showinfo("Error", f"Failed to open serial port: {port}")
            return
    else:
        showinfo("Error", "Please select a port.")
        return
    
    message = ""
    
    while serial_on:
        if ser.in_waiting > 0:
            uarttext = ser.read_all().decode()

            print("UART IN +++++++++")
            print(uarttext)
            print("+++++++++ \n")




            ending=0
            while(uarttext):
                ending = uarttext.find("q")
                if(ending == -1):
                    break

                message += uarttext[0:ending]

                print("~~~~~v")
                print(message)
                print("~~~~~\n")

                add_text(message)


                message = "" #clear message
                uarttext = uarttext[ending+1:] #front of buffer used up

            message = uarttext #whatver is left over
            print("finish processing buffer. Rollover: \n")
            print(message)
            print("------------- \n \n")

            


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

autoscroll = tk.IntVar(value=1)
autoscroll_check = tk.Checkbutton(mainframe, text="Autoscroll", variable=autoscroll)
autoscroll_check.pack()


consoleframe = tk.Frame(mainframe)
consoleframe.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(consoleframe)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Create a text display widget
text_display = tk.Text(consoleframe, yscrollcommand=scrollbar.set, height=10)
text_display.configure(state=tk.DISABLED)
text_display.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar to work with the text display
scrollbar.config(command=text_display.yview)




# Create a checkbox for toggling autosend keystrokes
auto_send = tk.IntVar(value=0)
autosend_check = tk.Checkbutton(mainframe, text="Send keystrokes immediately", variable=auto_send)
autosend_check.pack()


entryframe = tk.Frame(mainframe)
entryframe.pack()

# label for the send textentry
entrylabel = tk.Label(entryframe, text = "Send:")
entrylabel.pack(side=tk.LEFT)

def add_text(text):
    text_display.configure(state=tk.NORMAL)
    text_display.insert(tk.END, text + '\n')
    text_display.configure(state=tk.DISABLED)
    if(autoscroll.get()):
        text_display.see(tk.END)

def send_data():
    text = entry.get()
    if text:
        global ser
        if(ser is not None):
            if(ser.is_open):
                ser.write(text.encode())
        entry.delete(0, tk.END)
        add_text(text)

# Create a text entry widget
entry = tk.Entry(entryframe)
# Bind the Enter key to add_text function
entry.bind("<Return>", lambda event: send_data())

def on_keypress(event):
    if auto_send.get() == 1:
        key = event.char
        entry.delete(0, tk.END)
        entry.insert(0, key)
        send_data()

# Bind the KeyPress event to the on_keypress function
entry.bind("<KeyPress>", on_keypress)

entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

# img = tk.Image("photo", file="serpent.png")
# root.tk.call('wm','iconphoto', root._w, img)

# Start the tkinter event loop
root.mainloop()
