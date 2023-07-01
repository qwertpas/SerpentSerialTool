import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import numpy as np
import time

from blitting import BlitManager


class PlotWindowPlt:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Serpent Plotter")

        # Create a Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(4,4))

        # Create a Matplotlib canvas within the frame
        canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        canvas.get_tk_widget().pack()

        self.optionframe = tk.Frame(self.window)
        self.optionframe.pack(fill=tk.BOTH, expand=True)


        # Create a text entry for adjusting x and y limits
        limits_frame = tk.Frame(self.window)
        limits_frame.pack(pady=10)
        x_limit_entry = tk.Entry(limits_frame, width=10)
        x_limit_entry.pack(side=tk.LEFT, padx=5)
        y_limit_entry = tk.Entry(limits_frame, width=10)
        y_limit_entry.pack(side=tk.LEFT, padx=5)

        def update_plot_limits(self=self):
            try:
                x_limit = float(x_limit_entry.get())
                y_limit = float(y_limit_entry.get())
                self.ax.set_xlim(0, x_limit)
                self.ax.set_ylim(0, y_limit)
                canvas.draw()
            except Exception as e:
                print(e)

        # Create a button to update plot limits
        update_button = tk.Button(limits_frame, text="Update Limits", command=update_plot_limits)
        update_button.pack(pady=10)


        def save_data_as_csv(self=self):
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    
                    # Write the labels as the header row
                    writer.writerow(self.labels)
                    
                    # Write the data rows
                    writer.writerows(self.data.T)

        # Create a button to browse for save location and save data as CSV
        save_button = tk.Button(self.window, text="Save CSV", command=save_data_as_csv)
        save_button.pack(pady=10)

        self.historylen = 100
        self.labels = ["series0"]
        self.data = np.zeros([len(self.labels), self.historylen]) #history of data points
        (ln,) = self.ax.plot(np.zeros(self.historylen), 'o-', label=self.labels[0], markersize=1)
        self.lines = [ln]
        self.bm = None
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 800)



    def lift(self):
        self.window.lift() #brings this window above other windows so you can see it

    def message_to_dict(message):
        data_dict = {}
        lines = message.strip().split("\n")
        for line in lines:
            try:
                parts = line.split(":")
                if len(parts) != 2: #ignore lines that don't have exactly one colon
                    continue
                key, value = parts
                key = key.strip()
                value = float(value.strip().split(" ")[0]) #only use the first "word" and ignore spaces
                data_dict[key] = value
            except Exception as e:
                print(e)
        return data_dict
    


    def plot_message(self, message:str):
        

        new_data = PlotWindowPlt.message_to_dict(message)

        if(len(new_data) != len(self.labels)):

            #add any series not in the data yet
            for key in new_data:
                if key not in self.labels:
                    self.labels.append(key)
                    self.data = np.append(self.data, [np.zeros(self.historylen)], axis=0)
                    (ln,) = self.ax.plot(np.zeros(self.historylen), label=key)
                    # (ln,) = self.ax.plot(np.zeros(self.historylen), 'o-', label=key, markersize=1)
                    self.lines.append(ln)

            #remove any series that aren't active
            to_delete = []
            for i in range(len(self.labels)): 
                if self.labels[i] not in new_data:
                    to_delete.append(i)
            for i in to_delete:
                self.data = np.delete(self.data, i, axis=0)
                self.labels.pop(i)
                self.lines.pop(i).remove()

            self.ax.legend()
            self.bm = BlitManager(self.fig.canvas, self.lines)


        self.data = np.roll(self.data, shift=-1, axis=1)
                
        i = 0
        for key in new_data:
            self.data[i][-1] = new_data[key]
            i += 1

        for i in range(len(self.data)):
            # self.ax.plot(self.data[i], label=self.labels[i])
            self.lines[i].set_ydata(self.data[i])
        self.bm.update()
        # self.fig.update()



        

if __name__ == "__main__":

    root = tk.Tk()
    serpent_plt = PlotWindow(root)

    for i in range(1000):
        serpent_plt.plot_message(f"m_angle  :   {i} dsdsdw\n temp: 66 \n \t")
        time.sleep(0.01)

    root.mainloop()

