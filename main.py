# Kyle Breen-Bondie - Final Project Blackjack Simulator
import random
import csv

class Card():
    """Single card object that holds a suit, a rank (card # or face), and a blackjack number value"""
    suit = ""      #suit
    rank = 0       #card number or str face
    value = 0      #number value in blackjack

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

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

    def __init__(self, betAmount):
        self.hand = []
        self.total = 0
        self.numOfAces = 0
        self.numOfAcesAs1 = 0
        self.betAmount = betAmount

    def __str__(self):
        toReturn = ""
        for c in range(len(self.hand)):
            if c != 0:
                toReturn += ", "
            toReturn += str(self.hand[c])
        return toReturn

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

    def draw1(self, Deck):
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


    def showHand(self):
        for c in self.hand:
            print(c)

    def getTotal(self):
        return self.total

    def isBust(self):
        """Checks if hand is bust and returns boolean"""
        if self.total > 21:
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
    if deck.cardCountOffset <= offSetThreshold:
        return bigBetAmount
    else:
        return minAmount

def getBlackJackAmount(initialBet):
    """Determines how much a blackjack pays."""
    return initialBet * 1.5    #set at 3 to 2

def getHitorStand(myHand, Dealer):
    """Determines, based on a table of what the dealer shows and the player has, whether to hit or stand
    Returns hit or stand string
    Table has 1 for hit and 0 for stand, dealer showing at top row, our total on side"""

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

    col4 = table[4]
    col5 = table[5]
    col16 = table[16]
    print(col16[8])

def playBlackJackLoop(numDecks, reshuf):
    """Loop that gets user input to continually play blackjack. Keeps track of wins, losses and ties for the session."""
    #reshuffle point should not be lower than 10
    deck = Deck(2, 20)
    myHand = Hand(0)
    dealer = Hand(0)
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
        myHand.newHand(deck, 2)
        dealer.newHand(deck, 1)
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
    twocard_winValues = ["Two Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_wins = 0
    twocard_lossValues = ["Two Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_losses = 0
    twocard_tieValues = ["Two Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    twocard_ties = 0
    threecard_winValues = ["Three Card Wins", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_wins = 0
    threecard_lossValues = ["Three Card Losses", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_losses = 0
    threecard_tieValues = ["Three Card Ties", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    threecard_ties = 0
    deck = Deck(numDecks, reshuf)
    money = 0     #starting money


    loops = 0
    while loops < gamesToSim:
        myHand = Hand(getBetAmount(deck))
        dealer = Hand(getBetAmount(deck))
        myHand.discardHand()      # ensures hand values are empty / reset
        dealer.discardHand()      # ensures dealer hand values are empty / reset

        myHand.newHand(deck, 2)
        dealer.newHand(deck, 2)
        handStartingValue = myHand.getTotal()

        while dealer.getTotal() <= 16:
            dealer.draw1(deck)

        #check if player won/lost/tied with 2 cards
        if (myHand.isBJ()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            money = money + getBlackJackAmount(myHand.betAmount)
        elif (dealer.isBust()) or (myHand.getTotal() > dealer.getTotal()):
            twocard_winValues[handStartingValue] += 1
            twocard_wins += 1
            money = money + myHand.betAmount
        elif myHand.getTotal() == dealer.getTotal():
            twocard_tieValues[handStartingValue] += 1
            twocard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            twocard_lossValues[handStartingValue] += 1
            twocard_losses += 1
            money = money - myHand.betAmount
        else:
            print("Error")

        myHand.draw1(deck)
        # check if player won/lost/tied with 3 cards
        if (myHand.isBust()):            #no matter what if player busts, it is a loss
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
        elif myHand.getTotal() > dealer.getTotal():
            threecard_winValues[handStartingValue] += 1
            threecard_wins += 1
        elif myHand.getTotal() == dealer.getTotal():
            threecard_tieValues[handStartingValue] += 1
            threecard_ties += 1
        elif myHand.getTotal() < dealer.getTotal():
            threecard_lossValues[handStartingValue] += 1
            threecard_losses += 1
        else:
             print("Error")

        if deck.needsReshuf:
            deck.reshuf()
        loops += 1

    #remove all 0-3 results from the lists
    del twocard_winValues[1:5]
    del twocard_lossValues[1:5]
    del twocard_tieValues[1:5]
    del threecard_winValues[1:5]
    del threecard_lossValues[1:5]
    del threecard_tieValues[1:5]

    #add the total for each list to the final cell
    twocard_winValues.append(twocard_wins)
    twocard_lossValues.append(twocard_losses)
    twocard_tieValues.append(twocard_ties)
    threecard_winValues.append(threecard_wins)
    threecard_lossValues.append(threecard_losses)
    threecard_tieValues.append(threecard_ties)

    #create betting info row
    betRow = ["Final $", money]

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerows([head_row])
        writer.writerows([twocard_winValues])
        writer.writerows([twocard_lossValues])
        writer.writerows([twocard_tieValues])
        writer.writerows([threecard_winValues])
        writer.writerows([threecard_lossValues])
        writer.writerows([threecard_tieValues])
        writer.writerows([betRow])


#playBlackJackLoop(2,20)
#simulation(1000,5,208)
getHitorStand()