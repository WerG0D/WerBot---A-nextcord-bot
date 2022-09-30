import nextcord
from nextcord.ext import commands

class CogSetup(commands.Cog, name="Comando pro adm ver as cogs", description="Carrega, descarrega e recarrega as cogs."):
     def __init__(self, bot):
        self.bot = bot
     
     COG_EMOJI = "⚙️"

    
    # Load Command
     @commands.command(name="load", description="Carrega a cog.", usage="<nome>")
     async def load(self, ctx, extensions):
        self.bot.load_extension(f"cogs.{extensions}") 
        await ctx.send("Cog carregadas.")

    # Unload Comamnd
     @commands.command(name="unload", description="Descarrega cogs.", usage="<nome>")
     async def unload(self, ctx, extensions):
        self.bot.unload_extension(f"cogs.{extensions}")
        await ctx.send("Cog descarregada")

    # Reload Command
     @commands.command(name="recarregar", description="Recarrega cogs.", usage="<nome>")
     async def reload(self, ctx, extensions):
        self.bot.reload_extension(f"cogs.{extensions}")
        await ctx.send("Cog recarregada.")

    
