
from core.pagination import CustomPagination
from rest_framework import generics, mixins, pagination, permissions, viewsets

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer


class ProductViewsets(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    GET: List all products, Get single product with id

    Customers and guests can view product list and single products
    """

    queryset = Product.objects.all().order_by("id", "name")
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET: List all products, Get Single order with order_id
    POST: Create an order for products

    Authenticated Customers can get a list of all orders belonging to them
    Authenticated Customers can get a single order with order_id belonging to them
    Authenticated Customers can create an order for products
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    lookup_field = "order_id"

    def get_queryset(self):
        """
        Return objects for each authenticated user
        """
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(customer__username=user.username).all()
        return Order.objects.none()
