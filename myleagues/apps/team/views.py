from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def team_page(request, team_id, league_id):
	return render_to_response("team.html", context_instance=RequestContext(request))