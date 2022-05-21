from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
import json

from .models import Profile, User


def index(request):
    
    # getting user id if user is not anonymous
    if request.user.is_authenticated:
        profile = Profile.objects.get(gamer = request.user)
        id = profile.id
        username = profile.gamer
    else:
        id = 0
        username = ''
    

    return render(request, 'escape/index.html', {
        'id': id,
        'username': username
    })


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
            return render(request, "escape/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "escape/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "escape/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "escape/register.html", {
                "message": "Username already taken."
            })

        profile = Profile(gamer = user)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "escape/register.html")

def save(request,id):

    # Get the profile of user whose progress has to be saved or retrieved
    try:
        profile = Profile.objects.get(gamer=request.user)

    except User.DoesNotExist:
        return JsonResponse({
            "error": "Profile does not exist."
        }, status=400)

    # Return a number indicating user's progress
    if request.method=='GET':
        savenum = profile.progress
        # if request.user.is_authenticated:
        #     pass
        return JsonResponse({
            "savenum": savenum
        })

    # Put a number indicating user's progress
    if request.method=='POST':
        res = json.loads(request.body)
        savenum = res['data']
        profile.progress = savenum
        profile.save()
        return HttpResponse(status=204)
