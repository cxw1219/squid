class DataValidationError(Exception):
    pass

class SecurityError(Exception):
    pass

class PriceIntegrityError(Exception):
    pass

class DataIntegrityError(Exception):
    pass

class RateLimitExceeded(Exception):
    pass

class DatabaseError(Exception):
    pass