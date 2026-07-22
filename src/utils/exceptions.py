class AppException(Exception):
    pass


class APIError(AppException):
    def __init__(self, service: str, status_code: int, message: str):
        self.service = service
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{service}] {status_code}: {message}")
