from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
# Built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from socialnetwork.models import *
from socialnetwork.forms import RegistrationForm, UserForm, UserProfileForm, AddPostForm, AddRelationshipForm
from datetime import datetime
import time
from django.db import transaction
from django.core import serializers
import json
from django.shortcuts import render_to_response
import os

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.conf import settings
from socialnetwork.s3 import s3_upload, s3_delete

@login_required
def home_page(request):
    # Sets up feed of all user posts
    user=request.user
    user_profile = UserProfile.objects.all()
    #user_profile = UserProfile.objects.get(user_id=request.user)
    posts = Post.objects.all().order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')

    # Hidden field to track whether posts are new for user
    if posts:
        last_post = posts[0].pk
    else:
        last_post = 0;

    return render(request, 'socialnetwork/global-stream.html', {'last_post' : last_post, 'posts' : posts, 'comments' : comments, 'user_profile': user_profile})

@login_required
def follower_stream(request):

    #Filters posts by users followed
    follows = Relationship.objects.filter(follower=request.user)
    num_follows = len(follows)
    follows_list = []
    for i in range (0, num_follows):
        follows_list.append(follows[i].followed)
    posts = Post.objects.filter(user__in=follows_list).order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')
    last_post = "FALSE"

    user=request.user
    user_profile = UserProfile.objects.all()

    return render(request, 'socialnetwork/follower-stream.html', {'last_post': last_post, 'posts' : posts, 'comments' : comments, 'user_profile': user_profile})

@login_required
def add_post(request):
    errors = []
    context = {}

    # Form for add post
    data = {'text': request.POST['post'], 'user' : request.user.id}
    form = AddPostForm(data)
    context['form'] = form

    # If form is not valid, display error message and global stream
    if not form.is_valid():
        posts = Post.objects.all().order_by('date_created').reverse()
        comments = Comment.objects.all().order_by('date_created')

        # Update hidden field to track last new post
        if posts:
            last_post = posts[0].pk
        else:
            last_post = 0;
        context = {'last_post' : last_post, 'posts' : posts, 'comments' : comments, 'error' : 'Post not valid. Please try again.'}
        return render(request, 'socialnetwork/global-stream.html', context)

    # Creates a new post if it is present as a parameter in the request
    if not 'post' in request.POST or not request.POST['post']:
    	errors.append('You must enter a post to add.')
    elif len(request.POST['post']) > 160:
        errors.append('Your post must be less than 160 characters.')
    else:
    	new_post = Post(text=form.cleaned_data['text'], user=form.cleaned_data['user'])
    	new_post.save()

    posts = Post.objects.all().order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')

    # Update hidden field to track last new post
    if posts:
        last_post = posts[0].pk
    else:
        last_post = 0;

    context = {'last_post' : last_post, 'posts' : posts, 'comments' : comments, 'errors' : errors}
    return render(request, 'socialnetwork/global-stream.html', context)

@login_required
def add_comment(request, id):
    errors = []

    # Creates a new post if it is present as a parameter in the request
    if not 'comment' in request.POST or not request.POST['comment']:
    	errors.append('You must enter a comment to add.')
    elif len(request.POST['comment']) > 160:
        errors.append('Your comment must be less than 160 characters.')
    else:
        post = Post.objects.get(id=id)
    	new_comment = Comment(text=request.POST['comment'], post=post, user=request.user)
    	new_comment.save()
    posts = Post.objects.all().order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')
    if posts:
        last_post = posts[0].pk
    else:
        last_post = 0;
    context = {'last_post' : last_post, 'post' : post, 'comment' : new_comment, 'errors' : errors}
    return render(request, 'socialnetwork/comment.html', context)


@login_required
def delete_post(request, id):
    errors = []

    # Deletes post if the logged-in user has an item matching the id
    try:
        post_to_delete = Post.objects.get(id=id, user=request.user)
        comments = Comment.objects.filter(post=post_to_delete)
        for comment in comments:
            comment.delete()
        post_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist in your stream.')

    posts = Post.objects.all().order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')
    if posts:
        last_post = posts[0].pk
    else:
        last_post = 0;
    context = {'last_post' : last_post, 'posts' : posts, 'comments' : comments, 'errors' : errors}
    return render(request, 'socialnetwork/global-stream.html', context)

@login_required
def delete_comment(request, id):
    errors = []

    # Deletes post if the logged-in user has an item matching the id
    try:
        comment_to_delete = Comment.objects.get(id=id, user=request.user)
        comment_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The comment did not exist in your stream.')
    posts = Post.objects.all().order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')
    if posts:
        last_post = posts[0].pk
    else:
        last_post = 0;
    context = {'last_post' : last_post, 'posts' : posts, 'comments' : comments, 'errors' : errors}
    return render(request, 'socialnetwork/global-stream.html', context)

