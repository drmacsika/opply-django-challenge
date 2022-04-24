from django.contrib.auth.hashers import make_password
from products.models import Order
from rest_framework import serializers

from .models import CustomUser


class CustomerSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        style={"input_type": "password", "placeholder": "Password"},
    )

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(CustomerSerializer, self).create(validated_data)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "password")


class SingleCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "first_name", "last_name")


class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "customer", "products")
