#===============================================================================
# Deck.py
# Calvin Au
# 8/5/2014
#===============================================================================
import blackjack

if __name__ == '__main__':
    print "Welcome to Blackjack"
    game = blackjack.Blackjack()
    while True:
        print "Your wins: %s \t\t Dealer wins: %s" % (game.userWins, game.dealerWins)
        userInput = raw_input("Would you like to play a game? (Y/N): ").upper()
        if not userInput in ['Y','N']:
            print "You did not enter a valid input"
        elif userInput == 'N':
            break
        else:
            print '\n'
            game.playGame()