import Tkinter as tk

root=tk.Tk()

vscrollbar = tk.Scrollbar(root)

c= tk.Canvas(root,background = "#D2D2D2",yscrollcommand=vscrollbar.set)

vscrollbar.config(command=c.yview)
vscrollbar.pack(side=tk.LEFT, fill=tk.Y)

f=tk.Frame(c) #Create the frame which will hold the widgets

c.pack(side="left", fill="both", expand=True)

#Updated the window creation
c.create_window(0,0,window=f, anchor='nw')

#Added more content here to activate the scroll
for i in range(100):
    tk.Label(f,wraplength=350 ,text="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.").pack()
    tk.Button(f,text="anytext").pack()

#Removed the frame packing
#f.pack()

#Updated the screen before calculating the scrollregion
root.update()
c.config(scrollregion=c.bbox("all"))

root.mainloop()