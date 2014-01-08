# post.models for lionlist
# by Ian Zapolsky
#
# TODO: add forms for all types of Posts
#
# django imports
from django.db import models

# third party imports
from smart_selects.db_fields import GroupedForeignKey
from autoslug import AutoSlugField

# app imports
from course.models import DepartmentModel, CourseModel


"""
PostModel is the generic class upon which all other types of posts for 
lionlist are built. it inherits date fields from TimeStampedModel.
"""

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PostManager(models.Manager):
    
    def get_by_title(self, search_string):
        return self.filter(title__icontains=search_string)
        
    def forsale_in_category(self, search_category):
        return self.filter(category=search_category, forsale=True).select_related()

    def wanted_in_category(self, search_category):
        return self.filter(category=search_category, forsale=False).select_related()

    def all_in_category(self, search_category):
        return self.filter(category=search_category).select_related()

    def forsale_by_user(self, search_user):
        return self.filter(poster=search_user, forsale=True).select_related()

    def wanted_by_user(self, search_user):
        return self.filter(poster=search_user, forsale=False).select_related()
    
    def all_by_user(self, search_user):
        return self.filter(poster=search_user).select_related()


class PostModel(TimeStampedModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', always_update=True)
    category = models.ForeignKey('category.CategoryModel')
    forsale = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='post_images', blank=True, default='')
    # default='/media/post_images/null.jpeg')
    poster = models.ForeignKey('account.UserProfile')
    poster_location = models.CharField(max_length=100)
    objects = PostManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/categories/"+self.category.slug+"/"+self.slug
    
    class Meta:
        ordering = ['slug']


"""
the remaining models build on the fields offered by PostModel but
specialize in some way to cater to a specific type of post. Becuase
PostModel is not abstract, we can still query all PostModel objects
and get a diverse list of all the specific types of PostModels we
have in the system.
"""

class BookModel(PostModel):
    author = models.CharField(max_length=200)
    edition = models.IntegerField(blank=True, null=True)
    isbn = models.BigIntegerField(blank=True, null=True)
    course = GroupedForeignKey(CourseModel, "department")
    
"""
class TicketModel(PostModel):
    event_location = models.CharField(max_length=200)
    date = models.DateTimeField()
"""
