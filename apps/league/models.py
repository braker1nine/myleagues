from datetime import datetime
from django.db import models
from idios.models import ProfileBase
from threadedcomments.models import ThreadedComment
from django_facebook.models import FacebookProfileModel


POSITION_CHOICES = (
	('QB', 'Quarterback'),
	('RB', 'Runningback'),
	('WR', 'Wide Receiver'),
	('TE', 'Tight End'),
	('K', 'Kicker'),
	('DEF', 'Defense'),
	('DL', 'Defensive Line'),
	('LB', 'Linebacker'),
	('DB', 'Defensive Back'),
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

LEAGUE_CHOICES = (
	(0, 'Head-to-Head'),
	(1, 'Cumulative'),
)

YEAR_CHOICES = (
	('2007', '2007'),
	('2008', '2008'),
	('2009', '2009'),
	('2010', '2010'),
	('2011', '2011'),
)

"""
	Extension of ProfileBase. For displaying an owner's fantasy football profile
	slug: for a users permanent url http://myleagu.es/user/(slug)
	leagues: all of the leagues an owner participates in
	friends: all of an owners friends (may be redundant w/ django-friends app already installed)
"""
class Owner(ProfileBase, FacebookProfileModel):
	slug = models.SlugField(unique=True)
	leagues = models.ManyToManyField('League', blank=True, related_name="owners")
	
	friends = models.ManyToManyField('Owner', blank=True)
	
	def get_absolute_url(self):
		return "/user/%s/" % self.slug
		
	def __unicode__(self):
		return u'%s' % self.slug
	
"""
	Team model for each team in a fantasy league
	name: team's name, pretty self explanatory
	profile_img: team profile image. Might need to rethink storage location
	slug: for a team's permanent url http://myleagu.es/league/(league_slug)/team/(team_slug)/
	
	league: the league object a team belongs to
	owner: owner the team belongs to
"""
class Team(models.Model):
	
	# Attributes
	name = models.CharField(max_length=30)
	profile_img = models.ImageField(upload_to="img/team_avatars/")
	slug = models.SlugField(unique=True)
	
	# Relationships
	league = models.ForeignKey('League', related_name="teams")
	owner = models.ForeignKey(Owner, related_name="owners")
	
	def __unicode__(self):
		return u'%s' % (self.name)
		
	def get_absolute_url(self):
		return u'/league/%s/team/%s' % (self.league.slug, self.slug)
		
	class Meta:
		unique_together = ("league", "owner") # makes sure an owner only has one team per league
		verbose_name = "team"
		verbose_name_plural = "teams"

"""
	A player object will be created for ever player in the NFL
"""
class Player(models.Model):
	first_name = models.CharField(max_length=30, verbose_name="First Name")
	last_name = models.CharField(max_length=30, verbose_name="Last Name")
	slug = models.SlugField(unique=True)
	nfl_team = models.CharField(max_length=30, choices=NFL_TEAM_CHOICES, verbose_name="NFL Team")
	position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name="Position")
	
	def get_absolute_url(self):
		return u'/player/%s/' % self.slug
	
	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name)
	
"""
	For each league, a PlayerProxy object will be created for each Player object. Contains league information for a player
	team: Current team that owns the player
	player: The player object the proxy corresponds to
	league: League the proxy object is in
	keeper: Will be set to true if the team decides it wants the player to be a keeper
	
	Also want to relate this to the draft pick if the player was drafted or add/drop object if player was added as FA?
"""
class PlayerProxy(models.Model):
	team = models.ForeignKey(Team, blank=True)
	player = models.ForeignKey(Player)
	league = models.ForeignKey('League')

