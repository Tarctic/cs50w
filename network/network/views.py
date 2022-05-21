from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import logging
    # logger = logging.getLogger("mylogger")
    # logger.info(data)

from .models import User, Person, Post
from .forms import PostForm

def index(request):
    return HttpResponseRedirect(reverse("posts", args=('all_posts',)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        first = request.POST["first"]
        last = request.POST["last"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        person = Person(username=user, first=first, last=last)
        person.save()
    
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):

    # Create and save post
    if request.method=='POST':
        content = request.POST.get('content')
        img = request.POST.get('img')
        a = Post(poster=request.user, content=content, img=img)
        a.save()
        return HttpResponseRedirect(reverse("index")) 

    # Call newpost.html with new post form
    if request.method=="GET":
        form = PostForm()
    return render(request, 'network/newpost.html', {
        'form': form
    })

def posts(request, posts):

    # Get all posts or posts that the user is following in decreasing order of creation date
    if request.method=='GET':
        if posts=='all_posts':
            post_list = list(Post.objects.all().order_by('-creation'))
        elif posts=='following':
            if request.user.is_authenticated:
                following_list = Person.objects.filter(username=request.user).values_list('following',flat=True)
                post_list = list(Post.objects.filter(poster__in=following_list).order_by('-creation'))
            else:
                return HttpResponseRedirect(reverse("index")) 

        # Paginate the posts
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_posts = [post.serialize() for post in page_obj]

        try:
            myuser = User.objects.get(username=request.user)
            me = myuser.username
        except:
            me = 'anonymous'

        return render(request, 'network/index.html', context={
            'page_obj': page_obj, 'posts':page_posts, 'me': me
        })

@login_required
def edit(request, id):

    # Get the post that has to be edited
    try:
        post = Post.objects.get(id=id)
    
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"Post with id {id} does not exist."
        }, status=400)
        
    # Save the new content of the post
    if request.method=='PUT':
        data = json.loads(request.body)
        if data.get("data") is not None:
            post.content = data["data"]
            post.save()
        
        return HttpResponse(status=204)

def like(request, id):

    # Get the post that has to be liked or information of which has to be obtained
    try:
        post = Post.objects.get(id=id)
    
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"Post with id {id} does not exist."
        }, status=400)

    # Return number of likes and information on whether the user has liked the post or not
    if request.method=='GET':
        likenum = len(post.likes.all())
        if request.user.is_authenticated:
            if request.user in post.likes.all():
                button = 'fas fa-heart'
            else:
                button = 'far fa-heart'
        else:
            button = 'far fa-heart'
        return JsonResponse({
            "mylike": button,
            "likenum": likenum
        })

    # Add or remove user's like
    if request.method=='PUT':
        data = json.loads(request.body)
        if data.get("data") is not None:
            if data["data"]:
                post.likes.add(request.user)
            else:
                post.likes.remove(request.user)
        return HttpResponse(status=204)

def profile(request, name):

    # Get the User and Person objects and all the posts of the person whose profile page is being accessed.
    try:
        username = User.objects.get(username=name)
        person = Person.objects.get(username=username)
        post_list = list(Post.objects.filter(poster=username).distinct().order_by('-creation'))

    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with username {username} does not exist."
        }, status=400)

    # Get the number of followers and following and paginate all the posts. Return all required data.
    if request.method=='GET':
        followersnum = len(person.followers.all())
        followingnum = len(person.following.all())
        if request.user.is_authenticated:
            if request.user in person.followers.all():
                button = 'Unfollow'
            else:
                button = 'Follow'
        
            display=True
            if request.user == username:
                display = False
        else:
            display = False
            button = 'Follow'

        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_posts = [post.serialize() for post in page_obj]

        try:
            myuser = User.objects.get(username=request.user)
            me = myuser.username
        except:
            me = 'anonymous'

        return render(request, 'network/profile.html', {
            'thisuser': person,
            'button': button,
            'display': display,
            'followers': followersnum,
            'following': followingnum,
            'posts': page_posts,
            'page_obj': page_obj,
            'me': me
        })

    # Add/remove user object of user to/from the person object of person being followed/unfollowed (followers)
    # Add/remove user object of person to/from the person object of user when user clicks follow/unfollow (following)
    if request.method=='PUT':
        data = json.loads(request.body)
        if data.get("follow") is not None:
            myuser = Person.objects.get(username=request.user)
            if data["follow"]:
                person.followers.add(request.user)
                myuser.following.add(username)
            else:
                person.followers.remove(request.user)
                myuser.following.remove(username)
        return HttpResponse(status=204)

