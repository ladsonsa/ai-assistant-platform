from fastapi import HTTPException
from starlette import status


class EmptyConversationError(HTTPException):
    """Exception raised when a chat request contains an empty conversation history.

    Attributes:
        status_code (int): HTTP status code associated with the error (400 Bad Request).
        detail (str): Human-readable explanation of the error.
    """

    def __init__(self) -> None:
        """Initializes the EmptyConversationError with a predefined status code and error message."""
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Conversation history cannot be empty.",
        )
