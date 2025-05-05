from django.contrib import admin
from .models import Manufacturer, Category, AutoPart, Cart, CartItem

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("brand", "year_established")
    search_fields = ("brand",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(AutoPart)
class AutoPartAdmin(admin.ModelAdmin):
    list_display = ("name", "part_number", "category", "manufacturer", "price", "stock")
    list_filter = ("category", "manufacturer")
    search_fields = ("name", "part_number")
    autocomplete_fields = ("category", "manufacturer")

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "auto_part", "quantity")
    autocomplete_fields = ("cart", "auto_part")
