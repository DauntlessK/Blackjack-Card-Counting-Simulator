# Kyle Breen-Bondie - Final Project Blackjack Simulator
import random

class Card():
    suit = ""      #suit
    rank = 0       #card number or face
    value = 0      #number value in blackjack
    altvalue = 0   #alt value for ace

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if isinstance(rank, int):
            self.value = rank
        elif rank == "Ace":
            self.value = 11
            self.altvalue = 1
        else:
            self.value = 10

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return (f'{self.get_rank()} of {self.get_suit()}')

class Deck():

    def __int__(self):
        deck = []
        discard = []
        suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
        rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]

        for s in suits:
            for r in rank:
                deck.append(Card(s, r))


    def shuffle(self):     #shuffles current deck
        random.shuffle(self.deck)
        print(self.deck[0])

    def draw(self):
        draw = self.deck.pop()
        self.discard.append(draw)
        self.deck.remove[0]
        print(draw)

deck1 = Deck()
deck1.shuffle()
#deck1.draw()