from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'socialnetwork.views.home_page', name='home_page'),
    url(r'^follower-stream$', 'socialnetwork.views.follower_stream', name='follower-stream'),
    url(r'^profile/(?P<id>\d+)$', 'socialnetwork.views.profile', name='profile'),
    url(r'^add-post$', 'socialnetwork.views.add_post', name='add-post'),
    url(r'^delete-post/(?P<id>\d+)$', 'socialnetwork.views.delete_post', name='delete-post'),
    url(r'^add-comment/(?P<id>\d+)$', 'socialnetwork.views.add_comment', name='add-comment'),
    url(r'^delete-comment/(?P<id>\d+)$', 'socialnetwork.views.delete_comment', name='delete-comment'),
    url(r'^edit_profile$', 'socialnetwork.views.edit_profile', name='edit_profile'),
    url(r'^photo/(?P<id>\d+)$', 'socialnetwork.views.get_photo', name='photo'),

    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^registration$', 'socialnetwork.views.registration', name='registration'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'socialnetwork.views.confirm_registration', name='confirm_registration'),

    #url(r'^get-post-json$', 'socialnetwork.views.get_post_json', name='get-post-json'),
    url(r'^get-posts/(?P<last_post>\d+)$', 'socialnetwork.views.get_posts', name='get-posts'),
)
