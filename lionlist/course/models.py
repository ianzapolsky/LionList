# course.models for lionlist
# by Ian Zapolsky (09/01/13)
#
# django imports
from django.db import models

# third party imports
from autoslug import AutoSlugField


class CourseManager(models.Manager):
    
    def get_by_department(self, department):
        return self.filter(department=department)


class CourseModel(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(max_length=100, populate_from='name')
    department = models.ForeignKey('DepartmentModel')
    objects = CourseManager()

    def get_absolute_url(self):
        return "/courses/"+self.slug

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['department']
    
class DepartmentModel(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=100, populate_from='name')

    def get_courses(self):
        return CourseModel.objects.get_by_department(self)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['slug']
