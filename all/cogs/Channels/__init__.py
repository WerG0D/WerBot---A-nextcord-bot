import random

import nextcord
from nextcord.ext import commands


class Channels(commands.Cog, description='Faz umas paradas com os canais'):

    COG_EMOJI = "📺"
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="statuscanais",
        aliases=["sc"],
        description="Mostra o status dos canais",
    )
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        channel = ctx.channel

        embed = nextcord.Embed(
            title=f"Status para **{channel.name}**",
            description=f"{'Categoria: {}'.format(channel.category.name) if channel.category else 'Esse canal não tem categoria'}",
            color=random.choice(self.bot.color_list),
        )
        embed.add_field(name="Canal do server:", value=ctx.guild.name, inline=False)
        embed.add_field(name="ID do canal", value=channel.id, inline=False)
        embed.add_field(
            name="Tópico do canal",
            value=f"{channel.topic if channel.topic else 'sem tópico.'}",
            inline=False,
        )
        embed.add_field(name="Posição do canal", value=channel.position, inline=False)
        embed.add_field(
            name="Tempo do slowmode", value=channel.slowmode_delay, inline=False
        )
        embed.add_field(name="O canal tem putaria doentia +18? (NSFW)", value=channel.is_nsfw(), inline=False)
        embed.add_field(name="O canal tem coisas fofas? (SFW)", value=channel.is_news(), inline=False)
        embed.add_field(
            name="Tempo de criação do canal", value=channel.created_at, inline=False
        )
        embed.add_field(
            name="Permissões do canal",
            value=channel.permissions_synced,
            inline=False,
        )
        embed.add_field(name="Hash do canal", value=hash(channel), inline=False)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, name="novo", description="Cria novas categorias e canais.",)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send("Comando inválido, use `categoria` ou `canal`")

    @new.command(
        name="categoria",
        description="Criar uma nova categoria",
        usage="<role> <Nome>",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: nextcord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            role: nextcord.PermissionOverwrite(read_messages=True),
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Qual foi menó fiz a categoria: {category.name} pra você")

    @new.command(
        name="canaç",
        description="Criar um novo canal",
        usage="<role> <nome>",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: nextcord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            role: nextcord.PermissionOverwrite(read_messages=True),
        }
        channel = await ctx.guild.create_text_channel(
            name=name,
            overwrites=overwrites,
            category=self.bot.get_channel(707945693582590005),
        )
        await ctx.send(f"Qual foi menó fiz o canal:{channel.name} pra você!")
        await channel.send(f"Qual foi menó fiz o canal:{channel.name} pra você!")

    @commands.group(invoke_without_command=True, name="delete", aliases=["d"], description="Deleta um canal ou categoria")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def delete(self, ctx):
        await ctx.send("Comando inválido, use `categoria` ou `canal`")

    @delete.command(
        name="categoria", description="Deleta uma categoria", usage="<categoia> [motivo]"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _category(self, ctx, category: nextcord.CategoryChannel, *, reason=None):
        await category.delete(reason=reason)
        await ctx.send(f"Qual foi menó eu deletei a categoria: {category.name} pra você!")

    @delete.command(
        name="canal", description="Deleta um canal", usage="<canal> [motivo]"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _channel(self, ctx, channel: nextcord.TextChannel = None, *, reason=None):
        channel = channel or ctx.channel
        await channel.delete(reason=reason)
        await ctx.send(f"Opa eu deletei o canal: {channel.name} pra você!")

    @commands.command(
        name="lockdown",
        description="Dar Lock ou unlock em um canal!",
        usage="[canal]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: nextcord.TextChannel = None):
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            # This is the same as the elif except it handles agaisnt empty overwrites dicts
            overwrites = {
                ctx.guild.default_role: nextcord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"OLHA O COVID, botei o canal: {channel.name} em lockdown. Tá fechado!")
        elif (
            channel.overwrites[ctx.guild.default_role].send_messages == True
            or channel.overwrites[ctx.guild.default_role].send_messages == None
        ):
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"OLHA O COVID, botei o canal: {channel.name} em lockdown. Tá fechado!")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"Chegou a vacina, o canal: {channel.name} não tá mais em lockdown, tá livre leve e solto.")


