from classes import *
import os
import platform

# MOVE VALIDATION FUNCTIONS

def attack_valid(card, table):
    if len(table) == 0 and isinstance(card, Card):
            return True
    if isinstance(card, Card):  # Because we are returning an int - 0 to make bita or to take, which doesn't have a val
        if card.val in [card.val for card in table]:
                return True
        else:
                return False
    elif card == 0:
        if len(table) != 0:
            return True
        else:
            return False
      
def defense_valid(card, table, trump):
    if isinstance(card, Card):
        if table[-1].suit == trump.suit:
            if card.val > table[-1].val and card.suit == table[-1].suit:
                    return True
            else:
                    return False
        else:
            if card.val > table[-1].val and card.suit == table[-1].suit or card.suit == trump.suit:
                return True
            else:
                return False
    elif card == 0:
        return True
    
    # elif card == "exit":
    #     return False



# PLAYER WITH THE SMALLEST TRUMP CARD GOES FIRST

def goesFirst(player1, computer, trump):
    playertrumps = [x for x in player1.hand if x.suit == trump.suit]
    comptrumps = [x for x in computer.hand if x.suit == trump.suit]
    
    if not playertrumps and comptrumps:
        return 2
    elif not comptrumps and playertrumps:
        return 1
    elif not comptrumps and not playertrumps:
        return 0
    elif playertrumps and comptrumps:
        playertrumps.sort(key = lambda x: x.val)
        comptrumps.sort(key = lambda x: x.val)
        if playertrumps[0].val < comptrumps[0].val:
            return 1
        else:
            return 2


# GAME UI

def UI(attacker, defender, trump, round):
    global mode
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("WELCOME TO THE GAME OF DURAK\n")
    print("TRUMP CARD:")
    trump.show()
    if not mode:            #TEST MODE
        print(f"Attacker Hand: {attacker.name}")
        attacker.showHand(trump)
        print(f"Defender Hand: {defender.name}")
        defender.showHand(trump)
    else:       #GAME MODE
        if isinstance(attacker, Player):
            print(f"Your Hand: {attacker.name}")
            attacker.showHand(trump)
            print(f"Computer's hand: {len(defender.hand)} cards")
        else:
            print(f"Your Hand: {defender.name}")
            defender.showHand(trump)
            print(f"Computer's hand: {len(attacker.hand)} cards")
    print("Cards in the Deck")
    print(len(deck.cards))
    print("Table")
    print("") if len(round) == 0 else [card.show() for card in round]
   
if platform.system() == "Windows":
    os.system("cls")
else:
    os.system("clear")         
print("WELCOME TO THE GAME OF DURAK")
print("FOR TEST MODE ENTER 0. FOR GAME MODE ENTER 1.")
mode = int(input())
print("PLEASE ENTER YOUR NAME")
name = input()

