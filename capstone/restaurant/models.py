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
    unit_price = models.FloatField()
    portions = models.IntegerField(default = 1)
    alergens = models.CharField(
        default = 'NA',
        choices = (
            ('PE', 'Peanuts'),
            ('WH', 'Wheat'),
            ('SF', 'Shellfish'),
            ('NA', 'None'),
        )
    )
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = "Owner (has full previliges to edit/delete item)",
        default = 1,
        )
    
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
        auto_now=False,
        auto_now_add=False,
        )
    table_no = models.IntegerField(
        default = 1,
        validators = [MinValueValidator(1), MaxValueValidator(10)], #Fix number of tables to be able to set it dynamically later on
        )
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    @property
    def total(self):
        return sum(item.menu_item.unit_price * item.quantity for item in self.orderitem_set.all())
    
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
        validators = [MinValueValidator(1)],
        )
    
    @property
    def subtotal(self):
        return self.menu_item.unit_price * self.quantity
    
    def __str__(self):
        return f'{self.quantity} x {self.menu_item.name} (JOD {self.menu_item.unit_price * self.quantity})'