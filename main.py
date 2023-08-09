# Kyle Breen-Bondie - Final Project Blackjack Simulator
import random
import csv
#import Image #Image package: py -m pip install Image
from tkinter import *
#from Pillow import Image   #pillow package
import time

class Card():
    """Single card object that holds a suit, a rank (card # or face), and a blackjack number value"""
    suit = ""      #suit
    rank = 0       #card number or str face
    value = 0      #number value in blackjack

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.img = f"cards/{self.get_rank()}_of_{self.suit}.png"

        #set blackjack value
        if isinstance(rank, int):    #assigns value of card (for blackjack) - if its just a number, assign #
            self.value = rank
        elif rank == "Ace":          #assigns values if rank is Ace
            self.value = 11
        else:                        #assigns value if rank is not a number or ace card (i.e. face card of any kind)
            self.value = 10

    def __str__(self):
        return (f'{self.get_rank()} of {self.get_suit()}')

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


class Deck():
    """Deck object that holds two lists of card objects. One being the deck, the other used (discarded) cards.
    Initialized with a reshuffle number"""
    deck = []                      #list of card objects that are to be drawn
    discard = []                   #list of card objects that were drawn
    reshufNum = 20                 #number of cards left in deck at which the discard is reshuffled into deck
    needsReshuf = False            #boolean that is enabled to reshuffle cards so it can be triggered after game is complete (not mid hand)
    cardCountOffset = 0            #counts 2-6 as +1, 7-9 as 0, and 10/ace as -1


    def __init__(self, numOfDecks, reshufNum):
        self.deck = []
        self.discard = []
        self.reshufNum = reshufNum
        suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
        rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        self.realCardCountOffset = self.cardCountOffset / numOfDecks

        for d in range(numOfDecks):
            for s in suits:
                for r in rank:
                    self.deck.append(Card(s, r))

        self.reshuf()

    def shuf(self):
        """shuffles deck list"""
        random.shuffle(self.deck)

    def reshuf(self):
        """Reshuffles the deck by first combining the discard back into the deck, shuffling deck, then clearing discard list"""
        print("---Reshuffling deck---")
        newDeck = self.deck + self.discard
        random.shuffle(newDeck)
        self.deck = newDeck
        self.discard.clear()
        self.needsReshuf = False

    def draw(self):
        """Returns one card by drawing (pop) a card from deck and adding that to the discard list"""
        if len(self.deck) < self.reshufNum:
            self.needsReshuf = True
        drawnCard = self.deck.pop()
        #adjusts offset
        if drawnCard.value <= 6:
            self.cardCountOffset += 1
        elif drawnCard.value >= 10:
            self.cardCountOffset -= 1
        self.discard.append(drawnCard)
        return(drawnCard)

class Hand():
    """A collection of cards like a deck. Has a list of card objects, a total (for blackjack) and
    two ace-counting variables to keep track of use of aces as 1 or 11s"""
    hand = []              #list of card objects
    total = 0              #total value in blackjack
    numOfAces = 0          #counts number of aces
    numOfAcesAs1 = 0       #counts aces that are used as a value of 1 (to prevent bust)
    betAmount = 0
    isDealer = False       #helps for organizing pngs in window

    def __init__(self, betAmount, isDealer):
        self.hand = []
        self.total = 0
        self.numOfAces = 0
        self.numOfAcesAs1 = 0
        self.betAmount = betAmount
        self.isDealer = isDealer

    def __eq__(self, otherHand):
        if self.total == otherHand.getTotal():
            return True
        else:
            return False

    def __lt__(self, otherHand):
        if self.total < otherHand.getTotal():
            return True
        else:
            return False

    def __gt__(self, otherHand):
        if self.total > otherHand.getTotal():
            return True
        else:
            return False

    def __str__(self):
        if self.isDealer:
            toreturn = "Dealer Hand: "
        else:
            toreturn = "My Hand: "
        for x in range (len(self.hand)):
            toreturn += str(self.hand[x])
            toreturn += " - "
        toreturn += str(self.total)
        return toreturn

    def draw1(self, Deck, window=None):
        """Draws 1 card from deck in parameter and adds it to the hand's list.
        Maintains hand's total for blackjack."""
        newCard = Deck.draw()
        self.hand.append(newCard)

        if newCard.rank == "Ace":
            self.numOfAces += 1

        self.total = self.total + newCard.value

        if self.numOfAcesAs1 < self.numOfAces:
            if self.isBust():
                self.total = self.total - 10
                self.numOfAcesAs1 += 1

        if window != None:
            window.addCard(newCard, self.isDealer, len(self.hand))


    def getTotal(self):
        return self.total

    def isBust(self):
        """Checks if hand is bust and returns boolean"""
        if self.total > 21:
            return True
        else:
            return False

    def isNotBust(self):
        """Checks if hand is bust and returns boolean"""
        if self.total <= 21:
            return True
        else:
            return False

    def isBJ(self):
        """Checks if hand is a blackjack (2 cards and 21 total) and returns boolean"""
        if self.total == 21 and len(self.hand) == 2:
            return True
        else:
            return False

    def newHand(self, Deck, cardsToDraw):
        """When creating new hand, draws card amount based on parameter, from deck given"""
        for n in range (cardsToDraw):
            self.draw1(Deck)

    def discardHand(self):
        """Resets the hand object's card list, total and ace variables"""
        self.total = 0
        self.hand = []
        self.numOfAces = 0
        self.numOfAcesAs1 = 0

