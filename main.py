# Kyle Breen-Bondie - Final Project Blackjack Simulator
import random

class Card():
    suit = ""      #suit
    rank = 0       #card number or face
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
    deck = []                      #list of card objects that are to be drawn
    discard = []                   #list of card objects that were drawn
    cardsInDeck = 0                #count of cards still in deck- unnecessary and can use length instead
    cardsInDiscard = 0             #count of cards in discard- same as above

    def __init__(self):
        self.deck = []
        self.discard = []
        suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
        rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

        for s in suits:
            for r in rank:
                self.deck.append(Card(s, r))
                self.cardsInDeck += 1

    def shuf(self):     #shuffles current deck
        random.shuffle(self.deck)

    def draw(self):
        drawnCard = self.deck.pop()
        self.discard.append(drawnCard)
        self.cardsInDeck -= 1
        self.cardsInDiscard += 1
        return(drawnCard)

    def lookAtDiscard(self):
        for c in self.discard:
            print(c)

class Hand():
    hand = []              #list of card objects
    total = 0              #total value in blackjack
    numOfAces = 0          #counts number of aces
    numOfAcesAs1 = 0       #counts aces that are used as a value of 1 (to prevent bust)

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
        newCard = Deck.draw()
        self.hand.append(newCard)

        if newCard.rank == "Ace":
            self.numOfAces += 1

        self.total = self.total + newCard.value

        if self.numOfAcesAs1 < self.numOfAces:
            if self.isBust():
                self.total = self.total - 10
                self.numOfAcesAs1 += 1

        if self.isBust():
            print("BUST!")

    def showHand(self):
        for c in self.hand:
            print(c)

    def getTotal(self):
        return self.total

    def isBust(self):
        if self.total > 21:
            return True
        else:
            return False

deck1 = Deck()
deck1.shuf()
myhand = Hand()
dealer = Hand()
myhand.draw1(deck1)
myhand.draw1(deck1)
dealer.draw1(deck1)
dealer.draw1(deck1)
myhand.showHand()
print(myhand)
print(myhand < dealer)