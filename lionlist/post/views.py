# post.views for lionlist
# by Ian Zapolsky
#
# django imports
import json
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# third party imports
from braces.views import LoginRequiredMixin

# app imports
from account.views import UserCreatedPostsView
from category.models import CategoryModel
from search.forms import SearchForm
from .models import *
from .forms import *


# post detail view

class PostDetailView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()

        # determine post type
        try:
            context['post'] = get_object_or_404(PostModel, slug__iexact=self.kwargs['slug'])
        except:
            return HttpResponseRedirect('/post_does_not_exist/')
        try:
            context['post'] = get_object_or_404(BookModel, slug__iexact=self.kwargs['slug'])
        except:
            pass

        # determine if user has admin priviliges on this post
        if self.request.user.get_profile() == context['post'].poster:
            context['admin'] = "yes"

        return render_to_response('post/post.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['post'] = get_object_or_404(PostModel, slug__iexact=self.kwargs['slug'])

        # determine if user has admin privileges on this post
        if self.request.user.get_profile() == context['post'].poster:
            context['admin'] = "yes"

        # save form handling 
        if request.POST.get('post_title', False):
            user = self.request.user.get_profile()
            user.saved_posts.add(PostModel.objects.get(title__iexact=request.POST['post_title']))
            msg = context['post'].title+" was successfully bookmarked."
            messages.add_message(request, messages.INFO, msg)

        return render_to_response('post/post.html', context, context_instance=RequestContext(self.request))


# post create view

class PostCreateView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['slug'])

        # determine post type and serve appropriate form 
        if context['category'].name == 'books':
            context['form'] = BookForm()
        else:
            context['form'] = PostForm()

        return render_to_response('post/create.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['slug'])
        
        # determine post type and handle appropriate form
        if context['category'].name == 'books':
            post_form = BookForm(request.POST, request.FILES)
            context['form'] = post_form
        else:
            post_form = PostForm(request.POST, request.FILES)
            context['form'] = post_form

        # set hidden fields in the post form
        user_profile = self.request.user.get_profile()
        post_form.instance.poster = user_profile 
        post_form.instance.category = context['category']
        post_form.instance.poster_location = user_profile.location
       
        # post form handling
        if post_form.is_valid():
            p = post_form.save()
            msg = p.title+" was successfully created."
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(p.get_absolute_url()) 
        else:
            return render_to_response('post/create.html', context, context_instance=RequestContext(self.request))


# post edit view

class PostEditView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['category_slug'])

        # determine post type and serve appropriate form 
        if context['category'].name == 'books':
            context['post'] = get_object_or_404(BookModel, slug__iexact=self.kwargs['slug'])
            context['form'] = BookForm(instance=context['post'])
        else:
            context['post'] = get_object_or_404(PostModel, slug__iexact=self.kwargs['slug'])
            context['form'] = PostForm(instance=context['post'])
            
        
        # check if the user trying to access was the poster
        if self.request.user.get_profile() != context['post'].poster:
            return render_to_response('post/error.html', context, context_instance=RequestContext(self.request))
        else: 
            return render_to_response('post/edit.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['category'] = get_object_or_404(CategoryModel, slug__iexact=self.kwargs['category_slug'])
        
        # determine post type 
        if context['category'].name == 'books':
            context['post'] = get_object_or_404(BookModel, slug__iexact=self.kwargs['slug'])
            context['form'] = BookForm(request.POST, request.FILES, instance=context['post'])
            post_form = BookForm(request.POST, request.FILES, instance=context['post'])
        else:
            context['post'] = get_object_or_404(PostModel, slug__iexact=self.kwargs['slug'])
            context['form'] = PostForm(request.POST, request.FILES, instance=context['post'])
            post_form = PostForm(request.POST, request.FILES, instance=context['post'])
            

        # delete form handling 
        if request.POST.get('delete_post', False):
            msg = context['post'].title+" was successfully deleted."
            context['post'].delete()
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect('/account/created/')

        # set hidden fields in the post form 
        user_profile = self.request.user.get_profile()
        post_form.instance.poster = user_profile 
        post_form.instance.category = context['category']
        post_form.instance.poster_location = user_profile.location

        # post form handling 
        if post_form.is_valid():
            p = post_form.save()
            msg = context['post'].title+" was successfully edited."
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(p.get_absolute_url())
        else:
            return render_to_response('post/edit.html', context, context_instance=RequestContext(self.request))

# ajax methods

def is_valid_title(request, title):

    response_data = {}

    if PostModel.objects.filter(title=title).count() > 0:
        response_data['error'] = True 
    else:
        response_data['error'] = False

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
