import asyncio
import aiohttp
from anvolt.models import errors
from typing import Union, Dict

e = errors


class TwitchClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer_token = None
        self.session = None

    async def set_session(self) -> None:
        loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10, connect=3), loop=loop
        )

    async def _get_bearer_token(self) -> str:
        await self.set_session()

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://id.twitch.tv/oauth2/token", data=data, headers=headers
            ) as response:
                response_json = await response.json()
                return response_json["access_token"]

    async def retrieve_user(self, username: str) -> str:
        await self.set_session()

        if not self.bearer_token:
            self.bearer_token = await self._get_bearer_token()

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.bearer_token}",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.twitch.tv/helix/users?login={username}", headers=headers
            ) as response:
                response_json = await response.json()
                return response_json["data"][0]

    async def retrieve_stream(self, user: Union[str, int]) -> Dict:
        await self.set_session()

        if not self.bearer_token:
            self.bearer_token = await self._get_bearer_token()

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.bearer_token}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.twitch.tv/helix/streams?user_id={user}",
                headers=headers,
            ) as response:
                response_json = await response.json()
                if response_json["data"]:
                    return response_json["data"][0]
                else:
                    raise e.UserOffline("User is not currently live.")

    async def is_live(self, user: Union[str, int]) -> bool:
        await self.set_session()

        if not self.bearer_token:
            self.bearer_token = await self._get_bearer_token()

        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.bearer_token}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.twitch.tv/helix/streams?user_id={user}",
                headers=headers,
            ) as response:
                response_json = await response.json()
                return response_json["data"] != []
