class UsernameAlreadyUsedException(Exception):
    detail = "Username already used"

class UserNotFoundException(Exception):
    detail = "User not found"

class IncorrectUserPasswordException(Exception):
    detail = "Incorrect User Password"

class TokenExpired(Exception):
    detail = "Token has expired"

class TokenNotValid(Exception):
    detail = "Token is not valid"

class TaskNotFound(Exception):
    detail = "Task Not Found"

class CategoryExistAlready(Exception):
    detail = "Category Exist Already"

class CategoryNotFound(Exception):
    detail = "Category not found"