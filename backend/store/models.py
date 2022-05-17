from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.validators import MinValueValidator
import uuid


class Promotion(models.Model):

    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        return self.description


class Collection(models.Model):

    title = models.CharField(max_length=255)
    # Product as string (Product are defined after Collection class)
    # related_name = '+' we don't need revers relational field
    featured_product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(
        Promotion, blank=True, related_name='products')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='orders')

    def customer_first_name(self):
        return self.customer.first_name

    def customer_last_name(self):
        return self.customer.last_name

    def __str__(self):
        for p_status in self.PAYMENT_STATUS_CHOICES:
            if p_status[0] == self.payment_status:
                return p_status[1]

    class Meta:
        ordering = ['payment_status']


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]
