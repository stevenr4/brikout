from django.shortcuts import render, redirect, get_object_or_404, render_to_response
#from app.forms import LoginForm, SignupForm, EventForm
from django.contrib import auth
from django.contrib.auth.models import User
from app.models import *
import datetime

# This allows us to make a dictionary and send it to the front end
#from django.template import RequestContext  ### I can't figure out where I got this from....
from django.utils import simplejson
from django.http import HttpResponse

# This is so we can grab the url string from a reverse url lookup.
from django.core.urlresolvers import reverse


# This is for calling and parsing the xml
#from xml.etree import ElementTree as ET ### Replaced by BeautifulSoup
from bs4 import BeautifulSoup as Soup
import urllib2
from django.db.models import Q

import math
from faker import Faker
import feedparser
# Create your views here.


























####################################################################################
####################################################################################


	####    ####	############	############	####    ####      ########
	####	####	############	############	####	####	############
	####	####		####		####			####	####	####	####
	####	####		####		####			####    ####	####	
	####	####		####		############	#### ## ####	##########	
	####	####		####		############	#### ## ####	  ##########
	#####  #####		####		####			############			####
	############		####		####			############	####	####
	  ########		############	############	 ########## 	############
		####		############	############	  ###  ###  	  ########


####################################################################################
####################################################################################








# This function logs out the user and redirects them to the login page
def logout(request):
	# Log the user out
	auth.logout(request)
 
	# Redirect them to the login page
	return redirect('app.views.login')


# This displays the login page
def login(request):

	# If the user is ALREADY LOGGED in, then let's get them to the main page
	if request.user is not None and request.user.is_active:
		return redirect('app.views.main')

	# Print that we are starting this function (Great for debugging early on)
	print "Starting 'app.view.login'..."

	# Set up an output message to be able to accurately output an error
	output_message = ""
	
	# Render out the page
	return render(request, 'login.tmpl', {'output_message': output_message})


