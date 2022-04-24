from rest_framework.routers import SimpleRouter

from .views import OrderViewset, ProductViewsets

app_name = "products"

router = SimpleRouter()
router.register("orders", OrderViewset, basename="orders")
router.register("", ProductViewsets, basename="products")


urlpatterns = router.urls