class ScoringSettings(models.Model):
	
	season = models.ForeignKey('Season', related_name='scoring_settings')

	# Position Settings
	qb = models.IntegerField(default=1, verbose_name="QB")
	wr = models.IntegerField(default=2, verbose_name="WR")
	rb = models.IntegerField(default=2, verbose_name="RB")
	te = models.IntegerField(default=1, verbose_name="TE")
	wr_rb = models.IntegerField(default=1, verbose_name="WR/RB")
	wr_te = models.IntegerField(default=1, verbose_name="WR/TE")
	rb_te = models.IntegerField(default=0, verbose_name="RB/TE")
	wr_rb_te = models.IntegerField(default=0, verbose_name="WR/RB/TE")
	k = models.IntegerField(default=1, verbose_name="K")
	defense = models.IntegerField(default=1, verbose_name="DEF")
	dl = models.IntegerField(default=0, verbose_name="DL")
	lb = models.IntegerField(default=0, verbose_name="LB")
	db = models.IntegerField(default=0, verbose_name="DB")
	
	
	# Scoring options
	pass_yds = models.IntegerField(default=25, verbose_name="Pass Yards") # number of yards per point
	pass_tds = models.FloatField(default=0, verbose_name="Pass TDs")
	pass_ints = models.FloatField(default=0, verbose_name="Interceptions")
	pass_att = models.FloatField(default=0, verbose_name="Pass Attempts")
	pass_comp = models.FloatField(default=0, verbose_name="Pass Completions")
	pass_inc = models.FloatField(default=0, verbose_name="Pass Incompletions")
	pass_sacks = models.FloatField(default=0, verbose_name="Sacks")
	pass_pick6 = models.FloatField(default=0, verbose_name="Pick 6's Thrown")
	# Consider bonuses for long pass/TDs - 40 yards?
	
	# Rushing
	rush_yds = models.IntegerField(default=10, verbose_name="Rush Yards") # number of yards per point
	rush_att = models.FloatField(default=0, verbose_name="Rush Attempts")
	rush_tds = models.FloatField(default=0, verbose_name="Rush TDs")
	# consider bonuses for long rush/TDs - 40?
	
	# Receiving
	rec_yds = models.FloatField(default=0, verbose_name="Receiving Yards")
	rec_rec = models.FloatField(default=0, verbose_name="Receptions")
	rec_tds = models.IntegerField(default=1, verbose_name="Receiving TDs") # number of yards per point
	# consider bonuses for long rec/TDs - 40?
	
	# Kick/punt returns
	ret_tds = models.FloatField(default=0, verbose_name="Return TDs")
	ret_yds = models.IntegerField(default=1, verbose_name="Return Yards") # of yards per point
	
	# Misc
	two_pt = models.FloatField(default=0, verbose_name="2 Point")
	fumbles = models.FloatField(default=0, verbose_name="Fumbles")
	fumb_lost = models.FloatField(default=0, verbose_name="Fumbles Lost")
	fumb_rec = models.FloatField(default=0, verbose_name="Fumbles Recovered")
	fumble_td = models.FloatField(default=0, verbose_name="Fumble TD")
	
	# Kickers
	fg_0_19 = models.FloatField(default=0, verbose_name="Field Goal Made 0-19")
	fg_20_29 = models.FloatField(default=0, verbose_name="Field Goal Made 20-29")
	fg_30_39 = models.FloatField(default=0, verbose_name="Field Goal Made 30-39")
	fg_40_49 = models.FloatField(default=0, verbose_name="Field Goal Made 40-49")
	fg_50_plus = models.FloatField(default=0, verbose_name="Field Goal Made 50+")
	fgmiss_0_19 = models.FloatField(default=0, verbose_name="Field Goal Miss 0-19")
	fgmiss_20_29 = models.FloatField(default=0, verbose_name="Field Goal Miss 20-29")
	fgmiss_30_39 = models.FloatField(default=0, verbose_name="Field Goal Miss 30-39")
	fgmiss_40_49 = models.FloatField(default=0, verbose_name="Field Goal Miss 40-49")
	fgmiss_50_plus = models.FloatField(default=0, verbose_name="Field Goal Miss 50+")
	pat_made = models.FloatField(default=0, verbose_name="PAT Made")
	pat_miss = models.FloatField(default=0, verbose_name="PAT Miss")
	
	# Defense
	shutout_pts = models.FloatField(default=15, verbose_name="Shutout Points")
	pts_per_pt = models.FloatField(default=1, verbose_name="Subtraction Per Point Allowed")
	def_sack = models.FloatField(default=0, verbose_name="Sacks")
	def_int = models.FloatField(default=0, verbose_name="INTs")
	def_fum_rec = models.FloatField(default=0, verbose_name="Fumble Rec")
	def_td = models.FloatField(default=0, verbose_name="Def TDs")
	def_safety = models.FloatField(default=0, verbose_name="Safeties")
	def_block_kick = models.FloatField(default=0, verbose_name="Blocked Kick")
	def_ret_yds = models.IntegerField(default=1, verbose_name="Return Yards") # of yards per point
	def_kpret_tds = models.FloatField(default=0, verbose_name="Punt Return Yards")
	def_4th_down_stops = models.FloatField(default=0, verbose_name="4th Down Stops")
	def_tackles_for_loss = models.FloatField(default=0, verbose_name="Tackles for Loss")
	def_yds_allowed_0 = models.FloatField(default=20, verbose_name="Pts for Allowing Zero Yards")
	def_pts_per_yard = models.FloatField(default=.0625, verbose_name="Subtraction Per Yard Allowed")
	def_3_and_out = models.FloatField(default=0, verbose_name="3 & Outs")
	
	# General Settings - might delete these?
	fractional_pts = models.BooleanField(default=True)
	negative_pts = models.BooleanField(default=True)


"""
	Season represents one season from a league
	year: Year the league is from
	active: True if league is from current year
	league: The league object with which this season is associated
	
	URL:
	If Active
	http://myleagu.es/league/(league.slug)
	
	If Inactive
	http://myleagu.es/archive/league/(league.slug)/(season.year)

"""
class Season(models.Model):
	year = models.CharField(max_length=4, choices=YEAR_CHOICES)
	active = models.BooleanField()
	league = models.ForeignKey('League', related_name='seasons')
	

