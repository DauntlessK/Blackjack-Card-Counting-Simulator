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

while (myHand.isBust() == False) and (myHand.isBJ() == False):
    # hit or stay input loop, checks if busted or hand is blackjack
    hitOrStay = input("Hit or Stay?")

    match hitOrStay:
        case "hit" | "h" | "Hit" | "H":
            myHand.draw1(deck, bjw)
        case _:
            break
    printTable(myHand, dealer)

# result checking - then dealer plays if necessary (not busted or blackjack)
if myHand.isBust():
    print("Bust! You lost!")
    losses += 1
elif myHand.isBJ():
    print("Blackjack! You win!")
    wins += 1
else:
    dealer.draw1(deck, bjw)
    while dealer.getTotal() <= 16:
        dealer.draw1(deck, bjw)
    printTable(myHand, dealer)
    if dealer.isBust():
        print("Dealer is bust! You win!")
        wins += 1
    elif myHand > dealer:
        print("You win!")
        wins += 1
    elif myHand == dealer:
        print("Push!")
        ties += 1
    else:
        print("You lose!")
        losses += 1
printRecord(wins, losses, ties)