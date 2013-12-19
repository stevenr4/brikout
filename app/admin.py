from django.contrib import admin
from app.models import UserExtension, Game, Event, System, EventInvite, BuddyInvite, News


# Register your models here.
admin.site.register(UserExtension)
admin.site.register(Game)
admin.site.register(Event)
admin.site.register(System)
admin.site.register(EventInvite)
admin.site.register(News)

admin.site.register(BuddyInvite)