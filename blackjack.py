import random

# setting string and value of cards to suits and rank variables.
# dictionary objects created to assign numerical value to strings
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# while game is playing
playing = True

class Cards:

    # card class where objects are assigned a suit and rank
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    # deck will hold card objects
    def __init__(self):
        self.deck = [] 
        for suit in suits:
            for rank in ranks:
                self.deck.append(Cards(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

class Hand:

    #card to calculate value of hand

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    # adjusting the value of ace as needed from 11 to 1
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self,total=100):
        self.total = total
        self.bet = 0

    def take_bet(self):
        while True:
            try:
                bet_amount = int(input('How much would you like to bet? '))
                if bet_amount <= self.total:
                    self.bet = bet_amount
                    break
                else:
                    print('Sorry, you do not have enough chips')
            except:
                print('Please enter a valid integer for your bet amount.')


    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def hit(deck,hand):
        one_card = deck.deal()
        hand.add_card(one_card)
        hand.adjust_for_ace

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input('Hit or Stand? Enter h or s: ')

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player Stands. Dealer's Turn")
            playing = False
        else:
            print('Sorry, please enter h or s.')
            continue
        break

def show_some(player,dealer):

    # Do not show the dealer's first card which would be at dealer.cards[0]
    # print the 2nd card which is at dealer.cards[1]
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    #show both of the player's cards/hand
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)

def show_all(player,dealer):

    # show all dealer's cards
    print("\n Dealer's hand: ")
    for card in dealer.cards:
        print(card)
    #calculating and display value of dealer's hand
    print(f"The value of the Dealer's hand is: {dealer.value}")
    
    #show all player's cards
    print("\n Player's hand: ")
    for card in player.cards:
        print(card)
    #calculating and display value of player'shand
    print(f"The value of the Player's hand is: {player.value}")

def player_busts(player,dealer,chips):
    print('PLAYER BUSTED! DEALER WINS!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('PLAYER WINS!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print('DEALER WINS!')
    chips.lose_bet()
    
def push(player,dealer):
    print('Dealer and player tie! PUSh')

while True:

    print('WELCOME TO BLACKJACK')

    # create and shuffle deck then deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # setting up player chips
    player_chips = Chips()
    player_chips.take_bet()

    # show cards but keeping one dealer card hidden
    show_some(player_hand,dealer_hand)

    while playing:

        # Asking player to hit or stand
        hit_or_stand(deck,player_hand)

        # show cards but keep one dealer card hidden
        show_some(player_hand,dealer_hand)

        # if plater's hand exceeds 21, run player_busts() and break loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

        # if player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # show all cards
        show_all(player_hand,dealer_hand)

        # winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
                
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
                
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
                
        else:
            push(player_hand,dealer_hand)

        # keeping player aware of their chips
        print(f'\n Player total chips are at: {player_chips.total}')

        # Ask if player wants to play again
        new_game = input('Would you like to play anther hand? y or n: ')

        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print('Thanks for playing, see you again!')
            break
