# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from django.db import models


class SurveyQueryset(models.QuerySet):
    def filter_is_deleted(self, is_deleted: bool):
        return self.filter(is_deleted=is_deleted)

    def filter_is_active(self, is_active: bool):
        return self.filter(is_active=is_active)

    def filter_by_category(self, category_id: int):
        return self.filter(category_id=category_id)


class SurveyManager(models.Manager):
    def get_queryset(self):
        return SurveyQueryset(self.model, using=self.db)
