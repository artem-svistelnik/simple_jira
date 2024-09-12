from fastapi import HTTPException, status

class ApiError(HTTPException):
    status_code: int
    detail: str

    def __init__(self, status_code: int = None, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)

    def __str__(self):
        return f"{self.status_code}: {self.detail}"


class DataConflictError(ApiError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Data conflict error"


class MultipleResultsError(ApiError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Multiple results found when only one expected"


class NotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found"
