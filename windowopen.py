import tkinter as tk


def add_text():
    text = entry.get()
    if text:
        text_display.configure(state=tk.NORMAL)
        text_display.insert(tk.END, text + '\n')
        text_display.configure(state=tk.DISABLED)
        entry.delete(0, tk.END)
        text_display.see(tk.END)


def on_text_change(event):
    # Get the current content of the text box
    current_text = text_display.get("1.0", tk.END).strip()

    # Perform the desired action based on the content change
    if current_text == "7":
        print("The number 7 was entered!")


root = tk.Tk()
root.title("Text Entry and Display")

# Create a frame to hold the checkbox, text display, and scrollbar
frame = tk.Frame(root)

# Create a checkbox for edit mode
auto_send = tk.IntVar()
edit_mode_checkbox = tk.Checkbutton(frame, text="Send keystrokes immediately", variable=auto_send)

# Create a scrollbar
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text display widget
text_display = tk.Text(frame, yscrollcommand=scrollbar.set)
text_display.configure(state=tk.DISABLED)

# Configure the scrollbar to work with the text display
scrollbar.config(command=text_display.yview)

# Create a text entry widget
entry = tk.Entry(root)

# Bind the Enter key to add_text function
entry.bind("<Return>", lambda event: add_text())


def on_keypress(event):
    if(auto_send.get()==1):
        key = event.char
        add_text()
        print("Key pressed:", key)


# Bind the KeyPress event to the on_keypress function
entry.bind("<KeyPress>", on_keypress)


frame.pack(fill=tk.BOTH, expand=True)
text_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
entry.pack(fill=tk.X)
edit_mode_checkbox.pack(side=tk.BOTTOM)




# Start the tkinter event loop
root.mainloop()
