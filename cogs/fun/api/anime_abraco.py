from discord.ext import commands
from discord import app_commands
import requests
import discord
import json

class AnimeAbraco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "anime-abraço",
        description = 'Abraço em anime!'
    )
    async def animeabraco(self, interaction: discord.Interaction):
        a = requests.get("https://some-random-api.ml/animu/hug")
        anime_r = a.json()
        anime_embed = discord.Embed()
        anime_embed.set_image(url=anime_r['link'])
        await interaction.response.send_message(embed=anime_embed)
       
    
async def setup(bot: commands.Bot):
    await bot.add_cog(AnimeAbraco(bot))
    
    