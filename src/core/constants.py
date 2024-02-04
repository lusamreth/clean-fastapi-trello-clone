from enum import Enum


class ErrorTitle(str, Enum):
    DOMAIN_ERROR = "Domain Verification Error"
    UNAUTHENTICATED = "Unauthenticated"
    UNAUTHORIZED = "Unauthorized"
    TOKEN_ERROR = "Token Gen Error"
    UNKNOWN = "Unknown error"
    NOT_FOUND = "Not Found"
    DATA_ACCESS = "Data access error"

    def __str__(self):
        return str(self.value)


class AppErrors(str, Enum):
    AUTH = "auth_error"
    VALIDATION = "validation"
    EMPTY = "not_found"
    INTERNAL = "internal_error"
    UNKNOWN = "unkown"
    DATA_ACCESS = "data_access"

    def __str__(self):
        return str(self.value)
