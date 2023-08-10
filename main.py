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
        self.numOfDecksLeft = numOfDecks
        self.needsReshuf = False

        for d in range(numOfDecks):
            for s in suits:
                for r in rank:
                    self.deck.append(Card(s, r))

        self.shuf()

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
        self.cardCountOffset = 0

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
        self.numOfDecksLeft = len(self.deck) / 52
        self.realCardCountOffset = self.cardCountOffset / self.numOfDecksLeft

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
        self.isSoft = False

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
            self.isSoft = True

        self.total = self.total + newCard.value

        if self.numOfAcesAs1 < self.numOfAces:
            if self.isBust():
                self.total = self.total - 10
                self.numOfAcesAs1 += 1

        if self.numOfAcesAs1 == self.numOfAces:
            self.isSoft = False

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
    offSetThreshold = +4.2    #point at which the player feels it is in his favor
    minAmount = 5             #minimum table bet
    bigBetAmount = 100        #big bet amount when advantageous
    if deck.realCardCountOffset >= offSetThreshold:
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

    #determine whether to use hard or soft hand table
    if myHand.isSoft:
    ##NEEDTODO: need to make a way to create the two action tables only once then reference correct chart
    ##          based on whether the hand is soft or hard
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
    #if myHand.total > 21:
    #    return "Stand"
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
    and bets the same hand 3 different ways to test the best way to make money"""

    head_row = ["Hand Starting Value", 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, "TOTAL"]
    hand_winValues = ["Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_wins = 0
    hand_lossValues = ["Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_losses = 0
    hand_tieValues = ["Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hand_ties = 0
    deck = Deck(numDecks, reshuf)
    moneyFlatBet = 0  # starting money for flat min bet
    flatBetAmount = 5  # how much flat better bets
    moneyRandBet = 0  # starting money for random bet
    minRandBetRange = 5  # min amount for random bet
    maxRandBetRange = 20  # max amount for random bet
    moneyCardCountBet = 0  # starting money for card counting bet method

    loops = 0
    while loops < gamesToSim:
        betAmount = getBetAmount(deck)
        myHand = Hand(betAmount, False)
        dealer = Hand(betAmount, True)
        myHand.discardHand()  # ensures hand values are empty / reset
        dealer.discardHand()  # ensures dealer hand values are empty / reset

        myHand.newHand(deck, 2)
        dealer.newHand(deck, 1)
        handStartingValue = myHand.getTotal()

        while getHitorStand(myHand, dealer) == "Hit" and myHand.getTotal() < 21:
            myHand.draw1(deck)

        while dealer.getTotal() <= 16 and myHand.isNotBust():
            dealer.draw1(deck)

        # check win/loss/tie scenarios
        if (myHand.isBJ()):
            hand_winValues[handStartingValue] += 1
            hand_wins += 1

            # get payouts for blackjack and add amounts to existing totals
            moneyCardCountBet = moneyCardCountBet + getBlackJackAmount(myHand.betAmount)
            moneyFlatBet = moneyFlatBet + getBlackJackAmount(flatBetAmount)
            moneyRandBet = moneyRandBet + getBlackJackAmount(random.randint(minRandBetRange, maxRandBetRange))
        elif (myHand.getTotal() < dealer.getTotal() and dealer.isNotBust()) or myHand.isBust():
            hand_lossValues[handStartingValue] += 1
            hand_losses += 1

            # money adjustments for player being less than dealer (if dealer is not bust) or if player busted
            moneyCardCountBet = moneyCardCountBet - getBetAmount(deck)
            moneyFlatBet = moneyFlatBet - flatBetAmount
            moneyRandBet = moneyRandBet - random.randint(minRandBetRange, maxRandBetRange)
        elif (dealer.isBust()) or (myHand.getTotal() > dealer.getTotal()):
            hand_winValues[handStartingValue] += 1
            hand_wins += 1

            # money adjustments for player being less than dealer (if dealer is not bust) or if player busted
            moneyCardCountBet = moneyCardCountBet + getBetAmount(deck)
            moneyFlatBet = moneyFlatBet + flatBetAmount
            moneyRandBet = moneyRandBet + random.randint(minRandBetRange, maxRandBetRange)
        elif myHand.getTotal() == dealer.getTotal():
            hand_tieValues[handStartingValue] += 1
            hand_ties += 1
        else:
            print("Error")

        if deck.needsReshuf:
            deck.reshuf()
        loops += 1

    # remove all 0-3 results from the lists
    del hand_winValues[1:4]
    del hand_lossValues[1:4]
    del hand_tieValues[1:4]

    # add the total for each list to the final cell
    hand_winValues.append(hand_wins)
    hand_lossValues.append(hand_losses)
    hand_tieValues.append(hand_ties)

    # create betting info row
    betRow1 = ["$ for flat bet:", moneyFlatBet]
    betRow2 = ["$ for random bet:", moneyRandBet]
    betRow3 = ["$ for card count bet:", moneyCardCountBet]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([hand_winValues])
        writer.writerows([hand_lossValues])
        writer.writerows([hand_tieValues])
        writer.writerows([betRow1])
        writer.writerows([betRow2])
        writer.writerows([betRow3])

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

def startNewGame(myHand, dealer, deck, games, window):
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
    if games > 0:
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
        self.games = 0

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
                                    command=lambda: startNewGame(self.myHand, self.dealer, self.deck, self.games, self))
        self.newGameButton.grid(row=4, column=4)
        self.quitButton = Button(text= "Quit", padx=20, pady=20,
                                 command= lambda: quitWindow(self.window))
        self.quitButton.grid(row=4, column = 6)
        self.winnerLabel = Label(text="WINNER", bg="#D0F0C0", font=(14))
        self.loserLabel = Label(text="LOSER", bg="#FA8072", font=(14))

        startNewGame(self.myHand, self.dealer, self.deck, self.games, self)

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
        self.games += 1

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
        self.winnerLabel.config(text="", bg="#000000")
        self.loserLabel.config(text="", bg="#000000")

    def ML(self):
        self.window.mainloop()


#playBlackJackGUI(1,20)
simulation(100000,5,104)
#simulation(2,5,104)
