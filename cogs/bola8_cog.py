import nextcord
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption
import random
import datetime
import asyncio


class Bola8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="bola8",
        description='Feedback aleatório'
    )
    async def bola8(self, interaction: Interaction, pergunta: str):
        respostas = ['Acredito que sim.', 'Hoje não, talvez amanhã?', 'Tente de novo daqui a pouco.', 'Não crie expectativas.', 'Crie expectativas.', 'Minhas fontes dizem que sim.', 'Minhas fontes dizem que não.', 'Isso é duvidoso.', 'Não tenho duvidas.', 'Sim.', 'Não.',
                     'É mais provável o Wer tomar banho.', 'Tão certo quanto o Wer não tomar banho.']

        bola8_embed = nextcord.Embed(title='**Bola 8 mágica!**', description='Um feedback supostamente aleatório. Supostamente.',
                                     colour=nextcord.Colour.random(), timestamp=datetime.datetime.now())
        bola8_embed.add_field(
            name='Dando feedback', value=f"**Pergunta: ** {pergunta}\n**Resposta: **  {random.choice(respostas)}", inline=False)
        await interaction.response.send_message(embed=bola8_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Bola8(bot))
