from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


def home(request):
    return render(request,"index.html")

@login_required(login_url='/accounts/login/')
def profile(request):
    # current_user = request.user
    # # get images for the current logged in user
    # images = Image.objects.filter(user_id=current_user.id)
    # # get the profile of the current logged in user
    # profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"images": images, "profile": profile})

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")    