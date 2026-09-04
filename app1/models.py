from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
   # mobile_number = models.IntegerField(unique=True,null=True)
    mobile_number = models.CharField(max_length=15, null=True, unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.username
class cart(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField(null=True)
    quantity_of_items = models.IntegerField(null=True)
    def total_price(self):
        return self.item_price * self.quantity_of_items