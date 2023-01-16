from typing import Union, List
from anvolt.errors import InvalidResponse


class Responses(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.code_response = kwargs.get("code_response")
        self.original_response = kwargs.get("original_response")

        if self.original_response and self.original_response.get("error"):
            raise InvalidResponse(
                f"Error reason: {self.original_response.get('error')}"
            )

    @property
    def url(self) -> Union[str, List[str]]:
        return self._url

    @url.setter
    def url(self, value) -> None:
        self._url = value

    @property
    def code_response(self) -> int:
        return self._code_response

    @code_response.setter
    def code_response(self, value) -> None:
        self._code_response = value

    @property
    def original_response(self) -> dict:
        return self._original_response

    @original_response.setter
    def original_response(self, value) -> None:
        self._original_response = value
