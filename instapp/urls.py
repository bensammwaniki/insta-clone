from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home),
    path("profile/", views.profile),
    path("login/", views.login),
    path('profile/update/', views.update_profile, name='update.profile'),
    path('upload/add/', views.postimage, name='save.image'),
]