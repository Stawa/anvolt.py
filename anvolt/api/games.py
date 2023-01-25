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

    def _make_request(
        self, route: str, produce: Optional[int] = None, response: str = "url"
    ) -> Responses:
        if not produce:
            res = self.http_request.get(route=route)

        url, original_response = (
            self.utils.produce(total=produce, route=route, request_type=response)
            if produce
            else (
                res.get(response),
                res,
            )
        )
        status_response = (
            [response.get("status_response") for response in original_response]
            if produce
            else original_response.get("status_response")
        )

        return Responses(
            url=url,
            text=original_response.get("text", None),
            status_response=status_response,
            player=original_response.get("player", None),
            character_name=original_response.get("character_name", None),
            percentage=original_response.get("percentage", None),
            original_response=original_response,
        )

    def truth(
        self, produce: Optional[int] = None, theme: Optional[Route] = Route.GAMES_TRUTH
    ) -> Responses:
        return self._make_request(route=theme.value, produce=produce, response="text")

    def dare(
        self, produce: Optional[int] = None, theme: Optional[Route] = Route.GAMES_DARE
    ) -> Responses:
        return self._make_request(route=theme.value, produce=produce, response="text")

    def shipper(
        self, player: Optional[str] = None, option: Route = Route.ANIGAMES_OPTION_WAIFU
    ) -> Responses:
        return self._make_request(
            route=f"{Route.ANIGAMES_SHIPPER.value}/?player={player}&target={option.value}"
        )

    def waifu(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.ANIGAMES_WAIFU.value, produce=produce)

    def husbando(self, produce: Optional[int] = None) -> Responses:
        return self._make_request(route=Route.ANIGAMES_HUSBANDO.value, produce=produce)
