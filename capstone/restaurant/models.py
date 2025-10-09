from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(
        "Item descritption",
        max_length=250,
        null = True,
        )
    ingredients = models.TextField(
        max_length=250,
        null = True,
        )
    is_available = models.BooleanField(default = True)
    unti_price = models.FloatField()
    portions = models.IntegerField(default = 1)