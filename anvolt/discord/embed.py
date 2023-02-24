from anvolt.models import MusicPropertiesEnums, MusicProperty
from datetime import datetime
from typing import List, Union
from math import ceil
import discord

DEFAULT_BUTTONS = ["⏪", "◀️", "▶️", "⏩"]
TITLE = "top"
FOOTER = "footer"


class PageEmbed:
    def __init__(
        self,
        messages: List[MusicProperty],
        buttons: List[str] = DEFAULT_BUTTONS,
        fields: int = 10,
        timeout: int = 60,
    ):
        self.messages = messages
        self.buttons = buttons
        self.fields = fields
        self.timeout = timeout

    def generate_embed(
        self,
        page_on: Union[TITLE, FOOTER] = FOOTER,
        value_fields: str = None,
        assets_format: List[MusicPropertiesEnums] = None,
        **kwargs,
    ):
        num_embeds = ceil(len(self.messages) / self.fields)
        enum_names = [asset.name.lower() for asset in assets_format]
        embeds = []

        title = kwargs.get("title", "")
        description = kwargs.get("description", "")
        footer = kwargs.get("footer", "")
        color = kwargs.get("color", discord.Color.from_rgb(170, 255, 0))
        timestamp = kwargs.get("timestamp", datetime.utcnow())

        for num in range(num_embeds):
            embed = discord.Embed(
                title=f"Page {num+1}/{num_embeds} {title}"
                if page_on == TITLE
                else title,
                description=description,
                color=color,
                timestamp=timestamp,
            )
            embed.set_footer(
                text=f"Page {num+1}/{num_embeds}" if page_on == FOOTER else footer
            )

            fields = self._get_fields(num)
            for field in fields:
                values = [
                    getattr(field["value"], enum_name) for enum_name in enum_names
                ]
                embed.add_field(
                    name=str(field["index"] + 1),
                    value=value_fields.format(*values),
                    inline=False,
                )

            embeds.append(embed)

        return embeds

    def _get_fields(self, num):
        start = num * self.fields
        end = start + self.fields
        fields = [
            {"index": index, "value": value}
            for index, value in enumerate(self.messages[start:end], start)
        ]
        return fields
