from django.shortcuts import render_to_response
from django.template import RequestContext

def profile_page(request, user_id):
	return render_to_response('owner.html', context_instance=RequestContext(request))