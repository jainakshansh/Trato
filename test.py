import Tkinter as tk
import requests
import urllib, cStringIO

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
        label = tk.Label(self, text="Welcome to Trato", font=LARGE_FONT)
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
        button2 = tk.Button(self, text="Back to Start",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()

        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text="Username", width=25)
        label1.pack()
        entry1 = tk.Entry(self, bd=1)
        entry1.pack()
        label2 = tk.Label(self, text="Password", width=25)
        label2.pack()
        entry2 = tk.Entry(self, show='*', bd=1)
        entry2.pack()
        button1 = tk.Button(self, text='Login', width=15, command=lambda: self.validation(entry1.get(), entry2.get(),
                                                                                          controller))
        button1.pack(pady=10)

    def validation(self, user, password, controller):
        print user
        print password
        if user == "tush" and password == "pass":
            print "Correct Pass"
            controller.show_frame(Home)
        else:
            print "Invalid Pass"


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button2 = tk.Button(self, text="Log Out",
                            command=lambda: controller.show_frame(Login))
        button2.pack()

        label = tk.Label(self, text="Search for property (Enter Area / Locality)", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        searchQuery = tk.Entry(self, bd=1)
        searchQuery.pack()

        v = tk.IntVar()
        r1 = tk.Radiobutton(self, text="Buy", variable=v, value=1).pack()
        r2 = tk.Radiobutton(self, text="Rent", variable=v, value=2).pack()

        submitButton = tk.Button(self, text="Search for properties",
                            command=lambda: self.makeSearchQuery(searchQuery.get(), v.get(), controller))
        submitButton.pack()

    def makeSearchQuery(self, searchQuery, value, controller):
        print searchQuery
        print value

        if value == 1:
            option = "buy"
        else:
            option = "rent"

        url = "https://api.nestoria.in/api"

        querystring = {"encoding": "json", "pretty": "1", "action": "search_listings", "country": "in",
                       "listing_type": option, "place_name": searchQuery}
        response = requests.request("GET", url, params=querystring)
        # print response.json()
        result = response.json()
        print result["response"]["listings"][0]["title"]
        # controller.show_frame(Home)



app = TratoApp()
app.mainloop()
