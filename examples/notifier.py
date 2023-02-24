from discord_webhook import DiscordEmbed
from anvolt.models import TwitchModels
from anvolt.notifier import NotifierClient
import asyncio

NotifierClient = NotifierClient(
    client_id="", client_secret="", webhook_url="WEBHOOK_URL"
)


async def embed():
    embed = DiscordEmbed(
        title="{} went live!",
        description="Attention all gamers! **{}** has just gone live on Twitch. Watch them play the latest games, win big, and have a blast! Join in on the fun now!",
        color="0FFF50",
    )
    embed.set_timestamp()
    await NotifierClient.send_webhook(
        user="StawaMan",
        webhook_message=embed,
        assets_format=[TwitchModels.USERNAME],
    )


asyncio.run(embed())


async def text():
    await NotifierClient.send_webhook(
        user="StawaMan",
        webhook_message="Attention all gamers! **{}** has just gone live on Twitch. Watch them play the latest games, win big, and have a blast! Join in on the fun now!",
        assets_format=[TwitchModels.USERNAME],
    )


asyncio.run(text())

# Discord Bot
import discord
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} Is ready.")
    await NotifierClient.start_event(bot=bot, user="stawaman")


@NotifierClient.event
async def on_notification_error(error):
    print(error)


@NotifierClient.event
async def on_notification_online(user, stream):
    print(user, stream)


@NotifierClient.event
async def on_notification_offline(user):
    print(user)


@bot.command()
async def send(ctx: commands.Context):
    embed = discord.Embed(
        title="{} is livestram now!",
        description="Hey everyone! **{}** is livestreaming about **{}**, his title stream was **{}**",
    )
    await NotifierClient.send_channel(
        ctx,
        channel=123,
        user="StawaMan",
        message=embed,
        assets_format=[
            TwitchModels.USERNAME,
            TwitchModels.STREAM_GAME_NAME,
            TwitchModels.STREAM_TITLE,
        ],
    )


bot.run("BOT_TOKEN")
