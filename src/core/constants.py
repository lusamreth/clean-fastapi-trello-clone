from enum import Enum


class ErrorTitle(Enum):
    DOMAIN_ERROR = "Domain Verification Error"
    UNAUTHENTICATED = "Unauthenticated"
    UNAUTHORIZED = "Unauthorized"
    TOKEN_ERROR = "Token Gen Error"
    UNKNOWN = "Unknown error"
    NOT_FOUND = "Not Found"


class AppErrors:
    AUTH = "auth_error"
    VALIDATION = "validation"
    EMPTY = "not_found"
    INTERNAL = "internal_error"
