
from tkinter import Tk, Canvas, Frame, BOTH

import numpy as np
import colorsys

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.create_line(15, 25, 200, 25)
        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))
        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85, tag="T")


        self.canvas.pack(fill=BOTH, expand=1)

        self.i=0
        self.start_random()

    def start_random(self):
        points = (np.random.random(size=10)*100).astype(int).tolist()
        print(points)

        # self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85+self.i*10, tag="Ti")

        rgb = colorsys.hsv_to_rgb(np.random.random(), 0.6, 0.5)
        
        # Convert RGB values to hexadecimal string
        hex_code = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )

        self.canvas.itemconfig("T", fill=hex_code)
        self.canvas.coords('T', points)
        self.after(100, self.start_random)

        self.i += 1



def main():

    root = Tk()
    ex = Example()
    root.geometry("400x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()