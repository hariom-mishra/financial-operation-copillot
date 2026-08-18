class ExpenseException(Exception):
    def __init__(self, message: str,status_code: int = 400):
        self.message = message
        self.status_code = status_code


class UserNotAuthenticatedException(ExpenseException):
    def __init__(self, message: str = "You are not authenticated"):
        super().__init__(message, status_code=401)


class UserNotFoundException(ExpenseException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=404)

