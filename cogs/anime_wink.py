import requests
import json
import nextcord
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption


class AnimeWink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="anime-piscada",
        description='Piscada fofa (ou não) em anime!'
    )
    async def animepiscada(self, interaction: nextcord.Interaction):
        a = requests.get("https://some-random-api.ml/animu/wink")
        anime_r = a.json()
        anime_embed = nextcord.Embed()
        anime_embed.set_image(url=anime_r['link'])
        await interaction.response.send_message(embed=anime_embed)


def setup(bot: commands.Bot):
    bot.add_cog(AnimeWink(bot))
