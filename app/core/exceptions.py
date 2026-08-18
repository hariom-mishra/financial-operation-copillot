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

class TokenValidationException(ExpenseException):
    def __init__(self, message: str = "Token validation failed"):
        super().__init__(message, status_code=400)

class TokenExpiredException(ExpenseException):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, status_code=400)

class TokenCreationException(ExpenseException):
    def __init__(self, message: str = "Token creation failed"):
        super().__init__(message, status_code=400)

class DatabaseConnectionException(ExpenseException):
    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message, status_code=500)

class UserExistsException(ExpenseException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, status_code=400)

class InvalidCredentialsException(ExpenseException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)
 
class TokenNotProvidedException(ExpenseException):
    def __init__(self, message: str = "Token not provided"):
        super().__init__(message, status_code=401)

class UnauthorizedException(ExpenseException):
    def __init__(self, message: str = "You are not authorized to perform this action"):
        super().__init__(message, status_code=403)