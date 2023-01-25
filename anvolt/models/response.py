from typing import Union, List, Dict
from anvolt.models.errors import InvalidResponse


class Responses(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.text = kwargs.get("text")
        self.status_response = kwargs.get("status_response")
        self.player = kwargs.get("player")
        self.character_name = kwargs.get("character_name")
        self.percentage = kwargs.get("percentage")
        self.original_response = kwargs.get("original_response")
        self._check_for_errors()

    def _check_for_errors(self):
        if isinstance(self.original_response, dict) and self.original_response.get(
            "error"
        ):
            raise InvalidResponse(
                f"Error reason: {self.original_response.get('error')}"
            )
        elif isinstance(self.original_response, list):
            errors = [
                response.get("error")
                for response in self.original_response
                if response.get("error")
            ]
            if errors:
                raise InvalidResponse(f"Error reason: {errors}")

    @property
    def url(self) -> Union[str, List[str]]:
        return self._url

    @url.setter
    def url(self, value) -> None:
        self._url = value

    @property
    def text(self) -> Union[str, List[str]]:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self._text = value

    @property
    def status_response(self) -> Union[List[int], int]:
        return self._status_response

    @status_response.setter
    def status_response(self, value) -> None:
        self._status_response = value

    @property
    def player(self) -> Union[str, None]:
        return self._player

    @player.setter
    def player(self, value) -> None:
        self._player = value

    @property
    def character_name(self) -> str:
        return self._character_name

    @character_name.setter
    def character_name(self, value) -> None:
        self._character_name = value

    @property
    def percentage(self) -> Union[str, None]:
        return self._percentage

    @percentage.setter
    def percentage(self, value) -> None:
        self._percentage = value

    @property
    def original_response(self) -> Union[List[Dict], Dict]:
        return self._original_response

    @original_response.setter
    def original_response(self, value) -> None:
        self._original_response = value
