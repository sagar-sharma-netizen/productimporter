from django.contrib import admin
from django.conf import settings
from .models import (Question, Survey)


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "question",
        "details",
        "answer_type"
    )
    search_fields = ("question",)
    list_filter = ("is_active", "is_deleted", "created_at", "modified_at", "question")
    readonly_fields = ()
    list_per_page = settings.DEFAULT_PAGE_SIZE
    raw_id_fields = ()

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "reporter_name",
        "reporter_email",
    )
    search_fields = ("reporter_name", "reporter_email")
    list_filter = ("is_active", "is_deleted", "created_at", "modified_at", "reporter_name")
    readonly_fields = ()
    list_per_page = settings.DEFAULT_PAGE_SIZE
    raw_id_fields = ()

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Survey, SurveyAdmin)
