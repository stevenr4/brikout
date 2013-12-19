from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',


    url(r'', include('social_auth.urls')),
    
    # Examples:
    # url(r'^$', 'brikout_v1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'app.views.login'),
    url(r'^login/$', 'app.views.login'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^brikout/$', 'app.views.main'),
    url(r'^profile/$', 'app.views.profile'),
    url(r'^profile/(?P<user_id>\d+)/$', 'app.views.profile'),
    url(r'^profile/search/$', 'app.views.search_users'),
    url(r'^event/create/$', 'app.views.create_event'),
    url(r'^event/(?P<event_id>\d+)/$', 'app.views.view_event'),
    url(r'^event/search/$', 'app.views.search_events'),
    url(r'^game/(?P<game_id>\d+)/$', 'app.views.view_game'),
    url(r'^game/search/$', 'app.views.search_games'),
    url(r'^system/(?P<system_id>\d+)/$', 'app.views.view_system'),
    url(r'^system/search/$', 'app.views.search_systems'),
    url(r'^notifications/$', 'app.views.notifications'),


    # API STUFFS
    url(r'^api01/user/$', 'app.views.api_user'),
    url(r'^api01/user/auth/$', 'app.views.api_user_auth'),
    url(r'^api01/user/buddies/$', 'app.views.api_user_buddies'),
    url(r'^api01/user/system/$', 'app.views.api_user_own_system'),
    url(r'^api01/user/game/$', 'app.views.api_user_own_game'),
    url(r'^api01/event/$', 'app.views.api_event'),
    url(r'^api01/event/list/$', 'app.views.api_event_list'),
    url(r'^api01/event/attend/$', 'app.views.api_event_attend'),
    url(r'^api01/event/invite/$', 'app.views.api_event_invite'),
    url(r'^api01/call/systems/$', 'app.views.api_call_systems'),
    url(r'^api01/call/games/$', 'app.views.api_call_games'),

    # Creating fake data
    url(r'^qwertyytrewq/users/$', 'app.views.api_create_fake_users'),
    url(r'^qwertyytrewq/systems/$', 'app.views.api_call_systems'),
    url(r'^qwertyytrewq/games/$', 'app.views.api_call_games'),
    url(r'^qwertyytrewq/ignrss/$', 'app.views.api_call_ign_rss_feed'),


    # ADMIN STUFFS
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
