import Tkinter as tk
import requests
import json
import urllib, cStringIO

LARGE_FONT = ("Verdana", 12)

result = '{}'

class TratoApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Login, Home, SearchResults):
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


def storesearch(result1):
    res = result1
    return res

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

        checkVar1 = tk.IntVar()
        checkVar2 = tk.IntVar()
        checkVar3 = tk.IntVar()

        label = tk.Label(self, text="No. of Bedrooms:", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        C1 = tk.Checkbutton(self, text="2", variable=checkVar1, onvalue=1, offvalue=0)

        C2 = tk.Checkbutton(self, text="3", variable=checkVar2, onvalue=1, offvalue=0)

        C3 = tk.Checkbutton(self, text="3+", variable=checkVar3, onvalue=1, offvalue=0)

        C1.pack()
        C2.pack()
        C3.pack()

        submitButton = tk.Button(self, text="Search for properties",
                            command=lambda: self.makeSearchQuery(searchQuery.get(), v.get(),
                                            checkVar1.get(), checkVar2.get(), checkVar3.get(), controller))
        submitButton.pack()

    def makeSearchQuery(self, searchquery, value, c1, c2, c3, controller):
        global result
        print searchquery
        print value
        if value == 1:
            option = "buy"
        else:
            option = "rent"

        if c1 == 1:
            bedrooms = 2
        if c2 == 1:
            bedrooms = 3
        if c3 == 1:
            bedrooms_max = 5
        else:
            bedrooms_max = bedrooms

        url = "https://api.nestoria.in/api"

        querystring = {"encoding": "json", "pretty": "1", "action": "search_listings", "country": "in",
                       "listing_type": option, "place_name": searchquery, "bedroom_min": bedrooms, "bedroom_max": bedrooms_max}

        response = requests.request("GET", url, params=querystring)
        # print response.json()
        result = response.json()
        storesearch(result)
        # print result["response"]["listings"][0]["title"]
        controller.show_frame(SearchResults)


class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        print "I reached the next window!"
        label = tk.Label(self, text="Search Results:", font=LARGE_FONT)
        label.grid(row=0)
        res = storesearch(result)







app = TratoApp()
app.mainloop()
