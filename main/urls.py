from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('settings', views.settings_view, name='settings'),
    path('upload', views.upload_view, name='upload'),
    path('follow', views.follow_view, name='follow'),
    path('search', views.search_view, name='search'),
    path('profile/<str:pk>', views.profile_view, name='profile'),
    path('like', views.like_view, name='like'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
