from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Collection, Product, Review, CartItem, Cart, Customer, OrderItem, Order


class CollectionSerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']


class ProductSerializer(serializers.ModelSerializer):

    reviews = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax'
    )

    def calculate_tax(self, product):
        return product.unit_price * Decimal(1.2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'inventory', 'unit_price',
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


class CreateCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            return serializers.ValidationError('The Product with given ID does not exists')
        return value

    def save(self, **kwargs):

        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id
            )

            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
            self.instance = cart_item

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
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
