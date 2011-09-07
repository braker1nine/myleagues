from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from league.models import League


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
		
class NewLeagueForm(ModelForm):
	
	class Meta:
		model = League
		exclude = ('year', 'active', 'dynasty',)
