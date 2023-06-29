from tkinter import *
import tkinter

class Application:

    def hello(self):
        msg = tkinter.messagebox.askquestion('title','question')

    def __init__(self, form):
        # form.resizable(0,0)
        form.minsize(200, 200)
        form.title('Top Level')

        # Global Padding pady and padx
        pad_x = 5
        pad_y = 5

        # Create controls

        label1 = Label(form, text="Label1")
        textbox1 = Entry(form)
        #command= parameter missing.


        textarea1 = Text(form, width=20, height=10)
        scrollbar1 = Scrollbar(form)


        textarea1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=textarea1.yview)

        button1 = Button(form, text='Button1')
        self.textbox = textbox1 # to make it accessible outside your __init__
        self.textarea = textarea1 # see above

        form.bind("<Return>", self.addchat)

        textarea1.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)
        scrollbar1.grid(row=0, column=2, padx=pad_x, pady=pad_y, sticky=W)
        textbox1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)
        button1.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky=W)

        form.mainloop()

    def addchat(self, event=None):
        txt = self.textbox.get()
        # gets everything in your textbox
        self.textarea.insert(END,"\n"+txt)
        # tosses txt into textarea on a new line after the end
        self.textbox.delete(0,END) # deletes your textbox text

root = Tk()
Application(root)