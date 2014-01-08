# account.forms for lionlist
# by Ian Zapolsky
#
# TODO: add ForgotPasswordForm and its associated view class in .views
#
# django imports
from django import forms
from django.core.validators import email_re
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# third party imports
from password_reset.forms import *
import registration

# app imports
from .models import UserProfile


# choice collections

SCHOOL_CHOICES = (
    ('Columbia', 'Columbia'),
    ('Barnard', 'Barnard'),
)

LOCATION_CHOICES = (
    ('empty', 'Campus Location'),
    ('Broadway', 'Broadway'),
    ('Brownstones', 'Brownstones'),
    ('Carman', 'Carman'),
    ('Claremont', 'Claremont'),
    ('East Campus', 'East Campus'),
    ('Furnald', 'Furnald'),
    ('Harmony', 'Harmony'),
    ('Hartley', 'Hartley'),
    ('Hogan', 'Hogan'),
    ('John Jay', 'John Jay'),
    ('McBain', 'McBain'),
    ('Nussbaum', 'Nussbaum'),
    ('River', 'River'),
    ('Ruggles', 'Ruggles'),
    ('Schapiro', 'Schapiro'),
    ('Wallach', 'Wallach'),
    ('Watt', 'Watt'),
    ('Wien', 'Wien'),
    ('Woodbridge', 'Woodbridge'),
    ('Other/Off Campus', 'Other/Off Campus'),
)


# overriding the default django authentication form 

class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        error_messages=({'required':'UNI required'}))

    password = forms.CharField(
        error_messages=({'required':'Password required'}),
        widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(CustomAuthenticationForm, self).clean()

        if cleaned_data.get('username', False):
            if User.objects.filter(username=cleaned_data['username']).count() < 1:
                msg = 'Invalid UNI'
                self._errors['username'] = self.error_class([msg])
                del cleaned_data['username']

        return cleaned_data 
            

# form to allow a user to edit password, email, and location

class UserEditForm(forms.Form):

    current_password = forms.CharField(
        label="current password",
        required=False,
        widget=forms.PasswordInput(attrs = {'size': 15}))

    new_password = forms.CharField(
        label="new password (leave blank to keep current)",
        required=False,
        widget=forms.PasswordInput(attrs = {'size': 15}))

    new_password_check = forms.CharField(
        label="confirm new password",
        required=False,
        widget=forms.PasswordInput(attrs = {'size': 15}))

    new_email = forms.CharField(
        label="new email",
        required=False)

    location = forms.ChoiceField(
        label="new location (leave blank to keep current)",
        required=False,
        widget=forms.Select,
        choices=LOCATION_CHOICES)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        new_password_check = cleaned_data.get("new_password_check")
        new_email = cleaned_data.get("new_email")
        location = cleaned_data.get("location")
        
        if not current_password:
            raise forms.ValidationError(
                'You must enter your current password to make any changes.')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('That password was incorrect.')

        if new_password and new_password_check:
            if len(new_password) < 5:
                raise forms.ValidationError(
                    'Your new password must be at least 5 characters.')
            if new_password != new_password_check:
                raise forms.ValidationError('Your new passwords do not match.')

        elif new_email:
            if not email_re.match(new_email):
                raise forms.ValidationError('Not a valid email address')

        elif location == 'empty':
            raise forms.ValidationError(
                'You have not changed any information.')

        return cleaned_data


# form to submit a username who forgot a password

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label="UNI",
        required=False,
        widget=forms.TextInput(attrs = {'size': 15}))
 
    def __init__(self, search_fields, case_sensitive, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        username = cleaned_data.get("username")

        if not username:
            raise forms.ValidationError('please enter your UNI')
        if User.objects.filter(username=username).count() == 0:
            raise forms.ValidationError('that\'s not a valid UNI')

        return cleaned_data


# custom form to override the django-password-reset default 

class CustomPasswordResetForm(PasswordResetForm):

    def clean(self):
        cleaned_data = super(CustomPasswordResetForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError(
                'please enter and confirm your password')
        if len(password1) < 5:
            msg = "your password must be at least 5 characters"
            self._errors['password1'] = self.error_class([msg])
            del cleaned_data['password1']
        if password1 != password2:
            msg = "your passwords do not match"
            self._errors['password1'] = self.error_class([msg])
            self._errors['password2'] = self.error_class([msg])
            del cleaned_data['password1']
            del cleaned_data['password2']
        return cleaned_data


# custom form to override the django-registration default

class CustomRegistrationForm(registration.forms.RegistrationForm):
    username = forms.CharField(label="UNI/Barnard ID", 
        error_messages=({'required':'Please enter your UNI.'}))
    password1 = forms.CharField(
        error_messages=({'required':'Please enter a password'}),
        widget=forms.PasswordInput())
    password2 = forms.CharField(
        error_messages=({'required':'Please confirm your password'}),
        widget=forms.PasswordInput())
    location = forms.ChoiceField(label="campus location", 
        error_messages=({'required':'Please choose a campus location'}),
        widget=forms.Select, 
        choices=LOCATION_CHOICES)
    #school = forms.ChoiceField(label="school",
    #    widget=forms.Select,
    #    choices=SCHOOL_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        self.fields.pop('email')
        self.email = 'uni@columbia.edu'

    def clean(self):
        cleaned_data = super(CustomRegistrationForm, self).clean()
        if cleaned_data.get('username', False) == False:
            raise forms.ValidationError('')
        elif not cleaned_data.get('password1', False):
            raise forms.ValidationError('Please enter a password.')
        elif len(cleaned_data.get('password1')) < 5:
            raise forms.ValidationError('Your password must be at least 5 characters.')
        elif not cleaned_data.get('password2', False):
            raise forms.ValidationError('Your passwords do not match.')
        elif cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('Your passwords do not match.')
        elif cleaned_data.get('location') == 'empty':
            raise forms.ValidationError('Please choose a campus location.')
    
        cleaned_data['email'] = cleaned_data['username']+"@columbia.edu"
        return cleaned_data
