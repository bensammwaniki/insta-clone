from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

import cloudinary
import cloudinary.uploader
import cloudinary.api

@login_required(login_url='/accounts/login/')
def home(request):
    images = Image.objects.all().order_by('-image_date')
    return render(request, 'index.html', {'images': images})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    images = Image.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"images": images, "profile": profile})

def login(request):
    return render(request,"login.html")