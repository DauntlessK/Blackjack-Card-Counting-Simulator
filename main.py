# Kyle Breen-Bondie - Final Project Blackjack Simulator

class Card():
    suit = ""
    value = ""

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def __str__(self):
        return (f'{self.get_value()} of {self.get_suit()}')

def create_deck():
    deck = []
    suits = ["Hearts", "Clubs", "Spades", "Diamonds"]
    values = [2,3,4,5,6,7,8,9,10,"Jack","Queen","King","Ace"]

    for s in suits:
        for v in values:
            deck.append(Card(s,v))

    print(deck[10])

create_deck()