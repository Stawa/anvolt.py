class APIOffline(Exception):
    """
    Raised when the AnVolt-API is unavailable.
    """


class InvalidStatusCode(Exception):
    """
    When the AnVolt-API returns an invalid status code, this exception is raised.
    """


class InvalidResponse(Exception):
    """
    When the AnVolt-API returns an invalid response, this event is triggered.
    """


class InvalidNumber(Exception):
    """
    Whenever a client requests a number that isolates the maximum, this error is thrown..
    """
