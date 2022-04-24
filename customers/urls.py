from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCustomerAPIView

app_name = "customers"


urlpatterns = [
    # Simple JWT
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("new/", CreateCustomerAPIView.as_view(), name="new_customer"),
]
