# reviews/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# Video1: Use Enums for constant choices
class RatingEnum(models.IntegerChoices):
    ONE = 1, _('1 - Poor')
    TWO = 2, _('2 - Fair')
    THREE = 3, _('3 - Good')
    FOUR = 4, _('4 - Very Good')
    FIVE = 5, _('5 - Excellent')

class Manufacturer(models.Model):
    brand = models.CharField(max_length=100)
    year_established = models.PositiveIntegerField()

    def __str__(self):
        return self.brand

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AutoPart(models.Model):
    name = models.CharField(max_length=150)
    part_number = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auto_parts")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="auto_parts")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="auto_parts/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.part_number})"

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def display_price(self):
        return f"${self.price:.2f}"

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user}"

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    auto_part = models.ForeignKey(AutoPart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.auto_part.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.auto_part.price * self.quantity

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews")
    auto_part = models.ForeignKey(AutoPart, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=RatingEnum.choices, default=RatingEnum.THREE)
    comment = models.TextField(blank=True)
    image = models.ImageField(upload_to="reviews/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.auto_part.name} - {self.rating}★"

    @property
    def summary(self):
        return (self.comment[:47] + '...') if len(self.comment) > 50 else self.comment

    @property
    def image_url(self):
        return self.image.url if self.image else None