from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.http import Http404
from league.forms import NewUserForm

from league.models import Owner
from django.contrib.auth.models import User

# Create your views here.
def league_page(request, league_id):
	return render_to_response("league.html", context_instance=RequestContext(request))
	
def profile_page(request, user_id):
	try:
		profile = Owner.objects.get(slug=user_id)
	except Owner.DoesNotExist:
		raise Http404 #execute a search here instead?
		
	owner_user = profile.user
	return render_to_response('owner.html', locals(), context_instance=RequestContext(request))
	
def team_page(request, team_id, league_id):
	return render_to_response("team.html", context_instance=RequestContext(request))
	
def new_user(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_user = User.objects.create_user(cd['username'], cd['email'], cd['pass1'])
			if cd['first']:
				new_user.first_name = cd['first']
			if cd['last']:
				new_user.last_name = cd['last']
			new_owner = Owner(slug=slugify(cd['username']), user=new_user)
			new_owner.save()
			return HttpResponseRedirect('/new_user/created/')
	else:
		form = NewUserForm()
	return render_to_response('new_user.html', {'form':form}, context_instance=RequestContext(request))

def user_created(request):
	return render_to_response('user_created.html', locals(), context_instance=RequestContext(request))
	
def home_view(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new_user = User.objects.create_user(cd['username'], cd['email'], cd['pass1'])
			if cd['first']:
				new_user.first_name = cd['first']
			if cd['last']:
				new_user.last_name = cd['last']
			new_owner = Owner(slug=slugify(cd['username']), user=new_user)
			new_owner.save()
			return HttpResponseRedirect('/new_user/created/')
	else:
		form = NewUserForm()
	return render_to_response('home.html', {'form':form}, context_instance=RequestContext(request))
