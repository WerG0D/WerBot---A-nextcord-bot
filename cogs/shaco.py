from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption
import requests
import json
import nextcord

class Shaco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(
        name = "shaco",
        description = 'Do fundo do lodo de Summners Rift, o pior piadista... (em ingles)'
    )
    async def joke(self, interaction: nextcord.Interaction):
        j = requests.get("https://some-random-api.ml/joke")
        joke_r = j.json()
        joke_embed = nextcord.Embed(title='Quer ouvir uma piada?',
                               description=joke_r['joke'], colour=nextcord.Colour.random())  # Usa cor random
        await interaction.response.send_message(embed=joke_embed)
       
    
def setup(bot: commands.Bot):
    bot.add_cog(Shaco(bot))
    
    