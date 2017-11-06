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
        # frame.raise()
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

    def __init__(self, master, result):

        self.master = master
        self.frame = tk.Frame(self.master)
        self.title = tk.Label(self.frame, text="Property Search Results")
        self.title.grid(row=0)
        count = 1
        for set1 in result["response"]["listings"]:
            #print(set1["title"])
            #Image
            if count < 4:
                descrip = ""
                url = set1["img_url"]
                fileurl = cStringIO.StringIO(urllib.urlopen(url).read())
                image = Image.open(fileurl)
                resized = image.resize((200, 200), Image.ANTIALIAS)
                photo1 = ImageTk.PhotoImage(resized)
                imgLabel = tk.Label(self.frame, image=photo1)
                imgLabel.img = photo1
                imgLabel.grid(row=count,column=0, padx=20, pady=5)
                descrip = descrip + "Listing Title: " + set1["title"] + "\n\n" + "Key Features: " + set1["keywords"] + \
                          "\n\n" + "Price: " + set1["price_formatted"]
                # self.listingTitle = tk.Label(self.frame, text=set1["title"])
                # self.listingTitle.grid(row=count,column=1, padx=5, pady=3)
                # print "Key Features:"
                # self.keywords = tk.Label(self.frame, text=set1["keywords"])
                # self.keywords.grid(row=count,column=1, padx=5, pady=3)
                # print "Key Features:"
                # self.price = tk.Label(self.frame, text=set1["price_formatted"])
                # self.price.grid(row=count,column=1, padx=5, pady=3)
                self.description = tk.Label(self.frame, text= descrip)
                self.description.grid(row=count, column=1, padx= 10)
                count = count+1
        self.frame.grid()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Login(root)
    root.mainloop()


if __name__ == '__main__':
    main()
