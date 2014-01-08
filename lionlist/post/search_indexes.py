# post.search_indexes for lionlist
# by Ian Zapolsky (09/11/13)
#
# django imports
import datetime
from django.utils.timezone import utc

# third party imports
from haystack import indexes

# app imports
from .models import PostModel, BookModel
from category.models import CategoryModel

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return PostModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all().exclude(category=CategoryModel.objects.get(name="books"))
        # return self.get_model().objects.filter(created=datetime.datetime.utcnow().replace(tzinfo=utc)) 
        # naive: return self.get_model().objects.filter(created=datetime.datetime.now())

class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return BookModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
