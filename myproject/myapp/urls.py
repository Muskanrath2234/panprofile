from django.urls import path
from . import views

urlpatterns = [
    # Image Upload URL and Result URL
    path('upload_pan/', views.upload_pan, name='upload_pan'),
    path('result/', views.result, name='result'),

    # Show Pan Info URL
    path('show_pan_info/', views.all_pan, name='all_pan'),
    path('user_pan/', views.user_pan, name='user_pan'),

    # Other URLs
    path('home/', views.index, name="home"),
    path('profile/', views.Profile_1, name="Profile"),
    path('', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
]
