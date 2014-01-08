# category.admin for lionlist
# by Ian Zapolsky
#
# django imports
from django.contrib import admin

# app imports
from .models import CategoryModel

admin.site.register(CategoryModel)
