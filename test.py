import Tkinter as tk

LARGE_FONT = ("Verdana", 12)


class TratoApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Login, Home):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Login",
                           command=lambda: controller.show_frame(Login))
        button.pack()

        button2 = tk.Button(self, text="Search Home",
                            command=lambda: controller.show_frame(Home))
        button2.pack()


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text="Username", width=25)
        label1.pack()
        entry1 = tk.Entry(self, bd=1)
        entry1.pack()
        label2 = tk.Label(self, text="Password", width=25)
        label2.pack()
        entry2 = tk.Entry(self, show='*', bd=1)
        entry2.pack()
        button1 = tk.Button(self, text='Login', width=15, command=lambda: controller.show_frame(Home))
        button1.pack(pady=10)
        button2 = tk.Button(self, text="Back to Start",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(Login))
        button2.pack()


app = TratoApp()
app.mainloop()