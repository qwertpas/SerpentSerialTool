import tkinter as tk



def add_text():
    text = entry.get()
    if text:
        text_display.configure(state=tk.NORMAL)
        text_display.insert(tk.END, text + '\n')
        text_display.configure(state=tk.DISABLED)
        entry.delete(0, tk.END)
        text_display.see(tk.END)


root = tk.Tk()
root.title("Text Entry and Display")

# Create a frame to hold the radio button, text display, and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a radio button for edit mode
edit_mode = tk.IntVar()
edit_mode_checkbox = tk.Checkbutton(frame, text="Capture keystrokes", variable=edit_mode)
edit_mode_checkbox.pack()

# Create a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text display widget
text_display = tk.Text(frame, yscrollcommand=scrollbar.set)
text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_display.configure(state=tk.DISABLED)

# Configure the scrollbar to work with the text display
scrollbar.config(command=text_display.yview)

# Create a text entry widget
entry = tk.Entry(root)
entry.pack(side=tk.BOTTOM, fill=tk.X)

# Bind the Enter key to add_text function
entry.bind("<Return>", lambda event: add_text())

def on_keypress(event):
    if(edit_mode.get()==1):
        key = event.char
        print("Key pressed:", key)

# Bind the KeyPress event to the on_keypress function
text_display.bind("<KeyPress>", on_keypress)

# Start the tkinter event loop
root.mainloop()
