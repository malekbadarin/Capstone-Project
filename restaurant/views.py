from django.shortcuts import render, redirect
from .models import Menu, Order, User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.utils import timezone

# Create your views here.
guest_paths_list = [
    'home',
    'about',
    'login',
    'signup',
    #'staff',
]

auth_paths_list = [
    'home',
    'about',
    'order-menu',
    'profile',
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

def menu_helper_function(request):
    menu = Menu.objects.all().order_by('id')
    order = Order.objects.filter(user = request.user, status = 'O').first()
    if not order:
        order_type = 'I'
    else:
        order_type = order.order_type
    for item in menu:
        try:
            item.quantity = item.orderitem_set.filter(order_id = order.id).first().quantity
            item.id=str(item.id)
        except:
            item.quantity = 0
    print(f'------------------------------------\nmenu: {Menu}\nmenu.objects.all(): {Menu.objects.all()}\nmenu.objects.all().order_by(id): {Menu.objects.all().order_by('id')}\nmenu.objects.all().order_by(id)[0] {Menu.objects.all().order_by('id')[0]}\nmenu.objects.all().order_by(id)[0].name: {Menu.objects.all().order_by('id')[0].id}\n------------------------------------')
    return menu, order_type

@login_required
def order_menu(request):
    menu, order_type = menu_helper_function(request)
    #print(f'----------{order_type}--------------')
    return render(request, 'restaurant/order_menu.html', {'menu': menu, 'order': order_type, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

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
        user = request.user
        """ addresses = User.useraddress_set.filter(user = user)
        try:
            default_address = addresses.first()
        except:
            default_address = '' """
        response = request.POST
        menu_item_names = [item.name for item in Menu.objects.all()]
        order = Order.objects.filter(user = request.user, status = 'O').first() #tries to find an open order for the user if no open order is found, creates a new order
        if not order:
            order = Order(user = user)
            order.save()
        order_item_names = [item.menu_item.name for item in order.orderitem_set.all()]
        for key, value in response.items():
            key = key.replace("___", " ") #convert the name of the input tag back into an item name
            #print(f'-----------------{key}-----------------')
            if key in menu_item_names:
                menu_item_id = Menu.objects.filter(name = key).first().id
                if key in order_item_names:
                    old_quantity = order.orderitem_set.get(menu_item__name = key).quantity
                    #print(f'---item_id {menu_item_id} old quantity {old_quantity} new quantity {int(value)}---')
                    order.update_item(menu_item_id, int(value))
                    continue
                else:
                    order.add_item(menu_item_id, int(value))
            try:
                if key == 'order-type':
                    order.update_type(value)
                    #print(f'order-type: {value}')
            except:
                print(f'Order probably does not exist. order_type {value} not saved')
        if not order.total:
            order.delete()
            return redirect('order-menu')
        else:
            return render(request, 'restaurant/order_review.html', {'order': order, 'tables': [table for table in range(1,11)], 'auth_paths': auth_paths_list})
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
            key = key.replace("___", " ") #convert the name of the input tag back into an item name
            #print(f'-----------------{key}-----------------')
            if key in menu_item_names:
                menu_item_id = Menu.objects.filter(name = key).first().id
                order.update_item(menu_item_id, int(value))
            elif key == 'table':
                #print(f'table: {value}')
                try:
                    order.table_no = int(value)
                    #TODO: add logic to check table availability and remove unavailable tables (will require a Table model)
                except:
                    print(f'Order probably does not exist. table_no {value} not saved')
            elif key == "party":
                #print(f'party: {value}')
                try:
                    order.party = int(value)
                    #TODO: add logic to check persons vs table availability (will probably require changes to the table selection UI and logic)
                except:
                    print(f'Order probably does not exist. party {value} not saved')
            elif key == "reservation-datetime":
                print(f'reservation-datetime: {value}')
                try:
                    reservation_time_object = timezone.make_aware(datetime.strptime(value, '%Y-%m-%dT%H:%M')) #Convert the input into a datetime object (which django expects for a DateTimeField, and then make it aware of its timezone to avoid conflicts)
                    order.reservation_time = reservation_time_object
                    #TODO: add logic to constrain available reservation time both on frontend (for workhours/workdays), and backend (for ensuring no conflict in reservations)
                except:
                    print(f'Order probably does not exist. reservation-datetime {value} not saved')
            elif key == "pickup-time":
                print(f'pickup-time: {value}')
                try:
                    reservation_time_object = timezone.make_aware(datetime.combine(datetime.today(), datetime.strptime(value, '%H:%M').time())) #Similar to above, but first combine the time input with today's date
                    order.reservation_time = reservation_time_object
                    #TODO: add logic to constrain available reservation time both on frontend (disable on off days)
                except:
                    print(f'Order probably does not exist. pickup-time {value} not saved')
        order.status = 'P'
        order.save()
        if not order.total:
            order.delete()
            return redirect('order-menu')
    #else:
    #    print('------------GET-------------')
    return render(request, 'restaurant/order_confirmation.html', {'order': order, 'auth_paths': auth_paths_list})

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    return render(request, "user/profile.html", {'orders':orders, 'auth_paths': auth_paths_list})

@login_required
def staff(request):
    return redirect("staff-home")