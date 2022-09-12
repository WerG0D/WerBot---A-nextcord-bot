from discord.ext import commands
from discord import app_commands
import discord

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(
        name = "kick",
        description = 'mete o pé na bunda de alguém!'
    )
    @commands.has_permissions(kick_members=True)
    async def self(interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f'Usuário {member.mention} foi kickado temporariamente.')
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))
    
    