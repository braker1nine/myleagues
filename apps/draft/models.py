from django.db import models
from league.models import Player, League, Team, Owner

# Create your models here.

class DraftPlayerProxy(models.Model):
	player = models.ForeignKey(Player)
	owner = models.ForeignKey(Owner)
	rank = models.IntegerField()
	available = models.BooleanField()
	
	class Meta:
		unique_together = ("rank", "owner")

class Draft(models.Model):
	league = models.OneToOneField(League, related_name="draft")

class Round(models.Model):
	round = models.IntegerField(editable=False)
	draft = models.ForeignKey(Draft)

class Pick(models.Model):
	pick = models.IntegerField(editable=False)
	player = models.ForeignKey(PlayerProxy, unique=True, blank=True)
	team = models.ForeignKey(Team)
	round = models.ForeignKey(Round)
	