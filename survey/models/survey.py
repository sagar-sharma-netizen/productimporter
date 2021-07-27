from __future__ import unicode_literals

from django.db import models
from survey.models import TimeStampable
from survey.managers.survey import SurveyManager, SurveyQueryset


class Survey(TimeStampable):
    """
    Sub Category Model
    """
    reporter_name = models.CharField(
        verbose_name="Reporter Name",
        db_index=True,
        max_length=256
    )
    reporter_email = models.CharField(
        verbose_name="Report Email",
        blank=True,
        max_length=256,
        db_index=True
    )
    answers = models.JSONField(
        verbose_name="Survey Result",
        default=dict
    )

    @property
    def as_dict(self):
        return {
            "pk": self.pk,
            "reporter_name": self.reporter_name,
            "reporter_email": self.reporter_email,
            "answers": self.answers
        }
    objects = SurveyManager.from_queryset(SurveyQueryset)()

    def __unicode__(self):
        return f"{self.reporter_name} {self.reporter_email} survey"

    def __str__(self):
        return f"{self.reporter_name} {self.reporter_email} survey"
