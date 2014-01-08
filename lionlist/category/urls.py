# category.urls for lionlist
# by Ian Zapolsky
#
# django imports
from django.conf.urls import patterns, url

# app imports
from post.views import *
from .views import *


urlpatterns = patterns('category.views',

    # list of all categories
    url(r'^$', CategoryListView.as_view()),

    # choose category when creating post
    url(r'^create/$', ChooseCreateView.as_view()),

    # generic create
    url(r'^create/(?P<slug>[-\w\d]+)/$', PostCreateView.as_view()),

    # generic category detail 
    url(r'^(?P<slug>[-\w\d]+)/$', CategoryDetailView.as_view()),

    # generic create 
    # url(r'^(?P<slug>[-\w\d]+)/create/$', PostCreateView.as_view()),

    # generic post detail
    url(r'^(?P<category_slug>[-\w\d]+)/(?P<slug>[-\w\d]+)/$', PostDetailView.as_view()),

    # gneric post edit
    url(r'^(?P<category_slug>[-\w\d]+)/(?P<slug>[-\w\d]+)/edit/$', PostEditView.as_view()),
)
