# category.admin for lionlist
# by Ian Zapolsky
#
# django imports
from django.contrib import admin

# app imports
from .models import DepartmentModel, CourseModel

admin.site.register(DepartmentModel)
admin.site.register(CourseModel)
