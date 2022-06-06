from decimal import Decimal
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import serializers
from .models import Collection, Product, Review, CartItem, Cart, Customer, OrderItem, Order


class CollectionSerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']


class ProductSerializer(serializers.ModelSerializer):

    reviews = serializers.PrimaryKeyRelatedField(read_only=True, Many=True)
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price',
                  'price_with_tax', 'collection', 'reviews']


class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class ReviewSerializer(serializers.ModelSerializer):

    date = serializers.DateField(read_only=True)

    class Meta:
        model = Review
        fields = ['name', 'description', 'date']

    def create(self, validated_data):

        return Review.objects.create(product_id=self.context['product_id'], **validated_data)


class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item):
        return item.product.unit_price * item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):

    created_at = serializers.DateField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price']


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name']


class CustomerSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date', 'membership', 'phone']


class OrderItemSerializer(serializers.ModelSerializer):

    products = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):

    item = OrderItemSerializer(many=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'customer', 'placed_at']
