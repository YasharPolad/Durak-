# Durak
Russian game of Durak against the computer. The computer AI is written by me. 
It features extensive validation checks for user "moves", and two modes of play - Test mode, 
where you can see the computer's "hand", and the game mode, where the computer's hand is hidden.
For more information about the game and the rules please visit https://en.wikipedia.org/wiki/Durak

# Gameplay
This is a command line game - you interact with the game by entering specific input. The game is 
played between a user and the computer AI. When you first start the game choose test mode (see computer's cards),
or gamemode, enter your name and start. Whether you are attacking or defending, you have 3 valid input options: 
0, a number not exceeding the number of cards in your hand, or exit.

Your hand is always sorted. First you have your trump cards sorted. Then each of the other suits, each sorted themselves.

Let's  assume this is your hand:
1:  K ♣
2:  10 ♠
3:  Q ♠
4:  A ♠
5:  7 ♥
6:  J ♥

If you are attacking, input 1 to play King of clubs, 2 to enter 10 of spades, 3 for Queen of spades and etc. Enter zero
if you don't have a card to attack (Rule of the game: you can only attack with the card values that are already on the table)
Enter exit if you want to exit the game. 

Additionally, if the computer takes the cards, you can play cards "Vdoqonku".
Basically, this means that you can make your opponent take extra cards. The values of these cards also must be among
the cards already played on the table. If your opponent has N cards left in her hands after the attack (Before she takes),
you can play N-1 vdoqonku cards. Just inpput the card numbers seperated with space. Otherwise, input 0 to pass.

If you are defending, playing cards and exiting will have the same rules. But 0 now will mean that you are taking 
the cards on the table. 