def get_posts(request, last_post):

    # Updates posts newer than the last post on the page
    last = last_post
    user=request.user
    user_profile = UserProfile.objects.get(user_id=request.user)
    posts = Post.objects.filter(id__gt=last).order_by('date_created').reverse()

    comments = Comment.objects.all().order_by('date_created')
    if posts:
        last = posts[0].pk
    return render(request, 'socialnetwork/posts.html', {'last' : last, 'posts' : posts, 'comments' : comments, 'user_profile': user_profile, 'user':user})

def profile(request, id):
    # Catch for missing profile
    user_profile = get_object_or_404(User, id=id)
    if not user_profile:
        raise Http404

    user_profile2 = UserProfile.objects.get(user_id=id)
    user_profile_set = UserProfile.objects.all()
    # Sets up list of just the selected user's posts
    posts = Post.objects.filter(user=user_profile).order_by('date_created').reverse()
    comments = Comment.objects.all().order_by('date_created')

    #Determines following relationship
    user = request.user
    user2 = user_profile
    relationship = Relationship.objects.filter(follower=user, followed=user2)
    if relationship:
        follow = 1
    else:
        follow = 0

    #No relationship change, just getting relationship
    if request.method == 'GET':
        return render(request, 'socialnetwork/profile.html', {'follow': follow, 'relationship': relationship, 'posts' : posts, 'comments' : comments, 'user_profile' : user_profile, 'user_profile2' : user_profile2 , 'user_profile_set' : user_profile_set})

    #POST = relationship change. Determine change, save change and update
    #If not following, follow
    if follow == 0:

        data = {'follower': user.id, 'followed': user2.id}
        form = AddRelationshipForm(data)

        # Relationship goes through form
        if not form.is_valid():
            return render(request, 'socialnetwork/profile.html', {'follow' : follow, 'relationship': relationship, 'posts' : posts, 'comments' : comments, 'user_profile' : user_profile, 'user_profile2' : user_profile2 , 'user_profile_set' : user_profile_set, 'error' : 'Follow request not valid.'})

        relationship = Relationship(
            follower=user,
            followed=user2)
        relationship.save()
        follow = 1
    #If following, unfollow
    else:
        Relationship.objects.filter(
            follower=user,
            followed=user2).delete()
        follow = 0
    return render(request, 'socialnetwork/profile.html', {'follow' : follow, 'relationship': relationship, 'posts' : posts, 'comments' : comments, 'user_profile' : user_profile, 'user_profile2' : user_profile2 , 'user_profile_set' : user_profile_set})

@login_required
def edit_profile(request):

    if request.method == 'GET':
        user = request.user
        user_profile=UserProfile.objects.get(user=request.user)
        uform = UserForm(instance=user)
        pform = UserProfileForm(instance=user_profile)
        context = {'user_profile': user_profile, 'user': user, 'pform': pform, 'uform': uform}
        return render(request, 'socialnetwork/edit_profile.html', context)

    user = request.user
    user_profile = UserProfile.objects.select_for_update().get(user=request.user)

    #Get forms of both User and extended User Profile models
    uform = UserForm(request.POST, instance=user)
    pform = UserProfileForm(request.POST, request.FILES, instance=user_profile)

    #Validate forms
    if not uform.is_valid():
        context = { 'user': user, 'user_profile': user_profile, 'uform': uform, 'pform': pform , 'message':"Form not valid."}
        return render(request, 'socialnetwork/edit_profile.html', context)

    if not pform.is_valid():
        context = { 'errors': pform.errors, 'user': user, 'user_profile': user_profile, 'uform': uform, 'pform': pform, 'message':"Form is not valid. Try again." }
        return render(request, 'socialnetwork/edit_profile.html', context)


    if pform.cleaned_data['picture']:
        url = s3_upload(pform.cleaned_data['picture'], user_profile.pk)
        user_profile.picture_url = url
        user_profile.save()

    pform.save()
    uform.save()

    context = {
    'user':  user,
    'user_profile': user_profile,
    'uform': uform,
    'pform': pform,
    }
    return render(request, 'socialnetwork/edit_profile.html', context)

@transaction.atomic
def registration(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/registration.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/registration.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])


    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False

    new_user_profile = UserProfile(user=new_user)
    new_user.save()
    new_user_profile.save()


    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to Social Network!  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(),
       reverse('confirm_registration', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="christinalipson29@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs-confirmation.html', context)


    # Logs in the new user and redirects to his/her global stream
    #new_user = authenticate(username=request.POST['username'], \
    #                        password=request.POST['password1'])
    #login(request, new_user)
    #return redirect(reverse('home_page'))

def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'socialnetwork/confirmed.html', {})

def get_photo(request, id):
    user_profile = get_object_or_404(UserProfile, user_id=id)
    if not user_profile.picture:
        raise Http404
    return HttpResponse(user_profile.picture, content_type=user_profile.content_type)


#Redirect after login
def redirect(request):
    return HttpResponseRedirect('/socialnetwork/')
