from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('menu/', views.menu, name = 'menu'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
    path('order/menu/', views.order_menu, name = "order-menu"),
    path('order/review/<int:order_id>', views.orderreview, name = 'order-review'), #order review, edit, and placement view
    path('order/confirmation/<int:order_id>', views.order_confirmation, name = 'order-confirmation'),
]