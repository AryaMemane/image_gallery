from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_pin, name='upload_pin'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('like/<int:pin_id>/', views.like_pin, name='like_pin'),
    path('download/<int:pin_id>/', views.download_pin, name='download_pin'),
    path('delete_pin/<int:pin_id>/', views.delete_pin, name='delete_pin'),
]


