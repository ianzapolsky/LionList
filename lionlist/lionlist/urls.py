# lionlist.urls for lionlist
# by Ian Zapolsky
#
# django imports
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin

# app imports
from category.views import CategoryListView
from search.views import SearchView

# activate admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# homepage
	url(r'^$', CategoryListView.as_view()),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),
	
	# account.urls
    url(r'^account/', include('account.urls')),
    url(r'^account/', include('registration.backends.default.urls')),

	# category.urls
	url(r'^categories/', include('category.urls')),

    # course.urls
    url(r'^courses/', include('course.urls')),

    # search.urls
    url(r'^search/', include('search.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

#urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',

        # static
        url(r'^static/(.*)$',
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}), 

        # media
        url(r'^media/(.*)$', 
            'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )

if not settings.DEBUG:
    handler404 = 'lionlist.views.error404'
    handler500 = 'lionlist.views.error500'
