from typing import Dict
import os
import io
import re
import zlib
import aiohttp
import dotenv

import nextcord as discord
from nextcord.ext import commands

from Misc.extras import fuzzy
from Misc.messages import DeletarMensagem
from Misc.messages.buttons.docs import DocsView

from algoliasearch.search_client import SearchClient

dotenv.load_dotenv()


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode("utf-8")

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b""
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b"\n")
            while pos != -1:
                yield buf[:pos].decode("utf-8")
                buf = buf[pos + 1:]
                pos = buf.find(b"\n")


class Docs(commands.Cog, name="Document", description="Manda link para a documentação das consultas"):

    COG_EMOJI = "📃"

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.startup())
        # Fill out from trying a search on the ddevs portal
        app_id = os.getenv("ALGOLIA_SEARCH_APP_ID")
        api_key = os.getenv("ALGOLIA_SEARCH_API_KEY")
        self.search_client = SearchClient.create(app_id, api_key)
        self.index = self.search_client.init_index("discord")

    async def startup(self):
        self.bot.session = aiohttp.ClientSession()

    def get_level_str(self, levels):
        last = ""
        for level in levels.values():
            if level is not None:
                last = level
        return last

    def parse_object_inv(self, stream: SphinxObjectFileReader, url: str) -> Dict:
        result = {}
        inv_version = stream.readline().rstrip()

        if inv_version != "# Sphinx inventory version 2":
            raise RuntimeError("Invalid objects.inv file version.")

        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]  # not needed

        line = stream.readline()
        if "zlib" not in line:
            raise RuntimeError(
                "Invalid objects.inv file, not z-lib compatible.")

        entry_regex = re.compile(
            r"(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)")
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(":")
            if directive == "py:module" and name in result:
                continue

            if directive == "std:doc":
                subdirective = "label"

            if location.endswith("$"):
                location = location[:-1] + name

            key = name if dispname == "-" else dispname
            prefix = f"{subdirective}:" if domain == "std" else ""

            key = (
                key.replace("nextcord.", "")
                .replace("nextcord.ext.commands.", "")
                .replace("nextcord.ext.menus.", "")
                .replace("nextcord.ext.ipc.", "")
                .replace("discord.", "")
                .replace("discord.ext.commands.", "")
                .replace("disnake.", "")
                .replace("disnake.ext.commands.", "")
            )

            result[f"{prefix}{key}"] = os.path.join(url, location)

        return result

    async def build_docs_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with self.bot.session.get(page + "/objects.inv") as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        "Cannot build docs lookup table, try again later."
                    )

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self._docs_cache = cache

    async def do_docs(self, ctx: commands.Context, key, obj):
        page_types = {
            "master": "https://discordpy.readthedocs.io/en/latest/",
            "nextcord": "https://docs.nextcord.dev/en/latest/",
            "disnake": "https://docs.disnake.dev/en/latest/",
            "py-cord": "https://docs.pycord.dev/en/master/",
            "menus": "https://nextcord-ext-menus.readthedocs.io/en/latest",
            "ipc": "https://nextcord-ext-ipc.readthedocs.io/en/latest",
            "python": "https://docs.python.org/3",
        }

        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self, "_docs_cache"):
            await ctx.trigger_typing()
            await self.build_docs_lookup_table(page_types)

        obj = re.sub(
            r"^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)
        obj = re.sub(
            r"^(?:nextcord\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)
        obj = re.sub(
            r"^(?:disnake\.(?:ext\.)?)?(?:commands\.)?(.+)", r"\1", obj)

        if key.startswith("master"):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == "_":
                    continue
                if q == name:
                    obj = f"abc.Messageable.{name}"
                    break

        cache = list(self._docs_cache[key].items())

        def transform(tup):
            return tup[0]

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:8]

        embed = discord.Embed(colour=discord.Colour.blurple())
        if len(matches) == 0:
            return await ctx.send("Could not find anything. Sorry.", view=DeletarMensagem(ctx))

        embed.description = "\n".join(
            f"[`{key}`]({url})" for key, url in matches)
        ref = ctx.message.reference
        refer = None
        if ref and isinstance(ref.resolved, discord.Message):
            refer = ref.resolved.to_reference()

        objct = []

        for obj in matches[0]:
            objct.append(obj)

        await ctx.send(embed=embed, reference=refer, view=DocsView(ctx=ctx, key=objct[0], url=objct[1]))

    @commands.group(name='docs', aliases=["doc", "rtfm"], description="Encontra documentos para a API do discord para o Python", help="Pega documentação da API discord e python", invoke_without_command=True)
    async def docs_group(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "master", query)
    # <!-- NEXTCORD DOCUMENTATION -->

    @docs_group.command(name="nextcord", description="Documentação do nextcord<:nextcord:960775252873457724>")
    async def docs_nextcord(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "nextcord", query)

    # <!-- DISNAKE DOCUMENTATION -->
    @docs_group.command(name="disnake", description="Encontra a documentação do <:disnake:960776137296994314> disnake")
    async def docs_disnake(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "disnake", query)
    # <!-- PY-CORD DOCUMENTATION -->

    @docs_group.command(name="py-cord", description="Encontra a documentação do <:pycord:960776193701978122> py-cord")
    async def docs_pycord(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "py-cord", query)

    # <!-- NEXTCORD EXTENSION DOCUMENTATION -->

    @docs_group.command(name="ipc", description="Encontra a documentação do <:nextcord:960775252873457724> nextcord-ext-ipc")
    async def docs_nextcord_ipc(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "ipc", query)

    @docs_group.command(name="menus", description="Encontra a documentação do <:nextcord:960775252873457724> nextcord-ext-menus")
    async def docs_nextcord_menus(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "menus", query)

    # <!-- PYTHON DOCUMENTATION -->
    @docs_group.command(name="python", description="Encontra a documentação do <:python:935932879714779227> python")
    async def docs_python(self, ctx: commands.Context, *, query: str = None):
        await self.do_docs(ctx, "python", query)

    # <!-- DISCORD DOCUMENTATION -->
    @commands.command(name="ddocs", description="Pega a documentação oficial do <:discord:932504870701908068>discord.")
    async def discord_docs(self, ctx: commands.Context, *, query):
        result = await self.index.search_async(query)
        description = ""
        hits = []

        for hit in result["hits"]:
            title = self.get_level_str(hit["hierarchy"])

            if title in hits:
                continue

            hits.append(title)
            url = hit["url"].replace(
                "https://discord.com/developers/docs", "https://discord.dev"
            )

            description += f"[{title}]({url})\n"
            if len(hits) == 10:
                break

        embed = discord.Embed(
            title="Sua ajuda chegou!",
            description=description,
            color=discord.Color.random(),
        )
        await ctx.send(embed=embed, view=DeletarMensagem(ctx))

    # <!-- DOCUMENTATION CACHE DELETE -->
    @commands.command(description="Deleta o cache da documentação (Wer apenas)",
                      help="Deleta cache dos docs", aliases=["purge-docs", "deldocs"]
                      )
    @commands.is_owner()
    async def docscache(self, ctx: commands.Context):
        del self._docs_cache
        embed = discord.Embed(title="Caches deletados.",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed, view=DeletarMensagem(ctx))
