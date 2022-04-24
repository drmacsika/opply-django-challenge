from decimal import Decimal

from customers.serializers import CustomerSerializer
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Order, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    """
    GET: List all products, Get single product with id
    POST: Create an order for products

    - Handles the List and Retrieve actions for Products
    - Handles the Create action for Orders,
    since all we need is just id and quantity
    """

    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ("id", "name", "price", "quantity")

    def validate_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with the id '{value}' does not exist"
            )
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value

    def validate(self, data):
        product_id = data.get("id")
        quantity = data.get("quantity")
        product = Product.objects.get(id=product_id)
        if product.is_out_of_stock:
            raise serializers.ValidationError(
                f"Product with the id '{product_id}' is out of stock."
            )
        if product.insufficient_quantity(quantity):
            raise serializers.ValidationError(
                f"Not enough products in stock. Only {product.quantity} left."
            )
        return data


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ("order_id", "customer", "products")

    def validate_products(self, value):
        """
        This validation is essential to prevent the same ids
        from being used in multiple
        objects that are being created in the same request.
        """
        ids = [id for v in value for id in v.values()]
        if len(set(ids[0::2])) != len(ids[0::2]):
            raise serializers.ValidationError(
                "One or more product ids are repeated. Please specify one product id per item."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        authenticated_username = self.context["request"].user.username
        customer = validated_data["customer"]
        products = validated_data["products"]

        if customer.get("username") != authenticated_username:
            raise serializers.ValidationError(
                "Customer username is not the logged in user. Please login with the customer username."
            )
        customer = User.objects.get(username=authenticated_username)

        total_amount = Decimal(0.0)
        product_queryset = []
        for product in products:
            product_id = product.get("id")
            quantity = product.get("quantity")
            product_obj = Product.objects.get(id=product_id)

            # Calculates the total amount of the order
            total_amount += product_obj.price * quantity

            # Decrements the quantity of the product
            product_obj.order_product(quantity)
            product_queryset.append(product_obj)

        # Creates the order
        try:
            order = Order.objects.create(customer=customer, total_amount=total_amount)
            order.products.set(product_queryset)
            order.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error creating order: {e}")

        return validated_data


class CustomerOrderHistorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ("id", "customer", "total_amount", "products")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for i in ["customer", "id", "total_amount"]:
            data.pop(i)

        data["customer_username"] = instance.customer.username
        if instance.customer.email:
            data["customer_email"] = instance.customer.email
        data["total_products_ordered"] = len(data["products"])
        data["total_amount_spent_on_order"] = instance.total_amount
        data["date_ordered"] = instance.created_at.strftime("%d/%m/%Y")
        data["products_ordered"] = [
            {"name": p.name, "price": p.price, "quantity": p.quantity}
            for p in instance.products.all()
        ]
        data.pop("products")
        return data
