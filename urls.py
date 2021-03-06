from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from bookmarks.feeds import BookmarkFeed
from bookmarks.models import BookmarkInstance
from microblogging.feeds import TweetFeedAll, TweetFeedUser, TweetFeedUserWithFriends
from microblogging.models import Tweet
from swaps.models import Offer
from tagging.models import TaggedItem
from wakawaka.models import WikiPage

from pinax.apps.account.openid_consumer import PinaxConsumer
from pinax.apps.photos.models import Image
from pinax.apps.topics.models import Topic
from pinax.apps.tribes.models import Tribe

from draft.views import draft_page
from league.views import league_page, team_page, profile_page, new_user, user_created, welcome, player_page, home
from league.forms import NewLeagueWizard, NewLeague_BasicInfoForm, NewLeague_InviteFriendsForm, NewLeague_ScoringForm
from gametime.views import decision


handler500 = "pinax.views.server_error"


tweets_feed_dict = {"feed_dict": {
    "all": TweetFeedAll,
    "only": TweetFeedUser,
    "with_friends": TweetFeedUserWithFriends,
}}


bookmarks_feed_dict = {"feed_dict": {"": BookmarkFeed }}


urlpatterns = patterns("",
    #url(r"^$", direct_to_template, {
    #    "template": "welcome.html",
    #}, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    #url(r"^about/", include("about.urls")),
    #url(r"^account/", include("pinax.apps.account.urls")),
    #url(r"^openid/(.*)", PinaxConsumer()),
    #url(r"^profiles/", include("pinax.apps.profiles.urls")),
    #url(r"^bbauth/", include("pinax.apps.bbauth.urls")),
    #url(r"^authsub/", include("pinax.apps.authsub.urls")),
    url(r"^invitations/", include("friends_app.urls")),
    #url(r"^notices/", include("notification.urls")),
    #url(r"^messages/", include("messages.urls")),
    #url(r"^announcements/", include("announcements.urls")),
    #url(r"^tweets/", include("microblogging.urls")),
    #url(r"^tribes/", include("pinax.apps.tribes.urls")),
    #url(r"^comments/", include("threadedcomments.urls")),
    #url(r"^i18n/", include("django.conf.urls.i18n")),
    #url(r"^bookmarks/", include("bookmarks.urls")),
    #url(r"^photos/", include("pinax.apps.photos.urls")),
    #url(r"^avatar/", include("avatar.urls")),
    #url(r"^swaps/", include("swaps.urls")),
    #url(r"^flag/", include("flag.urls")),
    #url(r"^locations/", include("locations.urls")),
    #url(r"^feeds/tweets/(.*)/$", "django.contrib.syndication.views.feed", tweets_feed_dict),
    #url(r"^feeds/bookmarks/(.*)/?$", "django.contrib.syndication.views.feed", bookmarks_feed_dict),
    url(r"^beta/league/(?P<league_id>[a-zA-Z0-9_]{5,30})/team/(?P<team_id>[a-zA-Z0-9_]{5,30})/$", team_page),
    url(r"^beta/league/(?P<league_id>[a-zA-Z0-9_]{5,30})/draft/$", draft_page),
    url(r"^beta/league/(?P<league_id>[a-zA-Z0-9_]{5,30})/$", league_page),
    #url(r"^league/archive/(?P<league_id>[a-zA-Z0-9_]{5,30})/(?P<year>[0-9]{4})/$", league_archive),
    url(r"^beta/player/(?P<player_slug>[a-zA-Z_]{5,50})/$", player_page),
    url(r"^beta/user/(?P<user_id>[a-zA-Z0-9_]{5,20})/$", profile_page),
    url(r"^beta/new_user/$", new_user),
    url(r"^beta/new_user/created/$", user_created),
    url(r"^beta/new_league/$", NewLeagueWizard([NewLeague_BasicInfoForm])),
    url(r"^beta/gametime/$", decision),
    url(r'^beta/home/$', home),
    url(r'^threadedcomments/', include('threadedcomments.urls')),
    url(r'^beta/$', welcome),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'facebook/', include('django_facebook.urls')),
)

## @@@ for now, we'll use friends_app to glue this stuff together

friends_photos_kwargs = {
    "template_name": "photos/friends_photos.html",
    "friends_objects_function": lambda users: Image.objects.filter(is_public=True, member__in=users),
}

friends_blogs_kwargs = {
    "template_name": "blog/friends_posts.html",
    "friends_objects_function": lambda users: Post.objects.filter(author__in=users),
}

friends_tweets_kwargs = {
    "template_name": "microblogging/friends_tweets.html",
    "friends_objects_function": lambda users: Tweet.objects.filter(sender_id__in=[user.id for user in users], sender_type__name="user"),
}

friends_bookmarks_kwargs = {
    "template_name": "bookmarks/friends_bookmarks.html",
    "friends_objects_function": lambda users: Bookmark.objects.filter(saved_instances__user__in=users),
    "extra_context": {
        "user_bookmarks": lambda request: Bookmark.objects.filter(saved_instances__user=request.user),
    },
}

#urlpatterns += patterns("",
#    url(r"^photos/friends_photos/$", "friends_app.views.friends_objects", kwargs=friends_photos_kwargs, name="friends_photos"),
#    url(r"^blog/friends_blogs/$", "friends_app.views.friends_objects", kwargs=friends_blogs_kwargs, name="friends_blogs"),
#    url(r"^tweets/friends_tweets/$", "friends_app.views.friends_objects", kwargs=friends_tweets_kwargs, name="friends_tweets"),
#    url(r"^bookmarks/friends_bookmarks/$", "friends_app.views.friends_objects", kwargs=friends_bookmarks_kwargs, name="friends_bookmarks"),
#)

tagged_models = (
    dict(title="Blog Posts",
        query=lambda tag : TaggedItem.objects.get_by_model(Post, tag).filter(status=2),
        content_template="pinax_tagging_ext/blogs.html",
    ),
    dict(title="Bookmarks",
        query=lambda tag : TaggedItem.objects.get_by_model(BookmarkInstance, tag),
        content_template="pinax_tagging_ext/bookmarks.html",
    ),
    dict(title="Photos",
        query=lambda tag: TaggedItem.objects.get_by_model(Image, tag).filter(safetylevel=1),
        content_template="pinax_tagging_ext/photos.html",
    ),
    dict(title="Swap Offers",
        query=lambda tag : TaggedItem.objects.get_by_model(Offer, tag),
    ),
    dict(title="Topics",
        query=lambda tag: TaggedItem.objects.get_by_model(Topic, tag),
    ),
    dict(title="Tribes",
        query=lambda tag: TaggedItem.objects.get_by_model(Tribe, tag),
    ),
    dict(title="Wiki Articles",
        query=lambda tag: TaggedItem.objects.get_by_model(WikiPage, tag),
    ),
)
tagging_ext_kwargs = {
    "tagged_models": tagged_models,
}

#urlpatterns += patterns("",
#    url(r"^tags/(?P<tag>.+)/(?P<model>.+)$", "tagging_ext.views.tag_by_model",
#        kwargs=tagging_ext_kwargs, name="tagging_ext_tag_by_model"),
#    url(r"^tags/(?P<tag>.+)/$", "tagging_ext.views.tag",
#        kwargs=tagging_ext_kwargs, name="tagging_ext_tag"),
#    url(r"^tags/$", "tagging_ext.views.index", name="tagging_ext_index"),
#)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
