class APIOffline(Exception):
    """
    An error will occur if the `AnVolt-API` is unavailable.
    """


class InvalidStatusCode(Exception):
    """
    When the `AnVolt-API` returns an invalid status code, this exception is raised.
    """


class InvalidResponse(Exception):
    """
    When the `AnVolt-API` returns an invalid response, this event is triggered.
    """


class InvalidNumber(Exception):
    """
    Whenever a client requests a number that isolates the maximum, this error is thrown.
    """


class InvalidChannel(Exception):
    """
    An error will occur when an incorrect channel ID is provided by the user.
    """


class InvalidArgument(Exception):
    """
    An error may occur when the argument provided is incorrect or if an error is raised by the user.
    """


class AlreadyConnected(Exception):
    """
    An error will occur if the bot/client is already connected to a voice channel.
    """


class NotConnected(Exception):
    """
    An error will occur if the user is not connected to a voice channel.
    """


class PlayerAlreadyPaused(Exception):
    """
    An exception that is raised when the player is already paused.
    """


class PlayerNotPaused(Exception):
    """
    An exception that is raised when the player isn't paused.
    """


class PlayerEmpty(Exception):
    """
    An exception raised when the player has no contents.
    """


class QueueEmpty(Exception):
    """
    An exception raised when the queue has no contents.
    """


class UserOffline(Exception):
    """
    An exception raised when user is offline.
    """
