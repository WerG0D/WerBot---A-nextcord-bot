from discord.ext import commands
from discord import app_commands
import datetime
import discord

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "ping",
        description = 'Mostra o ms da conexão do bot'
    )
    async def perfil(self, interaction: discord.Interaction):
        ping_embed = discord.Embed(title='Ping!', description='Descobre a latência atual.',
                               colour=discord.Colour.random(), timestamp=datetime.datetime.now())
        ping_embed.add_field(name='Conectado ao Discord',
                         value=f'Latência: {round(self.bot.latency * 1000)}ms.', inline=False)
        await interaction.response.send_message(embed=ping_embed)
       
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    
    