import django.views.generic as gen_views
from urllib import request
from django.shortcuts import render, redirect
from .models import Menu, Order
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
paths_list = [
    'home',
    'about',
    'menu',
    'login',
    'signup',
]

def home(request):
    return render(request, 'index.html', {'paths': paths_list})

def about(request):
    return render(request, 'about.html', {'paths': paths_list})

def menu(request):
    return render(request, 'restaurant/menu.html', {'menu': Menu.objects.all(), 'paths': paths_list})

class Login(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paths'] = paths_list
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
    context = {'form': form, 'paths': paths_list, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def orderreview(request, order_id):
    order = Order.objects.filter(id = order_id)[0] #Select the first -and only- item in the query set
    return render(request, 'restaurant/order_review.html', {'paths': paths_list, 'order': order})

class OrderConfirmation(gen_views.DetailView):
    pass