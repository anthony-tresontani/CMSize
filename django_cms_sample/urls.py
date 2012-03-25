from django.conf.urls import patterns, url, include
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    ('^home/$', direct_to_template, {
        'template': 'home.html'
    })
)
