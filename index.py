from tkinter import *
import tkinter.messagebox
top = Tk()

def ButtonClick():
    tkinter.messagebox.showinfo("Button was clicked", "Button!!")

L1 = Label(top, text="User Name")
L1.pack(fill=X,padx=10)
E1 = Entry(top, bd=1)
E1.pack(fill=X, padx=10)

L2 = Label(top, text="Password")
L2.pack(fill=X, padx=10)
E2 = Entry(top, bd=1)
E2.pack(fill=X, padx=10)

B = Button(top, text = "Login", command=ButtonClick)
B.pack(fill=X, padx=10)

top.mainloop()
