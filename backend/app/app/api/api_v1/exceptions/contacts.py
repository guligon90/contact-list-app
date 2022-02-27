from app.api.api_v1.exceptions.base import GenericAPIException, status


class ContactDuplicatedException(GenericAPIException):
    """
    Exception raised for errors in the contact RESTful APU.
    """

    def __init__(
        self, phone_number: str, status_code: str = status.HTTP_400_BAD_REQUEST
    ):
        self.status_code = status_code
        self.detail = {
            "error": self.__class__.__name__,
            "message": f"A contact with the phone number {phone_number} already exists",
        }

        super().__init__(self.status_code, self.detail)


class ContactAPIException(GenericAPIException):
    pass
