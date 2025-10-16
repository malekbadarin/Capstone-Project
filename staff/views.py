from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from restaurant.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
guest_staff_list = [
    'customer',
    'staff-login',
]

auth_staff_list = [
    'staff-home',
    'active-orders',
    'completed-orders',
]

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

def customer(request):
    return render('home')

class StaffLogin(LoginRequiredMixin, LoginView):
    template_name = 'staff_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paths'] = guest_staff_list
        return context

@user_passes_test(is_staff_user)
@login_required
def staff_home(request):
    return render(request, 'staff_index.html', {'guest_paths': guest_staff_list ,'auth_paths': auth_staff_list})

@user_passes_test(is_staff_user)
@login_required
def active_orders(request):
    active_orders_list = Order.objects.filter(status = 'P')
    return render(request, 'staff/active_orders.html', {'orders': active_orders_list, 'guest_paths': guest_staff_list ,'auth_paths': auth_staff_list})

@user_passes_test(is_staff_user)
@login_required
def completed_orders(request):
    completed_orders_list = Order.objects.filter(Q(status = 'R') | Q(status = 'C'))
    return render(request, 'staff/completed_orders.html', {'orders': completed_orders_list,'guest_paths': guest_staff_list ,'auth_paths': auth_staff_list})