from discord.ext import commands
from discord import app_commands
import requests
import discord
import json

class Shaco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "shaco",
        description = 'Do fundo do lodo de Summners Rift, o pior piadista... (em ingles)'
    )
    async def joke(self, interaction: discord.Interaction):
        j = requests.get("https://some-random-api.ml/joke")
        joke_r = j.json()
        joke_embed = discord.Embed(title='Quer ouvir uma piada?',
                               description=joke_r['joke'], colour=discord.Colour.random())  # Usa cor random
        await interaction.response.send_message(embed=joke_embed)
       
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Shaco(bot))
    
    