while True:

    # INITIALIZE THE GAME

    Game = True
    Quit = False
    round = []      #CARDS ON THE TABLE
    deck = Deck()
    deck.shuffle()
    player1 = Player(name)
    computer = Computer()
    for _ in range(0, 6):       #INITIALIZE HANDS
        player1.draw(deck)
        computer.draw(deck)
    trump = deck.trump()            #TRUMP CARD
    attacker = player1      #default values
    defender = computer
    goesfirst = goesFirst(player1, computer, trump) #determine who goes first
    if goesfirst == 0:   #no one has a trump, start over  
        continue
    elif goesfirst == 2:
        attacker, defender = defender, attacker
        



    # GAME LOOP

    while Game:

    
        # TAKING CARDS FROM THE DECK
        while len(defender.hand) < 6:       # If it was bita, the roles switched, and attacker is now defender, taking first.  
            if deck.cards:                  # If it was taken, the defender has > 6 cards, so the attacker takes, defender doesn't
                defender.draw(deck)         # # If it was taken, but the defender has <= 6 cards, then the deck is empty
            else: 
                break 
        while len(attacker.hand) < 6:
            if deck.cards:
                attacker.draw(deck)
            else:
                break
                        
        
        # ROUND LOOP
        
        while True:

            #CHECK FOR THE WINNER AND AUTOMATIC BITA FROM THE PREVIOUS ROUND
            
            if len(attacker.hand) == 0 and len(deck.cards) == 0: 
                Game = False
                if len(defender.hand) == 0: #DRAW
                    Winner = 0
                Winner = attacker
                break
            elif len(round) == 12:          #CANNOT ATTACK WITH MORE THAN 6 CARDS
                round.clear()
                attacker, defender = defender, attacker 
                break
            elif len(attacker.hand) == 0 and len(deck.cards) != 0:  #BITA IF ATTACKER HAS NO CARDS LEFT
                round.clear()
                attacker, defender = defender, attacker 
                break
            elif len(attacker.hand) == 1 and len(deck.cards) == 24: # FIRST ROUND ONLY 5 CARDS CAN BE PLAYED
                round.clear()
                attacker, defender = defender, attacker 
                break

            if len(defender.hand) == 0 and len(deck.cards) == 0:
                Game = False
                Winner = defender
                break
            elif len(defender.hand) == 0 and len(deck.cards) != 0:
                round.clear()
                attacker, defender = defender, attacker # ATTACKER AND DEFENDER SWAP
                break
            
            
            UI(attacker, defender, trump, round)

            #ATTACKER'S MOVE
            if isinstance(attacker, Computer):  #IF THE ATTACKER IS COMPUTER
                move = attacker.attack(round, trump, deck, defender)

            else:
                print("Your Move. Attack!")
                move = attacker.play()
                
                while not attack_valid(move, round): #MOVE VALIDATION FOR HUMAN PLAYER
                    if isinstance(move, Card):
                        attacker.takeCard(move)                 # TAKE BACK THE MOVE AND MAKE ANOTHER
                        UI(attacker, defender, trump, round)
                        print("Please enter a valid card")
                        move = attacker.play()
                    else:
                        if move == "inputtoohigh":          #NON INTEGER AND LARGE INPUTS WILL RETURN NONETYPE VALUE, WHICH IS "FALSE"
                            UI(attacker, defender, trump, round)
                            print(f"Please enter an input between 1 and {len(attacker.hand)}")
                            move = attacker.play()
                        elif move == "inputnondigit":
                            UI(attacker, defender, trump, round)
                            print(f"Please enter an INTEGER input")
                            move = attacker.play()
                        elif move == 0:
                            UI(attacker, defender, trump, round)
                            print("You can't pass on the first move. Please enter another move")
                            move = attacker.play()
                        elif move == "exit":
                            UI(attacker, defender, trump, round)
                            exitinput = input("Are you sure you want to exit? (Y/N)")
                            if exitinput.upper() == "Y":
                                Game = False
                                Quit = True
                                break
                            else: 
                                UI(attacker, defender, trump, round)
                                print("Your Move")
                                move = attacker.play()
                            
                if Game == False:
                    break        
                
            if move == 0:           # BITA
                round.clear()
                attacker, defender = defender, attacker # ATTACKER AND DEFENDER SWAP
                break
            

            round.append(move)      # ONCE THE MOVE IS VALID
            UI(attacker, defender, trump, round)

            # DEFENDERS MOVE 
            if isinstance(defender, Computer):
                move = defender.defend(round, trump, deck)

                if move == 0:   # TAKE THE CARDS
                    print (f"You can play {len(defender.hand) - 1} vdoqonku cards")
                    print("To pass enter 0. Otherwise enter cardnumbers with space inbetween")
                    vdoqonkulist = attacker.vdoqonku()
                    while True:
                        if len(vdoqonkulist) > len(defender.hand) - 1:
                            UI(attacker, defender, trump, round)
                            print (f"You can only play {len(defender.hand) - 1} vdoqonku cards")
                            vdoqonkulist = attacker.vdoqonku()
                        elif len(vdoqonkulist) == 1 and vdoqonkulist[0] == 0:
                            break
                        else:
                            for card in vdoqonkulist:
                                if not attack_valid(card, round):
                                    UI(attacker, defender, trump, round)
                                    print("Your Input wasn't valid", end = ":") 
                                    card.show()
                                    vdoqonkulist = attacker.vdoqonku()
                                    break
                            else:
                                round = round + vdoqonkulist
                                for i in vdoqonkulist:
                                    attacker.hand.remove(i)
                                break

                    for card in round:
                        defender.takeCard(card)
                    round.clear()   # CLEAR THE TABLE
                    break
            
            else:
                print("Your Move. Defend!")
                move = defender.play()  #EITHER 0 OR CARD OBJECT OR EXIT DEPENDING ON THE INPUT
            
                while not defense_valid(move, round, trump):   # TAKE BACK THE MOVE AND MAKE ANOTHER
                    if isinstance(move, Card):
                        defender.takeCard(move)
                        UI(attacker, defender, trump, round)
                        print("Please enter a valid card")
                        move = defender.play()
                    else:
                        if move == "inputtoohigh":          #NON INTEGER AND LARGE INPUTS WILL RETURN NONETYPE VALUE, WHICH IS "FALSE"
                            UI(attacker, defender, trump, round)
                            print(f"Please enter an input between 1 and {len(defender.hand)}")
                            move = defender.play()
                        elif move == "inputnondigit":
                            UI(attacker, defender, trump, round)
                            print(f"Please enter an INTEGER input")
                            move = defender.play()
                        elif move == "exit":
                            UI(attacker, defender, trump, round)
                            exitinput = input("Are you sure you want to exit? (Y/N)")
                            if exitinput.upper() == "Y":
                                Game = False
                                Quit = True
                                break
                            else: 
                                UI(attacker, defender, trump, round)
                                print("Your Move")
                                move = defender.play()
            
                if Game == False:
                    break
                
                if move == 0:   # TAKE THE CARDS
                    for card in round:
                        defender.takeCard(card)
                    round.clear()   # CLEAR THE TABLE
                    vdoqonku = attacker.vdoqonku(round, trump, deck, defender)
                    round += vdoqonku
                    if len(round) > 0:
                        UI(attacker, defender, trump, round)
                        print("Press enter to take computer's extra/vdoqonku cards:")
                        input()
                        for card in round:
                            defender.takeCard(card)
                        round.clear()   # CLEAR THE TABLE
                    break
            
            round.append(move)  # ONCE THE MOVE IS VALID

    if  Quit == False: 
        if Winner == 0:
             print(f"GAME IS OVER. IT'S A DRAW!")  
        else:           
            print(f"GAME IS OVER. {Winner.name} wins")   
        again = input("Do you want to play again? (Y/N)")
        if again.upper() == "N":
            break
    else:
        print(f"GAME IS OVER.")   
        again = input("Do you want to play again? (Y/N)")
        if again.upper() == "N":
            break
                           
    


