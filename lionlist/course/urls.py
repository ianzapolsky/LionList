# account.urls for lionlist
# by Ian Zapolsky
#
# django imports
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

# app imports
from .views import *
from post.views import PostDetailView

urlpatterns = patterns('course.views',

	  # list of all courses, by department
	  url(r'^$', CourseListView.as_view()),

    # course detail
    url(r'(?P<slug>[-\w\d]+)/$', CourseDetailView.as_view()),

)
