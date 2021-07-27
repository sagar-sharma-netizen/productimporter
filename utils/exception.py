from __future__ import unicode_literals
from typing import List, Optional


class CustomException(Exception):
    """
    custom Exception class.
    """

    def __init__(
        self,
        title: str,
        detail: Optional[str] = "",
        invalid_params: Optional[List] = None,
    ):
        if invalid_params is None:
            invalid_params = []
        self._title = title
        self._detail = detail
        self._invalid_params = invalid_params
        super(CustomException, self).__init__(title)

    @property
    def title(self):
        """title: exception message"""
        return self._title

    @property
    def detail(self):
        """detail: exception detail message"""
        return self._detail

    @property
    def invalid_params(self):
        """exception params that cause the exception"""
        return self._invalid_params

    def as_dict(self):
        """return dict object of the exception"""
        return {
            "title": self._title,
            "detail": self._detail,
            "invalid_params": self._invalid_params,
        }


class HTTPException(Exception):
    """
    HTTPException class. This is sepcific to HTTP layer.

    - status : HTTP status code
    - title : exception's title message
    - detail : exception's user friendly detailed message
    - invalid_paras: list of data point names with its exception message.
    e.g.
    {
        "status":400,
        "title": "Incorrect username and password",
        "detail": "Ensure that the username and password included in the request are correct",
        "invalid_params": [{
            "name": "username",
            "reason": "Ensure that the username and password included in the request are correct"
        }]
    }
    """

    def __init__(
        self,
        status: int,
        title: str,
        detail: Optional[str] = "",
        invalid_params: Optional[List] = None,
    ):
        if invalid_params is None:
            invalid_params = []
        self._status = status
        self._title = title
        self._detail = detail
        self._invalid_params = invalid_params
        super(HTTPException, self).__init__(title)

    @classmethod
    def from_custom_exception(cls, error: CustomException):
        """Initialise HTTPException from GraniteException instance"""
        http_exception_status_code_mapper = {
            CustomException: 422,
        }
        return cls(
            status=http_exception_status_code_mapper[error.__class__],
            title=error.title,
            detail=error.detail,
            invalid_params=error.invalid_params,
        )

    @property
    def status(self):
        """status: exception HTTP status"""
        return self._status

    def as_dict(self):
        """return dict object of the exception"""
        return {
            "status": self._status,
            "title": self._title,
            "detail": self._detail,
            "invalid_params": self._invalid_params,
        }
