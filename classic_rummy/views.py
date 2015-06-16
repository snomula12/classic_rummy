from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import RedirectView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
import sys
import random
from sets import Set
		

class Card(object):

	def __init__(self, rank, suit):		
		self.rank = rank
		self.suit = suit

class Deck(object):

	def __init__(self):
		suits = ['Hearts', 'Spades', 'Daimonds', 'Clubs']
		ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]
		self.cards = []
		for suit in suits:
			for rank in ranks:
				self.cards.append(Card(rank, suit))


class ClassisRummyView(TemplateView):
    '''
        This view sets up the game for 4 users. Sends the remaning cards are open deck and also has an open card choice
    '''
    template_name = "classic_rummy.html"
    
    def dispatch(self, request, *args, **kwargs):
    	self.deck = Deck()
    	
    	self.number_of_cards = 7
    	self.players = 4
    	self.game = {}
    	self.delte_cards_index = []
    	self.remaining_deck_index = []
    	self.you = False
    	index = []

    	for j in range(0,51): 
    		index.append(j)
    		
    	for i in range(0, self.players): 
    		self.random_list = random.sample(index, self.number_of_cards)
    		self.card_list = {}
    		
    		for num in self.random_list:
    			self.card_list[num]= {'card':self.deck.cards[num]}
    			self.delte_cards_index.append(num)
    			index.remove(num)
    		
    		if not self.you:
    			self.game['you'] = {'list':self.random_list,'cards':self.card_list}
    			self.you = True
    		else:
    			self.game[i] = {'list':self.random_list,'cards':self.card_list}

		
			
    	self.open_card = random.sample(index, 1)
    	self.delte_cards_index.append(self.open_card[0])
    	
        index.remove(self.open_card[0])
    	self.open_card_index = self.open_card[0]
    	self.open_card = self.deck.cards[self.open_card[0]]
    	
    	self.remaining_deck_index  = index
    	
    	return super(ClassisRummyView, self).dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        
        context = super(ClassisRummyView, self).get_context_data(**kwargs)
        context['game'] = self.game
        context['remaining_deck_index'] = self.remaining_deck_index
        context['open_card'] = self.open_card
        context['open_card_index'] = self.open_card_index
        return context

def draw_card(request):
    '''
        Every time the user clicks on Draw a new Card button a random card is selected from the remaing deck.
        And for Auto players this method also selects a random card to discard based on users current list of cards
    '''
    deck = Deck()
    remaining_deck =request.POST.getlist('remaining_deck[]')
    random_draw = random.sample(remaining_deck, 1)
    remaining_deck.remove(random_draw[0])
    
    try:
        new_card = deck.cards[int(random_draw[0])]
        success = True
    except:
        new_card = None
        success = False
    
    current_card_list, random_discard =  request.POST.get('current_card_list', None), None
    if current_card_list is not None:
        current_card_list = current_card_list[1:-1].split(',')
        random_discard = random.sample(current_card_list, 1)
        random_discard =  int(random_discard[0])

    retval = { 'success': success, 'random_discard':random_discard,  'new_card_index':int(random_draw[0]),   'new_card_rank': new_card.rank, 'new_card_suit':new_card.suit, 'remaining_deck': remaining_deck  }
    return HttpResponse(simplejson.dumps(retval), mimetype="application/json")

def update_player_cards(request):
    '''
        Every time the user clicks of a Get Card Button or discard button the users current_card_list is updated accordingly
    '''
    success, card_list, player_won = False, None, False
    if request.POST.get('action') == 'add':
        card_list = request.POST.getlist('card_list')
        card_list = card_list[0][:-1]
        card_list = str(card_list) + ', ' + str(request.POST.get('new_card_index')) + "]"
        success = True
        player_won = False

    elif request.POST.get('action') == 'remove':
        card_list = request.POST.getlist('card_list')
        card_list = str(card_list[0])
        replace_string = ', ' + str(request.POST.get('new_card_index')) 
        card_list = card_list.replace(replace_string, "")
        
        success = True
        player_won = check_classic_rummy(card_list)

    retval = { 'success': success, 'card_list':card_list, 'player_won':player_won}
    return HttpResponse(simplejson.dumps(retval), mimetype="application/json")

def check_classic_rummy(card_list):

    '''
        Based on the card index we can figure out if the set of card is a classic_rummy or not.
        1. To Find straight 4 card_index from card_list must be consecative 
        2. If we find the that there is a straight in the card_list, then the remaining cards must be of the same rank .  
    '''

    card_list = card_list[1:-1].split(',')
    cards = []
    
    for i in card_list:
        cards.append(int(i))
    
    cards = sorted(cards)
    is_straight = check_for_straight(cards)
    
    if is_straight:
        for item in is_straight:
            cards.remove(item)
        
        is_three_of_kind =  check_three_of_kind(cards)

        if is_three_of_kind:
            return  True

    return False

def check_for_straight(card_list):
    
    run = []
    result = [run]
    expect = None

    for card in card_list:
        if (card == expect) or (expect is None):
            run.append(card)
        else:
            run = [card]
            result.append(run)
        expect = card + 1 

    for item in result:
        if len(item) == 4:
            return item
    return False

def check_three_of_kind(card_list):
    
    if card_list[0]+13 == card_list[1] and card_list[1]+13 == card_list[2]:
        return True
    
    return False
