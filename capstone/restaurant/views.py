#import django.views.generic as gen_views
from urllib import request
from django.shortcuts import render, redirect
from .models import Menu
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
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        #print("POST:", request.POST)                # pretty readable already
        print("Keys:", request.POST.keys())         # what fields are there
        print("Username:", request.POST.get('username'))
        print("Raw dict:", request.POST.dict())
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('home')
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'paths': paths_list}
    return render(request, 'registration/signup.html', context)