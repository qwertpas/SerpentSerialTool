import sys
import tkinter as tk
import numpy as np
from colorsys import hsv_to_rgb
from periodics import PeriodicSleeper

class Plot(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        parent.wm_title("Serpent Plotter")
        parent.wm_geometry("800x400")
        self.canvas = tk.Canvas(self, background="gray12")
        self.canvas.bind("<Configure>", self.on_resize)

        self.yaxis_frame = tk.Frame(parent)
        self.yaxis_frame.pack()

        self.side_frame = tk.LabelFrame(parent,text='Scale',padx=5, pady=5)
        self.side_frame.pack(side=tk.RIGHT, fill='both')

        self.legend_label = tk.Label(self.side_frame, text="set the sacle")
        self.legend_label.pack()

        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.pack(expand=True, fill=tk.BOTH)


        self.historylen = 100
        self.labels = []
        self.data = np.array([])
        # self.scale = np.array([])
        self.hues = []
        self.w = parent.winfo_width()
        self.h_2 = parent.winfo_height() / 2.

        self.message = "" #buffer that some external loop updates, then the plotter displays it periodically

        self.textoffset = np.array([-10, 0]) #offsets for the labels

        self.temp_tags = [] #strings of y axis mark tags that get redrawn on resize

        self.plotloop()
        
    def disp(self, val):
        pad = 20
        return (self.h_2 - pad) * (1 - val) + pad
    def invdisp(self, disp):
        pad = 20
        return 1 - (disp-pad)/(self.h_2-pad)

    def on_resize(self, event=None):
        self.w = self.winfo_width()
        self.h_2 = self.winfo_height() / 2.

        for temp_tag in self.temp_tags:
            self.canvas.delete(temp_tag)  # Delete line item from the canvas

        for y in np.arange(-1, 1.01, 0.2):
            y = round(y, 2)
            marktag = f"_M{y}"
            gridtag = f"_G{y}"
            self.temp_tags.append(marktag)
            self.temp_tags.append(gridtag)
            h = int(self.disp(y))
            if(y==0):
                self.canvas.create_line(0, self.disp(y), self.w, self.disp(y), tag=gridtag, fill="#AAAAAA")
            else:
                self.canvas.create_line(0, self.disp(y), self.w, self.disp(y), tag=gridtag, fill="#454545")
            self.canvas.create_text(10, h, anchor='w', text=f"{y}", tag=marktag)

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
                    self.data = np.delete(self.data, i, axis=0)
                    self.canvas.delete(self.labels[i])
                    self.canvas.delete(f"{self.labels[i]}L")
                    to_delete.append(i)
            for i in to_delete:
                print(f"removing {self.labels[i]}")
                self.labels.pop(i)

            #add lines that don't exist yet
            added_new = False
            for new_label in new_labels:
                if new_label not in self.labels:
                    self.labels.append(new_label)
                    if len(self.data) > 0:
                        self.data = np.append(self.data, [np.zeros(self.historylen)], axis=0)
                    else:
                        self.data = np.array([np.zeros(self.historylen)])
                    self.canvas.create_line(0,0,0,0, tag=f"{new_label}L")
                    self.canvas.create_text(0, 0, anchor="e", tag=f"{new_label}T", text=new_label)

                    
                    new_scaleinput = tk.Entry(self.side_frame)
                    new_scaleinput.pack()

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

        if m == 0:
            return

        # data_scaled = self.data @ self.scale
        # data_scaled = self.h_2 * (1 - self.data) #scale data y-values for the display
        data_scaled = self.disp(self.data)

        #canvas.coords() takes in a flattened input: x1,y1,x2,y2,... 
        #next 3 lines adds a column vectors to every other index of the data 2D array which are the x values.
        xvals_row = np.linspace(start=0, stop=self.w, num=n)
        xvals_arr = np.tile(xvals_row, (len(self.labels), 1))

        # print("xvals_arr: \n", xvals_arr)
        # print("data_scaled: \n", data_scaled)
        
        points = np.dstack([xvals_arr, data_scaled]).reshape(m, 2*n)

        for i in range(len(self.labels)):
            self.canvas.coords(f"{self.labels[i]}L", points[i].tolist())
            self.canvas.coords(f"{self.labels[i]}T", (points[i][-2:] + self.textoffset).tolist())

count = 0
def main():
    np.set_printoptions(precision=2, suppress=True)

    root = tk.Tk()
    plot = Plot(root)

    def senddata():
        global count
        count += 1

        message = ""
        for i in range((int)(count / 200)+1):
            if(i > 4):
                break
            message = message + f"{i}: {np.sin(count/50+i)} \n"
        plot.set(message)
    datastream = PeriodicSleeper(senddata, 0.01)

    root.mainloop()
    return 0

if __name__ == '__main__':
    sys.exit(main())