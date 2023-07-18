import tkinter as tk
from tkinter.messagebox import showinfo, askokcancel
import serial.tools.list_ports
import threading
import time
# from serpent_plt import PlotWindow
from tkinterplot import Plot
from periodics import PeriodicSleeper


root = tk.Tk()
root.title("Serpent Serial Tool")

# Top level frame that stacks everything vertically
mainframe = tk.Frame(root)
mainframe.pack(fill=tk.BOTH, expand=True)


portframe = tk.Frame(mainframe)
portframe.pack()

# label for the port dropdown
portlabel = tk.Label(portframe, text = "Port:")
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
    if port_names:
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
baudlabel = tk.Label(baudframe, text = "Baudrate:")
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

messagebuffer = ""
plot_handler = None

def start_serial():
    port = port_var.get()
    print(f"Connecting to {port} at {baudrate_var.get()} baud")

    global ser
    if port:
        try:
            ser = serial.Serial(port, baudrate=baudrate_var.get(), timeout=1)
            ser.read_all()
        except Exception as e:
            print(e)
            showinfo("Error", f"Failed to open serial port: {port}")
            return
    else:
        showinfo("Error", "Please select a port.")
        return
    
    message = ""
    delimiter = '\n'
    global messagebuffer

    count = 0
    while serial_on:
        messagecount = 0
        starttime = time.time()
        if ser.in_waiting > 0:
            try:
                uarttext = ser.read_all().decode('utf-8', errors='ignore')
            except Exception as e:
                print(e)
                continue

            if(delimiter != '\t'):
                if(uarttext.find('\t') != -1):
                    delimiter = '\t'

            ending=0
            while(uarttext):
                ending = uarttext.find(delimiter)
                if(ending == -1):
                    break

                message += uarttext[0:ending]
                add_text(message)
                messagebuffer = message

                messagecount += 1

                message = "" #clear message
                uarttext = uarttext[ending+len(delimiter):] #front of buffer used up

            message = uarttext #whatver is left over

        time.sleep(0.033)
        # print("messages per second: ", messagecount / (time.time() - starttime))
        count+=1
        
    ser.close()

def send_to_plot():
    global messagebuffer
    if(plotwindow):
        plotwindow.set(messagebuffer)


def toggle_serial():
    global serial_on, serial_thread, plot_handler
    serial_on = not serial_on 
    if serial_on: #turning on
        
        serial_thread = threading.Thread(target=start_serial, daemon=True)
        serial_thread.start()

        plot_handler = PeriodicSleeper(send_to_plot, 0.01)

        runbutton.config(text="Pause")
    else: #turning off
        # if(serial_thread):
        #     serial_thread.join()
        plot_handler.stop()
        if plotwindow:
            plotwindow.pause()
        runbutton.config(text="Run")

runbutton = tk.Button(baudframe, text="Run", command=toggle_serial)
runbutton.pack(side=tk.RIGHT, before=baud_dropdown)

optionframe = tk.Frame(mainframe)
optionframe.pack()

options_mb = tk.Menubutton(optionframe, text="Options")
options_mb.menu = tk.Menu(options_mb)
options_mb["menu"] = options_mb.menu

autoscroll = tk.IntVar(value=1)
autosend = tk.IntVar(value=0)

options_mb.menu.add_checkbutton(label="Autoscroll", variable=autoscroll)
options_mb.menu.add_checkbutton(label="Send immediately", variable=autosend)
options_mb.pack(side=tk.LEFT)

plotwindow = None
def open_plot_w_root():
    global plotwindow
    try:
        plotwindow.lift()
    except:
        window=tk.Toplevel(root)
        plotwindow = Plot(window)

button = tk.Button(optionframe, text="Open Plot", command=open_plot_w_root)
button.pack(side=tk.RIGHT)


consoleframe = tk.Frame(mainframe)
consoleframe.pack(fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(consoleframe)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Create a text display widget
text_display = tk.Text(consoleframe, font=('Arial',25), yscrollcommand=scrollbar.set, height=10, width=20)
text_display.configure(state=tk.DISABLED)
text_display.pack(fill=tk.BOTH, expand=True)

text_display.config(font=("Courier", 20))

# Configure the scrollbar to work with the text display
scrollbar.config(command=text_display.yview)



entryframe = tk.Frame(mainframe)
entryframe.pack()

# label for the send textentry
entrylabel = tk.Label(entryframe, text = "Send:")
entrylabel.pack(side=tk.LEFT)

def add_text(text):
    if(serial_on):
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
        # add_text(text)

# Create a text entry widget
entry = tk.Entry(entryframe)
# Bind the Enter key to add_text function
entry.bind("<Return>", lambda event: send_data())

def entry_keypress(event):
    if autosend.get() == 1:
        key = event.char
        entry.delete(0, tk.END)
        entry.insert(0, key)
        send_data()

fontsize=20
def console_keypress(event):
    if(event.state == 8 or event.state == 4): #command or control is pressed at the same time
        global fontsize
        if(event.char == '='):
            fontsize += 2
            text_display.config(font=("Courier", fontsize))
            print('up')
        elif(event.char == '-'):
            fontsize -= 2
            text_display.config(font=("Courier", fontsize))
            print('down')



# Bind the KeyPress event to the on_keypress function
entry.bind("<KeyPress>", entry_keypress)
text_display.bind("<KeyPress>", console_keypress)

entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)

# img = tk.Image("photo", file="serpent.png")
# root.tk.call('wm','iconphoto', root._w, img)


def on_closing():
    root.destroy()
    exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()