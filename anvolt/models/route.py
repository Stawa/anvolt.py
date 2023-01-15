from enum import Enum


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
