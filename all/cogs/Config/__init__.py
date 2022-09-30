import random, asyncio, nextcord
from nextcord.ext import commands
from Misc.bancodedados.config import Blacklist_DB


class Configuration(commands.Cog, description="Configura o bot."):

    COG_EMOJI = "<:config:956526378008846437>"
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.blacklist_db = Blacklist_DB(self.bot)
             
    @commands.command(
        name="prefixo",
        aliases=["changeprefix", "setprefix"],
        description="Muda o prefixo da sua guilda!",
        usage="[prefixo]",
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.has_guild_permissions(manage_guild=True)    
    async def prefix(self, ctx, *, prefix=";"):
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefixo": prefix})
        await ctx.send(
            f"O prefixo da guilda agora é `{prefix}`"
        )

    @commands.command(
        name="deleteprefix", aliases=["dp"], description="Deleta o prefixo!"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        await self.bot.config.unset({"_id": ctx.guild.id, "prefixo": 1})
        await ctx.send("O prefixo foi deletado! Voltou a ser o default ';' ") 

    @commands.command(
        name="blacklist", description="Blacklista um usuário", usage="<usuário>"
    )
    @commands.is_owner()
    async def blacklist(self, ctx: commands.Context, user: nextcord.Member):
        if ctx.message.author.id == user.id:
            msg = await ctx.send("🚫 Você não pode se blacklistar!")
            await asyncio.sleep(5)
            await msg.delete()

        if await self.blacklist_db.check_user_blacklisted_status(user.id):
            embed = nextcord.Embed(title="🚫 O usuário já está blacklistado", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            
        else:
            await self.blacklist_db.create_user_table(ctx.message.guild.id, user)
            embed = nextcord.Embed(title=f"✅ Blacklistado com sucesso {user.name}.", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            

    @commands.command(
        name="unblacklist",
        description="Unblacklista um usuário",
        usage="<ususario>",
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, user: nextcord.Member):
    
        
        if ctx.message.author.id == user.id:
            msg = await ctx.send("🚫 Você não pode se desblacklistar!")
            await asyncio.sleep(5)
            await msg.delete()

        if not await self.blacklist_db.check_user_blacklisted_status(user.id):
            embed = nextcord.Embed(title="🚫 O usuário não está blacklistado", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            
        else:
            await self.blacklist_db.delete_user_table(user.id)
            embed = nextcord.Embed(title=f"✅ Unblacklistado com successo:  {user.name}.", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
    
    @commands.command(
        name="logout",
        aliases=["close", "stopbot"],
        description="Desliga o bot",
    )
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention}, Tô vazando, cachorras. :wave:")
        await self.bot.close()

