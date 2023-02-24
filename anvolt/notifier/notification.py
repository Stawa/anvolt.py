from anvolt.notifier import TwitchClient
from anvolt.models import TwitchModels, errors as e
from anvolt.discord import Event
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from discord.ext import commands
from typing import Union, List, Optional
import discord
import discord_webhook


class NotifierClient(Event):
    def __init__(
        self, client_id: str, client_secret: str, webhook_url: Optional[str] = None
    ):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.webhook_url = webhook_url
        self.client = TwitchClient(self.client_id, self.client_secret)

    async def start_event(self, bot: commands.Bot = None, user: Union[str, int] = None):
        await bot.wait_until_ready()

        retrieve_user = await self.client.retrieve_user(user)

        if isinstance(user, str):
            user = retrieve_user["id"]

        try:
            stream_items = await self.client.retrieve_stream(user=user)
        except e.UserOffline:
            await self.call_event(
                event_type="on_notification_offline", user=retrieve_user
            )
            return

        await self.call_event(
            event_type="on_notification_online", user=retrieve_user, stream=stream_items
        )

    async def send_webhook(
        self,
        user: Union[str, int] = None,
        webhook_message: Union[DiscordEmbed, str] = None,
        assets_format: List[TwitchModels] = None,
    ) -> None:
        webhook = AsyncDiscordWebhook(url=self.webhook_url)
        retrieve_user = await self.client.retrieve_user(user)

        if isinstance(user, str):
            user = retrieve_user["id"]

        items = await self.client.retrieve_stream(user=user)
        assets_format_values = [asset.value for asset in assets_format]
        assets = [
            items.get(asset) if asset in items else retrieve_user.get(asset)
            for asset in assets_format_values
        ]

        if await self.client.is_live(user=user):
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

    async def send_channel(
        self,
        ctx: commands.Context,
        channel: int = None,
        user: Union[str, int] = None,
        message: Union[discord.Embed, str] = None,
        assets_format: List[TwitchModels] = None,
    ) -> discord.Message:
        channel = ctx.guild.get_channel(channel)

        if not channel:
            await self.call_event(
                event_type="on_notification_error",
                ctx=ctx,
                error=e.InvalidChannel(
                    "Invalid channel ID. Please enter a valid channel ID."
                ),
            )

        retrieve_user = await self.client.retrieve_user(user)

        if isinstance(user, str):
            user = retrieve_user["id"]

        items = await self.client.retrieve_stream(user=user)
        assets_format_values = [asset.value for asset in assets_format]
        assets = [
            items.get(asset) if asset in items else retrieve_user.get(asset)
            for asset in assets_format_values
        ]

        if isinstance(message, discord.Embed):
            thumbnail_size = {"width": 1280, "height": 720}
            thumbnail_url = items[TwitchModels.STREAM_THUMBNAIL_URL.value].format(
                **thumbnail_size
            )

            message.title = message.title.format(
                retrieve_user[TwitchModels.USERNAME.value]
            )
            message.description = message.description.format(*assets)
            message.set_thumbnail(
                url=retrieve_user[TwitchModels.PROFILE_IMAGE_URL.value]
            )
            message.set_image(url=thumbnail_url)
        elif isinstance(message, str):
            message = message.format(*assets)

        if channel:
            if await self.client.is_live(user=user):
                if isinstance(message, discord.Embed):
                    return await channel.send(embed=message)
                return await channel.send(message)
