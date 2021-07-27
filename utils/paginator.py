from __future__ import unicode_literals

from contextlib import suppress

from django.core.paginator import Paginator


def paginate_queryset(queryset, page: int, page_size: int) -> dict:
    """
    Paginate Django queryset

    Args:
        queryset: queryset object
        page (int): page
        page_size (int): page_size

    Return:
        {
            "results": [...],
            "count": 12,
            "next_page": null,
            "previous_page": 1
        }
    """
    if page is None:
        page = 1
    if page_size is None:
        page_size = 10
    page = int(page)
    page_size = int(page_size)
    results = []
    previous_page = None
    next_page = None
    paginator = Paginator(queryset, page_size)
    with suppress(Exception):
        paginator.validate_number(page)
        results = paginator.page(page).object_list
        paginator.validate_number(page + 1)
        next_page = page + 1
    with suppress(Exception):
        # Prev page can still be valid - hence separate
        paginator.validate_number(page - 1)
        previous_page = page - 1
    return {
        "results": results,
        "count": paginator.count,
        "next_page": next_page,
        "previous_page": previous_page,
    }
