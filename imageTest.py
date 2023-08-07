#simple image test

from tkinter import *

class blackjackWindow():

    def __init__(self):
        self.window = Tk()
        self.window.geometry("700x500")
        self.window.title("KBB's Blackjack")

    def addCard(self):
        cardImage = PhotoImage(file="cards/Ace_of_Clubs.png")
        newlabel = Label(self.window, image=cardImage, bg="green")
        newlabel.pack()

    def ML(self):
        self.window.mainloop()

bjw = blackjackWindow()
bjw.addCard()
bjw.ML()