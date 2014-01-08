# account.urls for lionlist
# by Ian Zapolsky
#
# django imports
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

# third party imports
from password_reset.views import Recover, RecoverDone, ResetDone
from registration.backends.default.views import ActivationView, RegistrationView

# app imports
from .views import *
from .forms import CustomAuthenticationForm

urlpatterns = patterns('account.views',

	  # login and logout
	  url(r'^login/$', login, {'authentication_form': CustomAuthenticationForm, 
                           'template_name': 'account/login.html'}),
	  url(r'^logout/$', logout, {'next_page': '/'}),

    # create/register user with django-registration
    url(r'^register/$', CustomRegistrationView.as_view(), name='registration_register'),

	  # edit user
	  url(r'^edit/$', UserEditView.as_view()),

	  # created posts
	  url(r'^created/$', UserCreatedPostsView.as_view()),

	  # bookmarked posts
	  url(r'^saved/$', UserSavedPostsView.as_view()),

    # forgot password with django-password-reset
    url(r'^forgot/$', Recover.as_view(), name='password_reset_recover'),
    url(r'^forgot/(?P<signature>.+)/$', RecoverDone.as_view(), name='password_reset_sent'),
    url(r'^reset/success/$', TemplateView.as_view(template_name='password_reset/success.html')),
    url(r'^reset/(?P<token>[\w:-]+)/$', PasswordResetView.as_view(), name='password_reset_reset'),
    url(r'^reset/done/$', ResetDone.as_view(), name='password_reset_done'),

    # ajax experiment
    url(r'^ajax/is_username/(.+)/$', is_username),
    url(r'^ajax/is_valid_password/(.*)/(.*)/$', is_valid_password),
    url(r'^ajax/validate_passwords/(.*)/(.*)/$', validate_passwords),
    url(r'^ajax/is_valid_email/(.*)/$', is_valid_email),

)
