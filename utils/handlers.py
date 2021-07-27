# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals
import json
import traceback
from contextlib import suppress
from json.decoder import JSONDecodeError
from typing import Dict, List, Tuple
from utils.logger import Logger
# lib imports
from django.http import HttpRequest, HttpResponse
from utils.exception import CustomException, HTTPException


def _request_handler(
    request: HttpRequest, config: Dict
) -> Tuple[Dict, Dict, Dict]:
    """
    Process Django request instance and returns version, params, post data
    """
    params = request.GET.dict()
    body = {}
    headers = {
        header: request.META.get(header) for header in config.get("headers")
    } if config.get("headers") else {}

    if request.content_type == "application/json":
        with suppress(JSONDecodeError):
            body = json.loads(request.body)
    else:
        body = request.POST.dict()
        for file, value in request.FILES.items():
            body[file] = value

    return headers, params, body


def handle_api_exception(func):
    """
    Decorator function to handle any exception from APIs.
    It serialise error data as dict response.
    """

    def inner(*args, **kwargs):
        """
        handler api exception
        """
        request = args[0]
        content_type = "application/json"
        try:
            body, status = func(*args, **kwargs)
        except CustomException as error:
            exp = HTTPException.from_custom_exception(error)
            body = _serialize(exp.as_dict())
            status = exp.status
        except HTTPException as error:
            body = _serialize(error.as_dict())
            status = error.status
        except Exception as error:
            error_traceback = traceback.format_exc()
            Logger.error(error_traceback)
            body = "Something went wrong"
            status = 500
        return HttpResponse(
            json.dumps(body), status=status, content_type=content_type
        )

    return inner


def _serialize(
    body
) -> Dict:
    """
    Serialize fields into json dumpable objects
    """
    return body


def api_handler():
    """
    API Handler
    :return:
    """
    def decorator(func):
        """
        Decorator
        :param func:
        :return:
        """
        def inner(request, *args, **kwargs):
            module_name = func.__module__.split(".")[-1]
            api_name = func.__name__
            method = request.method
            headers, params, body = _request_handler(
                request=request, config={}
            )
            request_params = {
                "method": method,
                "headers": headers,
            }
            print("params", params)
            body, status = func(
                request_params, params, body, *args, **kwargs
            )
            response = _serialize(body)
            return response, status
        return inner
    return decorator
