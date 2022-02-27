from typing import Any, Dict

from fastapi import HTTPException, status


class GenericAPIException(HTTPException):
    def __init__(
        self, status_code: int, detail: Dict[str, Any] = None, headers: dict = None
    ) -> None:
        super().__init__(
            status_code=status_code
            if isinstance(status_code, int)
            else status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

        self.headers = headers
