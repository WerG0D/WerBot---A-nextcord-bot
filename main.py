import nextcord
from nextcord.ext import commands, tasks
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType
from config import TOKEN, PREFIX, OWNER
import os
import aiosqlite
from itertools import cycle


# Os intents (permissões) do bot, não recomendo deixar no all()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, case_insensitive=True, allowed_mentions=nextcord.AllowedMentions(
    users=True,
    everyone=False,
    roles=False,
    replied_user=True,
)
)

for fn in os.listdir("./cogs"):  # Carrega as cogs
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")


@bot.event
async def on_ready():
    print(f"Bot ID: {bot.user.id}\nNome do Bot: {bot.user.name}")
    setattr(bot, "db", await aiosqlite.connect("main.db"))
    status_swap.start()

# Trocador de atividade ---
frases = cycle(['a bunda lá no chão', 'Merda nos pombos!', 'League of Gays',
               'Não sei matemática básica', 'Wer me solta por favor'])  # Frases da atividade do bot, usando itertools pq preguiça de loopar isso, tnt faz perfomance. Sim eu sou péssimo.


# Usando o modulo de tasks do discord.py pra criar a função de swap da atividade. Coloque um valor maior ou igual a 10 segundos, para não travar o bot.
@tasks.loop(seconds=10)
async def status_swap():
    await bot.change_presence(activity=nextcord.Game(next(frases)))

# Trocador de atividade ---


# Comandos de contole de cogs. Só o dono pode usar, utilize para recarregar, carregar e descarregar as cogs.
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
    except commands.ExtensionAlreadyLoaded:
        return await ctx.send("a Cog já está carregada")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog não encontrada")
    await ctx.send("Cog carregada")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog não encontrada")
    await ctx.send("Cog recarregada")


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
    except commands.ExtensionNotFound:
        return await ctx.send("Cog não encontrada")
    await ctx.send("Cog descarregada")


@bot.command()
@commands.is_owner()
async def check(ctx, cog_name):
    try:
        bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog carregada")
    except commands.ExtensionNotFound:
        await ctx.send("Cog não carregada")
    else:
        await ctx.send("Cog descarregada")
        bot.unload_extension(f"cogs.{cog_name}")


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        em = nextcord.Embed(
            title="Comando apenas do  FODÃO WER.",
            description=f"Apenas o dono deste bot, `{OWNER}` pode usar este comando.",
        )
        await ctx.send(embed=em, delete_after=20)
        return
    else:
        em = nextcord.Embed(
            title="Um erro ocorreu :(", description=f"```{error}```")
        await ctx.send(embed=em, delete_after=30)
        return
    


bot.run(TOKEN)  # O token deve ser colado no arquivo config.py
