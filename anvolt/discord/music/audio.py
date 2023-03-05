from anvolt.models import MusicPlatform, errors
from typing import Dict, List, Union
from pytube import YouTube, Playlist
import aiohttp
import re
import youtube_dl
import asyncio

e = errors
YoutubeUri = [
    MusicPlatform.YOUTUBE_QUERY,
    MusicPlatform.YOUTUBE_URL,
    MusicPlatform.YOUTUBE_PLAYLIST,
    MusicPlatform.YOUTUBE_LIVESTREAM,
]
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-loglevel panic -hide_banner -nostats -nostdin -vn -b:a 192k -ac 2",
}
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


class AudioStreamFetcher:
    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop = loop
        self.session = None

    def _check_url(self, query: str) -> MusicPlatform:
        youtube_extractor = youtube_dl.extractor.get_info_extractor("Youtube")
        re_compile = re.compile(
            r"(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)"
        )
        soundcloud_pattern = re.compile("^https://soundcloud.com/")

        if "liveStreamability" in YouTube(query).vid_info.get("playabilityStatus"):
            return MusicPlatform.YOUTUBE_LIVESTREAM

        if re_compile.match(query):
            return MusicPlatform.YOUTUBE_PLAYLIST

        if re.match(soundcloud_pattern, query):
            return MusicPlatform.SOUNDCLOUD

        return MusicPlatform.YOUTUBE_QUERY

    async def set_session(self) -> None:
        loop = asyncio.get_event_loop() or self.loop

        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10, connect=3), loop=loop
        )

    async def _retreive_soundcloud_url(self, query: str, client_id: str) -> Dict:
        await self.set_session()

        async with self.session.get(
            f"https://api-widget.soundcloud.com/resolve?url={query}&format=json&client_id={client_id}",
        ) as response:
            await self.session.close()
            return await response.json()

    async def _retreive_youtube_search(self, query: str) -> List[str]:
        await self.set_session()

        async with self.session.get(
            f"https://www.youtube.com/results?search_query={query}",
        ) as response:
            video_ids = re.findall("watch\?v=(\S{11})", await response.text())
            await self.session.close()
            return video_ids

    async def _retreive_youtube_playlist(self, playlist_url: str) -> List[YouTube]:
        playlist = Playlist(playlist_url)
        videos = [video for video in playlist.videos]
        return videos

    async def _extract_soundcloud_info(
        self, query: str, client_id: str
    ) -> Union[List, Dict]:
        url = await self._retreive_soundcloud_url(query, client_id)

        if "tracks" in url:
            urls = [items for items in url.get("tracks")]
            return url, urls

        await self.set_session()

        async with self.session.get(
            f"{url.get('media')['transcodings'][0]['url']}?client_id={client_id}"
        ) as response:
            await self.session.close()
            return await response.json(), url

    async def _extract_youtube_info(self, query: str) -> Union[List, YouTube, Dict]:
        check_type = self._check_url(query)

        if not query.startswith("https"):
            search = await self._retreive_youtube_search(query=query)
            query = "https://www.youtube.com/watch?v={}".format(search[0])

        if check_type == MusicPlatform.YOUTUBE_PLAYLIST:
            return await self._retreive_youtube_playlist(query)

        if check_type == MusicPlatform.YOUTUBE_LIVESTREAM:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                return ydl.extract_info(query, download=False)

        return YouTube(query)

    async def retrieve_audio(
        self, source: MusicPlatform = None, query: str = None, **kwargs
    ) -> Union[List, Dict]:
        task = None

        if source in YoutubeUri:
            task = asyncio.ensure_future(self._extract_youtube_info(query))

        if source == MusicPlatform.SOUNDCLOUD:
            task = asyncio.ensure_future(
                self._extract_soundcloud_info(query, client_id=kwargs.get("client_id"))
            )

        await asyncio.wait([task])
        return task.result()
