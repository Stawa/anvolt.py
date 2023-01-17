from anvolt.request import HttpRequest
from anvolt import __version__
from packaging import version
import os


class Updater:
    def __init__(self):
        self.http_request = HttpRequest(
            custom_url="https://anvolt.vercel.app/api/version/"
        )
        self.latest_version = None

    def _fetch_latest_version(self):
        """Fetch the latest version of the package from the server."""
        payload = {"language": "python"}
        self.latest_version = self.http_request.post(json=payload)

    def _check_version(self) -> None:
        """Check if the installed version is the latest version"""
        self._fetch_latest_version()

        if version.parse(__version__) == version.parse(
            self.latest_version.get("latest_stable_version")
        ):
            return
        if version.parse(__version__) < version.parse(
            self.latest_version.get("latest_stable_version")
        ):
            os.system("pip install anvolt.py --upgrade")

    def check_for_updates(self) -> None:
        """Check if a new version is available and update if needed."""
        self._check_version()
