import nextcord
import datetime
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(
        name = "ping",
        description = 'Mostra o ms da conexão do bot'
    )
    async def perfil(self, interaction: nextcord.Interaction):
        ping_embed = nextcord.Embed(title='Ping!', description='Descobre a latência atual.',
                               colour=nextcord.Colour.random(), timestamp=datetime.datetime.now())
        ping_embed.add_field(name='Conectado ao Discord',
                         value=f'Latência: {round(self.bot.latency * 1000)}ms.', inline=False)
        await interaction.response.send_message(embed=ping_embed)
       
    
def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
    
    