# account.models for lionlist
# by Ian Zapolsky
#
# django imports
from django.db import models
from django.contrib.auth.models import User

# app imports
from post.models import PostModel


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=50)
    saved_posts = models.ManyToManyField(PostModel, blank=True)
    custom_email = models.EmailField(blank=True)
    #school = models.CharField(max_length=50)
    
    def forsale(self):
        return PostModel.objects.forsale_by_user(self)

    def wanted(self):
        return PostModel.objects.wanted_by_user(self)

    def created(self):
        return PostModel.objects.all_by_user(self)

    def saved(self):
        return self.saved_posts
     
    def get_email(self):
        if self.custom_email:
            return self.custom_email
        else:
            return self.user.username+"@columbia.edu"
   
    def __unicode__(self):
        return self.user.username


"""
after ~12 hours of struggling with django admin calling my post_save
signal twice, I decided to create a profile property on the User object
and handle UserProfile automatic creation this way. 
"""

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
