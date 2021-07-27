from django.forms.models import model_to_dict


def serialize(queryset):
    return [model_to_dict(item) for item in queryset]
