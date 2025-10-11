from django.contrib import admin
from .models import Menu, Order, OrderItem, UserAddress

# Register your models here.
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserAddress)