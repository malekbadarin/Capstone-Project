from django.shortcuts import render, redirect
from .models import Menu, Order, OrderItem, UserAddress
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django import forms

# Create your views here.
guest_paths_list = [
    'home',
    'about',
    'login',
    'signup',
    'staff',
]

auth_paths_list = [
    'home',
    'about',
    'order-menu',
    'staff',
]

def home(request):
    return render(request, 'index.html', {'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

def about(request):
    return render(request, 'about.html', {'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

""" def menu(request):
    return render(request, 'restaurant/menu.html', {'menu': Menu.objects.all(), 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list}) """

class Login(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paths'] = guest_paths_list
        return context
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Created user:", user.pk, user.username)
            login(request, user)
            return redirect('order-menu')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'

@login_required
def order_menu(request):
    menu = Menu.objects.all().order_by('id')
    order = Order.objects.filter(user = request.user, status = 'O').first()
    for item in menu:
        try:
            item.quantity = item.orderitem_set.get(order_id = order.id).quantity
        except:
            item.quantity = 0
    return render(request, 'restaurant/order_menu.html', {'menu': menu, 'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

"""
Old order creation and update logic. Did not rely on forms. Most likely less secure.
@login_required
def add_item(request, item_id):
    order = Order.objects.filter(user = request.user, status = 'O').first()
    if order:
        try:
            item = Order.objects.get(id = order.id).orderitem_set.get(menu_item_id = item_id) #Get the order > get OrderItem set > get item
            item.quantity += 1
        except:
            item = OrderItem(order_id = order.id, menu_item_id = item_id)
    else:
        default_address = UserAddress.objects.filter(user = request.user).first()
        if not default_address:
            default_address = UserAddress(user = request.user)
            default_address.save()
        order = Order(user = request.user, address = default_address)
        order.save()
        item = OrderItem(order_id = order.id, menu_item_id = item_id)
    item.save()
    return redirect("order-menu")

@login_required
def remove_item(request, item_id):
    order = Order.objects.filter(user = request.user, status = 'O').first()
    if order:
        try:
            item = Order.objects.get(id = order.id).orderitem_set.get(menu_item_id = item_id) #Get the order > get OrderItem set > get item
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                current_order = Order.objects.get(id = order.id)
                if current_order.total == 0: #Deletes empty orders
                    current_order.delete()
        except:
            pass
    return redirect("order-menu")

@login_required
def orderreview(request, order_id):
    order = Order.objects.get(id = order_id)
    return render(request, 'restaurant/order_review.html', {'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})"""

@login_required
def orderreview(request):
    if request.method == 'POST':
        response = request.POST.copy()
        del response['csrfmiddlewaretoken']
        valid_order = False
        new_order = Order(user = request.user)
        new_order.save()
        for key, value in response.items():
            menu_item = Menu.objects.filter(id = int(key)).first()
            if int(value) > 0:
                valid_order = True
                try:
                    new_order_item = OrderItem(order = new_order, menu_item = menu_item, quantity = int(value))
                    new_order_item.save()
                    print(new_order_item)
                except:
                    pass
        if not valid_order:
            new_order.delete()
        else:
            return render(request, 'restaurant/order_review.html', {'order': new_order, 'tables': [table for table in range(1,11)]})
    else:
        return redirect('order-menu')

"""
Also outdated function that did not utilise forms and csrf.
@login_required
def order_confirmation(request, order_id):
    order = Order.objects.filter(id = order_id)[0] #Select the first -and only- item in the query set
    if order.status == 'O': #Changes the status of the order to Placed instead of Open
        order.status = 'P'
        order.date_placed = datetime.now()
        order.save()
    return render(request, 'restaurant/order_confirmation.html', {'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list}) """

@login_required
def staff(request):
    return redirect("staff-home")