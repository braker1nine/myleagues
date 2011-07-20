from django.db import models

# Create your models here.

class League(models.Model):
	
	
class Team(models.Model):
	name = models.CharField(max_length=30)
	avatar = models.FilePathField
	league = models.ForeignKey(League)
	
	def __unicode__(self):
		return u'%s' % self.name