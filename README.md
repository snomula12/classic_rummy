# classic_rummy
This is small game i created using python and jquery

Requirments to run this project.

1. Virtual Environment
1. Python 
2. Django 

Please follow the link to setup django
https://www.djangoproject.com/download/

Once you have this setup, please download the django project into the virtual environment.

Then start the django server
  1. cd classic_rummy
  2. Python manage.py runserver
  3. In a web brower please visit http://127.0.0.1:8000/classic/rummy/


I tried to implement the first 2 Challenges
  1. Game Mechanics
  2. Goal Detection

It took me 5-6 hours to implement this whole project and currenlty there might be some bugs.

Known Bugs:
1. There are some issues with how the remainging cards deck is handled and how discard cards should go back into the deck.


How to Play:
  You will be playing as Player-you and you will have first turn. 
  There are two option for a user, Draw a new card or Get the open card.
  Once you draw a card you need to discard a one card.


Child Rummy is a simple variation of [Rummy](http://en.wikipedia.org/wiki/Rummy):

- Each player is dealt 7 cards from a 52 card deck (no jokers)
- A player wins by being the first to have both a 
  3-of-a-kind (same card value, different suits) and a 4-card-run (same suit,
  incrementing card value) in their hand, where the cards used for each goal are
  mutually exclusive.
- After dealing, the remaining cards are stacked face-down (called
  the stack), and the top card on the stack is turned face-up next to the stack,
  (beginning the discard pile).
- Play is round robin, with each player's turn consists of picking a card from
  either the top of the stack or the top of the discard pile, adding the card
  to their hand, and then discarding to the top of the discard pile.
- A player can only declare they win during their turn, and must still discard
  at the end of their turn and still have a winning hand.
- If the stack is empty immediately after a player picks a card, before the 
  player can discard the discard pile is shuffled and becomes the stack.

