from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCustomerViewset, CustomerOrderHistoryViewset

app_name = "customers"

router = SimpleRouter()

router.register("new", CreateCustomerViewset, basename="users")
router.register("order-history", CustomerOrderHistoryViewset, basename="customers")


urlpatterns = [
    # Simple JWT
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
] + router.urls
