# search.forms for lionlist
# by Ian Zapolsky (09/13/13)
#
# django imports
from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'size':20}),
        required=True,
        label='')
