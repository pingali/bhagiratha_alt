from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save 
from bitfield import BitField
import simplejson as json 
from .forms import LoginForm, SignupForm
from django.contrib import messages 
import logging

log = logging.getLogger("bhagirath.apps.account.models")

class UserProfile(models.Model): 

    user = models.ForeignKey(User, unique=True)    
    # Add more stuff here 
 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        log.debug("Adding user profile for %s " % instance.username)
        p = UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
