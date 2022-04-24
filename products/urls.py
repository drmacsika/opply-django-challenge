from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import OrdersViewset, ProductViewsets

app_name = "products"

router = SimpleRouter()
router.register("orders", OrdersViewset, basename="orders")
router.register("", ProductViewsets, basename="products")


urlpatterns = router.urls