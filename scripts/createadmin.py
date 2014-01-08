#!/usr/bin/env python

print "Running scripts/createadmin.py\n\n\n"

from django.contrib.auth.models import User
#from app.models import UserExtension

if User.objects.count() == 0:
	print "Creating an admin..."
	admin = User.objects.create(username='stevenr4')
	admin.set_password('tmppass')
	admin.is_superuser = True
	admin.is_staff = True
	admin.save()
	# admin_ext = UserExtension(user = admin)
	# admin_ext.save()
	print "Success creating admin"

