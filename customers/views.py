from core.pagination import CustomPagination
from django.contrib.auth import get_user_model
from products.models import Order
from products.serializers import CustomerOrderHistorySerializer
from rest_framework import mixins, permissions, viewsets

from .serializers import UserSerializer

User = get_user_model()


class CreateCustomerViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    POST: Create a new customer
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerOrderHistoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    GET: Get a customer's order history
    """

    queryset = Order.objects.all()
    serializer_class = CustomerOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Return objects for each authenticated user
        """
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(customer__username=user.username).all()
        return Order.objects.none()
