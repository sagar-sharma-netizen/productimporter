from django.contrib import admin
from django.conf import settings
from .models import (Product)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "sku",
        "name",
        "details"
    )
    search_fields = ("sku", "name",)
    list_filter = ("is_active", "is_deleted", "created_at", "modified_at", "sku", "name")
    readonly_fields = ()
    list_per_page = settings.DEFAULT_PAGE_SIZE
    raw_id_fields = ()

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


# Register your models here.
admin.site.register(Product, ProductAdmin)
