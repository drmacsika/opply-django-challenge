from customers.serializers import SingleCustomerSerializer
from rest_framework import serializers

from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    customer = SingleCustomerSerializer(many=False)

    class Meta:
        model = Order
        fields = ("order_id", "customer", "products")
        depth = 1
