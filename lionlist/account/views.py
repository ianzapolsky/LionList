# account.views for lionlist
# by Ian Zapolsky
#
# django imports
from django.contrib import messages
from django.core.validators import email_re
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.generic import View
from django.contrib.auth.models import User

# ajax
from django.http import HttpResponse
import json

# third party imports
import registration
import boto.ses
from braces.views import LoginRequiredMixin
from password_reset.views import Reset
from password_reset.forms import PasswordRecoveryForm
from registration.views import RegistrationView

# app imports
from .forms import UserEditForm, CustomPasswordResetForm, CustomRegistrationForm
from .models import UserProfile
from post.models import PostModel
from search.forms import SearchForm


# user edit page

class UserEditView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['form'] = UserEditForm(request.user)
        context['user'] = self.request.user
        return render_to_response('account/edit.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['user'] = self.request.user

        # create form handling
        edit_form = UserEditForm(request.user, request.POST)
        context['form'] = edit_form
        if edit_form.is_valid():
            new_password = edit_form.cleaned_data['new_password']
            location = edit_form.cleaned_data['location']
            new_email = edit_form.cleaned_data['new_email']
            user = self.request.user
            user_profile = user.get_profile()
            if len(new_password) > 0:
                user.set_password(new_password)
            if len(new_email) > 0:
                user_profile.custom_email = new_email
            if location != 'empty':
                user_profile.location = location
            user_profile.save()
            user.save()
            msg = "Your account was successfully edited!"
            messages.add_message(request, messages.INFO, msg)
       
        return render_to_response('account/edit.html', context, context_instance=RequestContext(self.request)) 


# lists all the posts which a given user has created

class UserCreatedPostsView(LoginRequiredMixin, View):
   
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['user'] = self.request.user
        self.user_profile = self.request.user.get_profile()
        context['posts'] = self.user_profile.created()
        return render_to_response('account/created.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm(request.POST)
        context['user'] = self.request.user
        self.user_profile = self.request.user.get_profile()
        context['posts'] = self.user_profile.created()

        return render_to_response('account/created.html', context, context_instance=RequestContext(self.request))


# lists all the posts wich a given user has bookmarked

class UserSavedPostsView(LoginRequiredMixin, View):
   
    def get(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['user'] = self.request.user
        self.user_profile = self.request.user.get_profile()
        context['posts'] = self.user_profile.saved_posts.all()
        return render_to_response('account/saved.html', context, context_instance=RequestContext(self.request))

    def post(self, request, *args, **kwargs):
        context = {}
        context['search_form'] = SearchForm()
        context['user'] = self.request.user
        self.user_profile = self.request.user.get_profile()
        context['posts'] = self.user_profile.saved_posts.all()

        # delete form handling
        if request.POST.get("post_title", False):
            user = self.request.user.get_profile()
            user.saved_posts.remove(PostModel.objects.get(title__iexact=request.POST['post_title']))
            msg = request.POST['post_title']+" was successfully deleted from your bookmarked posts."
            messages.add_message(request, messages.INFO, msg)
            context['posts'] = self.user_profile.saved_posts.all()

        return render_to_response('account/saved.html', context, context_instance=RequestContext(self.request))


# custom password reset view to override the django-password-reset default

class PasswordResetView(Reset):
    form_class = CustomPasswordResetForm
    success_url = "/account/reset/success/"


# custom registration view to override the django-registration default 

class CustomRegistrationView(registration.backends.default.views.RegistrationView):
    form_class = CustomRegistrationForm

    def get_form_class(self, request):
        return CustomRegistrationForm

    def register(self, request, **kwargs):
        new_user = super(CustomRegistrationView, self).register(request, **kwargs)
        uni = kwargs.get('username', False)
        password = kwargs.get('password', False)
        location = kwargs.get('location', False)
        try:
            profile = new_user.get_profile()
        except:
            profile = UserProfile(user=new_user)
        profile.location = location
        new_user.email = profile.get_email()
        profile.save()
        new_user.save()
        return new_user


# ajax methods

def is_username(request, username):

    response_data = {}

    if User.objects.filter(username=username).count() < 1:
        response_data['msg'] = False
    else:
        response_data['msg'] = True

    return HttpResponse(json.dumps(response_data), 
                        content_type="application/json")

def is_valid_password(request, username, password):
    
    response_data = {}

    if User.objects.filter(username=username).count() < 1:
        response_data['msg'] = False
    else:
        user = User.objects.get(username=username)
        if not user.check_password(password):
            response_data['msg'] = False
        else:
            response_data['msg'] = True

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")

def validate_passwords(request, password1, password2):

    response_data = {}

    if len(password1) < 5:
        response_data['error'] = True
        response_data['msg'] = 'Your password must be at least 5 characters long.'
    else:
        if password1 != password2:
            response_data['error'] = True
            response_data['msg'] = 'Your passwords do not match.'
        else:
            response_data['error'] = False

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")

def is_valid_email(request, email):
    
    response_data = {}

    if not email_re.match(email):
        response_data['error'] = True
        response_data['msg'] = 'Not a valid email address'
    else:
        response_data['error'] = False
        response_data['msg'] = ''

    return HttpResponse(json.dumps(response_data),
                        content_type="application/json")
  
    
        
        






