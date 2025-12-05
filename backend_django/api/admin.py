from django.contrib import admin
from .models import Product, CustomUser, Cart, CartItem, Order, OrderItem
from django.contrib.auth.admin import UserAdmin

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)
