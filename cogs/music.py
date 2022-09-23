import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import wavelink
from wavelink.ext import spotify
import datetime

#Novamente, uma cog feita pelo Glowstik. Eu troquei algumas funcionalidades, e talvez alguma coisa ou outra não funcione propriamente, mas está funcional na presente data. (15/09/2022)

class ControlPanel(nextcord.ui.View):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx
    
    @nextcord.ui.button(label="Despausar/Pausar", style=nextcord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("Primeiro inicie o comando antes de usar os botões.", ephemeral=True)
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused():
            await self.vc.resume()
            await interaction.message.edit(content="Despausado", view=self)
        else:
            await self.vc.pause()
            await interaction.message.edit(content="Pausado", view=self)

    @nextcord.ui.button(label="Queue", style=nextcord.ButtonStyle.blurple)
    async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("Primeiro inicie o comando antes de usar os botões.", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("A fila está vazia!", ephemeral=True)
    
        em = nextcord.Embed(title="Queue")
        queue = self.vc.queue.copy()
        songCount = 0

        for song in queue:
            songCount += 1
            em.add_field(name=f"Musica °{str(songCount)}", value=f"`{song}`")
        await interaction.message.edit(embed=em, view=self)
    
    @nextcord.ui.button(label="Pular", style=nextcord.ButtonStyle.blurple)
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("Primeiro inicie o comando antes de usar os botões.", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("A fila está vazia!", ephemeral=True)

        try:
            next_song = self.vc.queue.get()
            await self.vc.play(next_song)
            await interaction.message.edit(content=f"Agora tocando: `{next_song}`", view=self)
        except Exception:
            return await interaction.response.send_message("A fila tá vazia chefe.", ephemeral=True)
    
    @nextcord.ui.button(label="Disconnect", style=nextcord.ButtonStyle.red)
    async def disconnect(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("Primeiro inicie o comando antes de usar os botões.", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        await interaction.message.edit(content="Disconnect :P", view=self)

class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self): #Troque os dados da Node, estou deixando um gratuito aqui mas pode ser que esteja fora do ar quando vc acessar. O token do spotify é exemplificativo e deve ser trocado também.
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='lavalink.oops.wtf', port=443, password="www.freelavalink.ga", https=True, spotify_client=spotify.SpotifyClient(client_id="7c9fb485e5fe4940bb7ac5dd065f1b2f", client_secret="678e907d32d140c3940f6838a19f853e"))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node <{node.identifier}> está pronta!')
        print("Brook está no convés e pronto para tocar!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
        try:
            ctx = player.ctx
            vc: player = ctx.voice_client
            
        except nextcord.HTTPException:
            interaction = player.interaction
            vc: player = interaction.guild.voice_client
        
        if vc.loop:
            return await vc.play(track)
        
        if vc.queue.is_empty:
            return await vc.disconnect()

        next_song = vc.queue.get()
        await vc.play(next_song)
        try:
            await ctx.send(f"Agora tocando: {next_song.title}")
        except nextcord.HTTPException:
            await interaction.send(f"Agora tocando: {next_song.title}")

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await ctx.send(f'Tocando `{search.title}`')          
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f'Adicionei `{search.title}` a lista')
        vc.ctx = ctx
        try:
            if vc.loop: return
        except Exception:
            setattr(vc, "loop", False)
        
    @commands.command()
    async def panel(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("toque musica primeiro")
        
        em = nextcord.Embed(title="Painel de Musica", description="controle o bot com os botões abaixo:")
        view = ControlPanel(vc, ctx)
        await ctx.send(embed=em, view=view)
        
    @nextcord.slash_command(description="Toca uma música")
    async def play(interaction: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description="Canal de voz para entrar"), search: str = SlashOption(description="Nome da música")):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if not interaction.guild.voice_client:
            vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        elif not getattr(interaction.author.voice, "channel", None):
            return await interaction.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = interaction.guild.voice_client
        
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            await interaction.send(f'Tocando `{search.title}`')          
        else:
            await vc.queue.put_wait(search)
            await interaction.send(f'Adicionei `{search.title}` a lista')
        vc.interaction = interaction
        try:
            if vc.loop: return
        except Exception:
            setattr(vc, "loop", False)
        
    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("toque musica primeiro")

        await vc.pause()
        await ctx.send("pausei a musica.")
        
    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        if vc.is_playing():
            return await ctx.send("A musica já está tocando")

        await vc.resume()
        await ctx.send("A música voltou a tocar!")
        
    @commands.command()
    async def skip(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("toque musica primeiro")
        
        try:
            next_song = vc.queue.get()
            await vc.play(next_song)
            await ctx.send(content=f"Agora tocando: `{next_song}`")
        except Exception:
            return await ctx.send("A fila tá vazia chefe.")
        
        await vc.stop()
        await ctx.send("parei a musica.")
        
    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.disconnect()
        await ctx.send("Te vejo depois :D")
        
    @commands.command()
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("toque musica primeiro;")
        try: 
            vc.loop ^= True
        except:
            setattr(vc, "loop", False)
        if vc.loop:
            return await ctx.send("Loop iniciado.")
        else:
            return await ctx.send("Loop desativado.")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou em um canal de voz.")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty:
            return await ctx.send("A fila está vazia!")
        
        em = nextcord.Embed(title="Queue")
        
        queue = vc.queue.copy()
        songCount = 0
        for song in queue:
            songCount += 1
            em.add_field(name=f"Musica °{str(songCount)}", value=f"`{song}`")
            
        await ctx.send(embed=em)

    @commands.command()
    async def volume(self, ctx: commands.Context, volume: int):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("toque musica primeiro")
        
        if volume > 100:
            return await ctx.send('Este volume é alto demais.')
        elif volume < 0:
            return await ctx.send("Este volume é baixo demais.")
        await ctx.send(f"Volume agora está em:`{volume}%`")
        return await vc.set_volume(volume)

    @commands.command()
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("Eu não estou no canal de voz :(")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing(): 
            return await ctx.send("Não tem nada tocando.")

        em = nextcord.Embed(title=f"Agora tocando: {vc.track.title}", description=f"Artista: {vc.track.author}")
        em.add_field(name="Duração", value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        em.add_field(name="Informação extra", value=f" URL da musica: [Clique aqui]({str(vc.track.uri)})")
        return await ctx.send(embed=em)

    @commands.command()
    async def splay(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Entre em um canal de voz primeiro")
        else:
            vc: wavelink.Player = ctx.voice_client
            
        if vc.queue.is_empty and not vc.is_playing():
            try:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                await vc.play(track)
                await ctx.send(f'Tocando `{track.title}`')
            except Exception as e:
                await ctx.send("Por favor, use apenas links do Spotify")
                return print(e)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f'Adicionei `{search.title}` a lista')
        vc.ctx = ctx
        try:
            if vc.loop: return
        except Exception:
            setattr(vc, "loop", False)    
        
def setup(bot):
    bot.add_cog(Music(bot))
    