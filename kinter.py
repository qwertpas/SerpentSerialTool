import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys, os
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

print("\n" + application_path)

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# data1 = {'country': ['A', 'B', 'C', 'D', 'E'],
#          'gdp_per_capita': [45000, 42000, 52000, 49000, 47000]
#          }
# df1 = pd.DataFrame(data1)

# data2 = {'year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
#          'unemployment_rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
#          }  
# df2 = pd.DataFrame(data2)

# data3 = {'interest_rate': [5, 5.5, 6, 5.5, 5.25, 6.5, 7, 8, 7.5, 8.5],
#          'index_price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]
#          }
# df3 = pd.DataFrame(data3)

root = tk.Tk()

img = tk.Image("photo", file="bracks.png")
root.tk.call('wm','iconphoto', root._w, img)


# figure1 = plt.Figure(figsize=(6, 5), dpi=100)
# ax1 = figure1.add_subplot(111)
# bar1 = FigureCanvasTkAgg(figure1, root)
# bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# df1 = df1[['country', 'gdp_per_capita']].groupby('country').sum()
# df1.plot(kind='bar', legend=True, ax=ax1)
# ax1.set_title('Country Vs. GDP Per Capita')

# figure2 = plt.Figure(figsize=(3, 4), dpi=100)
# ax2 = figure2.add_subplot(111)
# line2 = FigureCanvasTkAgg(figure2, root)
# line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# df2 = df2[['year', 'unemployment_rate']].groupby('year').sum()
# df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
# ax2.set_title('Year Vs. Unemployment Rate')

# figure3 = plt.Figure(figsize=(3, 4), dpi=100)
# ax3 = figure3.add_subplot(111)
# ax3.scatter(df3['interest_rate'], df3['index_price'], color='g')
# scatter3 = FigureCanvasTkAgg(figure3, root)
# scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
# ax3.legend(['index_price'])
# ax3.set_xlabel('Interest Rate')
# ax3.set_title('Interest Rate Vs. Index Price')

label = tk.Label(root, text="Hello World!") # Create a text label
label.pack(padx=20, pady=20) # Pack it into the window

root.mainloop()