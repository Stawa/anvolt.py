from __future__ import annotations
import functools
from anvolt.discord.music.audio import AudioStreamFetcher, YoutubeUri, FFMPEG_OPTIONS
from anvolt.models import MusicProperty, MusicEnums, MusicPlatform, QueueSession, errors
from anvolt.discord import Event
from discord.ext import commands
from typing import List, Tuple, Union, Optional, Callable, Dict, Any
import asyncio
import discord
import time

VocalGuildChannel = Union[discord.VoiceChannel, discord.StageChannel]
e = errors


class AnVoltMusic(Event, AudioStreamFetcher):
    def __init__(self, bot: commands.Bot, **kwargs):
        super().__init__()
        self.bot = bot
        self.default_volume = kwargs.get("default_volume", 15)
        self.inactivity_timeout = kwargs.get("inactivity_timeout", 60)
        self.client_id = kwargs.get("client_id", None)

        self.num = 0
        self.queue: Dict[QueueSession] = {}
        self.history: Dict[QueueSession] = {}
        self.currently_playing: Dict[List[MusicProperty]] = {}
        self.combined_queue: Dict[List[MusicProperty]] = {}

        self._check_opus()

    def _check_opus(self) -> None:
        if not discord.opus.is_loaded():
            discord.opus._load_default()

    async def _check_inactivity(self, ctx: commands.Context):
        if not self.inactivity_timeout:
            return

        while True:
            await asyncio.sleep(10)

            if ctx.voice_client:
                members = list(
                    filter(lambda x: not x.bot, ctx.voice_client.channel.members)
                )

                if len(members) == 0:
                    await asyncio.sleep(self.inactivity_timeout)
                    await ctx.voice_client.disconnect(force=True)

    async def _check_connection(self, ctx: commands.Context) -> bool:
        if not ctx.voice_client:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.NotConnected("Client isn't connected to a voice channel."),
            )
            return False

        if not ctx.author.voice:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.NotConnected("User isn't connected to a voice channel."),
            )
            return False

        return True

    async def _play_next(self, ctx: commands.Context) -> None:
        queue = self.queue.get(ctx.guild.id)
        current_playing = self.currently_playing.get(ctx.guild.id)

        if not queue or not queue.queue:
            self.currently_playing.pop(ctx.guild.id, None)
            self.queue.pop(ctx.guild.id, None)

            await self.call_event(event_type="on_music_end", ctx=ctx)
            return

        if current_playing.loop == MusicEnums.QUEUE_LOOPS:
            if ctx.guild.id not in self.combined_queue:
                self.combined_queue[ctx.guild.id] = [current_playing] + queue.queue

            next_track = self.combined_queue[ctx.guild.id][self.num]
            self.task_loop(
                self.bot.loop,
                self.play(
                    ctx,
                    query=next_track,
                    volume=current_playing.volume or self.default_volume,
                    loop=MusicEnums.QUEUE_LOOPS,
                ),
            )

            self.num = (self.num + 1) % len(self.combined_queue[ctx.guild.id])
            return

        if current_playing.loop == MusicEnums.LOOPS:
            self.task_loop(
                self.bot.loop,
                self.play(
                    ctx,
                    query=current_playing,
                    volume=current_playing.volume or self.default_volume,
                    loop=MusicEnums.LOOPS,
                ),
            )
            return

        next_song = queue.queue.pop(0)
        self.task_loop(
            self.bot.loop,
            self.play(
                ctx,
                query=next_song,
                volume=current_playing.volume or self.default_volume,
                loop=MusicEnums.NO_LOOPS,
            ),
        )

    def ensure_connection() -> Callable:
        def decorator(func: Callable):
            async def wrapper(self, ctx, *args, **kwargs):
                if await self._check_connection(ctx):
                    return await func(self, ctx, *args, **kwargs)

            return wrapper

        return decorator

    def add_queue(self, ctx: commands.Context, player: MusicProperty) -> None:
        self.queue.setdefault(ctx.guild.id, QueueSession()).queue.append(player)

    def remove_queue(self, ctx: commands.Context, num: int) -> None:
        if self.queue.get(ctx.guild.id):
            self.queue[ctx.guild.id].queue.pop(num)

    def add_history(self, ctx: commands.Context, player: MusicProperty) -> None:
        self.history.setdefault(ctx.guild.id, QueueSession()).history.append(player)

    def parse_duration(self, duration: Union[str, float]) -> str:
        if duration == "LIVE":
            return "LIVE"

        duration = time.strftime("%H:%M:%S", time.gmtime(duration))
        return duration[3:] if duration.startswith("00") else duration

    async def get_queue(self, ctx: commands.Context) -> Optional[MusicProperty]:
        currently_playing = self.currently_playing.get(ctx.guild.id)

        if currently_playing.loop == MusicEnums.QUEUE_LOOPS:
            if ctx.guild.id in self.combined_queue:
                return self.combined_queue[ctx.guild.id][self.num :]
            return self.queue[ctx.guild.id].queue[self.num :]

        if self.queue.get(ctx.guild.id):
            return self.queue[ctx.guild.id].queue

    async def get_history(self, ctx: commands.Context) -> Optional[MusicProperty]:
        if self.history.get(ctx.guild.id):
            return self.history[ctx.guild.id].history

    async def now_playing(
        self, ctx: commands.Context, parse_duration: bool = True
    ) -> Optional[MusicProperty]:
        currently_playing = self.currently_playing.get(ctx.guild.id)

        if not currently_playing:
            return None

        start_time = currently_playing.start_time

        if ctx.voice_client.is_paused():
            start_time = (
                currently_playing.start_time + time.time() - currently_playing.last_time
            )

        current_duration = time.time() - start_time

        if parse_duration:
            current_duration = self.parse_duration(duration=current_duration)

        currently_playing.current_duration = current_duration
        return currently_playing

    async def join(
        self, ctx: commands.Context, mute: bool = False, deafen: bool = False
    ) -> Optional[Tuple[VocalGuildChannel, discord.VoiceClient]]:
        if not ctx.author.voice:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.NotConnected("User isn't connected to a voice channel."),
            )
            return

        channel = ctx.author.voice.channel
        voice_client = await channel.connect(
            cls=discord.VoiceClient, self_mute=mute, self_deaf=deafen
        )
        self.bot.loop.create_task(self._check_inactivity(ctx))
        return channel, voice_client

    @ensure_connection()
    async def disconnect(self, ctx: commands.Context) -> Optional[VocalGuildChannel]:
        channel = ctx.voice_client.channel
        await ctx.voice_client.disconnect(force=True)
        return channel

    @ensure_connection()
    async def volume(self, ctx: commands.Context, volume: int = None) -> Optional[int]:
        currently_playing = self.currently_playing.get(ctx.guild.id)

        if not volume:
            return round(ctx.voice_client.source.volume * 100)

        if not (0 <= volume <= 100):
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.InvalidNumber("Invalid volume, it must be between 0 and 100."),
            )
            return

        if not currently_playing:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

        ctx.voice_client.source.volume = volume / 100
        currently_playing.volume = volume

        return round(ctx.voice_client.source.volume * 100)

    @ensure_connection()
    async def pause(self, ctx: commands.Context) -> Optional[bool]:
        if not ctx.voice_client.is_playing():
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

        if ctx.voice_client.is_paused():
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerAlreadyPaused("The music player is already paused."),
            )
            return

        ctx.voice_client.pause()
        now_playing = self.currently_playing.get(ctx.guild.id)
        now_playing.last_time = time.time()
        return True

    @ensure_connection()
    async def resume(self, ctx: commands.Context) -> Optional[bool]:
        if not ctx.voice_client.is_paused():
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerNotPaused("The music player isn't paused."),
            )
            return

        ctx.voice_client.resume()
        now_playing = self.currently_playing.get(ctx.guild.id)
        now_playing.current_duration += str(time.time() - now_playing.last_time)
        return True

    @ensure_connection()
    async def skip(self, ctx: commands.Context) -> Optional[bool]:
        if not ctx.voice_client.is_playing():
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

        if ctx.voice_client:
            ctx.voice_client.stop()

        return True

    @ensure_connection()
    async def loop(self, ctx: commands.Context):
        if not ctx.guild.id in self.currently_playing:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

        current_playing = self.currently_playing.get(ctx.guild.id)
        current_playing.loop = (
            MusicEnums.LOOPS
            if current_playing.loop != MusicEnums.LOOPS
            else MusicEnums.NO_LOOPS
        )

        return current_playing.loop

    @ensure_connection()
    async def queueloop(self, ctx: commands.Context):
        if not ctx.guild.id in self.currently_playing:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

        if not ctx.guild.id in self.queue:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.QueueEmpty(
                    "Unable to activate the queueloop because there are no items in the queue."
                ),
            )
            return

        current_playing = self.currently_playing.get(ctx.guild.id)
        current_playing.loop = (
            MusicEnums.QUEUE_LOOPS
            if current_playing.loop != MusicEnums.QUEUE_LOOPS
            else MusicEnums.NO_LOOPS
        )

        if current_playing.loop == MusicEnums.NO_LOOPS:
            self.combined_queue.pop(ctx.guild.id, None)

        return current_playing.loop

    @ensure_connection()
    async def play(
        self, ctx: commands.Context, query: Union[str, MusicProperty], **kwargs
    ) -> Optional[MusicProperty]:
        voice = ctx.voice_client
        volume = kwargs.get("volume", self.default_volume)
        loop = kwargs.get("loop", MusicEnums.NO_LOOPS)
        player = query if isinstance(query, MusicProperty) else None

        if not isinstance(query, MusicProperty):
            platform = self._check_url(query)

            if platform in YoutubeUri:
                sound_info = await self.retrieve_audio(
                    platform, query, client_id=self.client_id
                )

            if platform == MusicPlatform.SOUNDCLOUD:
                audio, sound_info = await self.retrieve_audio(
                    platform, query, client_id=self.client_id
                )

            if not sound_info:
                return None

            if isinstance(sound_info, list):
                for item in sound_info:
                    if platform in YoutubeUri:
                        sound_info = await self.retrieve_audio(
                            platform,
                            item,
                            client_id=self.client_id,
                        )

                    if platform == MusicPlatform.SOUNDCLOUD:
                        audio, sound_info = await self.retrieve_audio(
                            platform,
                            item.get("permalink_url"),
                            client_id=self.client_id,
                        )

                    player = MusicProperty(
                        audio_url=sound_info.get("url")
                        if platform in YoutubeUri
                        else audio.get("url"),
                        video_id=sound_info.get("id"),
                        video_url=sound_info.get("permalink_url")
                        if platform == MusicPlatform.SOUNDCLOUD
                        else f"https://www.youtube.com/watch?v={sound_info.get('id')}",
                        title=sound_info.get("title"),
                        duration=round(sound_info.get("duration") / 1000)
                        if platform == MusicPlatform.SOUNDCLOUD
                        else (
                            "LIVE"
                            if sound_info.get("is_live")
                            else sound_info.get("duration")
                        ),
                        thumbnails=sound_info.get(
                            "artwork_url"
                            if platform == MusicPlatform.SOUNDCLOUD
                            else "thumbnails"
                        ),
                        is_live=sound_info.get("is_live")
                        if platform in YoutubeUri
                        else False,
                        requester=ctx.author,
                    )

                    if voice.is_playing():
                        self.add_queue(ctx, player)

                    if not voice.is_playing():
                        await self.play(ctx, query=player)

                return

            player = MusicProperty(
                audio_url=sound_info.get("url")
                if platform in YoutubeUri
                else audio.get("url"),
                video_id=sound_info.get("id"),
                video_url=sound_info.get("permalink_url")
                if platform == MusicPlatform.SOUNDCLOUD
                else f"https://www.youtube.com/watch?v={sound_info.get('id')}",
                title=sound_info.get("title"),
                duration=round(sound_info.get("duration") / 1000)
                if platform == MusicPlatform.SOUNDCLOUD
                else (
                    "LIVE" if sound_info.get("is_live") else sound_info.get("duration")
                ),
                thumbnails=sound_info.get(
                    "artwork_url"
                    if platform == MusicPlatform.SOUNDCLOUD
                    else "thumbnails"
                ),
                is_live=sound_info.get("is_live") if platform in YoutubeUri else False,
                requester=ctx.author,
            )

        if voice.is_playing():
            self.add_queue(ctx=ctx, player=player)
            return player

        source = discord.FFmpegPCMAudio(player.audio_url, options=FFMPEG_OPTIONS)
        voice.play(
            source,
            after=lambda e: self.task_loop(self.bot.loop, self._play_next(ctx)),
        )
        voice.source = discord.PCMVolumeTransformer(
            original=source, volume=volume / 100
        )

        player.start_time = time.time()
        player.loop = loop
        player.volume = volume
        self.currently_playing[ctx.guild.id] = player

        if loop == MusicEnums.NO_LOOPS:
            self.add_history(ctx, player)

        await self.call_event(event_type="on_music_start", ctx=ctx, player=player)
