from typing import Union, List, Dict
from anvolt.models.errors import InvalidResponse


class Responses(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.status_response = kwargs.get("status_response")
        self.original_response = kwargs.get("original_response")

        if isinstance(self.original_response, dict):
            if self.original_response and self.original_response.get("error"):
                raise InvalidResponse(
                    f"Error reason: {self.original_response.get('error')}"
                )

        if isinstance(self.original_response, list):
            for response in self.original_response:
                if response and response.get("error"):
                    raise InvalidResponse(f"Error reason: {response.get('error')}")

    @property
    def url(self) -> Union[str, List[str]]:
        return self._url

    @url.setter
    def url(self, value) -> None:
        self._url = value

    @property
    def status_response(self) -> Union[List[int], int]:
        return self._status_response

    @status_response.setter
    def status_response(self, value) -> None:
        self._status_response = value

    @property
    def original_response(self) -> Union[List[Dict], Dict]:
        return self._original_response

    @original_response.setter
    def original_response(self, value) -> None:
        self._original_response = value
