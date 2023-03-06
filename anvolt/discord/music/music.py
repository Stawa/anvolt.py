from __future__ import annotations
from anvolt.discord.music.audio import AudioStreamFetcher, YoutubeUri, FFMPEG_OPTIONS
from anvolt.models import MusicProperty, MusicEnums, MusicPlatform, QueueSession, errors
from anvolt.discord import Event
from discord.ext import commands
from typing import List, Tuple, Union, Optional, Callable, Dict
from pytube import YouTube
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

        self.num = 1
        self.queue: Dict[QueueSession] = {}
        self.history: Dict[QueueSession] = {}
        self.currently_playing: Dict[List[MusicProperty]] = {}
        self.combined_queue: Dict[List[MusicProperty]] = {}

        self._check_opus()

    def _check_opus(self) -> None:
        if not discord.opus.is_loaded():
            discord.opus._load_default()

    async def cleanup(self, ctx: commands.Context):
        while True:
            await asyncio.sleep(10)

            if ctx.guild.id in self.queue:
                self.currently_playing.pop(ctx.guild.id, None)
                self.queue.pop(ctx.guild.id, None)

            if ctx.guild.id in self.combined_queue:
                self.combined_queue.pop(ctx.guild.id, None)

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
                    await self.call_event(
                        event_type="on_inactivity_timeout",
                        ctx=ctx,
                        error=e.InactivityTimeout(
                            "The bot has been automatically disconnected by inactivity_timeout"
                        ),
                    )

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

    async def _create_player(
        self,
        sound_info: Union[Dict, YouTube],
        audio: Dict,
        requester: discord.Member,
        volume: Union[int, float],
        loop: MusicEnums,
    ) -> MusicProperty:
        if isinstance(audio, Dict):
            audio_url = audio.get("url")
            video_id = sound_info.get("id")
            video_url = sound_info.get("permalink_url")
            video_title = sound_info.get("title")
            video_duration = round(sound_info.get("duration") / 1000)
            video_thumbnails = sound_info.get("artwork_url")
            is_live = False

        if isinstance(sound_info, Dict) and not audio:
            audio_url = sound_info.get("url")
            video_id = sound_info.get("id")
            video_url = f"https://www.youtube.com/watch?v={sound_info.get('id')}"
            video_title = sound_info.get("title")
            video_duration = "LIVE"
            video_thumbnails = sound_info.get("thumbnails")
            is_live = sound_info.get("is_live")

        if isinstance(sound_info, YouTube):
            is_live = sound_info.streams.last().is_live
            audio_url = sound_info.streams.last().url
            video_id = sound_info.video_id
            video_url = sound_info.watch_url
            video_title = sound_info.title
            video_duration = "LIVE" if is_live else sound_info.length
            video_thumbnails = (
                sound_info.vid_info.get("videoDetails", {})
                .get("thumbnail", {})
                .get("thumbnails")
            )

        return MusicProperty(
            audio_url=audio_url,
            video_id=video_id,
            video_url=video_url,
            title=video_title,
            duration=video_duration,
            thumbnails=video_thumbnails,
            is_live=is_live,
            requester=requester,
            start_time=time.time(),
            loop=loop,
            volume=volume,
        )

    async def _fetch_audio(self, query: str) -> Union[Dict, Tuple]:
        platform = self._check_url(query)

        if platform in YoutubeUri:
            sound_info = await self.retrieve_audio(
                platform, query, client_id=self.client_id
            )
            return None, sound_info

        if platform == MusicPlatform.SOUNDCLOUD:
            audio, sound_info = await self.retrieve_audio(
                platform, query, client_id=self.client_id
            )

            return audio, sound_info

    async def _play_next(self, ctx: commands.Context) -> None:
        queue = self.queue.get(ctx.guild.id)
        current_playing = self.currently_playing.get(ctx.guild.id)

        loop_map = {
            MusicEnums.NO_LOOPS: MusicEnums.NO_LOOPS,
            MusicEnums.LOOPS: MusicEnums.LOOPS,
            MusicEnums.QUEUE_LOOPS: MusicEnums.QUEUE_LOOPS,
        }
        loop = loop_map.get(current_playing.loop, MusicEnums.NO_LOOPS)

        if not queue or not queue.queue:
            if loop == MusicEnums.NO_LOOPS:
                self.currently_playing.pop(ctx.guild.id, None)
                self.queue.pop(ctx.guild.id, None)

                await self.call_event(event_type="on_music_end", ctx=ctx)
                return

        if current_playing.loop == MusicEnums.QUEUE_LOOPS:
            if ctx.guild.id not in self.combined_queue:
                self.combined_queue[ctx.guild.id] = [current_playing] + queue.queue

            player = self.combined_queue[ctx.guild.id][self.num]
            player.loop = MusicEnums.QUEUE_LOOPS
            self.num = (self.num + 1) % len(self.combined_queue[ctx.guild.id])

        else:
            next_song = queue.queue.pop(0)
            player = current_playing if loop == MusicEnums.LOOPS else next_song
            player.loop = (
                MusicEnums.LOOPS if loop == MusicEnums.LOOPS else MusicEnums.NO_LOOPS
            )

        self.task_loop(self.bot.loop, self.play_audio(ctx, player=player))

    def ensure_connection() -> Callable:
        def decorator(func: Callable):
            async def wrapper(self, ctx, *args, **kwargs):
                if await self._check_connection(ctx):
                    return await func(self, ctx, *args, **kwargs)

            return wrapper

        return decorator

    async def add_queue(self, ctx: commands.Context, player: MusicProperty) -> None:
        self.queue.setdefault(ctx.guild.id, QueueSession()).queue.append(player)

    async def remove_queue(self, ctx: commands.Context, num: int) -> None:
        if self.queue.get(ctx.guild.id):
            self.queue[ctx.guild.id].queue.pop(num)

    async def add_history(self, ctx: commands.Context, player: MusicProperty) -> None:
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
        if not ctx.voice_client:
            await self.call_event(
                event_type="on_music_error",
                ctx=ctx,
                error=e.PlayerEmpty("No song is currently being played."),
            )
            return

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

        if currently_playing.duration == "LIVE":
            current_duration = "LIVE"

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
        self.bot.loop.create_task(self._check_inactivity(ctx)).add_done_callback(
            self.handle_coroutine_exception
        )
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

    async def play_audio(self, ctx: commands.Context, player: MusicProperty):
        voice = ctx.voice_client

        if ctx.voice_client.is_playing():
            return

        source = discord.FFmpegPCMAudio(player.audio_url, options=FFMPEG_OPTIONS)
        voice.play(
            source,
            after=lambda e: self.task_loop(self.bot.loop, self._play_next(ctx)),
        )
        voice.source = discord.PCMVolumeTransformer(
            original=source, volume=player.volume / 100
        )
        self.currently_playing[ctx.guild.id] = player

        if player.loop != MusicEnums.LOOPS or MusicEnums.QUEUE_LOOPS:
            await self.add_history(ctx, player)

        await self.call_event(event_type="on_music_start", ctx=ctx, player=player)

    async def create_player(
        self,
        ctx: commands.Context,
        query: Union[str, MusicProperty],
        volume: int,
        loop: MusicEnums,
        sound_info: List,
    ) -> List[MusicProperty]:
        player = query if isinstance(query, MusicProperty) else None
        saved_players = []
        task = None

        for sound in sound_info:
            if isinstance(sound, Dict):
                audio, sound = await self._fetch_audio(
                    sound.get("permalink_url") if audio else sound
                )
                player = await self._create_player(
                    sound, audio, ctx.author, volume, loop
                )

            task = asyncio.ensure_future(
                self._create_player(sound, None, ctx.author, volume, loop)
            )
            await asyncio.wait([task])
            player = task.result()
            saved_players.append(player)

            if ctx.guild.id in self.currently_playing:
                await self.add_queue(ctx=ctx, player=player)

            await self.play_audio(ctx, player)

        return saved_players

    @ensure_connection()
    async def play(
        self, ctx: commands.Context, query: Union[str, MusicProperty], **kwargs
    ) -> Optional[MusicProperty]:
        volume = kwargs.get("volume", self.default_volume)
        loop = kwargs.get("loop", MusicEnums.NO_LOOPS)

        if isinstance(query, MusicProperty):
            player = query
        else:
            audio, sound_info = await self._fetch_audio(query)

        if isinstance(sound_info, List):
            return await self.create_player(ctx, query, volume, loop, sound_info)

        player = await self._create_player(sound_info, audio, ctx.author, volume, loop)

        if ctx.guild.id in self.currently_playing:
            self.task_loop(self.bot.loop, self.add_queue(ctx=ctx, player=player))
            return player

        await self.play_audio(ctx, player)
        self.task_loop(self.bot.loop, self.cleanup(ctx))
