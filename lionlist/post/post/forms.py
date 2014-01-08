# post.forms for lionlist
# by Ian Zapolsky
#
# django imports
import traceback
 
from django import forms

# app imports
from .models import PostModel, BookModel
# from .models import TicketModel


TYPE_CHOICES = (
    ('forsale', 'for sale'),
    ('wanted', 'wanted'),
)

class PostForm(forms.ModelForm):

    class Meta:
        model = PostModel
        fields = ['title', 'description', 'image', 'forsale', 'price']
        widgets = {
            'forsale': forms.Select(choices=TYPE_CHOICES),
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'post title'
        self.fields['title'].help_text = '(required)'
        self.fields['description'].label = 'description'
        self.fields['description'].help_text = '(optional)'
        self.fields['image'].label = 'image'
        self.fields['image'].help_text = '(optional)'
        self.fields['forsale'].label = 'for sale or wanted' 
        self.fields['forsale'].help_text = '(required)'
        self.fields['price'].label = 'price'
        self.fields['price'].help_text = '(required) -- e.g. 15, 15.0 or 15.00'

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        title = cleaned_data.get("title")
        price = cleaned_data.get("price")

        try:
            existing = PostModel.objects.get(title=title)
        except:
            existing = None
        if existing and existing != self.instance:
            msg = ('please choose a different title, this title is already taken')
            self._errors['title'] = self.error_class([msg])
            del cleaned_data['title']
        return cleaned_data


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'post title'
        self.fields['title'].help_text = '(required)'
        self.fields['description'].label = 'description'
        self.fields['description'].help_text = '(optional)'
        self.fields['image'].label = 'image'
        self.fields['image'].help_text = '(optional)'
        self.fields['forsale'].label = 'for sale or wanted' 
        self.fields['forsale'].help_text = '(required)'
        self.fields['price'].label = 'price'
        self.fields['price'].help_text = '(required) -- e.g. 15, 15.0, 15.00'
        self.fields['author'].label = 'author'
        self.fields['author'].help_text = '(required)'
        self.fields['edition'].label = 'edition'
        self.fields['edition'].help_text = '(optional) -- e.g. 7'
        self.fields['isbn'].label = 'isbn'
        self.fields['isbn'].help_text = '(optional) -- please do not use dashes'
        self.fields['course'].label = 'department/course'
        self.fields['course'].help_text = '(required) -- if not affiliated with a course please select the department/course NOT AFFILIATED WITH COURSE'
    
    class Meta:
        model = BookModel
        fields = ['title', 'author', 'edition', 'isbn', 
                  'course', 'description', 'image', 'forsale', 'price'] 
        widgets = {
            'forsale': forms.Select(choices=TYPE_CHOICES),
            'course': forms.Select(),
            'description': forms.Textarea(),
        }

    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        title = cleaned_data.get("title")

        try:
            existing = BookModel.objects.get(title=title)
        except:
            existing = None
        if existing and existing != self.instance:
            msg = ('please choose a different title, this title is already taken')
            self._errors['title'] = self.error_class([msg])
            del cleaned_data['title']
        return cleaned_data
