from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('menu/', views.menu, name = 'menu'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('signup/', views.signup, name = 'signup'),
]