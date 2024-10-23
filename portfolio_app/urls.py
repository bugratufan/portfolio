from django.urls import path
from . import views 
from .views import list_blogs, blog_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('services/', views.services, name='services'),
    path('blogs/', views.list_blogs, name='blogs'),
    path('blogs/<str:filename>/', blog_detail, name='blog_detail'),
]   
