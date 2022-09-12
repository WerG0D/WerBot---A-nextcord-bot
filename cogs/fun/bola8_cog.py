from discord.ext import commands
from discord import app_commands
import discord
import random
import datetime

class Bola8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "bola8",
        description = 'Feedback aleatório'
    )
    async def bola8(self, interaction: discord.Interaction, pergunta: str):
        respostas = ['Acredito que sim.', 'Hoje não, talvez amanhã?', 'Tente de novo daqui a pouco.', 'Não crie expectativas.', 'Crie expectativas.', 'Minhas fontes dizem que sim.', 'Minhas fontes dizem que não.', 'Isso é duvidoso.', 'Não tenho duvidas.', 'Sim.', 'Não.',
                 'É mais provável o Wer tomar banho.', 'Tão certo quanto o Wer não tomar banho.']

        bola8_embed = discord.Embed(title='**Bola 8 mágica!**', description='Um feedback supostamente aleatório. Supostamente.',
                                colour=discord.Colour.random(), timestamp=datetime.datetime.now())
        bola8_embed.add_field(
        name='Dando feedback', value=f"**Pergunta: ** {pergunta}\n**Resposta: **  {random.choice(respostas)}", inline=False)
        await interaction.response.send_message(embed=bola8_embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Bola8(bot))
    
    