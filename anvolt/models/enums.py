from enum import Enum, IntEnum


class Route(Enum):
    """
    Enum that contains all accessible endpoints from the API category.
    """

    # Sfw Category
    BITE = "sfw/bite"
    HEADPAT = "sfw/headpat"
    HIGHFIVE = "sfw/highfive"
    HUG = "sfw/hug"
    POKE = "sfw/poke"
    RUN = "sfw/run"
    SLAP = "sfw/slap"
    SMILE = "sfw/smile"

    # Nsfw Category
    YURI = "nsfw/yuri"
    YAOI = "nsfw/yaoi"
    KILL = "nsfw/kill"

    # Games Category
    ANIGAMES_TRUTH = "anigames/truth"
    ANIGAMES_DARE = "anigames/dare"
    ANIGAMES_WAIFU = "anigames/waifu"
    ANIGAMES_HUSBANDO = "anigames/husbando"
    ANIGAMES_SHIPPER = "anigames/shipper"
    GAMES_TRUTH = "games/truth"
    GAMES_DARE = "games/dare"

    # AniGames Argument Option
    ANIGAMES_OPTION_WAIFU = "waifu"
    ANIGAMES_OPTION_HUSBANDO = "husbando"


class TwitchModels(Enum):
    """Enum class representing the different fields for Twitch user and stream data"""

    # Users
    USER_ID = "id"
    USERNAME = "login"
    DISPLAY_NAME = "display_name"
    DESCRIPTION = "description"
    PROFILE_IMAGE_URL = "profile_image_url"
    OFFLINE_IMAGE_URL = "offline_image_url"
    VIEW_COUNT = "view_count"
    CREATED_AT = "created_at"

    # Stream
    STREAM_ID = "id"
    STREAM_USER_ID = "user_id"
    STREAM_USERNAME = "user_login"
    STREAM_USER_NAME = "user_name"
    STREAM_GAME_ID = "game_id"
    STREAM_GAME_NAME = "game_name"
    STREAM_TYPE = "type"
    STREAM_TITLE = "title"
    STREAM_VIEWER_COUNT = "viewer_count"
    STREAM_STARTED_AT = "started_at"
    STREAM_LANGUAGE = "language"
    STREAM_THUMBNAIL_URL = "thumbnail_url"
    STREAM_TAG_IDS = "tag_ids"
    STREAM_TAGS = "tags"
    STREAM_IS_MATURE = "is_mature"


class MusicPropertiesEnums(Enum):
    AUDIO_URL = 0
    VIDEO_ID = 1
    VIDEO_URL = 2
    TITLE = 3
    DURATION = 4
    CURRENT_DURATION = 5
    THUMBNAILS = 6
    IS_LIVE = 7
    REQUESTER = 8
    VOLUME = 9
    START_TIME = 10
    LOOP = 11


class MusicEnums(IntEnum):
    """An enumeration class defining various music player settings, including loop options."""

    NO_LOOPS = 0
    LOOPS = 1
    QUEUE_LOOPS = 2


class MusicPlatform(IntEnum):
    """An enumeration class defining the available platforms supported by anvolt.py"""

    YOUTUBE_URL = 0
    YOUTUBE_QUERY = 1
    YOUTUBE_PLAYLIST = 2
    YOUTUBE_LIVESTREAM = 3
    SOUNDCLOUD = 4
