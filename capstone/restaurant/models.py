from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        verbose_name = "Owner (has full previliges to edit/delete item)",
        default = 1,
        )