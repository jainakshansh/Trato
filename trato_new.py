import Tkinter as tk
import requests
import urllib, cStringIO
from PIL import Image, ImageTk
# from twisted.internet.defer import inlineCallbacks
# from twisted.internet.task import react
# from requests_threads import AsyncSession

LARGE_FONT = ("Verdana", 20)


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

        # Change back to Start Page when not debugging
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")


    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        self.controller = controller
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
        # file handling, encrypt mdhash
        if user == "tush" and password == "pass":
            print "Correct Pass"
            controller.show_frame(Home)
        else:
            print "Invalid Pass"


class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.variableexample = 3
        self.result = {}
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

    # @inlineCallbacks
    def makeSearchQuery(self, searchquery, value, c1, c2, c3, controller):
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
            if bedrooms:
                bedrooms_max = bedrooms
            else:
                bedrooms_max = 5

        # session = AsyncSession()

        url = "https://api.nestoria.in/api"

        querystring = {"encoding": "json", "pretty": "1", "action": "search_listings", "country": "in",
                     "listing_type": option, "place_name": searchquery, "bedroom_min": bedrooms, "bedroom_max": bedrooms_max}
        response = requests.request("GET", url, params=querystring)

        # response = session.get(url, querystring)
        # print response.json()
        # self.result = yield response
        # print self.result
        self.result = response.json()
        # print self.result
        # print "Home: " + self.result["response"]["listings"][0]["title"]
        # self.newWindow = tk.Toplevel(self.master)
        # self.app = SearchResults(self.newWindow, result)
        controller.show_frame(SearchResults)



class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Property Search Results")
        title.grid(row=0)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.populateScreen)

    def populateScreen(self, event):
        homeobject = self.controller.get_page(Home)
        result = homeobject.result
        count = 1
        print result
        for set1 in result["response"]["listings"]:
            print(set1["title"])
            # Image
            if count < 8:
                descrip = ""
                url = set1["img_url"]
                fileurl = cStringIO.StringIO(urllib.urlopen(url).read())
                image = Image.open(fileurl)
                resized = image.resize((200, 200), Image.ANTIALIAS)
                photo1 = ImageTk.PhotoImage(resized)
                imgLabel = tk.Label(self, image=photo1)
                imgLabel.img = photo1
                imgLabel.grid(row=count, column=0, padx=20, pady=5)
                descrip = descrip + "Listing Title: " + set1["title"] + "\n\n" + "Key Features: " + set1["keywords"] + \
                          "\n\n" + "Price: " + set1["price_formatted"]
                listingTitle = tk.Label(self, text=set1["title"])
                listingTitle.grid(row=count,column=1, padx=5, pady=3)
                print "Key Features:"
                keywords = tk.Label(self, text=set1["keywords"])
                keywords.grid(row=count,column=1, padx=5, pady=3)
                print "Key Features:"
                price = tk.Label(self, text=set1["price_formatted"])
                price.grid(row=count,column=1, padx=5, pady=3)
                description = tk.Label(self, text=descrip)
                description.grid(row=count, column=1, padx=10)
                count = count + 1


app = TratoApp()
app.mainloop()
