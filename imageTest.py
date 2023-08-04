#simple image test

from tkinter import *

window = Tk()
window.geometry("700x500")
window.title("KBB's Blackjack")
testimg = PhotoImage(file="cards/Ace_of_Clubs.png")
newlabel = Label(window, image=testimg)

newlabel.pack()

window.mainloop()