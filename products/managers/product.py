# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from django.db import models


class ProductQueryset(models.QuerySet):
    def filter_is_deleted(self, is_deleted: bool):
        return self.filter(is_deleted=is_deleted)

    def filter_is_active(self, is_active: bool):
        return self.filter(is_active=is_active)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, using=self._db)
