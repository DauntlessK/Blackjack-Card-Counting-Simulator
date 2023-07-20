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

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return (f'{self.get_rank()} of {self.get_suit()}')

class Deck():
    deck = []
    discard = []
    cardsInDeck = 0
    cardsInDiscard = 0

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
    hand = []
    total = 0
    numOfAces = 0
    numOfAcesAs1 = 0

    def draw1(self, Deck):
        newCard = Deck.draw()
        self.hand.append(newCard)

        if newCard.rank == "Ace":
            self.numOfAces =+ 1

        self.total = self.total + newCard.value

        #if self.numOfAces == 1 and self.total > 21:
        #    self.total = self.total - 10
        #elif self.numOfAces == 2 and self.total > 21:  #technically don't need this for final
        #    print("NEED TO FIGURE LOGIC OUT")          #but additional logic needed to change multiple aces from 11 to 1

        if self.numOfAcesAs1 < self.numOfAces:
            if self.total > 21:
                self.total = self.total - 10
                self.numOfAcesAs1 += 1
            #for x in range (self.numOfAces):


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
myhand.draw1(deck1)
myhand.draw1(deck1)
myhand.draw1(deck1)
myhand.draw1(deck1)
myhand.draw1(deck1)
myhand.draw1(deck1)
myhand.showHand()
print(myhand.getTotal())