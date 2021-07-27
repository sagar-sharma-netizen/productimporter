from __future__ import unicode_literals


from django.db import models
from survey.models.timestampable import TimeStampable
from survey.managers.question import QuestionManager, QuestionQueryset


class Question(TimeStampable):
    """
    Category Model
    """
    question = models.CharField(
        verbose_name="Question",
        db_index=True,
        max_length=256,
        unique=True
    )
    details = models.CharField(
        verbose_name="Question Details",
        blank=True,
        max_length=256
    )
    answer_type = models.CharField(
        choices=[("int", "Integer"), ("str", "String")],
        default="str",
        max_length=256
    )

    @property
    def as_dict(self):
        return {
            "pk": self.pk,
            "question": self.question,
            "details": self.details,
            "answer_type": self.answer_type
        }
    objects = QuestionManager.from_queryset(QuestionQueryset)()

    def __unicode__(self):
        return self.question

    def __str__(self):
        return self.question
