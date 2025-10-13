from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(
        "Item descritption",
        max_length = 250,
        null = True,
        )
    ingredients = models.TextField(
        max_length = 250,
        null = True,
        )
    is_available = models.BooleanField(default = True)
    unit_price = models.FloatField(
        default = 1.0,
        validators = [MinValueValidator(1)],
    )
    portions = models.IntegerField(default = 1)
    allergen = models.CharField(
        default = 'NA',
        choices = (
            ('PE', 'Peanuts'),
            ('WH', 'Wheat'),
            ('DA', 'Dairy'),
            ('SF', 'Shellfish'),
            ('NA', 'None'),
        )
    )

    @property
    def html_name(self):
        return self.name.replace(" ", "___")
    
    def __str__(self):
        return f"{self.name} (JOD {self.unit_price})"
    
class Order(models.Model):
    date_placed = models.DateTimeField(auto_now_add = True)
    status = models.CharField(
        default = 'O',
        max_length = 1,
        choices = (
            ('O', 'Open'),   #work around for not using sessions or cookies. Any added items will be placed in the Open order. Each user will have only one Open Order at a time.
            ('P', 'Placed'),
            ('R', 'Ready'),
            ('C', 'Closed'),
        )
    )
    order_type = models.CharField(
        default = 'I',
        max_length = 1,
        choices = [
            ('P', 'Pickup'),
            ('D', 'Delivery'),
            ('I', 'Dine In'),
        ]
    )
    party = models.IntegerField(
        default = 1,
        validators = [MinValueValidator(1)],
        )
    reservation_time = models.DateTimeField(
        blank = True,
        null =True,
        )
    table_no = models.IntegerField(
        default = 1,
        validators = [MinValueValidator(1), MaxValueValidator(10)], #TODO: Fix number of tables to be able to set it dynamically later on
        )
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        )
    address = models.CharField(
        blank = True,
        )

    def add_item(self, item_id, quantity):
        if quantity == 0:
            return 'Zero quantity item'
        else:
            new_item = OrderItem(order = self, menu_item_id = item_id, quantity = quantity)
            new_item.save()
            return 'Item created'
    
    def update_item(self, item_id, quantity):
        item = self.orderitem_set.get(menu_item_id = item_id)
        #print(f'Entered update function, item_id {item_id}, old quantity {item.quantity}, new quantity {quantity}')
        if quantity == 0:
            item.delete()
            return 'Item deleted'
        elif item.quantity != quantity:
            item.quantity = quantity
            item.save()
            return 'Quantity updated'
        return 'Quantity unchanged'
    
    def update_type(self, new_type):
        self.order_type = new_type
        self.save()
        return 'Type updated'

    @property
    def total(self):
        return sum(item.menu_item.unit_price * item.quantity for item in self.orderitem_set.all())
    
    @property
    def pickup_time(self):
        return self.reservation_time.time()
    
    @property
    def confirmation_number(self):
        return f'{self.user.id}-{self.id}-{self.date_placed.strftime("%Y%m%d%H%M%S")}'

    def __str__(self):
        return f'Order {self.confirmation_number} - {self.get_status_display()} (JOD {self.total})'

class OrderItem(models.Model):
    menu_item = models.ForeignKey(
        Menu,
        on_delete = models.CASCADE,
        )
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        )
    quantity = models.IntegerField(
        default = 1,
        )
    
    @property
    def subtotal(self):
        return self.menu_item.unit_price * self.quantity
    
    @property
    def html_name(self):
        return self.menu_item.name.replace(" ", "___")
    
    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name} (JOD {self.menu_item.unit_price * self.quantity}) --- (Order info: {self.order})'
    
class UserAddress(models.Model):
    building = models.CharField(
            blank = True,
            max_length = 25,
            )
    street = models.CharField(
            blank = True,
            max_length = 25,
            )
    region = models.CharField(
            "Region/Neighberhood",
            blank = True, 
            max_length = 25,
            )
    city = models.CharField(
            default = 'Amman',
            max_length = 25,
            )
    phone = models.CharField(
            default = '07',
            max_length = 25,
            )
    email = models.CharField(
            blank = True,
            max_length=25,
            )
    user = models.ForeignKey(
            User,
            on_delete = models.CASCADE,
            )
        
    def __str__(self):
        return f'{self.building} {self.street}, {self.region}, {self.city}'