import tkinter as tk

class Login:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label1 = tk.Label(self.frame, text="Username", width=25)
        self.label1.pack()
        self.entry1 = tk.Entry(self.frame, bd=1)
        self.entry1.pack()
        self.label2 = tk.Label(self.frame, text="Password", width=25)
        self.label2.pack()
        self.entry2 = tk.Entry(self.frame, bd=1)
        self.entry2.pack()
        self.button1 = tk.Button(self.frame, text = 'Login', width = 15, command = self.new_window)
        self.button1.pack(pady=10)
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Home(self.newWindow)


class Home:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Sign Out', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Login(root)
    root.mainloop()

if __name__ == '__main__':
    main()