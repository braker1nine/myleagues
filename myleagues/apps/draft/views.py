from django.shortcuts import render_to_response

def draft_page(request, league_id):
	return render_to_response('draft.html')
	
	
# Displays the current users team on the left sidebar
#def my_team(request):


# Displays the league's draft board in the middle of the screen
#def draft_board(request):

# Displays the previous, current, and next picks above the draft board
#def pick_summary(request):

# Displays the available players (dependent on search field and some boolean position selectors
#def available_players(request):