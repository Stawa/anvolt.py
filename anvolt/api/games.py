from anvolt.request import HttpRequest
from anvolt.models.response import Responses
from anvolt.models.enums import Route
from anvolt.utils import Utils
from typing import Optional


class Games:
    def __init__(self, client_id: Optional[str], client_secret: Optional[str] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_request = HttpRequest()
        self.utils = Utils()

    def _make_request(self, route: str, produce: Optional[int] = None) -> Responses:
        url, response = (
            (self.utils.produce(total=produce, route=route), None)
            if produce
            else (
                self.http_request.get(route=route).get("url"),
                self.http_request.get(route=route),
            )
        )
        status_code = response.get("status_code")
        return Responses(url=url, status_code=status_code, original_response=response)

    def truth(
        self, produce: Optional[int] = None, theme: Optional[Route] = Route.GAMES_TRUTH
    ) -> Responses:
        return self._make_request(route=theme.value.value, produce=produce)

    def dare(
        self, produce: Optional[int] = None, theme: Optional[Route] = Route.GAMES_DARE
    ) -> Responses:
        return self._make_request(route=theme.value, produce=produce)
