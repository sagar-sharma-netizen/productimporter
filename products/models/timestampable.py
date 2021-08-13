# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from products.managers.timestampable import (
    TimeStampableManager,
    TimeStampableQueryset,
)


class TimeStampable(models.Model):
    """
    Add default necessary columns to the models.
    Add soft delete property to models.
    """

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)
    is_deleted = models.BooleanField(_("Is deleted instance"), default=False)
    is_active = models.BooleanField(_("Is active instance"), default=True)

    undeleted = TimeStampableManager.from_queryset(TimeStampableQueryset)()

    class Meta:
        abstract = True

    # noinspection PyMethodOverriding
    def delete(self, force: bool = False):
        self.is_deleted = True
        if force:
            super().delete()
        self.save()
