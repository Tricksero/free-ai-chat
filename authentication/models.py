from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # Add any additional fields or modifications to the User model
    pass

    #class Meta:
        ## Specify the app_label to match your renamed authentication app
        #app_label = 'authentication'

# Specify unique related_names for groups and user_permissions fields
#Group.add_to_class('user_set', models.ManyToManyField(User, related_name='authentication_user_set'))
#Permission.add_to_class('user_set', models.ManyToManyField(User, related_name='authentication_user_set'))
