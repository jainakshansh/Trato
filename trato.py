import Tkinter as tk
import requests
import Tkconstants as tkc
from PIL import Image, ImageTk
import urllib, cStringIO

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
        self.entry2 = tk.Entry(self.frame, show='*', bd=1)
        self.entry2.pack()
        self.button1 = tk.Button(self.frame, text='Login', width=15, command=self.validation)
        self.button1.pack(pady=10)
        self.frame.pack()

    def validation(self):
        user = self.entry1.get()
        password = self.entry2.get()
        if user == "tush" and password == "pass":
            print "Correct Pass"
            self.loginToSearch()

        else:
            print "Invalid Pass"

    def loginToSearch(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Home(self.newWindow)

    def close_windows(self):
        self.master.destroy()


class Home:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label1 = tk.Label(self.frame, text="Search for property (Enter Area / Locality) ", width=50)
        self.label1.pack()
        self.searchQuery = tk.Entry(self.frame, bd=1)
        self.searchQuery.pack()
        query = self.searchQuery.get()
        self.SubmitButton = tk.Button(self.frame, text='Search', width=25, command=self.search)
        self.SubmitButton.pack()
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def search(self):
        print self.searchQuery.get()
        print "Hello"
        url = "https://api.nestoria.in/api"

        querystring = {"encoding": "json", "pretty": "1", "action": "search_listings", "country": "in",
                       "listing_type": "buy", "place_name": self.searchQuery.get()}

        response = requests.request("GET", url, params=querystring)
        # print response.json()
        result = response.json()
        print result["response"]["listings"][0]["title"]
        self.searchToResults(result)

    def searchToResults(self, result):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SearchResults(self.newWindow, result)

    def close_windows(self):
        self.master.destroy()


class SearchResults:

    # def on_configure(canvas):
    #     canvas.configure(scrollregion=canvas.bbox('all'))

    def __init__(self, master, result):
        # canvas = tk.Canvas(self)
        # canvas.pack(side=tkc.LEFT)
        # bar = tk.Scrollbar(self.frame, command=canvas.yview)
        # bar.pack(side=tkc.RIGHT, fill=tkc.Y)
        # canvas.configure(yscrollcommand=bar.set)
        # canvas.bind('<Configure>', self.on_configure)
        # frame = tk.Frame(canvas)
        # canvas.create_window((0, 0), window=frame, anchor='nw')
        self.master = master
        self.frame = tk.Frame(self.master)
        self.title = tk.Label(self.frame, text="Property Results", width=50)
        self.title.pack()

        for set1 in result["response"]["listings"]:
            #print(set1["title"])
            #Image
            url = set1["img_url"]
            fileurl = cStringIO.StringIO(urllib.urlopen(url).read())
            image = Image.open(fileurl)
            photo1 = ImageTk.PhotoImage(image)
            imgLabel = tk.Label(self.frame, image=photo1)
            imgLabel.img = photo1
            imgLabel.pack()
            self.listingTitle = tk.Label(self.frame, text=set1["title"], width=50)
            self.listingTitle.pack()
            self.keywords = tk.Label(self.frame, text=set1["keywords"], width=50)
            self.keywords.pack()
            self.price = tk.Label(self.frame, text=set1["price_formatted"], width=50)
            self.price.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
