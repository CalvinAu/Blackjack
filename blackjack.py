#===============================================================================
# Blackjack.py
# Calvin Au
# 7/25/13
#===============================================================================
import random
import time
class Deck(object):
    '''Represents a 52 card deck: 4 suits, 13 cards each'''
    def __init__(self):
        self.suit = ["Hearts", "Spades", "Clubs", "Diamonds"] #0 = Hearts, 3 = Diamonds
        self.rank = [None, 'Ace', '2', '3', '4', '5', '6', '7',
                      '8', '9', '10', 'Jack', 'Queen', 'King']
        self.order = [] #order of the cards, initialized by Deck.shuffle
        for suit in self.suit:
            for rank in range(1, len(self.rank)):
                self.order += [[suit, self.rank[rank]]] #Card id: [suit, rank]
    
    def shuffle(self):
        '''Shuffles the deck by randomizing the order of the cards'''
        random.shuffle(self.order)
        
        
class Blackjack(Deck):
    '''Represents a game of blackjack'''
    def __init__(self):
        Deck.__init__(self)
        self.dealer = [] #represents cards for dealer
        self.player = [] #represents cards for player
        self.points = {} #Dictionary that hold point values
        for rank in range(2, 11):
            self.points[str(rank)] = rank
        faces = {'Ace(1)':1, 'Ace(11)':11, 'Jack':10, 'Queen':10, 'King':10}
        self.points.update(faces)
        self.userWins = 0
        self.dealerWins = 0
    
    def deal(self, player):
        player += [self.order[0]]
        self.order.remove(self.order[0])

        
    def calcPoints(self, person):
        '''Calculates the points in a player's hand'''
        points = 0
        for card in person:
            points += self.points[card[1]]
        return points
    
    def bust(self, player):
        '''Returns whether or not the player is over 21'''
        points = self.calcPoints(player)
        if points <= 21:
            return False
        else:
            return True
        
    def checkAce(self, player):
        time.sleep(1)
        if player == self.player and self.player[-1][1] == 'Ace':
                while True:
                    aceInput = raw_input("Do you want your ace to be a 1 or 11? (1/11): ")
                    if aceInput == '1':
                        self.player[-1][1] = 'Ace(1)'
                        break
                    elif aceInput == '11':
                        self.player[-1][1] = 'Ace(11)'
                        break
                    else:
                        print "You did not enter a valid input"
        if player == self.dealer:
            for card in self.dealer:
                if card[1] == 'Ace':
                    card[1] = 'Ace(11)'
                if card[1] in ['Ace', 'Ace(1)', 'Ace(11)'] and self.calcPoints(self.dealer) > 21:
                    card[1] = 'Ace(1)'
        
    def dealerAI(self):
            while self.calcPoints(self.dealer) < 17:
                self.deal(self.dealer)
                print "The dealer was dealt a %s of %s" % (self.dealer[-1][1], self.dealer[-1][0])
                self.checkAce(self.dealer)
                time.sleep(1)
            if self.calcPoints(self.dealer) > 21:
                self.checkAce(self.dealer)
            if self.calcPoints(self.dealer) == 17:
                hitChance = random.randint(0, 1)
                if hitChance == 0:
                    return
                else:
                    self.deal(self.dealer)
                    time.sleep(1)
                    print "The dealer was dealt a %s of %s" % (self.dealer[-1][1], self.dealer[-1][0])
                    self.checkAce(self.dealer)
                    return

    
    def __str__(self, end = False): #boolean end = true displays entire summary
        '''String formatting for the Blackjack object
        
        Displays game summary'''
        summary = 'Current Summary:\n'
        if end == True:
            summary += "Dealer's hand: "
            for card in self.dealer:
                summary += "%s of %s, " % (card[1], card[0])
            summary += "\n\t Points: " + str(self.calcPoints(self.dealer))
        else:
            summary += "Dealer's hand: [Unknown Card], "
            for card in self.dealer:
                if card == self.dealer[0]: #omits hidden first card
                    continue
                summary += "%s of %s, " % (card[1], card[0])
            #summary += "\n\tPoints showing: " + str(self.calcPoints(self.dealer) - self.points[self.dealer[0][1]])
        summary += "\nYour hand: "
        for card in self.player:
            summary += "%s of %s, " % (card[1], card[0])
        summary += "\n\tPoints: " + str(self.calcPoints(self.player))
        return summary
        
    def playGame(self):
        '''Executes the game'''
        self.dealer, self.player = [], [] #resets hands
        self.shuffle()
        for times in range(2):
            self.deal(self.player)
            print "You were dealt the %s of %s" % (self.player[-1][1], self.player[-1][0])
            self.checkAce(self.player) #Checks for aces (1/11 to choose)
            time.sleep(1)
            self.deal(self.dealer)
            if times == 1:
                print "Dealer was dealt the %s of %s" % (self.dealer[-1][1], self.dealer[-1][0]) #Only prints face up card
            else:
                print "Dealer was dealt a card (face down)"
            self.checkAce(self.dealer)
            time.sleep(1)
        print self
        while True:
            userInput = raw_input("Hit or Stay? (Hit/Stay): ").lower()
            while not userInput in ['hit', 'stay']:
                print "You did not enter a valid input"
                userInput = raw_input("Hit or Stay? (Hit/Stay): ").lower()
            if userInput == 'hit':
                self.deal(self.player)
                print "You were dealt the %s of %s" % (self.player[-1][1], self.player[-1][0])
                self.checkAce(self.player)
                time.sleep(1)
                print self
                time.sleep(1)
                if self.bust(self.player) == True:
                    print "You busted.  Dealer wins"
                    self.dealerWins += 1
                    time.sleep(2)
                    return
            else:
                break
        self.dealerAI()
        time.sleep(1)
        print self.__str__(end=True)
        time.sleep(1)
        dealerPoints = self.calcPoints(self.dealer)
        userPoints = self.calcPoints(self.player)
        if dealerPoints > 21:
            print "The dealer busted.  You win."
            self.userWins += 1
        elif dealerPoints < userPoints:
            print "You win."
            self.userWins += 1
        elif dealerPoints == userPoints:
            print "Tie game."
        else:
            print "You lose."
            self.dealerWins += 1
        time.sleep(2)
        return
            
        
if __name__ == '__main__':
    print "Welcome to Blackjack"
    blackjack = Blackjack()
    while True:
        print "Your wins: %s \t\t Dealer wins: %s" % (blackjack.userWins, blackjack.dealerWins)
        userInput = raw_input("Would you like to play a game? (Y/N): ")
        if not userInput in ['Y','N']:
            print "You did not enter a valid input"
        elif userInput == 'N':
            break
        else:
            blackjack.playGame()
            
