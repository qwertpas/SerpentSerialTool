import sys
import tkinter as tk
import numpy as np
from numpy import log10, ceil, floor
from colorsys import hsv_to_rgb
from periodics import PeriodicSleeper

class Plot(tk.Frame):
    def __init__(self, parent):
        self.historylen = 100
        self.labels = []
        self.data = np.array([])
        self.scales = np.array([])
        self.saved_scales = {}      #dict for history of labels and scales, so scale is preserved if data is spotty
        self.hues = []
        self.w = parent.winfo_width()
        self.h = parent.winfo_height()
        self.epsilon = 1e-9 #minimum floating value to display
        self.max = self.epsilon
        self.min = -self.epsilon

        self.message = "" #buffer that some external loop updates, then the plotter displays it periodically

        self.textoffset = np.array([-10, 0]) #xy offset for the labels
        self.temp_tags = [] #strings of y axis mark tags that get redrawn on resize
        self.scale_frames = []

        self.paused = False

        self.setup_graphics(parent)
        self.plotloop()

    def setup_graphics(self, parent):
        tk.Frame.__init__(self, parent)

        parent.wm_title("Serpent Plotter")
        parent.wm_geometry("800x400")
        self.canvas = tk.Canvas(self, background="gray12")
        self.canvas.bind("<Configure>", self.on_resize)

        self.yaxis_frame = tk.Frame(parent)
        self.yaxis_frame.pack()

        self.side_frame = tk.LabelFrame(parent,text='Scale',padx=5, pady=5)
        self.side_frame.pack(side=tk.RIGHT, fill='both')

        history_frame = tk.Frame(self.side_frame)
        history_frame.pack(side=tk.BOTTOM)

        historylabel = tk.Label(history_frame, text="# pts:")
        historylabel.pack()

        historyentry = tk.Entry(history_frame, width=5, validate="key", validatecommand=(self.register(self.validate_numeric), '%P', '%d'))
        historyentry.insert(0, f"{self.historylen}")
        historyentry.pack(side=tk.BOTTOM, before=historylabel)
        historyentry.bind("<Return>", lambda event: self.set_history(historyentry))

        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.pack(expand=True, fill=tk.BOTH)


    def pause(self):
        self.paused = True
        
    def disp(self, val):
        val=(val-self.min)/(self.max-self.min) #map any value to 0 to +1
        pad = 20
        return (self.h - 2*pad) * (1-val) + pad
    
    def find_nice_range(xmin, xmax):
        diff = xmax-xmin
        n = ceil(log10(diff / 5) - 1)
        s = diff / 10**(n+1)
        if s <= 1:
            s = 1
        elif s <= 2:
            s = 2
        else:
            s = 5
        step = s*10**n
        bot = floor(xmin/step)*step
        try:
            return np.arange(bot, xmax+step, step)
        except Exception as e:
            print(e)
            print(xmin, xmax, bot, xmax+step, step)



    def on_resize(self, event=None):
        self.w = self.winfo_width()
        self.h = self.winfo_height()

        for temp_tag in self.temp_tags:
            self.canvas.delete(temp_tag)  # Delete line item from the canvas

        for y in Plot.find_nice_range(self.min, self.max):
            if abs(y) < self.epsilon:
                y = 0
            marktag = f"_M{y}"
            gridtag = f"_G{y}"
            self.temp_tags.append(marktag)
            self.temp_tags.append(gridtag)
            h = int(self.disp(y))

            if y == 0:
                self.canvas.create_line(0, self.disp(y), self.w, self.disp(y), tag=gridtag, fill="#AAAAAA")
            else:
                self.canvas.create_line(0, self.disp(y), self.w, self.disp(y), tag=gridtag, fill="#454545")
            self.canvas.create_text(10, h, anchor='w', text=f"{y:0.4g}", tag=marktag)
        
        # self.data = np.zeros_like(self.data)
        self.draw()

    def str_to_data(message:str):
        new_labels = []
        new_data = []
        lines = message.strip().split("\n")
        for line in lines:
            try:
                parts = line.split(":")
                if len(parts) != 2: #ignore lines that don't have exactly one colon
                    continue
                label, value = parts
                label = label.strip()
                if label in new_labels:
                    continue        #is a duplicate entry in the same message
                value = float(value.strip().split(" ")[0]) #only use the first "word" and ignore spaces
                new_labels.append(label)
                new_data.append(value)
            except Exception as e:
                print(e)
        return new_labels, new_data
    
    def hue_to_hex(hue:float):
        rgb = hsv_to_rgb(hue % 1, s=0.5, v=0.8)
        hex_code = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        return hex_code
    
    def set(self, message):
        self.message = message
        self.paused = False

    def validate_numeric(self, is_insert, new_value):
        if is_insert == 0:
            return True     #allow deletion
        return new_value.isdigit() or new_value == "."
    
    def set_history(self, entry):
        value = int(entry.get())
        if value >= 2:
            if value < self.historylen:
                self.data.resize((len(self.data), value))
            else:
                #pad the front with zeros
                self.data = np.concatenate([np.zeros((len(self.data), value - self.historylen)), self.data], axis=1)
            self.historylen = value




    def rescale(self, entry, label):
        text = entry.get()
        try:
            value = float(text)
            i = self.labels.index(label)
            self.scales[i] = value
            self.saved_scales[label] = value
            print(f"rescale {label} with {value}")
            print(f"saved scales: {self.saved_scales}")
        except Exception as e:
            print(e)
            # print("Scale input is not a float")


    def plotloop(self):
        '''
        - delete any inactive series by removing the label, data, and canvas line
        - if there is a new series, add it to the label, data, and canvas line
            - recalculate and apply evenly spaced hues to existing lines
        '''
        new_labels, new_data = Plot.str_to_data(self.message)

        if len(new_labels) > 0:

            #remove any data and lines that aren't active
            to_delete = [] #indexes of labels to delete
            for i in range(len(self.labels)): 
                if self.labels[i] not in new_labels:
                    self.canvas.delete(f"{self.labels[i]}L") #delete the plotline
                    self.canvas.delete(f"{self.labels[i]}T") #delete the drawn text
                    to_delete.append(i)
            if to_delete:
                for i in sorted(to_delete, reverse=True):
                    del_label = self.labels.pop(i)
                    self.scale_frames[i].destroy()
                    self.scale_frames.pop(i)
                    print(f"removed series: {del_label}")

                self.data = np.delete(self.data, to_delete, axis=0)    
                self.scales = np.delete(self.scales, to_delete, axis=0)    


            #add lines that don't exist yet
            added_new = False
            for new_label in new_labels:
                if new_label not in self.labels:
                    self.labels.append(new_label)
                    if len(self.data) > 0:
                        self.data = np.append(self.data, [np.zeros(self.historylen)], axis=0)
                        self.scales = np.append(self.scales, 1)
                    else:
                        self.data = np.array([np.zeros(self.historylen)])
                        self.scales = np.array([1.])
                    if new_label in self.saved_scales: #restore the last used scale for this label
                        self.scales[-1] = self.saved_scales[new_label]

                    self.canvas.create_line(0,0,0,0, tag=f"{new_label}L", width=2)
                    self.canvas.create_text(0, 0, anchor="e", tag=f"{new_label}T", text=new_label)

                    scale_frame = tk.Frame(self.side_frame)
                    scale_frame.pack()
                    self.scale_frames.append(scale_frame)

                    scalelabel = tk.Label(scale_frame, text=new_label)
                    scalelabel.pack()
        
                    scaleentry = tk.Entry(scale_frame, width=5, validate="key", validatecommand=(self.register(self.validate_numeric), '%P', '%d'))
                    scaleentry.insert(0, f"{self.scales[-1]:g}")
                    scaleentry.pack(side=tk.RIGHT, before=scalelabel)
                    scaleentry.bind("<Return>", lambda event: self.rescale(scaleentry, new_label))

                    added_new = True
                    print(f"added new series: {new_label}")

            #update line colors if any lines were added
            if added_new:
                m = len(self.labels)
                hues = np.linspace(0, 1, m + 1) #last item is 1, which is the same hue as 0 so it is unused
                for i in range(m):
                    self.canvas.itemconfig(f"{self.labels[i]}L", fill=Plot.hue_to_hex(hues[i]))
                    self.canvas.itemconfig(f"{self.labels[i]}T", fill=Plot.hue_to_hex(hues[i]))

            # print(f"concating {[self.data, np.array([new_data])[:,np.newaxis]]}")   
            self.data = np.concatenate([self.data[:,1:], np.array(new_data)[:,np.newaxis]], axis=1)   #combine shifted old data and new data
            self.after_idle(self.draw)

        self.after(33, self.plotloop)


    def draw(self):
        m = len(self.labels)
        n = self.historylen

        if m == 0 or self.paused:
            return
        
        data_scaled = self.data * self.scales.reshape((-1,1))

        do_resize = False
        max_new = np.max(data_scaled)
        if abs(max_new - self.max) > 1e-6:
            self.max = max_new
            do_resize = True
        min_new = np.min(data_scaled)
        if abs(min_new - self.min) > 1e-6:
            self.min = min_new
            do_resize = True
        if abs(self.max - self.min) < self.epsilon:     #if max-min=0, scale is infinite
            self.max += self.epsilon
            self.min -= self.epsilon
        if do_resize:
            self.on_resize()

        disp_data = self.disp(data_scaled)

        #canvas.coords() takes in a flattened input: x1,y1,x2,y2,... 
        #next 3 lines adds a column vectors to every other index of the data 2D array which are the x values.
        xvals_row = np.linspace(start=0, stop=self.w, num=n)
        xvals_arr = np.tile(xvals_row, (len(self.labels), 1))
        
        points = np.dstack([xvals_arr, disp_data]).reshape(m, 2*n)

        for i in range(len(self.labels)):
            self.canvas.coords(f"{self.labels[i]}L", points[i].tolist())
            self.canvas.coords(f"{self.labels[i]}T", (points[i][-2:] + self.textoffset).tolist())

count = 0
def main():
    np.set_printoptions(precision=2, suppress=True)

    root = tk.Tk()
    plot = Plot(root)

    import time

    def senddata():
        global count
        count += 1

        period = 100

        message = ""
        for i in range((int)(count / period)+1):
            if(i > 4):
                break
            message = message + f"y{i}: {np.sin(time.time()+i)} \n"
        
        # if count > 5*period:
        #     count = 0

        plot.set(message)
    
    PeriodicSleeper(senddata, 0.01)

    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main())