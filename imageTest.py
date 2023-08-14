#simple image test

from tkinter import *

class blackjackWindow():

    def __init__(self):
        self.window = Tk()
        self.window.geometry("700x500")
        self.window.title("KBB's Blackjack")

    def addCard(self):
        backImage = PhotoImage(file="cards/back.png")
        backLabel = Label(self.window, image=backImage)
        backLabel.pack()

    def ML(self):
        self.window.mainloop()

bjw = blackjackWindow()
bjw.addCard()
bjw.ML()