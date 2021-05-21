import random

class Card(object):
    card_dict = {6:6, 7:7, 8:8, 9:9, 10:10, 11:"J", 12:"Q", 13:"K", 14:"A"}
    
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
    
    def show(self):
        print(f"{self.card_dict[self.val]} {self.suit}")

    def __radd__(self, other):      #We need this when calculating the sum of the cards on the table
        return other + self.val

class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        for suit in ["♠", "♣", "♦", "♥"]:
            for v in range(6, 15):
                self.cards.append(Card(suit, v))

    def show(self):
        for card in self.cards:
            card.show()
    
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            rand = random.randint(0, i)
            self.cards[i], self.cards[rand] = self.cards[rand], self.cards[i]

    def draw(self):
        return self.cards.pop()

    def trump(self):
        return self.cards[0]


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    
    def draw(self, deck):
        self.hand.append(deck.draw())
    
    def showHand(self, trump):
        self.sortHand(trump)
        i = 1
        for card in self.hand: 
            print(i, end = ":  ") 
            i += 1
            card.show()
    
    def play(self):
        userinput = input()
        if userinput.isdigit():     #CHECK FOR ACCIDENTAL NON-INTEGER INPUTS
            cardnumber = int(userinput)
            if cardnumber > len(self.hand): #CHECK FOR ACCIDENTAL INPUTS EXCEEDING CARDS IN THE HAND
                return "inputtoohigh"    
            else: 
                if cardnumber == 0:
                    return 0
                else:
                    return self.hand.pop(cardnumber - 1)
        else:
            if userinput == "exit":
                return "exit"
            else: 
                return "inputnondigit"

    def vdoqonku(self):       #THIS METHOD IS ONLY CALLED WHEN THE OPPOSITION IS DEFENDING
        vdoqonkulist = list(map(int, input().strip().split()))
        cardslist = []
        for i in vdoqonkulist:
            if i == 0:
                cardslist = []
                cardslist.append(0)
                return cardslist
            else:
                cardslist.append(self.hand[i - 1])
        return cardslist

    def sortHand(self,trump):
        suits = {'♠':[], "♣":[], "♥":[], "♦":[]}
        for i in self.hand:
            if i.suit == '♠':
                suits['♠'].append(i)
            elif i.suit == "♣":
                suits['♣'].append(i)
            elif i.suit == "♥":
                suits['♥'].append(i)
            elif i.suit == "♦":
                suits['♦'].append(i)
        suits['♠'].sort(key = lambda card: card.val)
        suits['♣'].sort(key = lambda card: card.val)
        suits['♥'].sort(key = lambda card: card.val)
        suits['♦'].sort(key = lambda card: card.val)
    

        self.hand = suits.pop(trump.suit) 
        for suit in suits:
            self.hand += suits[suit]
        

    def takeCard(self, card):
        self.hand.append(card)



