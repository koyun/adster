from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from ads.api import UserResource,AdResource,AdImageResource, RegisterResource

v1_api = Api(api_name = 'v1')
v1_api.register(AdResource())
v1_api.register(AdImageResource())
v1_api.register(RegisterResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adster.views.home', name='home'),
    # url(r'^adster/', include('adster.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    (r'^$', direct_to_template,
        { 'template': 'index.html' }, 'index'),
    (r'^api/', include(v1_api.urls)),

)
