#===============================================================================
# blackjack.py
# Calvin Au
# 8/5/2014
#===============================================================================
import random
import time
import deck
        
class Blackjack(deck.Deck):
    '''Represents a game of blackjack'''
    def __init__(self):
        super(Blackjack, self).__init__()
        self.dealer = [] #represents cards for dealer
        self.player = [] #represents cards for player
        self.points = {} #Dictionary that hold point values
        for rank in range(2, 11):
            self.points[str(rank)] = rank
        faces = {'Ace (1)':1, 'Ace (11)':11, 'Jack':10, 'Queen':10, 'King':10}
        self.points.update(faces)
        self.userWins = 0
        self.dealerWins = 0
    
    def deal(self, person):
        '''Deals the card off the top of the deck to the specified person'''
        person += [self.order[0]]
        
        #Aces default to an 11 point value (soft ace), will change to 1 if
        #person's points go over 21 (through checkAce)
        if person[-1][1] == 'Ace': person[-1][1] = 'Ace (11)'
        
        #To maintain Deck invariant, move card to the back of the deck, then
        #remove it from the top
        self.order += [self.order[0]]
        self.order.remove(self.order[0])

        
    def calcPoints(self, person):
        '''Calculates the points in a person's hand by finding the point values
           of the ranks in the points dictionary'''
        points = 0
        for card in person:
            #print 'Getting value of %s\n' % (card[1])
            points += self.points[card[1]] #Card id: [suit, rank]
        return points
    
    def bust(self, person):
        '''Returns whether or not the person busts (points are over 21)'''
        points = self.calcPoints(person)
        if points <= 21: return False
        else: return True
        
    def checkAce(self, person):
        '''Checks if an Ace (11) busts a person.  If it does, automatically
           change Ace (11) to Ace (1)'''
        for card in person:
            if card[1] == 'Ace (11)' and self.calcPoints(person) > 21:
                card[1] = 'Ace (1)'
        
    def dealerAI(self):
        '''Simulates dealer decisions based upon the player's hand'''
        while self.calcPoints(self.dealer) < 17:
            self.deal(self.dealer)
            print "The dealer was dealt a %s of %s" % (self.dealer[-1][1], self.dealer[-1][0])
            self.checkAce(self.dealer)
            time.sleep(1)
        if self.calcPoints(self.dealer) > 17:
            if self.calcPoints(self.dealer) > self.calcPoints(self.player): return
            elif self.calcPoints(self.dealer) == self.calcPoints(self.player):
                hitChance = random.randint(0,1) #50% chance dealer will try to win
                if hitChance == 0: self.deal(self.dealer)
                else: return
        else:
            self.deal(self.dealer)
            time.sleep(1)
            print "The dealer was dealt a %s of %s" % (self.dealer[-1][1], self.dealer[-1][0])
            self.checkAce(self.dealer)
            return

    
    def __str__(self, end = False): #if end = true: displays entire summary
        '''String formatting for the Blackjack object
           Displays game summary'''
        summary = 'Current Summary:\n'
        if end == True:
            summary += "Dealer's hand: "
            for card in self.dealer:
                summary += "%s of %s, " % (card[1], card[0])
            summary += "\nDealer's points: " + str(self.calcPoints(self.dealer))
        else:
            summary += "Dealer's hand: [Unknown Card], "
            for card in self.dealer:
                if card == self.dealer[0]: #omits hidden first card
                    continue
                summary += "%s of %s, " % (card[1], card[0])
        summary += "\nYour hand: "
        for card in self.player:
            summary += "%s of %s, " % (card[1], card[0])
        summary += "\nYour points: " + str(self.calcPoints(self.player))
        return summary
        
    def playGame(self):
        '''Executes the game'''
        self.dealer, self.player = [], [] #clears hands
        self.shuffle()
        for times in range(2):
            self.deal(self.player)
            print "You were dealt the %s of %s" % (self.player[-1][1], self.player[-1][0])
            self.checkAce(self.player) #Checks for Ace
            time.sleep(1)
            self.deal(self.dealer)
            if times == 1: #Only prints face up card on the 2nd time
                print "Dealer was dealt the %s of %s\n" % (self.dealer[-1][1], self.dealer[-1][0]) 
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
            print '\n'
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
                    time.sleep(1)
                    return
            else:
                time.sleep(1)
                break
        self.dealerAI()
        time.sleep(1)
        print self.__str__(end=True)
        time.sleep(1)
        dealerPoints = self.calcPoints(self.dealer)
        userPoints = self.calcPoints(self.player)
        if dealerPoints > 21:
            print "The dealer busted.  You win.\n"
            self.userWins += 1
        elif dealerPoints < userPoints:
            print "You win.\n"
            self.userWins += 1
        elif dealerPoints == userPoints:
            print "Tie game.\n"
        else:
            print "You lose.\n"
            self.dealerWins += 1
        time.sleep(2)
        return