from django.db import models

from idios.models import ProfileBase

class UserProfile(ProfileBase):
	#name = 

# Might just put these fields in the league class?
class Positions(models.Model):
	qb = models.IntegerField(default=0)
	wr = models.IntegerField(default=0)
	rb = models.IntegerField(default=0)
	te = models.IntegerField(default=0)
	wr_rb = models.IntegerField(default=0)
	wr_te = models.IntegerField(default=0)
	rb_te = models.IntegerField(default=0)
	wr_rb_te = models.IntegerField(default=0)
	k = models.IntegerField(default=0)
	defense = models.IntegerField(default=0)
	
# consider changing these to integers?
class Scoring(models.Model):
	# Passing
	pass_yds = models.IntegerField(default=25) # number of yards per point
	pass_tds = models.FloatField(default=0)
	pass_ints = models.FloatField(default=0)
	pass_att = models.FloatField(default=0)
	pass_comp = models.FloatField(default=0)
	pass_inc = models.FloatField(default=0)
	pass_sacks = models.FloatField(default=0)
	pass_pick6 = models.FloatField(default=0)
	# Consider bonuses for long pass/TDs - 40 yards?
	
	# Rushing
	rush_yds = models.IntegerField(default=10) # number of yards per point
	rush_att = models.FloatField(default=0)
	rush_tds = models.FloatField(default=0)
	# consider bonuses for long rush/TDs - 40?
	
	# Receiving
	rec_tds = models.FloatField(default=0)
	rec_rec = models.FloatField(default=0)
	rec_yds = models.IntegerField(default=1) # number of yards per point
	# consider bonuses for long rec/TDs - 40?
	
	# Kick/punt returns
	ret_tds = models.FloatField(default=0)
	ret_yds = models.IntegerField(default=1) # of yards per point
	
	# Misc
	two_pt = models.FloatField(default=0)
	fumbles = models.FloatField(default=0)
	fumb_lost = models.FloatField(default=0)
	fumble_td = models.FloatField(default=0)
	
	# Kickers
	fg_0_19 = models.FloatField(default=0)
	fg_20_29 = models.FloatField(default=0)
	fg_30_39 = models.FloatField(default=0)
	fg_40_49 = models.FloatField(default=0)
	fg_50_ = models.FloatField(default=0)
	fgmiss_0_19 = models.FloatField(default=0)
	fgmiss_20_29 = models.FloatField(default=0)
	fgmiss_30_39 = models.FloatField(default=0)
	fgmiss_40_49 = models.FloatField(default=0)
	fgmiss_50_ = models.FloatField(default=0)
	pat_made = models.FloatField(default=0)
	pat_miss = models.FloatField(default=0)
	
	# Defense
	def_pts_0 = models.FloatField(default=0)
	def_pts_1_6 = models.FloatField(default=0)
	def_pts_7_13 = models.FloatField(default=0)
	def_pts_14_20 = models.FloatField(default=0)
	def_pts_21_27 = models.FloatField(default=0)
	def_pts_28_34 = models.FloatField(default=0)
	def_pts_35_ = models.FloatField(default=0)
	def_sack = models.FloatField(default=0)
	def_int = models.FloatField(default=0)
	def_fum_rec = models.FloatField(default=0)
	def_td = models.FloatField(default=0)
	def_safety = models.FloatField(default=0)
	def_block_kick = models.FloatField(default=0)
	def_ret_yds = models.IntegerField(default=1) # of yards per point
	def_kpret_tds = models.FloatField(default=0)
	def_4th_down_stops = models.FloatField(default=0)
	def_tackles_for_loss = models.FloatField(default=0)
	def_yds_neg = models.FloatField(default=0)
	def_yds_0_99 = models.FloatField(default=0)
	def_yds_100_199 = models.FloatField(default=0)
	def_yds_200_299 = models.FloatField(default=0)
	def_yds_300_399 = models.FloatField(default=0)
	def_yds_400_499 = models.FloatField(default=0)
	def_yds_500_ = models.FloatField(default=0)
	def_3_and_out = models.FloatField(default=0)
	
	# General Settings
	fractional_pts = models.BooleanField(default=True)
	negative_pts = models.BooleanField(default=True)

class League(models.Model):
	name = models.CharField(max_length=30)
	slug = models.SlugField()
	
	
	
class Team(models.Model):
	name = models.CharField(max_length=30)
	avatar = models.FilePathField
	league = models.ForeignKey(League)
	user = models.ForeignKey(UserProfile)
	
	def __unicode__(self):
		return u'%s' % self.name
		

# Possibilities
#	- Trade
#	- Add
#	- Drop
#	- Add/Drop - combine the two? 
class Transaction(models.Model):
	date = models.DateTimeField()
	league = models.ForeignKey(League)

	class Meta:
		abstract = True
	
	
class trade(Transaction):
	offers = 
	
class team_trade(models.Model):
	team = models.ForeignKey(Team)
	players = models.ManyToManyField(Player)
	accepted = models.BooleanField()


class add(Transaction):
	team = models.OneToOneField(Team)
	player = models.ForeignKey(Player)


class drop(Transaction):
	team = models.OneToOneField(Team)
	player = models.ForeignKey(Player)


		












