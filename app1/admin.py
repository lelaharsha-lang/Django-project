
from django.contrib import admin
from .models import User, cart

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'mobile_number', 'image')

@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'quantity_of_items', 'total_price')