class Computer(object):
    def __init__(self):
        self.name = "Computer"
        self.hand = []
        self.tableunique = []
    
    def showHand(self, trump):
        i = 1
        for card in self.hand: 
            print(i, end = ":  ") 
            i += 1
            card.show()
        
    
    def draw(self, deck):
        self.hand.append(deck.draw())
    
    ############################################ COMPUTER AI ###########################################################
    def attack(self, table, trump, deck, defender):  
        smallest = Card("hearts", 15) #fictitious card with largest value
        smallesttrump = Card("hearts", 15) #fictitious trump card
        flag = 0
        trumpflag = 0
        
        if len(table) == 0: #THE FIRST MOVE
            self.tableunique = []        #reset the list of the unique cards on the table
            for card in self.hand:
                if card.suit != trump.suit and card.val < smallest.val: 
                        smallest = card
                        flag = 1
                elif card.suit == trump.suit and card.val < smallesttrump.val:
                        smallesttrump = card
            if flag == 1:
                self.tableunique.append(smallest.val)    #attackers first card is unique
                self.hand.remove(smallest)
                return smallest
            else:   #PLAYING TRUMP ON THE FIRST MOVE, BECAUSE ALL YOUR CARDS ARE TRUMPS. 
                self.tableunique.append(smallesttrump.val)    
                self.hand.remove(smallesttrump)
                return smallesttrump

        else:   #NOT THE FIRST MOVE
            if table[-1].val not in self.tableunique: #Each iteration of round we have a new table state. But the only new card value on the
                self.tableunique.append(table[-1].val) #table can be from the defender. Thus in each new round check the last card.
            
            for card in self.hand:  #what are the smallest non-trump and trump cards I can play?
                if card.val in self.tableunique and card.suit != trump.suit and card.val < smallest.val:
                    flag = 1
                    smallest = card
                elif card.val in self.tableunique and card.suit == trump.suit and card.val < smallesttrump.val:
                    trumpflag = 1
                    smallesttrump = card
            
            if flag == 0 and trumpflag == 1:    #If only trump, and deck not empty, and there are more than 6 cards 
                if  len(deck.cards) != 0:       #on the table with low average, you can play a trump lower than 9
                    if len(table) >= 6 and sum(table)/len(table) <= 9:
                        if smallesttrump.val < 9:
                            self.hand.remove(smallesttrump)
                            return smallesttrump
                        else: return 0
                    else: return 0
                        
                else:               #if deck is empty and opponent has less than 3 cards play the trump, if more than 3 cards,
                    if len(defender.hand) <= 3:    #play the trump if its lower than Jack.
                        self.hand.remove(smallesttrump)
                        return smallesttrump
                    else:
                        if smallesttrump.val <= 11:
                            self.hand.remove(smallesttrump)
                            return smallesttrump
                        else: return 0

            elif flag == 0 and trumpflag == 0:  #BITA
                return 0
            
                
            elif flag == 1:     #If you have a non trump card
                if  len(deck.cards) != 0:
                    if smallest.val < 13:   #DONT GO KING OR ACE IF THERE ARE CARDS IN THE DECK LEFT
                        self.hand.remove(smallest)   #AND YOU WILL MAKE THE OPPONENT TAKE ONLY <= 6 CARDS. OTHERWISE 
                        return smallest                #YOU CAN GO K OR A
                    else:
                        if len(table) >= 6:
                            self.hand.remove(smallest)              
                            return smallest 
                        else:
                            return 0
                else:                           #IF NO CARDS LEFT IN THE TABLE GO WHATEVER YOU CAN
                    self.hand.remove(smallest)
                    return smallest

        
    def defend(self, table, trump, deck):
            if self.sortHand()[table[-1].suit]:
                for i in self.sortHand()[table[-1].suit]:   #if you have a card with higher value and same suit than the attacking card
                    if i.val > table[-1].val:                #play that card. This includes defending against trumps.
                        self.hand.remove(i)
                        return i
                    
            if self.sortHand()[trump.suit] and table[-1].suit != trump.suit:  #if the attacking card isn't trump, and if you have a trump card
                if len(deck.cards) != 0:                                        #if there are cards left in the deck
                    if len(table) >= 6 and sum(table)/len(table) <= 10:
                        play = self.sortHand()[trump.suit][0]                     #if the number of cards on the table is more than six
                        self.hand.remove(play)                              #with their average lower than ten, beat with your smallest trump
                        return play
                    elif len(table) >= 6 and sum(table)/len(table) > 10:        #if their average is higher than ten, taking isn't catastrophic,
                        if  self.sortHand()[trump.suit][0].val <= 10:           #so only beat if the trump is smaller than ten, otherwise take
                            play = self.sortHand()[trump.suit][0]                         
                            self.hand.remove(play)                
                            return play
                        else:
                            return 0
                    elif len(table) < 6 and sum(table)/len(table) > 10:     #if the card average is more than 10 and number of cards is less than 6
                        if  self.sortHand()[trump.suit][0].val <= 8:        #it's okay to take, so only beat with trump <= 8
                            play = self.sortHand()[trump.suit][0]                     
                            self.hand.remove(play)               
                            return play
                        else:
                            return 0
                    elif len(table) < 6 and sum(table)/len(table) <= 10:        #even if the avg is less than ten, less than 6 cards is still not
                        if  self.sortHand()[trump.suit][0].val <= 10:           #catastrophic, so only beat if trump is <= 10
                            play = self.sortHand()[trump.suit][0]                          
                            self.hand.remove(play)                
                            return play
                        else:
                            return 0
                    3
                else: 
                    play = self.sortHand()[trump.suit][0]                          #trump, beat with the smallest trump. If it is a trump
                    self.hand.remove(play)                #you had to beat it with a higher card in the above loop
                    return play         
            else:
                return 0

    def vdoqonku(self, table, trump, deck, defender):
        vdoqonkulist = []
        for card in self.hand:
            if len(vdoqonkulist) <= len(defender.hand) - 1:
                if card.val <= 10 and card.suit != trump.suit and card.val in [card.val for card in table]:
                    self.hand.remove(card)
                    vdoqonkulist.append(card)
                elif card.val > 10 and card.suit != trump.suit and card.val in [card.val for card in table] and not len(deck.cards):
                    self.hand.remove(card)
                    vdoqonkulist.append(card)
        return vdoqonkulist
    
    ############################################ COMPUTER AI ###########################################################

    def sortHand(self):
        suits = {'♠':[], "♣":[], "♥":[], "♦":[]}
        for i in self.hand:
            if i.suit == '♠':
                suits['♠'].append(i)
            elif i.suit == "♣":
                suits['♣'].append(i)
            elif i.suit == "♥":
                suits['♥'].append(i)
            elif i.suit == "♦":
                suits['♦'].append(i)
        suits['♠'].sort(key = lambda card: card.val)
        suits['♣'].sort(key = lambda card: card.val)
        suits['♥'].sort(key = lambda card: card.val)
        suits['♦'].sort(key = lambda card: card.val) 
        return suits         
        
    def takeCard(self, card):
        self.hand.append(card)
        

  
        