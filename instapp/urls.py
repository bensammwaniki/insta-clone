from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home),
    path("profile/", views.profile),
    path('profile/update/', views.update_profile, name='update.profile'),
    path('upload/add/', views.postimage, name='save.image'),
    path('like/<int:id>/', views.like_image, name='like.image'),
    path('comment/', views.save_comment, name='comment.add'),
    path('picture/<int:id>/', views.show_image, name='show.image'),
    path('search/', views.search_post, name='search.post')
]