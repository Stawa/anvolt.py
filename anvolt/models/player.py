from typing import Union, Optional, List
import discord


class QueueSession(object):
    def __init__(self, **kwargs) -> None:
        self.queue: Optional[List[MusicProperty]] = kwargs.get("queue", [])
        self.history: Optional[List[MusicProperty]] = kwargs.get("history", [])
        self.combined_queue: Optional[List[MusicProperty]] = kwargs.get(
            "combined_queue", []
        )


class MusicProperty(object):
    def __init__(self, **kwargs):
        self.audio_url: str = kwargs.get("audio_url")
        self.video_id: str = kwargs.get("video_id")
        self.video_url: str = kwargs.get("video_url")
        self.title: str = kwargs.get("title")
        self.duration: int = kwargs.get("duration")
        self.current_duration: Union[int, float] = kwargs.get("current_duration")
        self.thumbnails: str = kwargs.get("thumbnails")
        self.is_live: bool = kwargs.get("is_live")
        self.requester: discord.Member = kwargs.get("requester")
        self.volume: int = kwargs.get("volume")
        self.start_time: float = kwargs.get("start_time")
        self.last_time: float = kwargs.get("last_time")
        self.loop: bool = kwargs.get("loop")
