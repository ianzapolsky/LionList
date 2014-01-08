# category.forms for lionlist
# by Ian Zapolsky
#
# TODO: not sure SearchForm belongs here...
#
# django imports
from django import forms

# third party imports
from haystack.forms import SearchForm

LOCATION_CHOICES = (
    ('empty', 'any location'),
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

PRICE_CHOICES = (
    ('empty', 'any price'),
    ('5', '<= $5'),
    ('10', '<= $10'),
    ('15', '<= $15'),
    ('20', '<= $20'),
    ('50', '<= $50'),
    ('100', '<= $100'),
    ('150', '<= $150'),
    ('200', '<= $200'),
    ('300', '<= $300'),
)

TYPE_CHOICES = (
    ('all', 'all'),
    ('forsale', 'for sale'),
    ('wanted', 'wanted'),
)

class PostSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, 
        widget=forms.TextInput(attrs={'size':20}), 
        required=True,
        label="search")

    """
    def clean_query(self):
        query = self.cleaned_data.get('query')
        if not query:
            raise forms.ValidationError('please enter a query')
        return query
    """
    


class BaseFilterForm(forms.Form):
    keyword = forms.CharField(max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'size': 15}), 
        label="keyword")
    sell_type = forms.ChoiceField(label="for sale/wanted", 
        required=False, 
        widget=forms.Select,
        choices=TYPE_CHOICES)
    price = forms.ChoiceField(label="max price", 
        required=False, 
        widget=forms.Select, 
        choices=PRICE_CHOICES)
    location = forms.ChoiceField(label="campus location", 
        required=False, 
        widget=forms.Select, 
        choices=LOCATION_CHOICES)
