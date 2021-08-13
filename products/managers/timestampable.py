# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from django.db import models


class TimeStampableQueryset(models.QuerySet):
    def filter_is_deleted(self, is_deleted: bool):
        return self.filter(is_deleted=is_deleted)

    def filter_is_active(self, is_active: bool):
        return self.filter(is_active=is_active)

    def delete(self, force: bool = False):
        self.update(is_deleted=True)
        if force:
            super().delete()


class TimeStampableManager(models.Manager):
    def get_queryset(self):
        return (
            super(TimeStampableManager, self)
            .get_queryset()
            .filter_is_deleted(False)
        )
