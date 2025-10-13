from django.shortcuts import render, redirect
from .models import Menu, Order, OrderItem, UserAddress
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

def menu_helper_function(request):
    menu = Menu.objects.all().order_by('id')
    order = Order.objects.filter(user = request.user, status = 'O').first()
    for item in menu:
        item.html_id = item.name.replace(" ", "")
        try:
            item.quantity = item.orderitem_set.filter(order_id = order.id).first().quantity
        except:
            item.quantity = 0
    return menu

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
            item.quantity = item.orderitem_set.filter(order_id = order.id).first().quantity
        except:
            item.quantity = 0
    return render(request, 'restaurant/order_menu.html', {'menu': menu, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

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
def order_review(request):
    if request.method == 'POST':
        response = request.POST
        valid_order = False
        menu_item_names = [item.name for item in Menu.objects.all()]
        order = Order.objects.filter(user = request.user, status = 'O').first() #tries to find an open order for the user if no open order is found, creates a new order
        if not order:
            order = Order(user = request.user)
            order.save()
        order_item_names = [item.menu_item.name for item in order.orderitem_set.all()]
        for key, value in response.items():
            if key in menu_item_names and int(value) > 0:
                menu_item_id = Menu.objects.filter(name = key).first().id
                if key in order_item_names:
                    valid_order = True
                    old_quantity = order.orderitem_set.get(menu_item__name = key).quantity
                    print(f'---item_id {menu_item_id} old quantity {old_quantity} new quantity {int(value)}---')
                    if int(value) != old_quantity:
                        order.update_item(menu_item_id, int(value))
                    continue
                order.add_item(menu_item_id, int(value))
                valid_order = True
        if not valid_order:
            order.delete()
            return redirect('order-menu')
        else:
            return render(request, 'restaurant/order_review.html', {'order': order, 'tables': [table for table in range(1,11)]})
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
def order_confirmation(request, order_id):
    order = Order.objects.filter(id = order_id, user = request.user).first()
    if request.method == 'POST':
        response = request.POST
        menu_item_names = [item.name for item in Menu.objects.all()]
        for key, value in response.items():
            if key in menu_item_names and int(value) > 0:
                menu_item_id = Menu.objects.filter(name = key).first().id
                order.update_item(menu_item_id, int(value))
            elif key == 'table':
                print(f'table: {value}')
                try:
                    order.table = int(response[key])
                except:
                    pass #Lazy solution, but obscure if exception is raised. TODO: Fix esception handling for better maintainability.
                         #Also TODO: add logic to check table availability and remove unavailable tables (will require a Table model)
            elif key == "party":
                print(f'party: {value}')
                try:
                    order.party = int(response[key])
                except:
                    pass #Lazy solution, but obscure if exception is raised. TODO: Fix esception handling for better maintainability.
                         #Also TODO: add logic to check persons vs table availability (will probably require changes to the table selection UI and logic)
        order.status = 'P'
        order.save()
        if not order.total:
            order.delete()
            return redirect('order-menu')
    
    return render(request, 'restaurant/order_confirmation.html', {'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

@login_required
def staff(request):
    return redirect("staff-home")