def printTable(my, dealer):
    """Prints dealer's card(s), then player's cards"""
    print("DEALER SHOWING: ", end="")
    print(dealer)
    print("Hand: ", end = "")
    print(my)      #does not provide values / totals. can add

def printRecord(w, l, t):
    """Prints win, loss and tie values that are passed."""
    print("Your record: ", w, "W/", l, "L/", t, "T")

def getBetAmount(deck):
    """Controls the bet amount, what the bet threshold is, and the min and max bets.
    Returns the bet."""
    offSetThreshold = -10     #point at which the player feels it is in his favor
    minAmount = 5            #minimum table bet
    bigBetAmount = 50        #big bet amount when advantageous
    if deck.realCardCountOffset <= offSetThreshold:
        return bigBetAmount
    else:
        return minAmount

def getBlackJackAmount(initialBet):
    """Determines how much a blackjack pays."""
    return initialBet * 1.5    #set at 3 to 2

def getHitorStand(myHand, dealer):
    """Determines, based on a table of what the dealer shows and the player has, whether to hit or stand
    Returns hit or stand string
    Table has 1 for hit and 0 for stand, dealer showing at top row, our total on side"""

    dealerAdjustedValue = dealer.total - 3 #need to offset dealer totals by 3 because columns start at 2, not 0

    #dealer:  2  3  4  5  6  7  8  9 10 11
    table = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #0   notused
             [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  #1   notused
             [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  #2   notused
             [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  #3   notused
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #4
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #5
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #6
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #7
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #8
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #9
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #10
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  #11
             [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],  #12
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  #13
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  #14
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  #15
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],  #16
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #17
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #18
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #19
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  #20
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]  #21

    col = []
    for x in range(22):
        col.append(table[x])
    #print(col[17][0])
    if myHand.total < 21:
        return "Stand"
    val = col[myHand.total][dealerAdjustedValue]
    if val == 0:
        return "Stand"
    else:
        return "Hit"

def playBlackJackLoop(numDecks, reshuf):
    """Non-GUI version of BJ game (played via text in the console)"""
    #reshuffle point should not be lower than 10
    myHand = Hand(0, False)
    dealer = Hand(0, True)
    deck = Deck(1, 20)
    playing = True
    wins = 0
    losses = 0
    ties = 0

    while playing:
        playOrNot = input("****** Would you like to play?")

        match playOrNot:
            case "no" | "n" | "No" | "quit" | "q" | "Q" | "N":
                playing = False
                print("Thank you for playing.")
                printRecord(wins, losses, ties)
                break

        myHand.discardHand()       #ensures hand values are empty / reset
        dealer.discardHand()       #ensures dealer hand values are empty / reset
        myHand.draw1(deck)
        myHand.draw1(deck)
        dealer.draw1(deck)
        printTable(myHand, dealer)

        while (myHand.isBust() == False) and (myHand.isBJ() == False):
            #hit or stay input loop, checks if busted or hand is blackjack
            hitOrStay = input("Hit or Stay?")

            match hitOrStay:
                case "hit" | "h" | "Hit" | "H":
                    myHand.draw1(deck)
                case _:
                    break
            printTable(myHand, dealer)

        #result checking - then dealer plays if necessary (not busted or blackjack)
        if myHand.isBust():
            print("Bust! You lost!")
            losses += 1
        elif myHand.isBJ():
            print("Blackjack! You win!")
            wins += 1
        else:
            dealer.draw1(deck)
            while dealer.getTotal() <= 16:
                dealer.draw1(deck)
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
        if deck.needsReshuf:
            deck.reshuf()

def simulation(gamesToSim, numDecks, reshuf):
    """Simulate x number of games with y number of decks
    counts # of wins if 'player' stays at 2 cards, or hits once"""

    head_row = ["Hand Starting Value", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "TOTAL"]
    twocard_winValues = ["Two Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_wins = 0
    twocard_lossValues = ["Two Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_losses = 0
    twocard_tieValues = ["Two Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_ties = 0
    threecard_winValues = ["Three Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_wins = 0
    threecard_lossValues = ["Three Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_losses = 0
    threecard_tieValues = ["Three Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_ties = 0
    secondHand_winValues = ["Second Hand Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_wins = 0
    secondHand_lossValues = ["Second Hand Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_losses = 0
    secondHand_tieValues = ["Second Hand Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondHand_ties = 0
    deck = Deck(numDecks, reshuf)
    moneyTwoCard = 0     #starting money for two card
    moneyThreeCard = 0   #starting money for three card
    moneySecondHand = 0  #starting money for second hand (that hits/stands according to table)


    loops = 0
    while loops < gamesToSim:
        betAmount = getBetAmount(deck)
        myHand = Hand(betAmount, False)
        dealer = Hand(betAmount, True)
        myHand.discardHand()      # ensures hand values are empty / reset
        dealer.discardHand()      # ensures dealer hand values are empty / reset

        myHand.newHand(deck, 2)
        myHand2 = Hand(betAmount)
        myHand2.hand = myHand.hand
        myHand2.total = myHand.total
        myHand2.numOfAces = myHand.numOfAces
        myHand2.numOfAcesAs1 = myHand.numOfAcesAs1
        dealer.newHand(deck, 1)
        handStartingValue = myHand.getTotal()

        while getHitorStand(myHand2, dealer) == "Hit" :
            myHand2.draw1(deck)

        while dealer.getTotal() <= 16:
            dealer.draw1(deck)

        #check if player1 won/lost/tied with 2 cards
        if (myHand.isBJ()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            moneyTwoCard = moneyTwoCard + getBlackJackAmount(myHand.betAmount)
        elif (dealer.isBust()) or (myHand.getTotal() > dealer.getTotal()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            moneyTwoCard = moneyTwoCard + myHand.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            twocard_tieValues[handStartingValue] += 1
            twocard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            twocard_lossValues[handStartingValue] += 1
            twocard_losses += 1
            moneyTwoCard = moneyTwoCard - myHand.betAmount
        else:
            print("Error")

        #if hand2 did take a card, add third card to first hand so that the hands first 3 cards match
        if len(myHand2.hand) > 2:
            myHand.hand.append(myHand2.hand[2])
        else:
            myHand.draw1(deck)

        # check if player won/lost/tied with 3 cards
        if (myHand.isBust()):            #no matter what if player busts, it is a loss
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
            moneyThreeCard = moneyThreeCard - myHand.betAmount
        elif myHand.getTotal() > dealer.getTotal():
            threecard_winValues[handStartingValue] += 1
            threecard_wins += 1
            moneyThreeCard = moneyThreeCard + myHand.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            threecard_tieValues[handStartingValue] += 1
            threecard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
            moneyThreeCard = moneyThreeCard - myHand.betAmount
        else:
             print("Error")

        # check if player's second hand won/lost/tied
        if (myHand2.isBust()):  # no matter what if player busts, it is a loss
            secondHand_lossValues[handStartingValue] += 1
            secondHand_losses += 1
            moneySecondHand = moneySecondHand - myHand2.betAmount
        elif myHand.getTotal() > dealer.getTotal():
            secondHand_winValues[handStartingValue] += 1
            secondHand_wins += 1
            moneySecondHand = moneySecondHand + myHand2.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            secondHand_tieValues[handStartingValue] += 1
            secondHand_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            secondHand_lossValues[handStartingValue] += 1
            secondHand_losses += 1
            moneySecondHand = moneySecondHand - myHand.betAmount
        else:
            print("Error")

        if deck.needsReshuf:
            deck.reshuf()
        loops += 1

    #remove all 0-3 results from the lists
    del twocard_winValues[1:4]
    del twocard_lossValues[1:4]
    del twocard_tieValues[1:4]
    del threecard_winValues[1:4]
    del threecard_lossValues[1:4]
    del threecard_tieValues[1:4]
    del secondHand_winValues[1:4]
    del secondHand_lossValues[1:4]
    del secondHand_tieValues[1:4]

    #add the total for each list to the final cell
    twocard_winValues.append(twocard_wins)
    twocard_lossValues.append(twocard_losses)
    twocard_tieValues.append(twocard_ties)
    threecard_winValues.append(threecard_wins)
    threecard_lossValues.append(threecard_losses)
    threecard_tieValues.append(threecard_ties)
    secondHand_winValues.append(secondHand_wins)
    secondHand_lossValues.append(secondHand_losses)
    secondHand_tieValues.append(secondHand_ties)

    #create betting info row
    betRow = ["Final money for two card bets:", moneyTwoCard,"","Final money for three card bets:", moneyThreeCard,
              "", "Final money for table bets:", moneySecondHand]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([twocard_winValues])
        writer.writerows([twocard_lossValues])
        writer.writerows([twocard_tieValues])
        writer.writerows([threecard_winValues])
        writer.writerows([threecard_lossValues])
        writer.writerows([threecard_tieValues])
        writer.writerows([secondHand_winValues])
        writer.writerows([secondHand_lossValues])
        writer.writerows([secondHand_tieValues])
        writer.writerows([betRow])

def playBlackJackGUI(numDecks, reshuf):
    """Loop that gets user input to continually play blackjack. Keeps track of wins, losses and ties for the session."""
    #reshuffle point should not be lower than 10

    myHand = Hand(0, False)
    dealer = Hand(0, True)
    deck = Deck(numDecks, reshuf)
    playing = True
    wins = 0
    losses = 0
    ties = 0
    bjw = blackjackWindow(numDecks, reshuf, myHand, dealer, deck)

    bjw.ML()

def hit(hand, deck, window=None):
    """Triggered when hit button is pushed. Adds new card to player's hand."""
    if window != None:
        hand.draw1(deck, window)
        checkHand(hand, window)
    else:
        hand.draw1(deck)

def stand(dealer, myHand, deck, window=None):    #not set up for non-window usage
    """Triggered when stand button is pushed. Prompts dealer's actions then calls check winner."""
    dealer.draw1(deck, window)
    while dealer.total <= 16:
        dealer.draw1(deck, window)
    checkWinner(myHand, dealer, window)

def checkHand(hand, window):
    """Mid-game check to see if the game is over (mainly to check after a hit if player busted)"""
    if hand.isBust() and hand.isDealer:
        window.gameOver("Win")
    elif hand.isBust():
        window.gameOver("Lose")

def checkWinner(myHand, dealer, window):
    """If it gets to the end of the game, this checks final winner"""
    if dealer.total > myHand.total and dealer.isNotBust():
        window.gameOver("Lose")
    elif dealer.total < myHand.total or dealer.isBust():
        window.gameOver("Win")
    else:
        print("TIE")
        window.gameOver("Tie")

def startNewGame(myHand, dealer, deck, window):
    """Begins new game- clearing window, then removing cards from hands, then reshuffling if necessary then dealing"""
    #window must be cleared first- putting blank image over all existing card images
    window.clearCards()
    myHand.discardHand()           # ensures hand values are empty / reset
    dealer.discardHand()           # ensures dealer hand values are empty / reset

    #check for reshuffle
    if deck.needsReshuf:
        deck.reshuf()
    window.activatePlayButtons()

    #clear winner/loser label
    window.clearWLLabel()

    #draw cards
    myHand.draw1(deck, window)
    myHand.draw1(deck, window)
    dealer.draw1(deck, window)

    #check if blackjack was dealt
    if myHand.isBJ():
        window.gameOver("Win")

def quitWindow(window):
    window.destroy()

################# UI / WINDOWS
class blackjackWindow():
    """Blackjack GUI window to play blackjack. Holds hand and deck info, as well as wins and losses."""

    def __init__(self, numDecks, reshuf, myHand, dealer, deck):
        self.window = Tk()
        self.window.geometry("1100x700")
        self.window.title("KBB's Blackjack")
        self.myHand = myHand
        self.dealer = dealer
        self.deck = deck
        self.wins = 0
        self.losses = 0

        #add buttons to window in grid as well as wins and losses labels
        self.hitButton = Button(text="Hit", padx=20, pady=20,
                                command=lambda: hit(self.myHand, self.deck, self))
                                # needs to pass SELF not SELF.WINDOW for some reason
        self.hitButton.grid(row=4, column=2)
        self.standButton = Button(text="Stand", padx=20, pady=20,
                                  command=lambda: stand(self.dealer, self.myHand, self.deck, self))
        self.standButton.grid(row=4, column=3)
        self.winsLabel = Label(text=f'W: {self.wins}', font=(14))
        self.winsLabel.grid(row=0, column=0)
        self.lossesLabel = Label(text=f'L: {self.losses}', font=(14))
        self.lossesLabel.grid(row=0, column=1)
        self.newGameButton = Button(text="New Game", state=DISABLED, padx=20, pady=20,
                                    command=lambda: startNewGame(self.myHand, self.dealer, self.deck, self))
        self.newGameButton.grid(row=4, column=4)
        self.quitButton = Button(text= "Quit", padx=20, pady=20,
                                 command= lambda: quitWindow(self.window))
        self.quitButton.grid(row=4, column = 6)
        self.winnerLabel = Label(text="WINNER", bg="#D0F0C0", font=(14))
        self.loserLabel = Label(text="LOSER", bg="#FA8072", font=(14))

        startNewGame(self.myHand, self.dealer, self.deck, self)

    def addCard(self, card, isDealer, len):
        """Adds a card to the window table- top row is the dealer, bottom player"""

        #get image, then place into label
        cardImage = PhotoImage(file=card.img)
        newlabel = Label(self.window, image=cardImage)
        newlabel.image = cardImage
        #place new card image into correct row (dealer or player) then correct column
        if isDealer:
            newlabel.grid(row=2, column=len+1)
        else:
            newlabel.grid(row=3, column=len+1)

    def gameOver(self, result):
        """Triggers the end of the game, in a win or a loss state based on the string passed.
        Responsible for incrementing wins/losses, as well as changing the button states at game over."""

        print("Game Over! ", result)
        print(self.dealer)
        print(self.myHand)

        #disable playing buttons, then enable new game button
        self.newGameButton.config(state=ACTIVE)
        self.hitButton.config(state=DISABLED)
        self.standButton.config(state=DISABLED)

        #check win or loss and increment count, then recreate and place label
        if result == "Win":
            self.wins += 1
            winsLabel = Label(text=f'W: {self.wins}', font=(14))
            winsLabel.grid(row=0, column=0)
            self.winnerLabel.grid(row=4, column =0, columnspan=2)
        elif result == "Lose":
            self.losses += 1
            lossesLabel = Label(text=f'L: {self.losses}', font=(14))
            lossesLabel.grid(row=0, column=1)
            self.loserLabel.grid(row=4, column=0, columnspan=2)

    def clearCards(self):
        """Places blank images over any card images that were placed previously to remove all cards"""
        #clear player hand
        for x in range(len(self.myHand.hand)):
            if x > 1:
                cardImage = PhotoImage(file="cards/nocard.png")
                newlabel = Label(self.window, image=cardImage)
                newlabel.grid(row=3, column= x+2)

        #clear dealer hand
        for x in range(len(self.dealer.hand)):
            if x > 0:
                cardImage = PhotoImage(file="cards/nocard.png")
                newlabel = Label(self.window, image=cardImage)
                newlabel.grid(row=2, column=x+2)

    def activatePlayButtons(self):
        """Switches button states to allow playing"""
        self.hitButton.config(state=ACTIVE)
        self.standButton.config(state=ACTIVE)
        self.newGameButton.config(state=DISABLED)

    def clearWLLabel(self):
        #self.winnerLabel.config(text="", bg="#000000")
        #self.loserLabel.config(text="", bg="#000000")
        print("TEST")

    def ML(self):
        self.window.mainloop()


playBlackJackGUI(1,20)
#simulation(100000,5,104)
