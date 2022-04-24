from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CreateCustomerViewset, CustomerOrderHistoryViewset

app_name = "customers"

router = SimpleRouter()

router.register("new", CreateCustomerViewset, basename="customers")
router.register("order-history", CustomerOrderHistoryViewset, basename="customers")


urlpatterns = [
    # Simple JWT
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
] + router.urls
