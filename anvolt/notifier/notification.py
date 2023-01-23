from anvolt.notifier import TwitchClient
from anvolt.models import TwitchModels
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from typing import Union, List
import discord_webhook


class NotifierClient:
    def __init__(self, client_id: str, client_secret: str, webhook_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.webhook_url = webhook_url

    async def send_webhook(
        self,
        user: Union[str, int] = None,
        webhook_message: Union[DiscordEmbed, str] = None,
        assets_format: List[TwitchModels] = None,
    ) -> None:
        client = TwitchClient(self.client_id, self.client_secret)
        webhook = AsyncDiscordWebhook(url=self.webhook_url)
        retrieve_user = await client.retrieve_user(user)

        if isinstance(user, str):
            user = retrieve_user["id"]

        items = await client.retrieve_stream(user=user)
        assets_format_values = [asset.value for asset in assets_format]
        assets = [
            items.get(asset) if asset in items else retrieve_user.get(asset)
            for asset in assets_format_values
        ]

        if await client.is_live(user=user):
            if isinstance(webhook_message, discord_webhook.webhook.DiscordEmbed):
                thumbnail_size = {"width": 1280, "height": 720}
                thumbnail_url = items[TwitchModels.STREAM_THUMBNAIL_URL.value].format(
                    **thumbnail_size
                )

                if assets:
                    webhook_message.set_title(
                        webhook_message.title.format(
                            retrieve_user[TwitchModels.USERNAME.value]
                        )
                    )
                    webhook_message.set_description(
                        webhook_message.description.format(*assets)
                    )
                    webhook_message.set_thumbnail(
                        url=retrieve_user[TwitchModels.PROFILE_IMAGE_URL.value]
                    )

                webhook_message.set_image(url=thumbnail_url)
                webhook.add_embed(webhook_message)
            elif isinstance(webhook_message, str):
                if assets:
                    webhook_message = webhook_message.format(*assets)
                webhook.content = webhook_message

            await webhook.execute()
