# category.models for lionlist
# by Ian Zapolsky
#
# django imports
from django.db import models

# third party imports
from autoslug import AutoSlugField

# app imports
from post.models import PostModel


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=100, populate_from='name')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/categories/"+self.slug

    def forsale(self):
        return PostModel.objects.forsale_in_category(self)

    def wanted(self):
        return PostModel.objects.wanted_in_category(self)

    def all(self):
        return PostModel.objects.all_in_category(self)
    
    def get_count(self):
        return PostModel.objects.all_in_category(self).count()

    class Meta:
        ordering = ['pk']
