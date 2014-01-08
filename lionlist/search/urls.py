# search.urls for lionlist
# by Ian Zapolsky (09/13/13)
#
# django imports
from django.conf.urls import patterns, url

# app imports
from .views import *

urlpatterns = patterns('search.views',
    
    # search
    url(r'^$', SearchView.as_view()),

)