# This is the view for the main page
def main(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Print that somebody is trying to access the main page
	print "Starting 'app.views.main'..."

	news = News.objects.all()[:6]

	# Return the rendered tmpl
	return render(request, "main.tmpl",{"news":news})



# This is to display a profile page
def profile(request, user_id=None):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Print that we are starting this view
	print "Starting 'app.views.profile'..."
	print user_id

	# 
	profile_user = None


	if user_id == None:
		profile_user = request.user
	else:
		profile_user = get_object_or_404(User, pk=user_id)


	# Return the rendered tmpl
	return render(request, "profile.tmpl", {'profile_user': profile_user})



# This displays the page for the user's settings
def profile_settings(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Print that we are starting this view
	print "Starting 'app.views.profile_settings'...."

	# Make sure we are logged in
	if request.user is None or user.is_active:
		return redirect('app.views.login')
	else:
		return render(request, "profile_settings.tmpl")

# This displays the page to create an event
def create_event(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Print that we are starting this view
	print "Starting 'app.views.create_event'..."

	# Get a list of systems for the user to select
	list_of_systems = System.objects.all()

	# Render the page and send it
	return render(request,'create_event.tmpl', {'list_of_systems': list_of_systems})

# This displays the event that was given as an event_id
def view_event(request, event_id):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Get the event so we can render the page
	event = get_object_or_404(Event,pk = event_id)

	# True if you are invited
	invited = False

	u = request.user

	if u is not None and u.is_active:
		for ei in u.event_invites_received.all():
			if event == ei.event:
				invited = True

	# Render the page and send it
	return render(request,'view_event.tmpl', {'event':event, 'invited':invited})

# This will allow us to search for events to join up
def search_events(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Get the appropriate list for events <<<<<<<<<<<<<<<<<<<<<<<< TO DO <<<<<<<<<<<<<<<<<<<<<<<<<<
	# Possible Parameters
	user_id = 'any'
	game_id = 'any'
	system_id = 'any'
	sort_by = 'scheduled_time' # attendees 
	invite_only = 'any' # true false
	in_person = 'any' # true false

	if 'user_id' in request.GET:
		user_id = request.GET['user_id']
	if 'game_id' in request.GET:
		game_id = request.GET['game_id']
	if 'system_id' in request.GET:
		system_id = request.GET['system_id']
	if 'sort_by' in request.GET:
		sort_by = request.GET['sort_by']
	if 'invite_only' in request.GET:
		invite_only = request.GET['invite_only']
	if 'in_person' in request.GET:
		in_person = request.GET['in_person']


	event_query = Event.objects


	if user_id != 'any':
		event_query = event_query.filter(attendees__id=int(user_id))

	if system_id != 'any':
		event_query = event_query.filter(system__id=int(system_id))

	if game_id != 'any':
		event_query = event_query.filter(game__id=int(game_id))

	if invite_only != 'any':
		if invite_only == 'true':
			event_query = event_query.filter(invite_only=True)
		elif invite_only == 'false':
			event_query = event_query.filter(invite_only=False)

	if in_person != 'any':
		if in_person == 'true':
			event_query = event_query.filter(in_person=True)
		elif in_person == 'false':
			event_query = event_query.filter(in_person=False)

	if sort_by == 'attendees':
		event_query = event_query.order_by('-attendees')
		print "SORTING BY ATTENDEES!"
	else:
		event_query = event_query.order_by('scheduled_time')

	# Finally make the call
	event_list = event_query.all()[:10]

	# Render the page and send it
	return render(request,'search_events.tmpl', {'event_list': event_list})


# This will show the data for a certain game
def view_game(request, game_id):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Get the game so we can send it to the renderer
	game = get_object_or_404(Game, id=game_id)

	# Render the page and send it out
	return render(request,'view_game.tmpl', {'game':game})

# This will show the data for a certain system
def view_system(request, system_id):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Get the system so we can send it to the renderer
	system = get_object_or_404(System, id=system_id)

	# Render the page and send it out
	return render(request,'view_system.tmpl', {'system':system})

# Displays the page for searching for systems
def search_systems(request):
	
	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# Grab the systems to send to the page
	all_systems = System.objects.all()

	# Render the page and send it
	return render(request,'search_systems.tmpl', {'all_systems':all_systems})


# Displays the page for searching for videogames
def search_games(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	# POSSIBLE PARAMS
	advanced_search = 'false'
	page_number = 1
	page_size = 20
	name = ''
	system_id = 0
	genre = 'any'
	esrb = 'any'
	coop = 'either'
	sort_by = 'title'

	# Check if we have an advanced search
	if 'advanced' in request.GET:
		# Get it
		advanced_search = request.GET['advanced']

	# Check if we have a page number
	if 'page_number' in request.GET:
		# Set the page number
		page_number = int(request.GET['page_number'])

	# Check if we have a page_size
	if 'page_size' in request.GET:
		# Set the page size
		page_size = int(request.GET['page_size'])

	# Check if the name is being searched for
	if 'name' in request.GET:
		# Set the name
		name = request.GET['name']

	# Check if we have a system
	if 'system_id' in request.GET:
		# Set the system
		system_id = int(request.GET['system_id']);

	# Check if we have a genre
	if 'genre' in request.GET:
		# Set the genre
		genre = request.GET['genre'];

	# Check if we have esrb
	if 'esrb' in request.GET:
		# Set the esrb
		esrb = request.GET['esrb']

	# Check if we have coop
	if 'coop' in request.GET:
		# Set the coop
		coop = request.GET['coop']

	# Check if they're sorting by anything
	if 'sort_by' in request.GET:
		# Get the sort
		sort_by = request.GET['sort_by']


	### We handle the incoming data ###

	# Let's get the list by name first.
	games_query = Game.objects

	# Check if the name needs filtering
	if name != '':
		# See if the name is in the string
		games_query = games_query.filter(name__icontains=name)

	# Check if the system needs filtering
	if system_id != 0:
		# Filter the games by system
		games_query = games_query.filter(systems__id=system_id)

	# Check if the genres need filtering
	if genre != 'any':
		# Filter the games by genre
		games_query = games_query.filter(genres__name=genre)

	# Check if the esrb needs to be filtered
	if esrb != 'any':
		# Filter by esrb
		games_query = games_query.filter(esrb__code=esrb)

	# Check if we need to filter by coop
	if coop != 'either':
		# Get the boolean version of 'yes' or 'no'
		coop_bool = (coop == 'yes')
		# Filter by coop
		games_query = games_query.filter(coop=coop_bool)



	# These are the possible strings that we are sorting by:
	# title
	# popularity
	# release_date
	# max_players
	# rating


	# Last thing we do is to sort the remainder
	if sort_by == 'title':
		games_query = games_query.order_by('name')
	elif sort_by == 'popularity':
		games_query = games_query.order_by('-users')
	elif sort_by == 'release_date':
		games_query = games_query.order_by('-release_date')
	elif sort_by == 'max_players':
		games_query = games_query.order_by('-max_players')
	elif sort_by == 'rating':
		games_query = games_query.order_by('-rating')
	else:
		games_query = games_query.order_by('name')



	# Get the offset of where to start the query from
	page_offset = ((page_number - 1) * page_size)

	# Grab the list of games in our filtered query
	list_of_games = games_query.all()[page_offset:page_size + page_offset]

	# We can also get the total of PAGES from the query count
	total_games = games_query.count()

	# Pack it up..
	data = {
		'advanced_search': (advanced_search == 'true'),
		'list_of_games': list_of_games,
		'page_number': page_number,
		'page_size': page_size,
		'page_total': (((total_games - 1)//page_size) + 1),
		'total_games': total_games,
		'name':name,
		'system_id':system_id,
		'genre':genre,
		'esrb':esrb,
		'coop':coop,
		'sort_by':sort_by,
		## TTOTALLY INEFFICIENT!!! WHEN FINISHED, COME BACK AND MAKE THIS FAST!!!
		'list_of_systems':System.objects.all(),
		'list_of_genres':Genre.objects.all(),
		'list_of_esrb':ESRB.objects.all()
	}

	# Send it out...
	return render(request,'search_games.tmpl', data)


# Displays the page for searching for players
def search_users(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	print request.GET

	# These are the possible parameters
	page_size = 30
	name = ''
	event_id = 'any'
	system_id = 'any'
	game_id = 'any'
	buddy_id = 'any'

	# Check if the parameter is in the url and get it
	if 'name' in request.GET:
		name = request.GET['name']
	if 'event_id' in request.GET:
		event_id = request.GET['event_id']
	if 'system_id' in request.GET:
		system_id = request.GET['system_id']
	if 'game_id' in request.GET:
		game_id = request.GET['game_id']
	if 'buddy_id' in request.GET:
		buddy_id = request.GET['buddy_id']

	# Start up a query
	user_query = User.objects

	if name != '':# Filter the query to users that contain just the sent name string
		user_query = user_query.filter(Q(username__icontains=name) | Q(ext__user_xbox__icontains=name) | Q(ext__user_steam__icontains=name) | Q(ext__user_psn__icontains=name))

	if event_id != 'any':
		user_query = user_query.filter(events_attending__id=int(event_id))

	if system_id != 'any':
		user_query = user_query.filter(ext__systems__id=int(system_id))

	if game_id != 'any':
		user_query = user_query.filter(ext__games__id=int(game_id))

	if buddy_id != 'any':
		user_query = user_query.filter(ext__buddies__user__id=int(buddy_id))

	# Get the list of users
	user_list = user_query.all()[:30]

	# We also need to know the total amount of users
	total_users = user_query.count()

	# Pack up the data we are about to send
	data = {
		'name':name,
		'total_users': total_users,
		'list_of_users': user_list
	}

	# Send the data
	return render(request,'search_users.tmpl',data)

# The page that displays upcoming notifications
def notifications(request):

	# If the user is NOT LOGGED in, then let's get them to the login
	if request.user is None or not request.user.is_active:
		return redirect('app.views.login')

	return render(request,'notifications.tmpl')	
























































####################################################
####################################################


		####		############	############
	  ########  	############	############
	#####  #####	####	####		####
	####	####	####	####		####
	############	############		####
	############	############		####
	####	####	####				####
	####	####	####			############
	####	####	####			############


####################################################
####################################################




# # # # # ###   API SECTION   ### # # # # #



# This API returns a user's base data
def api_user(request):

	print "===============================================V V V V V V V"
	print request.GET
	print request.method
	print "===============================================^ ^ ^ ^ ^ ^ ^ "

	# The method was to get
	if request.method == "GET":


		print request.GET

		# Print that somebody made a call to this API
		print "api_user has been called!"

		user = User()

		# Check to see if a user_id was given
		if "user_id" in request.GET:
			# Get the user
			user = get_object_or_404(User, pk=request.GET['user_id'])
		else:
			#Get the logged in user
			user = request.user

			#Check to see if the user is valid
			if user is None or not user.is_active:
				return HttpResponse(simplejson.dumps({'success':False,'reason':"Logged in user isn't valid"}))

		# Create small data to send
		list_of_games = []
		for g in user.ext.games.all():
			list_of_games.append({'name':g.name,'id':g.id,'api_id':g.api_id})
		# Create small data to send
		list_of_systems = []
		for s in user.ext.systems.all():
			list_of_systems.append({'name':s.name,'id':s.id,'api_id':s.api_id})
		list_of_buddies = []
		for b in user.ext.buddies.all():
			list_of_buddies.append({'username':b.user.username,'user_id':b.user.id})

		# This is a dictionary of the data we are going to send back.
		dict_to_send = {
			"username": user.username,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"email": user.email,
			"is_superuser": user.is_superuser,
			"last_login": str(user.last_login),
			"date_joined": str(user.date_joined),
			"fb_id": user.ext.fb_id,
			"user_xbox": user.ext.user_xbox,
			"user_steam": user.ext.user_steam,
			"user_psn": user.ext.user_psn,
			"bio": user.ext.bio,
			"picture_url": user.ext.picture_url,
			"games": list_of_games,
			"systems": list_of_systems,
			'buddies': list_of_buddies,
			"_sent_params": request.GET,
			"success": True
		}

		print "ABOUT TO RETURN!!!"

		# Change the json into a string.
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')


	# Now we check if it's a post instead
	elif request.method == "POST":

		print "The method was a post"

		# Set a blank user, we fill it with the next if/else
		u = User()

		# If there is no 'user_id', then it means we are creating a new user
		if 'user_id' not in request.POST:

			print "Grabbing user..."
			# No user was sent, let's check if the current user is logged in
			u = request.user


			print "Checking user"
			if u is not None and u.is_active:

				print "The user is logged in"
				# The user is logged in, so we must be updating their data
				pass
			else:
				print "The user is not logged in"

				# Let's get the user's information to create the user
				username = request.POST['username']
				print username

				password = request.POST['password']

				print password

				# Create the user with a blank email
				u = User.objects.create_user(username,'',password)
				u.save()

				print u

				ue = UserExtension(user = u)

				ue.save()

				print ue


		# There is a 'user_id' included in the data, so we will try to update that user
		else:


			# Get the user
			u = get_object_or_404(User, pk=request.POST['user_id'])

		# Print that we got this far
		print "Creating/Changing " + u.username

		# Go through the variables, and fill in what we can IF it was in the POST
		if 'first_name' in request.POST:
			u.first_name = request.POST['first_name']
		if 'last_name' in request.POST:
			u.last_name = request.POST['last_name']
		if 'email' in request.POST:
			u.email = request.POST['email']
		if 'user_xbox' in request.POST:
			u.ext.user_xbox = request.POST['user_xbox']
		if 'user_steam' in request.POST:
			u.ext.user_steam = request.POST['user_steam']
		if 'user_psn' in request.POST:
			u.ext.user_psn = request.POST['user_psn']
		if 'bio' in request.POST:
			u.ext.bio = request.POST['bio']
		if 'picture_url' in request.POST:
			u.ext.picture_url = request.POST['picture_url']

		print "Made it past 'IF HELL'"
		# Now we save the updated and created user.
		u.save()
		u.ext.save()

		print u.ext.bio

		print "about to send back..."
			
		# Last, we return that it was successful and what the username is
		return HttpResponse(simplejson.dumps({'success':True,'username':u.username,'user_id': u.id,'params':request.POST}), mimetype='application/javascript')
	return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')


# This API authenticates a user's login or checks the status
def api_user_auth(request):

	# Let's create an empty dictionary to send at the end of this function
	dict_to_send = {}

	# Check if the caller is asking for information on the user
	if request.method == "GET":

		# Check if the caller is asking on it self or a different user
		if 'user_id' in request.GET:

			# Check if that user exists in the database
			if User.objects.filter(pk=request.GET['user_id']):

				# The user exists, now check if it is still active
				u = User.objects.get(pk=request.GET['user_id'])

				if u is not None and u.is_active:

					# Great, now we can send the status of the user!
					dict_to_send = {
						'success': True,
						'params': request.GET,
						'user_online': u.is_authenticated()
					}
				else:
					# Looks like the user is invalid
					dict_to_send = {
						'success': False,
						'params': request.GET,
						'reason': "Selected user was invalid."
					}
			else:

				# That object doesn't exist
				dict_to_send = {
					'success': False,
					'params': request.GET,
					'reason': "Selected user does not exist in the database."
				}
		else:

			# We're trying to get the logged in user.
			u = request.user

			# Check if the user is valid
			if u is not None and u.is_active:

				# Great, now we can send the status of the user!
				dict_to_send = {
					'success': True,
					'params': request.GET,
					'user_online': u.is_authenticated()
				}
			else:
				# Looks like the user is invalid
				dict_to_send = {
					'success': False,
					'params': request.GET,
					'reason': "Not logged into a valid user."
				}
	elif request.method == "POST":
		# The user is looking to log in or log out

		# Make sure the user sent a 'login' parameter, it is required
		if 'login' not in request.POST:
			dict_to_send = {
				'success': False,
				'params': "PASSWORD PROTECTED",
				'reason': "'login' parameter was not set!"
			}
		elif request.POST['login'] not in ('true','false'):  ######### *NOTE: The boolean returns back as a string!!!
			print request.POST['login']
			dict_to_send = {
				'success': False,
				'params': "PASSWORD PROTECTED",
				'reason': "'login' was not a boolean."
			}
		else:


			# Now we know if they are logging in or logging out. Let's handle both of those
			if request.POST['login'] == 'true':

				# Make sure we have a username and a password
				if 'username' not in request.POST or 'password' not in request.POST:
					dict_to_send = {
						'success': False,
						'params': "PASSWORD PROTECTED",
						'reason': "'username' and 'password' MUST be present when trying to login."
					}
				else:

					# Let's try to get the user from authentication
					u = auth.authenticate(username=request.POST['username'],password=request.POST['password'])

					# Now, let's see if that user is real AND it is active
					if u is not None and u.is_active:

						print "SUCCESSSS!!!"

						# GREAT! Let's log the the user end and send back a big fat SUCCESS!!
						auth.login(request,u)

						dict_to_send = {
							'success': True,
							'params': "PASSWORD PROTECTED",
							'user_id': u.id,
							'url': reverse('app.views.main')
						}

						print "SUPER SUCCESS!!!"
					else:
						# The user was not authenticated properly, wrong username or password
						dict_to_send = {
							'success': False,
							'params': "PASSWORD PROTECTED",
							'reason': "Username and password did not match."
						}
			else:
				# They are trying to log out, so log them out
				auth.logout(request)

				# Return a successful data
				dict_to_send = {
					'success': True,
					'params': request.POST
				}

	print "RETURNING: " + str(dict_to_send)
				
	return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")





# This API returns a list or adds/removes a buddy
def api_user_buddies(request):

	# Check if the method is a get
	if request.method == "GET":

		# Set a blank user, we fill it with the next if/else
		u = User()

		# If there is no 'user_id', then it means we use the logged in user
		if 'user_id' not in request.GET:

			# Create the user with a blank email
			u = request.user

		# There is a 'user_id' included in the data, so we will try to update that user
		else:
			
			# Get the user
			u = get_object_or_404(User, pk=request.GET['user_id'])



		if u is None or not u.is_active:
			return HttpResponse(simplejson.dumps({'success':False,'reason':"User is not valid."}), mimetype='application/javascript')
		else:

			# Create a temporary list to hold the buddies for us to send
			list_of_buddies = []
			for ue in u.ext.buddies.all():
				list_of_buddies.append({'username':ue.user.username,'user_id':ue.user.id})

			# Put all that data together in a clean dict
			dict_to_send = {
				'success':True,
				'buddies':list_of_buddies,
				'params':request.GET
			}

			# Send the dictionary!
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
	

	elif request.method == "POST":

		# buddy_id needs to be in the data for this to work. It is the buddy the user is adding
		if 'buddy_id' not in request.POST:
			return HttpResponse(simplejson.dumps({'success':False,'reason':"'buddy_id' is required to add a friend"}), mimetype='application/javascript')
		else:

			# Set a blank user, we fill it with the next if/else
			u = User()

			# If there is no 'user_id', then it means we are using the pre-existing user
			if 'user_id' not in request.POST:

				# Just get the user that is logged in
				u = request.user

			# There is a 'user_id' included in the data, so we will try to update that user
			else:
				
				# Get the user
				u = get_object_or_404(User, pk=request.POST['user_id'])


			# Now we check if the user who is adding a buddy is legit
			if u is None or not u.is_active: # NOT LEGIT, Send error json
				return HttpResponse(simplejson.dumps({'success':False,'reason':"User is not valid."}), mimetype='application/javascript')
			else: # IS LEGIT continue getting the buddy

				# Get the buddy ID so we can add them together
				b = get_object_or_404(User, pk=request.POST['buddy_id'])

				# A small variable to hold a string so we know what happened
				what_happened = ""

				# Now we see if we're adding or removing
				if 'unbuddy' in request.POST:

					# The unbuddy tag means we're removing this buddy from the list
					u.ext.buddies.remove(b.ext)
					
					what_happened = "removed"
				else:
					# Add him to the buddies 
					u.ext.buddies.add(b.ext)

					what_happened = "added"

				# Save everything, just to be sure
				u.ext.save()

				# Return the success json
				return HttpResponse(simplejson.dumps({'success':True,'reason':"The user " + u.username + " has " + what_happened + " " + b.username + " to/from their buddies list."}), mimetype='application/javascript')

	return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')



# This API returns a single event or creates a single event
def api_event(request):
	print request.POST

	# The user is requesting an event
	if request.method == "GET":

		# Make sure the user has specified which event they are trying to pull from
		if 'event_id' not in request.GET:

			#The user didn't specify an event, send them an error json
			return HttpResponse(simplejson.dumps({'success':False,'reason':"'event_id' is required when GETting an event."}), mimetype='application/javascript')

		# Let's get the event to send to the user
		e = get_object_or_404(Event,pk=request.GET['event_id'])

		# Create a list of attendees
		list_of_attendees = []
		for a in e.attendees.all():
			list_of_attendees.append({'username':a.username,'user_id':a.id})

		# Create a dict of the event's data to send to the user
		dict_to_send = {
			'title': e.title,
			'game': {
				'name': e.game.name,
				'game_id': e.game.id
			},
			'system': {
				'name': e.system.name,
				'system_id':e.system.id
			},
			'scheduled_time': str(e.scheduled_time),
			'owner':{
				'username': e.owner.username,
				'user_id': e.owner.id
			},
			'attendees': list_of_attendees,
			'private': e.private,
			'invite_only': e.invite_only,
			'in_person': e.in_person,
			'where': e.where,
			'success': True
		}

		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')

	# The user is creating an event OR updating an existing one.
	elif request.method == "POST":

		# Let's make sure the user is logged into a valid account before we do anything else
		u = request.user
		if u is None or not u.is_active:
			dict_to_send = {
				"success":False,
				'params':request.POST,
				'reason':"The user wasn't logged into a valid account"
			}
		else:
			# Create a variable to store the event.
			event = Event()
			print "Creating an event"


			# Check if the event_id was passed, this determines weither we will create a new event or not
			if 'event_id' not in request.POST:

				print "event_id was not supplied"

				# Make sure all the required variables are present to make a new event
				if 'millisecs' not in request.POST:
					dict_to_send = {
						'success': False,
						'params': request.POST,
						'reason': "There needs to be a 'millisecs' in the parameters."
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
				else:
					print "Adding owner : " + u.username
					# We now know we have the required data to make the event, we need an event owner
					event.owner = u
			else:
				# An event ID was supplied, let's retrieve the event to update
				event = get_object_or_404(Event,pk=str(request.POST['event_id']))

			# Now let's grab the data out of the post and put it into the event
			if 'title' in request.POST:
				print request.POST['title']
				event.title = request.POST['title']

			if 'game_id' in request.POST:
				game_id = request.POST['game_id']
				if game_id.isdigit():
					game = get_object_or_404(Game,pk=str(request.POST['game_id']))
					event.game = game
				else:
					event.game_is_any = True
					game = get_object_or_404(Game,pk='1')
					event.game = game
			else:
				event.game_is_any = True
				game = get_object_or_404(Game,pk='1')
				event.game = game

			if 'system_id' in request.POST:
				system_id = request.POST['system_id']
				if system_id.isdigit():
					system = get_object_or_404(System, pk=str(request.POST['system_id']))
					event.system = system
				else:
					event.system_is_any = True
					event.system = get_object_or_404(System,pk='1')

			else:
				event.system_is_any = True
				event.system = get_object_or_404(System,pk='1')

			if 'millisecs' in request.POST:
				millisecs = request.POST['millisecs']
				dt = datetime.datetime.fromtimestamp(int(millisecs)//1000)
				event.scheduled_time = dt
			if 'private' in request.POST:
				event.private = True if request.POST['private'] == 'true' else False
			if 'invite_only' in request.POST:
				event.invite_only = True if request.POST['invite_only'] == 'true' else False
			if 'in_person' in request.POST:
				event.in_person = True if request.POST['invite_only'] == 'true' else False
			if 'where' in request.POST:
				event.where = request.POST['where']
			if 'description' in request.POST:
				event.description = request.POST['description']

			# Now that we have the information from the data that was sent, we will save the event
			event.save()

			# Now that it's saved, let's add the owner to the list of attending
			event.attendees.add(u)


			##########################################
			#### FOR LOOP TO ADD INVITES TO USERS ####
			##########################################
			print "Checking Invites"
			print "Array: " + str(request.POST.getlist('invites[]'))
			print "Length: " + str(len(request.POST.getlist('invites[]')))
			# Get the IDs of all the buddies send
			invite_list = request.POST.getlist('invites[]')
			# Loop through all the IDs
			for i in invite_list:
				print "Starting; " + str(i)
				# Get the buddy, don't use get_object_or_404 because that 404s!!!
				if User.objects.filter(pk=i).exists():
					# Snag the buddy
					b = User.objects.get(pk=i)
					print b.username
					# Create an invite for the buddy
					ei = EventInvite(
						requester=u,
						receipent=b,
						event=event,
						message=u.username + " invited you to the event " + event.title
					)
					print ei.requester.username
					# Finally, save the event invite
					ei.save()
					print "Saved..."


			print "Event created and saved"
			# Because we reached here, we will return a successful reply
			dict_to_send = {
				'success': True,
				'event_id': event.id,
				'params': request.POST,
				'url': reverse('app.views.view_event', args=(event.id,))
			}
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
	else:
		return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')
	
#This has been taken care of in the view.
def api_event_list(request):
	pass

# This API allows a user to attend or accept an invite, also gets a list of events the user is attending.
def api_event_attend(request):

	# Gets users going to an event
	if request.method == "GET":

		# We can either get the events the user is going to or users going to the event
		if 'event_id' in request.GET:

			# We can now get the event from the event_id
			event = get_object_or_404(Event,pk=request.GET['event_id'])
			# We need to declare a variable to store the list of users into
			list_of_users = []

			# Now we need to know if we're getting the users that are attending or
			# the list of buddies that aren't attending
			if 'buddies_not_attending' in request.GET:
				
				# Let's make sure the value is true
				if request.GET['buddies_not_attending'] == 'true':
					
					# The user needs to be logged in for this to work
					u = request.user
					
					if u is not None and u.is_active:

						# Let's get the buddies and the attending users
						all_buddy_extensions = u.ext.buddies.all()
						all_attending_users = event.attendees.all()

						# Now we can sort through them
						for buddy_ext in all_buddy_extensions:
							# Let's get only the buddies that are NOT attending
							if buddy_ext.user not in all_attending_users:

								already_invited = False
								# WAIT! WE FORGOT TO CHECK IF THEY'RE ALREADY INVITED!!
								for ei in buddy_ext.user.event_invites_received.all():
									if ei.event == event:
										already_invited = True

								if already_invited == False:
									# Let's add it to the list
									list_of_users.append(buddy_ext.user)
								else:
									# THe user has already been invited
									pass
					else:
						# We can't get the buddies from somebody who is not logged in
						dict_to_send = {
							'success': False,
							'params': request.GET,
							'reason': "The user needs to be logged in to get a buddy list"
						}
				else:
					# We can just get the list normally
					list_of_users = event.attendees.all()
			else:
				# There was no 'buddies_not_attending, let's get the normal list
				list_of_users = event.attendees.all()


			# Now that we have the correct list of users, let's get just the data we need
			list_of_user_data = []

			# Let's go through the list
			for u in list_of_users:
				# Append the data that we will need
				list_of_user_data.append({'username':u.username,'id':u.id})

			# Now it's time to send the data
			dict_to_send = {
				'success': True,
				'params': request.GET,
				'list_of_users': list_of_user_data
			}

			# Send our data
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")


		
	elif request.method == "POST":
		
		# Let's first make sure the user is legit
		u = request.user
		
		# Now let's check to see if the user is valid
		if u is None or not u.is_active:
			#Return that the user was invalid
			return HttpResponse(simplejson.dumps({'success':False,'reason':"The user is not valid."}), mimetype='application/javascript')
		
		# We need the event that the user is accepting
		if 'event_id' not in request.POST:
			return HttpResponse(simplejson.dumps({'success':False,'reason':"An 'event_id' must be given."}), mimetype='application/javascript')
		
		# Get the event
		e = get_object_or_404(Event,id=request.POST['event_id'])



		# Let's check if they are leaving this event
		if 'leave' in request.POST:
			if request.POST['leave'] == 'true':
				# Let's see if they're attending the event before we try to remove them
				if u in e.attendees.all():
					e.attendees.remove(u)
					dict_to_send = {
						'success': True,
						'params': request.POST
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
				else:
					dict_to_send = {
						'success': False,
						'reason':"The user wasn't attending this event in the first place."
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")


		# Check if there are any invites we need to delete
		if u.event_invites_received.filter(event=e).exists():
			# We have a valid user. Let's delete all invites associated to this user attending this event
			u.event_invites_received.filter(event=e).delete()
			print "Delete invites"

		# Now we can add them to the event
		e.attendees.add(u)

		# We're all done here, wrap it up and send it out
		dict_to_send = {
			'success': True,
			'params': request.POST
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")

	else:
		return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')



# This API can pull a list of a user's invites, invites for an event, or create a new invite.
def api_event_invite(request):

	# Check to see what the method was
	if request.method == "GET":
		# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<RETURN LIST
		pass
	elif request.method == "POST":
		print "A"
		# Make sure somebody is logged in
		u = request.user
		if u is None or not u.is_active:
			# The user is invalid, return the error
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"The user either isn't logged in or is invalid"}), mimetype="application/javascript")
		print "B"
		# Make sure that we were given a buddy_id to invite
		if 'buddy_id' not in request.POST:
			# There wasn't a buddy to send the event invite to
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"There needs to be a 'buddy_id' in the parameters."}), mimetype="application/javascript")
		print "C"
		# Let's try to get that buddy User
		b = get_object_or_404(User,pk=request.POST['buddy_id'])
		print "D"
		# Now we need that event that the buddy is being sent to
		if 'event_id' not in request.POST:
			# There wasn't an event_id in the data, send an error
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"There needs to be a 'event_id' in the parameters."}), mimetype="application/javascript")
		print "E"
		# Now let's get that event
		e = get_object_or_404(Event,id=request.POST['event_id'])
		print "F"
		# Now that we have all that, there's one last parameter we need to take care of
		message = u.username + " would like to invite you to " + e.title + '.'
		print "G"
		# We will overrite the message if the user put in a message
		if 'message' in request.POST:
			# We know we have a message, now let's make sure it is filled in
			if len(request.POST['message']) > 0:
				# There was a message, use the user created message
				message = request.POST['message']
		print "H"
		# Before we create an invitation, we should check if there already is one
		if EventInvite.objects.filter(requester=u,receipent=b,event=e).exists():
			# We should not create this event invite, send a failure
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"The invite already exists."}), mimetype="application/javascript")

		# Now we create the invite
		ei = EventInvite(requester=u,receipent=b,event=e,message=message)
		print "H2"
		# ...and save it
		ei.save()
		print "I"
		# Prepare the success data
		dict_to_send = {
			'success':True,
			'params':request.POST,
			'event_invite_id':ei.id
		}
		print "J"
		# Send back the success
		return HttpResponse(simplejson.dumps(dict_to_send),mimetype="application/javascript")


	else:
		return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')

# This api gets the owned games of the user or adds/removes a game from their list of games
def api_user_own_game(request):
	if request.method == "GET":
		pass
	elif request.method == "POST":

		# The user is trying to own/disown a game. Let's first check to see if the user is valid
		u = request.user

		# Check the validity of the user
		if u is None or not u.is_active:
			# The user is not valid, send back error message
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"The user either isn't logged in or is invalid"}), mimetype="application/javascript")

		# Now we make sure they sent a 'game_id'
		if 'game_id' not in request.POST:
			# 'game_id' is not present, return the error
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"'game_id' needs to be present!"}), mimetype="application/javascript")
	
		# Let's get that game
		s = get_object_or_404(Game,pk=request.POST['game_id'])

		# Last step is to claim OR disown the game for the user
		if 'disown' in request.POST:
			if request.POST['disown'] == 'true':
				# We are disowning, let's remove it.
				if s in u.ext.games.all():
					# Remove the game
					u.ext.games.remove(s)
					# Send out a success response
					dict_to_send = {
						'success': True,
						'params': request.POST,
						'game_id': s.id
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
				else:
					# The game isn't even owned, send that error
					dict_to_send = {
						'success': False,
						'params': request.POST,
						'reason': "The game cannot be removed if it's not in the list."
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
			else:
				# Disown is something other than true, let's just go to adding it to the list
				pass
		else:
			# Disown was not in the request, move on to adding it to the list
			pass

		# We are now adding the game to the list of games owned by the user.

		# Check to make sure it's not already in the list
		if s in u.ext.games.all():
			# It's already in the games list, send the error
			dict_to_send = {
				'success': False,
				'params': request.POST,
				'reason': "The game cannot be added if it's already int the list."
			}
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
		else:
			# Everything matches up, let's add it and send the success
			u.ext.games.add(s)

			# Wrap it up....
			dict_to_send = {
				'success': True,
				'params': request.POST,
				'game_id': s.id
			}
			# Send it out...
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")


	else:
		return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')


# This api gets the owned systems of the user OR adds/removes a system from their lost of owned systems
def api_user_own_system(request):
	if request.method == "GET":
		pass
	elif request.method == "POST":

		# The user is trying to own/disown a system. Let's first check to see if the user is valid
		u = request.user

		# Check the validity of the user
		if u is None or not u.is_active:
			# The user is not valid, send back error message
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"The user either isn't logged in or is invalid"}), mimetype="application/javascript")

		# Now we make sure they sent a 'system_id'
		if 'system_id' not in request.POST:
			# 'system_id' is not present, return the error
			return HttpResponse(simplejson.dumps({'success':False,'params':request.POST,'reason':"'system_id' needs to be present!"}), mimetype="application/javascript")
	
		# Let's get that system
		s = get_object_or_404(System,pk=request.POST['system_id'])

		# Last step is to claim OR disown the system for the user
		if 'disown' in request.POST:
			if request.POST['disown'] == 'true':
				# We are disowning, let's remove it.
				if s in u.ext.systems.all():
					# Remove the system
					u.ext.systems.remove(s)
					# Send out a success response
					dict_to_send = {
						'success': True,
						'params': request.POST,
						'system_id': s.id
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
				else:
					# The system isn't even owned, send that error
					dict_to_send = {
						'success': False,
						'params': request.POST,
						'reason': "The system cannot be removed if it's not in the list."
					}
					return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
			else:
				# Disown is something other than true, let's just go to adding it to the list
				pass
		else:
			# Disown was not in the request, move on to adding it to the list
			pass

		# We are now adding the system to the list of systems owned by the user.

		# Check to make sure it's not already in the list
		if s in u.ext.systems.all():
			# It's already in the system, send the error
			dict_to_send = {
				'success': False,
				'params': request.POST,
				'reason': "The system cannot be added if it's already int the list."
			}
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
		else:
			# Everything matches up, let's add it and send the success
			u.ext.systems.add(s)

			# Wrap it up....
			dict_to_send = {
				'success': True,
				'params': request.POST,
				'system_id': s.id
			}
			# Send it out...
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")


	else:
		return HttpResponse(simplejson.dumps({'success':False,'reason':"The method used was not POST or GET"}), mimetype='application/javascript')


# This API returns the list of systems in the database
def api_system_list(request):

	# This can ONLY be a get request
	if request.method == "GET":

		# We're getting all the systems, so let's get started
		list_of_systems = System.objects.all()

		# We need a list for just the data that we plan to send
		list_of_system_data = []

		# Loop through the systems to get JUST the name and ID
		for system in list_of_systems:
			# Append what we want to the list of system data
			list_of_system_data.append({
					'name': system.name,
					'id': system.id
				})

		# Get together the data that we plan to send
		dict_to_send = {
			'success': True,
			'list_of_systems': list_of_system_data
		}

		# Send out the data
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")

	else:
		# The request was NOT a GET, send that fact
		dict_to_send = {
			'success': False,
			'reason': "The request method must be a GET"
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")




# This is to get the list of games (id and name) by just a string (name)  ** LIMITED TO 50
def api_game_list(request):

	# This can ONLY be a get request
	if request.method == "GET":

		# We NEED to have a 'name' parameter
		if 'name' not in request.GET:

			# There was no search name string, the array would be too big to give all games, send error
			dict_to_send = {
				'success': False,
				'params': request.GET,
				'reason': "There needs to be a 'name' in the GET parameters."
			}

			# Send out the error
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")

		# Get the name now that we know it exists
		name = request.GET['name']

		# Check that the name is not '' and that it has some length to it
		if len(name) <= 2:

			# Send out that the request failed because the name was empty or too short
			dict_to_send = {
				'success': False,
				'params': request.GET,
				'reason': "The 'name' parameter was either an empty string or too short"
			}

			# Send out the error
			return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")

		# We have what we need to look up the list of games, let's create the query
		list_of_games = Game.objects.filter(name__icontains=name).all()[:50] # **********************  THIS IS WHERE WE LIMIT IT

		# We need a variable to save our data to before we send it
		list_of_game_data = []

		# Let's get JUST the names and IDs of those games
		for game in list_of_games:

			# Add(append) into the array as an object
			list_of_game_data.append({
				'name':game.name,
				'id':game.id})

		# Set up the dict of the data that we want
		dict_to_send = {
			'success': True,
			'list_of_games': list_of_game_data,
			'params': request.GET
		}

		# Send the data
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")
	else:
		# The request was NOT a GET, send that fact
		dict_to_send = {
			'success': False,
			'reason': "The request method must be a GET"
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype="application/javascript")































































####################################################################
####################################################################


	########		############	############	############
	##########		############	############	############
	####  ######	####	####		####		####	####
	####	####	####	####		####		####	####
	####	####	############		####		############
	####	####	############		####		############
	####	####	####	####		####		####	####
	####  ######	####	####		####		####	####
	##########		####	####		####		####	####
	########		####	####		####		####	####



####################################################################
####################################################################






# This api, when called, gets all the systems and updates the database
def api_call_systems(request):

	# This is dangerous as anybody who knows this URL can do this command
	if request.method == 'GET':

		# We create the request pointed to the api to get all of the platforms
		req = urllib2.Request("http://thegamesdb.net/api/GetPlatformsList.php")
		# This is a workaround so the API own't 403-FORBIDDEN us from it
		req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
		# Now we try to 'open' the url and grab the response
		response = urllib2.urlopen(req)

		# Let's try to open up the response into a soup
		soup = Soup(response)

		# Go through every single platform and get its data
		for platform in soup.findAll({'platform': True}):

			# We get the api_id from the platform, because this is what we need if we want more info
			print "NEXT"
			api_id = platform.find('id').contents[0]
			print api_id

			# Now we get the name of the system
			name = platform.find('name').contents[0]
			print name

			# This is so we can assign a system in an if-statement and use it after
			s = System()

			# Check to see if this platform already exists in our database
			if System.objects.filter(api_id=api_id).exists():

				# We already have the data, so we're just updating what we have
				print "We're getting duplicate data... UPDATING: " + api_id + " - " + name
				s = get_object_or_404(System,api_id=api_id)
			else:
				# Since we don't have this one, we're just gonna create a new one
				print "Creating system to save: " + api_id + " - " + name
				s = System()

			# Assign the name and api_id we got earlier
			s.name = name
			s.api_id = api_id


			# Now we're going to have to do another request for the specific platform for more data.
			inner_req = urllib2.Request("http://thegamesdb.net/api/GetPlatform.php?id=" + api_id)
			inner_req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
			inner_response = urllib2.urlopen(inner_req)

			inner_soup = Soup(inner_response)


			platform_data = inner_soup.find('platform')

			# Since not all platforms have an overview, check if our current one does
			if platform_data.find('overview') is None:
				print "This platform doesn't have an overview.."
			else:
				print "This platform has an overview!"
				s.overview = platform_data.find('overview').contents[0]
				
			# Now we check for a rating if it's in our system.
			if platform_data.find('rating') is None:
				print "This platform doesn't have a rating..."
			else:
				print "This platform has a rating!"
				s.rating = platform_data.find('rating').contents[0]

			# Last part of our FOR loop is to save the data.
			s.save()


		# AFTER FOR LOOP
		# Create the dictionary to return a success
		dict_to_send = {
			'success':True,
			'params': request.GET
		}
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')
	return HttpResponse(simplejson.dumps({'success':False,'reason':"STOP"}), mimetype='application/javascript')







# This api, when called, goes through all of the systems and grabs all of their related games and matches them to the systems
def api_call_games(request):

	# This is dangerous as anyone who knows this URL can activate this command
	if request.method == 'GET':

		game_counter = 0

		# This will be our default amount of games per system
		amount = 5

		# We can overwrite this with a GET parameter
		if 'amount' in request.GET:
			amount = int(request.GET['amount'])


		# Go through all the systems, we will need them to get the games list for that system
		for system in System.objects.all():

			# Concatenate the URL to the final url
			print "Calling thegamesdb.net for the games related to: " + system.name + " - api_id:" + system.api_id
			request_url = "http://thegamesdb.net/api/GetPlatformGames.php?platform=" + system.api_id
			print request_url
			
			# Make a request with that url and do the attach header so the server won't 403 us
			req = urllib2.Request(request_url)
			req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
			response = urllib2.urlopen(req)

			# Get the soup of the response
			soup = Soup(response)


			# Now, we look for every single game in that response
			for game in soup.findAll({'game': True})[:amount]:##############################################################################################

				# This is just a counter to count the amount of games we've looped through
				game_counter += 1
				# This is just a user friendly loading bar
				print "Progress: " + str(game_counter//182) + "%  " + ("....." + str(game_counter))[-5:] + "/18200 - |" + ("#" * (game_counter//250)) + ("." * ((18200 - game_counter)//250)) + '|'

				# Find the id and save it
				api_id = game.find('id').contents[0]
				# Save the name (title) aswell
				name = game.find('gametitle').contents[0]

				# We create an empty game variable to save the data in an if-statement for later
				g = Game()

				# We check if there is already an instance of the object
				if Game.objects.filter(api_id=api_id).exists():
					# There already is one in the database, let's get that one to update it
					print system.name + " -We're getting duplicate data... : " + api_id + " - " + name
					g = get_object_or_404(Game,api_id=api_id)
					g.name = name
				else:
					# There wasn't a game in the database, let's create a new one with the api id and  name
					print system.name + " -             -------------------      Creating game to save: " + api_id + " - " + name
					g = Game(name=name,api_id=api_id)
					g.save()
					system.games.add(g)



					# Now that we have the game, we will try to pull MORE data from that said game...
					inner_req = urllib2.Request("http://thegamesdb.net/api/GetGame.php?id=" + api_id)
					inner_req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
					inner_response = urllib2.urlopen(inner_req)
					inner_soup = Soup(inner_response)
					game_data = inner_soup.find('game')


					# release_date
					if game_data.find('releasedate') is not None:
						release_date_text = game_data.find('releasedate').contents[0]  #   '02/24/2007'
						release_date_list = release_date_text.split('/')               # ['02','24','2007']
						print "Found release date: " + str(release_date_list)
						if len(release_date_list) == 3:
							release_date = datetime.date(
								year=int(release_date_list[2]),
								month=int(release_date_list[0]),
								day=int(release_date_list[1]))
							g.release_date = release_date
							print release_date
						else:
							print "Release date is not in a correct format."
					else:
						print "No release date"
						print "-"

					# overview
					if game_data.find('overview') is not None:
						g.overview = game_data.find('overview').contents[0]
						print "There was an overview."
					else:
						print "There was not an overview"

					# esrb
					if game_data.find('esrb') is not None:
						rating_string = game_data.find('esrb').contents[0]      #  'M - Mature'
						rating_list = rating_string.split(' - ')                # ('M', 'Mature')
						if ESRB.objects.filter(code=rating_list[0]).exists():
							print "ESRB given: " + rating_string
							esrb = ESRB.objects.get(code=rating_list[0])
							g.esrb = esrb
						else:
							print "------------------------------ESRB CREATED: " + rating_string
							esrb = ESRB(
								text=rating_list[1], # 'Mature'
								code=rating_list[0]  # 'M'
							)
							esrb.save()
							g.esrb = esrb
					else:
						print "No ESRB given"

					# genres
					if game_data.find('genres') is not None:
						tmp_genres = ""
						for genre_data in game_data.find('genres').findAll('genre'):
							genre_string = genre_data.contents[0]
							tmp_genres += genre_string + "  "
							if Genre.objects.filter(name=genre_string).exists():
								genre = Genre.objects.get(name=genre_string)
								g.genres.add(genre)
							else:
								print "---------------------------------------GENRE CREATED: " + genre_string
								genre = Genre(name=genre_string)
								genre.save()
								g.genres.add(genre)
						print "Genres given: " + genre_string
					else:
						print "No Genres were given"


					# max_players
					if game_data.find('players') is not None:
						max_players_string = game_data.find('players').contents[0]
						max_players = int(max_players_string.replace('+',''))
						g.max_players = max_players
						print "Max Players: " + str(max_players)
					else:
						print "No maximum players given"

					# rating
					if game_data.find('rating') is not None:
						g.rating = float(game_data.find('rating').contents[0])
						print "Rating: " + str(g.rating)
					else:
						print "No rating given"

					# coop
					if game_data.find('co-op') is not None:
						g.coop = (game_data.find('co-op').contents[0] == "Yes") # True or false
						print "Co-op: " + game_data.find('co-op').contents[0]
					else:
						print "No coop given."

					# Images
					if game_data.find('images') is not None:
						images = game_data.find('images')

						# Boxart
						if images.find('boxart', attrs={'side':'front'}) is not None:
							g.url_image_cover = images.find('boxart', attrs={'side':'front'}).contents[0]

						# Sceenshot
						if images.find('screenshot') is not None:
							if images.find('screenshot').find('original') is not None:
								g.url_image_screen = images.find('screenshot').find('original').contents[0]


					print "Saving..."
					g.save()



		# Dictionary of data to send back a successful run
		dict_to_send = {
			'success':True,
			'params': request.GET,
			'games': game_counter
		}

		# Send the success data
		return HttpResponse(simplejson.dumps(dict_to_send), mimetype='application/javascript')


	return HttpResponse(simplejson.dumps({'success':False,'reason':"STOP"}), mimetype='application/javascript')



# This function populates us with so many random users
def api_create_fake_users(request):

	fake = Faker()

	for i in xrange(100):
		print str(i) + "++++++++++++++++++++++++++++++++++++++++++++++++++ Creating another user..."
		u = User.objects.create_user(
			fake.user_name(),
			fake.email(),
			'c'
		)
		u.save()
		print u.username
		ue = UserExtension(
			user= u,
			fb_id= 1,
			user_xbox= fake.user_name(),
			user_steam= fake.user_name(),
			user_psn= fake.user_name(),
			bio= fake.text()
			)
		ue.save()
		print ue.user_xbox
		systems = System.objects.order_by("?").all()[:(fake.random_digit() + 1)]
		for s in systems:
			ue.systems.add(s)
			games = Game.objects.filter(systems=s).all()[:(fake.random_digit() + 1)]
			for g in games:
				ue.games.add(g)

		ue.save()

		list_of_buddies = User.objects.order_by('?').all()[:(fake.random_digit())]
		for b in list_of_buddies:
			u.ext.buddies.add(b.ext)
			print "buddy-" + b.username

		if fake.random_digit() % 3 == 0:
			game = Game.objects.all()[0] if ue.games.count() < 1 else ue.games.all()[0]
			game_is_any = True  if ue.games.count() < 1 else False
			event = Event(
				title= fake.text(max_nb_chars=20),
				game= game,
				system= ue.systems.all()[0],
				game_is_any = game_is_any,
				owner=u,
				private=False,
				in_person=False,
				invite_only=False,
				scheduled_time= fake.date_time_between(start_date="now", end_date="+1y"),
				description = fake.text(max_nb_chars=300)
				)
			event.save()
			print "Event+" + str(event.title)

			event.attendees.add(u)
			for b in list_of_buddies:
				if (fake.random_digit()) % 4 != 0:
					event.attendees.add(b)
			event.save()

	return False


# Get the data from the ign rss feed
def api_call_ign_rss_feed(request):

	# Display the feed data
	feed_data = feedparser.parse('http://feeds.ign.com/ign/all')
	dt = datetime.datetime.strptime(feed_data.entries[0].published,'%a, %d %b %Y %H:%M:%S %Z')

	# feed
	# status
	# updated
	# updated_parsed
	# encoding
	# bozo
	# headers
	# etag
	# href
	# version
	# entries
	# namespaces
	print feed_data

	for entry in feed_data.entries:
		print "Next entry..."
		# summary_detail
		# published_parsed
		# links
		# title
		# feedburner_origlink
		# authors
		# updated
		# summary
		# content
		# guidislink
		# title_detail
		# link
		# author
		# published
		# author_detail
		# id
		# updated_parsed
		if News.objects.filter(title=entry.title).exists():
			# We already have this entry
			print "Getting duplicate data, not saving..."
			pass
		else:
			print "Putting new feed in data! " + entry.title
			n = News(
				title = entry.title,
				url = entry.link,
				text = entry.content[0].value,
				# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADD A DATE HERE
				)
			n.save()

	return False

























