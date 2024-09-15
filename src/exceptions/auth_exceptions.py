from fastapi import status
from exceptions.base import ApiError


class PermissionDeniedError(ApiError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Permission denied"


class InvalidCredentials(ApiError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid Credentials"
