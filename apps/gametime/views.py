# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

def decision(request):
	return render_to_response('gametime.html', context_instance=RequestContext(request))