from anvolt.request import HttpRequest
from anvolt.models.response import Responses
from anvolt.models.enums import Route
from anvolt.utils import Utils
from typing import Optional


class Nsfw:
    def __init__(self, client_id: Optional[str], client_secret: Optional[str] = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.http_request = HttpRequest()
        self.utils = Utils()

    def _make_request(self, route: str, produce: Optional[int] = None) -> Responses:
        url, original_response = (
            self.utils.produce(total=produce, route=route)
            if produce
            else (
                self.http_request.get(route=route).get("url"),
                self.http_request.get(route=route),
            )
        )
        status_response = (
            [response.get("status_response") for response in original_response]
            if produce
            else original_response.get("status_response")
        )

        return Responses(
            url=url,
            status_response=status_response,
            original_response=original_response,
        )

    def yuri(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.YURI.value, produce=produce)

    def yaoi(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.YAOI.value, produce=produce)

    def kill(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.KILL.value, produce=produce)
