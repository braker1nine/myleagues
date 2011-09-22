from django.contrib import admin
from league.models import Owner, Player, Team, League, Transaction, trade, team_trade, add, drop, add_drop, Roster

admin.site.register(Owner)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(League)
admin.site.register(Transaction)
admin.site.register(trade)
admin.site.register(team_trade)
admin.site.register(add)
admin.site.register(drop)
admin.site.register(add_drop)
admin.site.register(Roster)