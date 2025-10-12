from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    #path('menu/', views.menu, name = 'menu'), #deprecated view replaced with order-menu
    path('login/', views.Login.as_view(), name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.Logout.as_view(), name = 'logout'),
    path('order/menu/', views.order_menu, name = "order-menu"),
    #path('order/add-item/<int:item_id>', views.add_item, name = "add-item"), #outdated path used to update each line item then refresh the page
    #path('order/remove-item/<int:item_id>', views.remove_item, name = "remove-item"), #outdated path used to update each line item then refresh the page
    path('order/review/', views.orderreview, name = 'order-review'), #order review, edit, and placement view
    path('order/confirmation/<int:order_id>', views.order_confirmation, name = 'order-confirmation'),
    path('staff/', views.staff, name = 'staff'),
]