# course.search_indexes for lionlist
# by Ian Zapolsky (09/11/13)
#
# django imports
import datetime
from django.utils.timezone import utc

# third party imports
from haystack import indexes

# app imports
from .models import CourseModel

class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return CourseModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
        # return self.get_model().objects.filter(created=datetime.datetime.utcnow().replace(tzinfo=utc)) 
        # naive: return self.get_model().objects.filter(created=datetime.datetime.now())
