from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'socialnetwork.views.redirect'),
    url(r'^socialnetwork/', include('socialnetwork.urls')),
)
