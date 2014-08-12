#===============================================================================
# deck.py
# Calvin Au
# 8/5/2014
#===============================================================================
import random

class Deck(object):
    '''Represents a 52 card deck: 4 suits, 13 cards each
    
       Order of the cards defaults to Hearts, Spades, Clubs, Diamonds, each in
       sequential order from Ace->King.  The deck is reordered by Deck.shuffle
       
       Invariant: Deck always has 52 cards, 1 for each combination of suit and rank'''
    def __init__(self):
        self.suit = ["Hearts", "Spades", "Clubs", "Diamonds"] #0 = Hearts, 3 = Diamonds
        self.rank = ['Ace', '2', '3', '4', '5', '6', '7',
                      '8', '9', '10', 'Jack', 'Queen', 'King']
        self.order = []
        for suit in self.suit:
            for rank in self.rank:
                self.order += [[suit, rank]] #Card id: [suit, rank]
    
    def shuffle(self):
        '''Shuffles the deck by randomizing the order of the cards'''
        random.shuffle(self.order)