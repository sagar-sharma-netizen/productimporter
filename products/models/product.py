from __future__ import unicode_literals


from django.db import models
from products.models.timestampable import TimeStampable
from products.managers.product import ProductManager, ProductQueryset


class Product(TimeStampable):
    """
    Product Model
    """
    sku = models.CharField(
        verbose_name="Product SKU",
        db_index=True,
        max_length=256,
        unique=True
    )
    name = models.CharField(
        verbose_name="Product Name",
        db_index=True,
        max_length=256,
        unique=True
    )
    details = models.CharField(
        verbose_name="Product Details",
        blank=True,
        max_length=256
    )

    @property
    def as_dict(self):
        return {
            "pk": self.pk,
            "sku": self.sku,
            "name": self.name,
            "details": self.details
        }
    objects = ProductManager.from_queryset(ProductQueryset)()

    def __unicode__(self):
        return self.sku

    def __str__(self):
        return self.sku
