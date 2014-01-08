# search.views for lionlist
# by Ian Zapolsky (09/13/13)
#
# python imports
import itertools

# django imports
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View

# third party imports
from braces.views import LoginRequiredMixin
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

# app imports  
from .forms import SearchForm
from course.models import CourseModel
from post.models import PostModel, BookModel


class SearchView(LoginRequiredMixin, View):
   
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()

        """
        this is awesome: with search configured this way we don't need
        to worry at all about search form catching and handling in the
        view
        """

        if request.GET.get('q', False):
            query = request.GET['q']
            context['post_list'] = itertools.chain(
                SearchQuerySet().filter(content=AutoQuery(query)).models(PostModel),
                SearchQuerySet().filter(content=AutoQuery(query)).models(BookModel),
            )
            context['course_list'] = SearchQuerySet().filter(content=AutoQuery(query)).models(CourseModel)
            context['query'] = query

        return render_to_response('search/search.html', context)

