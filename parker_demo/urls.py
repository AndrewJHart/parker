from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^page1/$', direct_to_template, {'template': 'page1.html',}),
    url(r'^load/$', direct_to_template, {'template': 'load.html',}),
    # Examples:
    # url(r'^$', 'parker_demo.views.home', name='home'),
    # url(r'^parker_demo/', include('parker_demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
