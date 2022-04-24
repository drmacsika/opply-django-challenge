import uuid

from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Product(BaseModel):
    """
    Model for Products.

    Reason for extra field: out_of_stock
    -------------------------------------
    Having a custom out_of_stock field allows us to
    control the products that are out of stock rather
    than letting the quantity determine it.
    This is useful when the admin wants to update the products
    while keeping the quantity in stock.
    """

    name = models.CharField(
        _("Name"), help_text=_("Enter product name."), max_length=255
    )
    price = models.DecimalField(
        _("Price"), help_text=_("Enter product price."), max_digits=10, decimal_places=2
    )
    quantity = models.IntegerField(
        _("Quantity"), help_text=_("Enter quantity of product to get."), default=1
    )  # Tracks the quantity of a product
    out_of_stock = models.BooleanField(
        _("Out of Stock"), help_text=_("Check if product is in stock"), default=False
    )

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"<Product {self.name}>"

    @property
    def is_out_of_stock(self):
        """
        Checks if any of the products in the order are out of stock.
        """
        return self.out_of_stock

    def insufficient_quantity(self, quantity):
        """
        Checks if the quantity of the product
        is less than the given quantity.
        """
        return self.quantity < quantity

    def order_product(self, quantity):
        """
        Decrements the quantity of a product by the given quantity.
        """
        if not self.insufficient_quantity(quantity):
            self.quantity -= quantity
            self.save()


class Order(BaseModel):
    """
    Model for orders.

    The id field is retained rather than overridden.
    We use a custom order_id field to track the order id.

    Since the total_amount field is automatically calculated,
    we set editable=False to avoid tampering with the data.
    """

    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_orders"
    )
    products = models.ManyToManyField("products.Product", related_name="product_orders")
    total_amount = models.DecimalField(
        _("Total Amount"),
        help_text=_("Total amount of all products automatically generated."),
        editable=False,
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return f"{self.customer} - {self.created_at}"

    def __repr__(self) -> str:
        return f"<Order {self.customer} - {self.created_at}>"


@receiver(models.signals.post_save, sender=Product)
def update_out_of_stock(sender, instance, **kwargs):
    """
    Updates the out_of_stock field of the product
    when the quantity is updated.

    Useful when you want to send an email to the admin
    to notify that a product is out of stock.
    """
    if not instance.out_of_stock:
        if instance.quantity < 1:
            instance.out_of_stock = True
            instance.save()
