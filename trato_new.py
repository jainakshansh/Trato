import Tkinter as tk
import requests
import urllib, cStringIO
from PIL import Image, ImageTk
# from twisted.internet.defer import inlineCallbacks
# from twisted.internet.task import react
# from requests_threads import AsyncSession

LARGE_FONT = ("Helvetica", 20)
MEDIUM_FONT = ("Helvetica", 16)


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
        self.show_frame(Home)

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
        searchQuery.insert(0,'Vashi')
        searchQuery.pack()

        label = tk.Label(self, text="Type", font=LARGE_FONT)
        label.pack(pady=8, padx=10)

        v = tk.IntVar()
        r1 = tk.Radiobutton(self, text="Buy", variable=v, value=1).pack(pady=3, padx=5)
        r2 = tk.Radiobutton(self, text="Rent", variable=v, value=2).pack(pady=5, padx=5)

        checkVar1 = tk.IntVar()
        checkVar2 = tk.IntVar()
        checkVar3 = tk.IntVar()

        label = tk.Label(self, text="No. of Bedrooms:", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        C1 = tk.Checkbutton(self, text="2", variable=checkVar1, onvalue=1, offvalue=0)

        C2 = tk.Checkbutton(self, text="3", variable=checkVar2, onvalue=1, offvalue=0)

        C3 = tk.Checkbutton(self, text="3+", variable=checkVar3, onvalue=1, offvalue=0)

        C1.pack(pady=2,padx=2)
        C2.pack(pady=2,padx=2)
        C3.pack(pady=2,padx=2)

        label = tk.Label(self, text="Radius:", font=LARGE_FONT)
        label.pack(pady=2, padx=5)

        slider = tk.Scale(self, from_=10, to_=60, orient=tk.HORIZONTAL)
        slider.pack(pady=1)

        submitButton = tk.Button(self, text="Search for properties", font=MEDIUM_FONT,
                            command=lambda: self.makeSearchQuery(searchQuery.get(), v.get(),
                                            checkVar1.get(), checkVar2.get(), checkVar3.get(), slider.get(), controller))
        submitButton.pack(padx=4,pady=4)

    # @inlineCallbacks
    def makeSearchQuery(self, searchquery, value, c1, c2, c3, radius, controller):
        print searchquery
        print value
        if value == 1:
            option = "buy"
        else:
            option = "rent"

        bedrooms = 3
        radiusVar = str(radius)+"km"
        print radiusVar

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
                     "listing_type": option, "place_name": searchquery, "bedroom_min": bedrooms, "bedroom_max": bedrooms_max,
                       "number_of_results": 10, "radius": radiusVar}
        response = requests.request("GET", url, params=querystring)

        self.result = response.json()

        controller.show_frame(SearchResults)



class SearchResults(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=2, height=500,width=700, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # title = tk.Label(self.interior, text="Property Search Results")
        # title.grid(row=0)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        def _on_mousewheel(event):
            self.canvas.yview_scroll(-1 * (event.delta / 120), "units")

        canvas.bind('<MouseWheel>', _on_mousewheel)

        canvas.bind('<Configure>', _configure_canvas)

        button2 = tk.Button(self.interior, text="Back",
                            command=lambda: controller.show_frame(Home))
        button2.grid(row=0, column=0, padx=20, pady=5)

        self.bind("<<ShowFrame>>", self.populateScreen)

    def populateScreen(self, event):
        homeobject = self.controller.get_page(Home)
        result = homeobject.result

        title = tk.Label(self.interior, text="Property Search Results", font=LARGE_FONT)
        title.grid(row=0,column=1,padx=20, pady=5)
        count = 1
        # print result
        for set1 in result["response"]["listings"]:
            # print(set1["title"])
            # Image
            if count < 11:
                descrip = ""
                url = set1["img_url"]
                fileurl = cStringIO.StringIO(urllib.urlopen(url).read())
                image = Image.open(fileurl)
                resized = image.resize((200, 200), Image.ANTIALIAS)
                photo1 = ImageTk.PhotoImage(resized)
                imgLabel = tk.Label(self.interior, image=photo1)
                imgLabel.img = photo1
                imgLabel.grid(row=count, column=0, padx=20, pady=5)
                descrip = descrip + "Listing Title: " + set1["title"] + "\n\n" + "Key Features: " + set1["keywords"] + \
                          "\n\n" + "Price: " + set1["price_formatted"]
                listingTitle = tk.Label(self.interior, text=set1["title"], font=MEDIUM_FONT)
                listingTitle.grid(row=count,column=1, padx=5, pady=3)
                keywords = tk.Label(self.interior, text=set1["keywords"], font=MEDIUM_FONT)
                keywords.grid(row=count,column=1, padx=5, pady=3)
                price = tk.Label(self.interior, text=set1["price_formatted"], font=MEDIUM_FONT)
                price.grid(row=count,column=1, padx=5, pady=3)
                description = tk.Label(self.interior, text=descrip)
                description.grid(row=count, column=1, padx=10)
                count = count + 1


app = TratoApp()
app.mainloop()
