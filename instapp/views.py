from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

@login_required(login_url='/accounts/login/')
def home(request):
    images = Post.objects.all().order_by('-image_date')
    return render(request, 'index.html', {'images': images})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    images = Post.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(user_id=current_user.id).first()
    return render(request, 'profile.html', {"images": images, "profile": profile})

@login_required(login_url='/accounts/login/')
def postimage(request):
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']
        image = Post(image_name=image_name, image_caption=image_caption, image=image_url,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()
        return redirect('/profile', {'success': 'Successfully posted'})
    else:
        return render(request, 'profile.html', {'danger': 'posting Failed'})

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_url
            profile.bio = bio
            profile.save()
        else:
            profile = Profile(user_id=current_user.id,
                              profile_photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.username = username
        user.last_name = last_name
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Updated your profile Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Update Failed'})    

@login_required(login_url='/accounts/login/')
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()
    # check if the user has already liked the image
    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():
        likes.delete()
        image = Post.objects.get(id=id)
        if image.like_count == 0:
            image.like_count = 0
            image.save()
        else:
            image.like_count -= 1
            image.save()
        return redirect('/')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Post.objects.get(id=id)
        image.like_count = image.like_count + 1
        image.save()
        return redirect('/')


@login_required(login_url='/accounts/login/')
def comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Post.objects.get(id=image_id)
        user = request.user
        comment = Comments(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()
        image.comment_count = image.comment_count + 1
        image.save()
        return redirect('/' + str(image_id))
    else:
        return redirect('/')        