# category.views for lionlist
# by Ian Zapolsky
#
# django imports
from django.template import RequestContext
from django.views.generic import View
from django.shortcuts import get_object_or_404, render_to_response

# third party imports
from braces.views import LoginRequiredMixin
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

# app imports
from .forms import BaseFilterForm
from .models import CategoryModel
from course.models import DepartmentModel, CourseModel
from post.models import PostModel, BookModel
from search.forms import SearchForm


# lists all the CategoryModels in the database (main page)

class CategoryListView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['object_list'] = CategoryModel.objects.all().order_by('name')
        context['departments'] = DepartmentModel.objects.all()
        context['courses'] = []
        return render_to_response('category/categories.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()   
        context['object_list'] = CategoryModel.objects.all().order_by('name')
        context['departments'] = DepartmentModel.objects.all()

        # department/course form handling
        if request.POST['department'] != 'empty':
            context['department'] = DepartmentModel.objects.get(name=request.POST['department'])
            context['courses'] = CourseModel.objects.filter(department=context['department'])
        else:
            context['department'] = 'empty'
            context['courses'] = []

        return render_to_response('category/categories.html', context, context_instance=RequestContext(self.request))


# lists all the PostModels within a given CategoryModel, with FilterForm

class CategoryDetailView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['filter_form'] = BaseFilterForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['slug'])
        context['object_list'] = PostModel.objects.filter(category=context['category'])
        context['departments'] = DepartmentModel.objects.all()
        context['courses'] = []
        return render_to_response('category/category.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['filter_form'] = BaseFilterForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['slug'])
        context['departments'] = DepartmentModel.objects.all()
        object_list = PostModel.objects.filter(category=context['category'])
        context['object_list'] = object_list

        # department/course form handling
        if request.POST.get('department', False):
            if request.POST['department'] != 'empty':
                context['department'] = DepartmentModel.objects.get(name=request.POST['department'])
                context['courses'] = CourseModel.objects.filter(department=context['department'])
                if request.POST.get('course', False):
                    if request.POST['course'] != 'empty':
                        context['course'] = CourseModel.objects.get(name=request.POST['course'])
                        object_list = BookModel.objects.filter(course=context['course'])
            else:
                context['department'] = 'empty'
                context['courses'] = []
        else:
            context['department'] = 'empty'
            context['courses'] = []

        # filter form handling
        filter_form = BaseFilterForm(request.POST)
        if filter_form.is_valid():

            # save POSTed data to push back to filter form for continuity
            data = {'price': filter_form.cleaned_data['price'],
                    'sell_type': filter_form.cleaned_data['sell_type'],
                    'location': filter_form.cleaned_data['location']}
            context['filter_form'] = BaseFilterForm(data)

            # object list filtering, using haystack API to handle keyword query 
            if len(filter_form.cleaned_data['keyword']) > 0:
                object_list = []
                results = SearchQuerySet().filter(content=AutoQuery(filter_form.cleaned_data['keyword'])).models(PostModel)
                for r in results:
                    try:
                        if r.object.category == context['category']:
                            object_list.append(r.object)
                    except:
                        pass

            if len(object_list) > 0:

                if filter_form.cleaned_data['sell_type'] != 'all' and len(filter_form.cleaned_data['sell_type']) > 0:
                    object_list = [x for x in object_list if x.forsale == filter_form.cleaned_data['sell_type']]

                if filter_form.cleaned_data['location'] != 'empty' and len(filter_form.cleaned_data['location']) > 0:
                    object_list = [x for x in object_list if x.location == filter_form.cleaned_data['location']]

                if filter_form.cleaned_data['price'] != 'empty' and len(filter_form.cleaned_data['price']) > 0:
                    upper_bound = int(filter_form.cleaned_data['price'])
                    object_list = [x for x in object_list if x.price <= upper_bound]

            context['object_list'] = object_list
            return render_to_response('category/category.html', context, context_instance=RequestContext(self.request))

        else:
            context['object_list'] = object_list
            return render_to_response('category/category.html', context, context_instance=RequestContext(self.request))


# choose a category to create a post in

class ChooseCreateView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['object_list'] = CategoryModel.objects.all().order_by('name')
        return render_to_response('category/choose.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['object_list'] = CategoryModel.objects.all()
        return render_to_response('category/choose.html', context, context_instance=RequestContext(self.request))
