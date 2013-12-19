"""

from django import forms
from django.core.validators import MaxLengthValidator
from app.models import User, Event, EventInvite, System, Game

class LoginForm(forms.ModelForm):
    class Meta(object):
        model = User
        fields = ["username","password"]
        widgets = {
            "password":forms.PasswordInput
        }

class SignupForm(LoginForm):
    confirm_password = forms.CharField(
        widget = forms.PasswordInput
    )


class EventForm(forms.ModelForm):
    class Meta(object):
        model = Event
        fields = ["game","system","attendees"]
"""