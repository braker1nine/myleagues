from django.db import models
from idios.models import ProfileBase


POSITION_CHOICES = (
	('QB', 'Quarterback'),
	('RB', 'Runningback'),
	('WR', 'Wide Receiver'),
	('TE', 'Tight End'),
	('K', 'Kicker'),
	('DEF', 'Defense'),
)

NFL_TEAM_CHOICES = (
	('ARI', 'Arizona Cardinals'),
	('ATL', 'Atlanta Falcons'),
	('BAL', 'Baltimore Ravens'),
	('BUF', 'Buffalo Bills'),
	('CAR', 'Carolina Panthers'),
	('CHI', 'Chicago Bears'),
	('CIN', 'Cincinnati Bengals'),
	('CLE', 'Cleveland Browns'),
	('DAL', 'Dallas Cowboys'),
	('DEN', 'Denver Broncos'),
	('DET', 'Detroit Lions'),
	('GB', 'Green Bay Packers'),
	('HOU', 'Houston Texans'),
	('IND', 'Indianapolis Colts'),
	('JAX', 'Jacksonville Jaguars'),
	('KC', 'Kansas City Chiefs'),
	('MIA', 'Miami Dolphins'),
	('MIN', 'Minnesota Vikings'),
	('NE', 'New England Patriots'),
	('NO', 'New Orleans Saints'),
	('NYG', 'New York Giants'),
	('NYJ', 'New York Jets'),
	('OAK', 'Oakland Raiders'),
	('PHI', 'Philadelphia Eagles'),
	('PIT', 'Pittsburgh Steelers'),
	('SD', 'San Diego Chargers'),
	('SEA', 'Seattle Seahawks'),
	('SF', 'San Francisco 49ers'),
	('STL', 'St. Louis Rams'),
	('TB', 'Tampa Bay Buccaneers'),
	('TEN', 'Tennessee Titans'),
	('WAS', 'Washington Redskins'),
)


WEEK_CHOICES = (
	(0, 'Draft'),
	(1, 'Week 1'),
	(2, 'Week 2'),
	(3, 'Week 3'),
	(4, 'Week 4'),
	(5, 'Week 5'),
	(6, 'Week 6'),
	(7, 'Week 7'),
	(8, 'Week 8'),
	(9, 'Week 9'),
	(10, 'Week 10'),
	(11, 'Week 11'),
	(12, 'Week 12'),
	(13, 'Week 13'),
	(14, 'Week 14'),
	(15, 'Week 15'),
	(16, 'Week 16'),
	(17, 'Week 17'),
)


class Owner(ProfileBase):
	name = models.CharField(max_length=30)
	slug = models.SlugField()
	leagues = models.ManyToManyField('League')
	
	friends = models.ManyToManyField('Owner')
	
class Team(models.Model):
	
	# Attributes
	name = models.CharField(max_length=30)
	profile_img = models.ImageField(upload_to="img/team_avatars/")
	
	
	# Relationships
	league = models.ForeignKey('League')
	owner = models.ForeignKey(Owner)


class Player(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	slug = models.SlugField()
	nfl_team = models.CharField(max_length=30, choices=NFL_TEAM_CHOICES)
	position = models.CharField(max_length=20, choices=POSITION_CHOICES)
	
class PlayerProxy(models.Model):
	team = models.ForeignKey(Team)
	player = models.ForeignKey(Player)


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
	fg_50_plus = models.FloatField(default=0)
	fgmiss_0_19 = models.FloatField(default=0)
	fgmiss_20_29 = models.FloatField(default=0)
	fgmiss_30_39 = models.FloatField(default=0)
	fgmiss_40_49 = models.FloatField(default=0)
	fgmiss_50_plus = models.FloatField(default=0)
	pat_made = models.FloatField(default=0)
	pat_miss = models.FloatField(default=0)
	
	# Defense
	def_pts_0 = models.FloatField(default=0)
	def_pts_1_6 = models.FloatField(default=0)
	def_pts_7_13 = models.FloatField(default=0)
	def_pts_14_20 = models.FloatField(default=0)
	def_pts_21_27 = models.FloatField(default=0)
	def_pts_28_34 = models.FloatField(default=0)
	def_pts_35_plus = models.FloatField(default=0)
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
	def_yds_500_plus = models.FloatField(default=0)
	def_3_and_out = models.FloatField(default=0)
	
	# General Settings
	fractional_pts = models.BooleanField(default=True)
	negative_pts = models.BooleanField(default=True)


class League(models.Model):
	name = models.CharField(max_length=30)
	slug = models.SlugField()
	
	# Position Settings
	qb = models.IntegerField(default=1)
	wr = models.IntegerField(default=2)
	rb = models.IntegerField(default=2)
	te = models.IntegerField(default=1)
	wr_rb = models.IntegerField(default=1)
	wr_te = models.IntegerField(default=1)
	rb_te = models.IntegerField(default=0)
	wr_rb_te = models.IntegerField(default=0)
	k = models.IntegerField(default=1)
	defense = models.IntegerField(default=1)
	
	scoring = models.ForeignKey(Scoring)
	

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
	name = models.CharField(max_length=10) #just to have something
	
	
class team_trade(models.Model):
	trade = models.ForeignKey(trade)
	team = models.ForeignKey(Team)
	players = models.ManyToManyField(PlayerProxy)
	accepted = models.BooleanField()


class add(Transaction):
	team = models.ForeignKey(Team)
	player = models.ForeignKey(PlayerProxy)


class drop(Transaction):
	team = models.ForeignKey(Team)
	player = models.ForeignKey(PlayerProxy)

class add_drop(Transaction):
	add = models.ForeignKey(add)
	drop = models.ForeignKey(drop)
	
	
class Roster(models.Model):
	week = models.IntegerField(choices=WEEK_CHOICES)
	team = models.ForeignKey(Team)
	players = models.ManyToManyField(Player)
	
			










