from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def league_page(request, league_id):
	return render_to_response("league.html", context_instance=RequestContext(request))