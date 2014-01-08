# course.views for lionlist
# by Ian Zapolsky (09/08/13)
#
# django imports
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404, render_to_response

# third party imports
from braces.views import LoginRequiredMixin

# app imports
from post.models import PostModel, BookModel
from .models import CourseModel, DepartmentModel
from category.forms import BaseFilterForm
from search.forms import SearchForm


# lists all the CourseModels in the database, organized by DepartmentModel

class CourseListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['departments'] = DepartmentModel.objects.all()
        context['courses'] = CourseModel.objects.all()
        return render_to_response('course/courses.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['departments'] = DepartmentModel.objects.all()
        context['courses'] = CourseModel.objects.all()
        return render_to_response('course/courses.html', context, context_instance=RequestContext(self.request))


# lists all the PostModels for a given CourseModel

class CourseDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['filter_form'] = BaseFilterForm()
        context['course'] = get_object_or_404(CourseModel, slug__iexact=self.kwargs['slug'])
        context['object_list'] = BookModel.objects.filter(course=context['course'])
        context['departments'] = DepartmentModel.objects.all()
        context['courses'] = []
        return render_to_response('course/course.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['filter_form'] = BaseFilterForm()
        context['course'] = get_object_or_404(CourseModel, slug__iexact=self.kwargs['slug'])
        context['departments'] = DepartmentModel.objects.all()
        object_list = BookModel.objects.filter(course=context['course'])
        context['object_list'] = BookModel.objects.filter(course=context['course'])

        # filter form handling
        filter_form = BaseFilterForm(request.POST)
        if filter_form.is_valid():

            # save POSTed data to push back to form
            data = {'price': filter_form.cleaned_data['price'],
                    'sell_type': filter_form.cleaned_data['sell_type'],
                    'location': filter_form.cleaned_data['location']}
            context['filter_form'] = BaseFilterForm(data)

            # FILTER 
            if filter_form.cleaned_data['sell_type'] != 'all' and len(filter_form.cleaned_data['sell_type']) > 0:
                object_list = object_list.filter(forsale=filter_form.cleaned_data['sell_type'])
            if len(filter_form.cleaned_data['keyword']) > 0:
                object_list = object_list.filter(title__icontains=filter_form.cleaned_data['keyword'])
            if filter_form.cleaned_data['location'] != 'empty' and len(filter_form.cleaned_data['location']) > 0:
                object_list = object_list.filter(poster_location=filter_form.cleaned_data['location'])
            if filter_form.cleaned_data['price'] != 'empty' and len(filter_form.cleaned_data['price']) > 0:
                upper_bound = int(filter_form.cleaned_data['price'])
                object_list = object_list.filter(price__lte=upper_bound)
            context['object_list'] = object_list
            return render_to_response('course/course.html', context, context_instance=RequestContext(self.request))
        else:
            context['object_list'] = object_list
            return render_to_response('course/course.html', context, context_instance=RequestContext(self.request))
