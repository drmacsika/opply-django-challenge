from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets

from .serializers import CustomerSerializer

User = get_user_model()


class CreateCustomerAPIView(generics.CreateAPIView):
    """
    POST: Create a new customer
    """

    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]  # Explicitly stated for reference


class GetCustomerOrderHistoryAPIView(generics.RetrieveAPIView):
    """
    GET: Get a customer's order history
    """

    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]  # Explicitly stated for reference
