from django.contrib import admin

from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "quantity",
        "out_of_stock",
        "is_deleted",
    )
    list_display_links = ("name",)
    list_filter = ("created_at", "updated_at", "is_deleted", "out_of_stock")
    list_editable = ("is_deleted",)
    list_per_page = 10
    date_hierarchy = "created_at"
    search_fields = ("id", "name")
    ordering = ("-id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_id",
        "customer",
        "total_amount",
        "is_deleted",
    )
    list_display_links = ("order_id",)
    list_filter = ("created_at", "updated_at", "is_deleted", "customer")
    list_editable = ("is_deleted",)
    list_per_page = 10
    date_hierarchy = "created_at"
    search_fields = ("order_id", "customer")
    ordering = ("-id",)