"""
	League object for each fantasy league
	name: league name
	avatar: league avatar (might not keep this)
	slug: Slug for the league permalink http://myleagu.es/league/(slug)
	dynasty: Corresponding dynasty object for the league - might need to be blank=True and only have dynasty if it gets renewed once
	trade_points: True if league allows you to trade points
"""
class League(models.Model):
	name = models.CharField(max_length=30, verbose_name="League Name")
	avatar = models.ImageField(upload_to="league_avatars")
	slug = models.SlugField(unique=True, verbose_name="League URL")
	
	def __unicode__(self):
		return u'%s' % self.name
	

"""
	Event class will be subclassed by both transaction and social events
	created: date/time the event was created
	likes: list of owners who've liked an event
	dislikes: list of owner who've disliked an event
	
	tagged_players: list of players who have been tagged in an event
	tagged_owners: list of owners who have been tagged in an event
"""
class Event(models.Model):
	created = models.DateTimeField(verbose_name="Date")
	updated = models.DateTimeField(verbose_name="Updated", default=datetime.now())	
	
	likes = models.ManyToManyField(Owner, related_name="%(class)s_likes", blank=True, verbose_name="Likes")
	dislikes = models.ManyToManyField(Owner, related_name="%(class)s_dislikes", blank=True, verbose_name="Dislikes")
	
	tagged_players = models.ForeignKey(Player, related_name="%(class)s_tags", blank=True, verbose_name="Tagged Players")
	tagged_owners = models.ForeignKey(Owner, related_name="%(class)s_tags", blank=True, verbose_name="Tagged Owners")
	
	class Meta:
		abstract = True
		ordering = ['-updated']
	

"""
	Status updates. In which users can tag players or other owners
	writer: Owner who is the author of the update
	text: text of the update. Still need to work out what the text will be if a player/owner is tagged. Security concern if it contains html
		
"""
class statusUpdate(Event):
	writer = models.ForeignKey(Owner, related_name="status_updates", verbose_name="Writer")
	text = models.TextField(max_length=500, verbose_name="Text")
	
	class Meta:
		verbose_name = "status update"
		verbose_name_plural = "status updates"

 
"""
	Basic model for transactions
	league: league in which the transaction occurred
"""
class Transaction(Event):
	season = models.ForeignKey(Season, related_name="transactions", verbose_name="Season")
	
	class Meta:
		verbose_name = "transaction"
		verbose_name_plural = "transactions"
	
"""
	represents a trade
	proposed_by: owner the trade was proposed by
	counter_offer_to: if this trade is a counter offer, this points to the trade its a counter offer to
"""
class trade(Transaction):
	proposed_by = models.ForeignKey(Owner, related_name="proposed_trades", verbose_name="Proposed By")
	counter_offer_to = models.ForeignKey('trade', blank=True)
	
	class Meta:
		verbose_name = "trade"
		verbose_name_plural = "trades"
	
"""
	Each trade proposal contains several team_trade objects. Represents the players each team will give
	up in the trade and whether the user accepted it
	trade: corresponding trade object
	team: the team offering the players
	players: the players the team will give up
	points: number of points the team will give up
	accepted: false until the team accepts the trade
"""
class team_trade(models.Model):
	trade = models.ForeignKey(trade, related_name="teamtrades", verbose_name="Trade")
	team = models.ForeignKey(Team, verbose_name="Team")
	players = models.ManyToManyField(PlayerProxy, verbose_name="Players", blank=True)
	points = models.FloatField(verbose_name="Points", blank=True)
	accepted = models.BooleanField(verbose_name="Accepted?")

"""
	Represents a player add
	team: team player was added to
	player: the player added
"""
class add(Transaction):
	team = models.ForeignKey(Team, verbose_name="Team")
	player = models.ForeignKey(PlayerProxy, verbose_name="Player")
	
	def __unicode__(self):
		return u'%s added %s' % (team.__unicode__(), player.__unicode__())

"""
	Represents a player drop
	team: team the player was dropped from
	player: the player dropped
"""
class drop(Transaction):
	team = models.ForeignKey(Team, verbose_name="Team")
	player = models.ForeignKey(PlayerProxy, verbose_name="Player")
	
	def __unicode__(self):
		return u'%s dropped %s' % (team.__unicode__(), player.__unicode__())

"""
	Is a combination of add and drops. Might delete the other two and just simplify to an add/drop
	object w/ an option list of players added and dropped
	add: add object
	drop: drop object
"""
class add_drop(Transaction):
	add = models.ForeignKey(add, verbose_name="Add")
	drop = models.ForeignKey(drop, verbose_name="Drop")
	
	def __unicode__(self):
		return u'%s, %s' % (add.__unicode__(), drop.__unicode__())
	
"""
	
"""
class Roster(models.Model):
	week = models.IntegerField(choices=WEEK_CHOICES)
	team = models.ForeignKey(Team)
	players = models.ManyToManyField(PlayerProxy)
	
	def __unicode__(self):
		return u'Week %s lineup for %s' % (week.__unicode__(), team.__unicode__())






