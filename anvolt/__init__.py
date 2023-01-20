from anvolt.api import Sfw, Nsfw, Games
from anvolt.trivia import Trivia
from anvolt.updater import Updater
from anvolt.utils import Utils
from typing import Optional

__name__ = "anvolt.py"
__version__ = "0.1.3"
__author__ = "Stawa"
__license__ = "MIT"


class AnVoltClient:
    """AnVoltClient is a class that allows you to interact with the AnVolt API."""

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        self.sfw = Sfw(client_id=client_id, client_secret=client_secret)
        self.nsfw = Nsfw(client_id=client_id, client_secret=client_secret)
        self.games = Games(client_id=client_id, client_secret=client_secret)
