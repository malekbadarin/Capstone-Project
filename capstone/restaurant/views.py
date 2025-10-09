import django.views.generic as gen_views
from django.shortcuts import render, HttpResponse
from .models import Menu

# Create your views here.
def home(request):
    return HttpResponse('Home')

def about(request):
    return HttpResponse('About')

class menu(gen_views.ListView):
    model = Menu
    context_object_name = 'menu'