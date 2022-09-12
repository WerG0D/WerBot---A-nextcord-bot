from discord.ext import commands
from discord import app_commands
import discord

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "ban",
        description = 'Invoca o martelo do ban!'
    )
    @commands.has_permissions(ban_members=True)
    async def self(interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f'Usuário {member.mention} foi marretado até a morte e nunca mais irá voltar.')
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))
    
    