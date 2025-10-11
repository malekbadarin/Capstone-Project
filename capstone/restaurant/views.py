from django.shortcuts import render, redirect
from .models import Menu, Order, OrderItem
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
guest_paths_list = [
    'home',
    'about',
    'menu',
    'login',
    'signup',
]

auth_paths_list = [
    'home',
    'about',
    'order-menu',
]

def home(request):
    return render(request, 'index.html', {'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

def about(request):
    return render(request, 'about.html', {'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

def menu(request):
    return render(request, 'restaurant/menu.html', {'menu': Menu.objects.all(), 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

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
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class Logout(LogoutView):
    next_page = '/'

def order_menu(request):
    menu = Menu.objects.all()
    try: #checks if there is an Open order for the user. If not, creates one
        order = Order.objects.get(user = request.user, status = 'O')
    except:
        order = Order(user = request.user)
        order.save()
    for item in menu:
        if item in order.orderitem_set.all():
            item.quantity = order.orderitem_set.get(menu_item_id = item.id).quantity
        else:
            item.quantity = 0
    return render(request, 'restaurant/order_menu.html', {'menu': menu, 'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list})

def add_item(request, order_id, item_id):
    try:
        item = Order.objects.get(id = order_id).orderitem_set.get(menu_item_id = item_id) #Get the order > get OrderItem set > get item
        item.quantity += 1
    except:
        item = OrderItem(order_id = order_id, menu_item_id = item_id)
    item.save()
    return redirect("order-menu")

def remove_item(request, order_id, item_id):
    print(f'order_id: {order_id}, item_id: {item_id}, {Order.objects.get(id = order_id).orderitem_set.get(menu_item_id = item_id)}')
    try:
        item = Order.objects.get(id = order_id).orderitem_set.get(menu_item_id = item_id) #Get the order > get OrderItem set > get item
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except:
        pass
    return redirect("order-menu")

def orderreview(request, order_id):
    order = Order.objects.get(id = order_id)
    return render(request, 'restaurant/order_review.html', {'order': order, 'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list, 'order': order})

def order_confirmation(request, order_id):
    order = Order.objects.filter(id = order_id)[0] #Select the first -and only- item in the query set
    if order.status == 'O': #Changes the status of the order to Placed instead of Open
        order.status = 'P'
        order.save()
    return render(request, 'restaurant/order_confirmation.html', {'guest_paths': guest_paths_list, 'auth_paths': auth_paths_list, 'order': order})