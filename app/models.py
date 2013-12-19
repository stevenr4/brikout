from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Genre(models.Model):
    name = models.TextField(max_length=127)

    def __unicode__(self):
        return self.name



class ESRB(models.Model):
    text = models.TextField(max_length=127)
    code = models.TextField(max_length=63)

    def __unicode__(self):
        return self.text


class Game(models.Model):
    name = models.TextField(max_length=127)
    api_id = models.TextField(max_length=127)
    url_image_cover = models.URLField(max_length=255,blank=True)
    url_image_screen = models.URLField(max_length=255,blank=True)

    release_date = models.DateField(blank=True,null=True)
    overview = models.TextField(max_length=4095,blank=True,null=True)
    esrb = models.ForeignKey(ESRB,blank=True,null=True,related_name="games")
    genres = models.ManyToManyField(Genre,blank=True,null=True,related_name="games")
    max_players = models.PositiveSmallIntegerField(blank=True,null=True)
    rating = models.FloatField(blank=True,null=True)
    coop = models.NullBooleanField(default=None)

    def __unicode__(self):
        return self.name

class System(models.Model):
    name = models.TextField(max_length=127)
    api_id = models.TextField(max_length=127)
    url_image = models.URLField(max_length=255,blank=True)
    games = models.ManyToManyField(Game,related_name="systems",blank=True,null=True)

    max_controllers = models.PositiveSmallIntegerField(default=1)
    rating = models.FloatField(blank=True,null=True)
    overview = models.TextField(max_length=4095,blank=True,null=True)
    def __unicode__(self):
        return self.name

class UserExtension(models.Model):

    private_user_xbox = models.BooleanField(default=True)
    private_user_psn = models.BooleanField(default=True)
    private_user_steam = models.BooleanField(default=True)
    private_user_bio = models.BooleanField(default=True)
    private_user_email = models.BooleanField(default=True)
    private_user_name = models.BooleanField(default=True)



    user = models.OneToOneField(User, related_name="ext",primary_key=True)

    fb_id = models.TextField(max_length=127)
    user_xbox = models.TextField(max_length=255,blank=True,null=True)
    user_steam= models.TextField(max_length=255,blank=True,null=True)
    user_psn  = models.TextField(max_length=255,blank=True,null=True)

    bio = models.TextField(max_length=511,blank=True)
    picture_url = models.URLField(max_length=255,blank=True,null=True)

    games = models.ManyToManyField('Game',related_name="users",blank=True)
    systems = models.ManyToManyField('System',related_name="users",blank=True)


    buddies = models.ManyToManyField('self',blank=True)


    def __unicode__(self):
        return self.user.username + "'s extension."

class Event(models.Model):
    description = models.TextField(max_length=4000, blank=True)

    title = models.TextField(max_length=511,blank=True)
    game = models.ForeignKey('Game',related_name="events",null=True,blank=True)
    game_is_any = models.BooleanField(default=False)
    system = models.ForeignKey('System', related_name="events",null=True,blank=True) ### NULL --> any game/system
    system_is_any = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(auto_now_add=False)
    owner = models.ForeignKey(User,related_name="events_started")
    attendees = models.ManyToManyField(User,related_name="events_attending",blank=True)

    private = models.BooleanField(default=True)
    invite_only = models.BooleanField(default=True)
    in_person = models.BooleanField(default=False)
    where = models.TextField(max_length=511,blank=True)

    def __unicode__(self):
        return "Event " + self.game.name + " on " + self.system.name + " during " + str(self.scheduled_time) + " | by " + self.owner.username

class EventInvite(models.Model):
    event = models.ForeignKey('Event',related_name="invites")
    requester = models.ForeignKey(User,related_name="event_invites_sent")
    receipent = models.ForeignKey(User,related_name="event_invites_received")
    message = models.TextField(max_length=1000,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Invite by " + self.requester.username + " to " + self.receipent.username + " to the event of | " + str(self.event)

class EventMessage(models.Model):
    event = models.ForeignKey('Event',related_name="messages")
    user = models.ForeignKey(User,related_name="event_messages")
    message = models.TextField(max_length=1000,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Message by " + self.user.username + " on the event: " + str(self.event)







class BuddyInvite(models.Model):
    requester = models.ForeignKey(User,related_name="buddy_invites_sent")
    receipent = models.ForeignKey(User,related_name="buddy_invites_received")
    message = models.TextField(max_length=1000,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Buddy invite by " + self.requester.username + " to " + self.receipent.username








class Chat(models.Model):
    users = models.ManyToManyField(User,related_name="chats")

    def __unicode__(self):
        return "Chat"

class ChatMessage(models.Model):
    user = models.ForeignKey(User,related_name="chat_messages")
    timestamp = models.DateTimeField(auto_now_add=True) 
    chat = models.ForeignKey(Chat, related_name="messages")
    message = models.TextField(max_length=2000,blank=True)

    def __unicode__(self):
        return "Chat message by " + self.user.username




class Notification(models.Model):
    user = models.ForeignKey(User,related_name="notifications")
    timestamp = models.DateTimeField(auto_now_add=True) 
    url = models.URLField()



class News(models.Model):
    title = models.TextField(max_length=500)
    url = models.TextField(max_length=500)
    text = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.title



