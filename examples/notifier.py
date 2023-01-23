from discord_webhook import DiscordEmbed
from anvolt.models import TwitchModels
from anvolt.notifier import NotifierClient
import asyncio

client = NotifierClient(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    webhook_url="WEBHOOK_URL",
)


async def embed():
    embed = DiscordEmbed(
        title="{} went live!",
        description="Attention all gamers! **{}** has just gone live on Twitch. Watch them play the latest games, win big, and have a blast! Join in on the fun now!",
        color="0FFF50",
    )
    embed.set_timestamp()
    await client.send_webhook(
        user="StawaMan",
        webhook_message=embed,
        assets_format=[TwitchModels.USERNAME],
    )


asyncio.run(embed())


async def text():
    await client.send_webhook(
        user="StawaMan",
        webhook_message="Attention all gamers! **{}** has just gone live on Twitch. Watch them play the latest games, win big, and have a blast! Join in on the fun now!",
        assets_format=[TwitchModels.USERNAME],
    )


asyncio.run(text())
