# post.admin for lionlist
# by Ian Zapolsky
#
# django imports
from django.contrib import admin

# app imports
from .models import PostModel, BookModel
# from .models import TicketModel

admin.site.register(PostModel)
admin.site.register(BookModel)
# admin.site.register(TicketModel)
