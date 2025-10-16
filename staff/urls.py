from django.urls import path
from . import views


urlpatterns = [
    path('', views.staff_home, name = 'staff-home'),
    path('customer/', views.customer, name = "customer"),
    path('login/', views.StaffLogin.as_view(), name = "staff-login"),
    path('active-orders/', views.active_orders, name = 'active-orders'),
    path('completed-orders/', views.completed_orders, name = 'completed-orders'),
]