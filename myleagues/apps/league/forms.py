from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from league.models import League
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard


#class NewUserErrorList(ErrorList):
#	def __unicode__(self):
#		return self.as_divs()
#	def as_divs(self):
 #		if not self: return u''
 #		return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error"><span%s</div>' % e for e in self])

class NewUserForm(forms.Form):
	first = forms.CharField(max_length=30, label="First Name", required=False)
	last = forms.CharField(max_length=30, label="Last Name", required=False)
	username = forms.CharField(max_length=30, min_length=2, label="Username")
	email = forms.EmailField(label="E-mail")
	pass1 = forms.CharField(widget=forms.PasswordInput, label="Your Password", min_length=8)
	pass2 = forms.CharField(widget=forms.PasswordInput, label="Repeat Password")
	
#	required_css_class = 'required'
#	error_css_class = 'error'
#	error_class = NewUserErrorClass
	
	def clean_pass1(self):
		if self.data['pass1'] != self.data['pass2']:
			raise forms.ValidationError('Passwords do not match')
		return self.data['pass1']
		
	def clean_username(self):
		if User.objects.get(username=self.data['username']):
			raise forms.ValidationError('Username already exists')
		return self.data['username']
		
		
class NewLeague_BasicInfoForm(forms.Form):
	name = forms.CharField(max_length=30, label="League Name")
	slug = forms.SlugField(help_text="May consist of letters, numbers, underscores, and hyphens.")
	trade_points = forms.BooleanField()
	draft_type = forms.ChoiceField(choices=((0, 'Standard'), (1, 'Auction'), (2, 'Paid Auction'),))
	competition = forms.ChoiceField(choices=((0, 'Head-to-Head'), (1, 'Cumulative'),))
	
	
class NewLeague_InviteFriendsForm(forms.Form):
	friends = forms.CharField(max_length=30)

class NewLeague_ScoringForm(forms.Form):
	pass_yds = forms.IntegerField(initial=25, label="Pass Yards") # number of yards per point
	pass_tds = forms.FloatField(initial=6, label="Pass TDs")
	pass_ints = forms.FloatField(initial=-2, label="Interceptions")
	pass_att = forms.FloatField(initial=0, label="Pass Attempts")
	pass_comp = forms.FloatField(initial=0, label="Pass Completions")
	pass_inc = forms.FloatField(initial=0, label="Pass Incompletions")
	pass_sacks = forms.FloatField(initial=-1, label="Sacks")
	pass_pick6 = forms.FloatField(initial=-2, label="Pick 6's Thrown")
	
	# Rushing
	rush_yds = forms.IntegerField(initial=10, label="Rush Yards") # number of yards per point
	rush_att = forms.FloatField(initial=0, label="Rush Attempts")
	rush_tds = forms.FloatField(initial=6, label="Rush TDs")
	# consider bonuses for long rush/TDs - 40?
	
	# Receiving
	rec_yds = forms.FloatField(initial=10, label="Receiving Yards") # of yards per point
	rec_rec = forms.FloatField(initial=1, label="Receptions")
	rec_tds = forms.IntegerField(initial=6, label="Receiving TDs")
	# consider bonuses for long rec/TDs - 40?
	
	# Kick/punt returns
	ret_tds = forms.FloatField(initial=6, label="Return TDs")
	ret_yds = forms.IntegerField(initial=25, label="Return Yards") # of yards per point
	
	# Misc
	two_pt = forms.FloatField(initial=2, label="2 Point")
	fumbles = forms.FloatField(initial=-1, label="Fumbles")
	fumb_lost = forms.FloatField(initial=-1, label="Fumbles Lost")
	fumb_rec = forms.FloatField(initial=1, label="Fumbles Recovered")
	fumble_td = forms.FloatField(initial=6, label="Fumble TD")
	
	# Kickers
	fg_0_19 = forms.FloatField(initial=1, label="Field Goal Made 0-19")
	fg_20_29 = forms.FloatField(initial=1, label="Field Goal Made 20-29")
	fg_30_39 = forms.FloatField(initial=2, label="Field Goal Made 30-39")
	fg_40_49 = forms.FloatField(initial=3, label="Field Goal Made 40-49")
	fg_50_plus = forms.FloatField(initial=5, label="Field Goal Made 50+")
	fgmiss_0_19 = forms.FloatField(initial=-2, label="Field Goal Miss 0-19")
	fgmiss_20_29 = forms.FloatField(initial=-1, label="Field Goal Miss 20-29")
	fgmiss_30_39 = forms.FloatField(initial=0, label="Field Goal Miss 30-39")
	fgmiss_40_49 = forms.FloatField(initial=0, label="Field Goal Miss 40-49")
	fgmiss_50_plus = forms.FloatField(initial=0, label="Field Goal Miss 50+")
	pat_made = forms.FloatField(initial=1, label="PAT Made")
	pat_miss = forms.FloatField(initial=-2, label="PAT Miss")
	
	# Defense
	shutout_pts = forms.FloatField(initial=15, label="Shutout Points")
	pts_per_pt = forms.FloatField(initial=1, label="Subtraction Per Point Allowed")
	def_sack = forms.FloatField(initial=1, label="Sacks")
	def_int = forms.FloatField(initial=2, label="INTs")
	def_fum_rec = forms.FloatField(initial=2, label="Fumble Rec")
	def_td = forms.FloatField(initial=6, label="Def TDs")
	def_safety = forms.FloatField(initial=1, label="Safeties")
	def_block_kick = forms.FloatField(initial=1, label="Blocked Kick")
	def_ret_yds = forms.IntegerField(initial=25, label="Return Yards") # of yards per point
	def_kpret_tds = forms.FloatField(initial=0, label="Punt Return Yards")
	def_4th_down_stops_punts = forms.FloatField(initial=0.5, label="4th Down Stops and Punts")
	def_tackles_for_loss = forms.FloatField(initial=0.5, label="Tackles for Loss")
	def_yds_allowed_0 = forms.FloatField(initial=20, label="Pts for Allowing Zero Yards")
	def_pts_per_yard = forms.FloatField(initial=.0625, label="Subtraction Per Yard Allowed")
	def_3_and_out = forms.FloatField(initial=1, label="3 & Outs")
	
	# General Settings - might delete these?
	fractional_pts = forms.BooleanField(initial=True)
	negative_pts = forms.BooleanField(initial=True)
	
	
class NewLeagueWizard(FormWizard):
	
	def done(self, request, form_list):
		
		return HttpResponseRedirect('/league-created/')
		
	def get_template(self, step):
		return 'league_wizard_%s.html' % step




