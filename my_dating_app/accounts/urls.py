from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.logIn, name='login'),
    path('logout', views.logOut, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate")
]
