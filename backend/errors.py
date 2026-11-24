from dataclasses import dataclass, field


@dataclass
class ErrorDetail:
    """A structured application error."""

    code: str
    message: str
    field: str | None = None


class RequestValidationError(Exception):
    """Raised when one or more request fields are invalid."""

    def __init__(self, errors: list[ErrorDetail]):
        self.errors = errors
        message = "; ".join(error.message for error in errors)
        super().__init__(message)


@dataclass
class ErrorResponse:
    """A consistent structure for application errors."""

    success: bool = False
    message: str = "Request validation failed."
    errors: list[ErrorDetail] = field(default_factory=list)
    request_id: str | None = None
