import os, dotenv, datetime, time, platform, nextcord, quickchart, psutil
from humanfriendly import format_timespan

from nextcord.ext import commands, menus

from Misc.bancodedados.vote import VoteManage
from Misc.extras import convert_size
from Misc.utilidades import Emojis, Tokens, Wer
from Misc.messages import DeletarMensagem
from Misc.utilidades import Wer

dotenv.load_dotenv()


class VoteButtonMenu(menus.ButtonMenu):
    def __init__(self, bot):
        super().__init__(disable_buttons_after=True)
        self.voteManage = VoteManage(bot)
        self.__id = Tokens.secret_id

    def makechart(self, likes, dislikes):
        qc = quickchart.QuickChart()
        qc.width = 640
        qc.height = 480
        qc.background_color = "#0D0C1D"
        qc.config = {
            "type": "outlabeledPie",
            "data": {
                "labels": ["Likes", "Dislikes"],
                "datasets": [{
                    "backgroundColor": ["#00FF00", "#FF0000"],
                    "data": [likes, dislikes],
                    "borderColor":'#00000000'
                }]
            },
            "options": {

                "title": {
                    "text": 'Vote Results',
                    "display": True,
                    "fontColor": 'white',
                    "fontSize": 20,
                    "fontFamily": 'lato'
                },
                "legend": {
                    "position": 'right',
                    "labels" : {
                        "fontColor" : "white"
                    }
                },
                'plugins': {
                    "outlabels": {
                        "text": "%l %p",
                        "color": "white",
                        "stretch": 30,
                        "font": {
                           "minSize": 15,
                        }
                    }
                },
            }
        }

        url = qc.get_url()
        return url

    async def send_initial_message(self, ctx, channel):

        embed = nextcord.Embed(title="O que você achou do bot?", color=0x00FF00,
                               url="https://github.com/WerG0D/WerBot---A-nextcord-bot", description="Ele é open source, então você pode ver o código dele e até mesmo contribuir com ele!")
        embed.set_author(name="WerG0D ",
                         icon_url=self.bot.user.display_avatar)
        embed.add_field(
            name="Sobre mim", value=f"Eu sou {self.bot.user}, que está comendo a bunda da sua mã-", inline=True)
        embed.add_field(name="Meu prefixo é ",
                        value=f"My prefix is `;`", inline=False)

        data = await self.voteManage.get_data(self.__id)

        likes = data["Likes"]
        dislikes = data["Dislikes"]

        url = self.makechart(likes, dislikes)

        embed.set_image(url='https://avatars.githubusercontent.com/u/51096748?v=4')

        embed.add_field(
            name="Para ajuda", value="Chega mais [https://github.com/WerG0D/WerBot---A-nextcord-bot](https://github.com/WerG0D/WerBot---A-nextcord-bot)", inline=True)
        embed.set_footer(text="Por WerG0D#5376")

        data = self.voteManage.get_data(self.__id) 

        if not data:
            dict = {
                "_id": self.__id,
                "Likes" : 0,
                "Dislikes" : 0
            }
            await self.voteManage.create_vote(dict)

        return await channel.send(f'Opa eae meu mano {ctx.author.mention}', view=self, embed=embed)

    @nextcord.ui.button(emoji="\N{THUMBS UP SIGN}")
    async def on_thumbs_up(self, button, interaction: nextcord.Interaction):
        status = await self.voteManage.check_user_vote_status(interaction.user.id)
        if not status:
            dictionary = {
                "_id": interaction.user.id,
                "voted": True
            }

            await self.voteManage.add_user_data(dictionary)
            await self.voteManage.add_like(self.__id)

            embed = nextcord.Embed(title="Oque você achou do bot?",
                                   url="https://github.com/WerG0D/WerBot---A-nextcord-bot", description="O bot é open source, então você pode ver o código dele e até mesmo contribuir com ele!")
            embed.set_author(name="WerG0D",
                             icon_url=self.bot.user.display_avatar)
            embed.add_field(name="Sobre mim" ,value=f"Eu sou {self.bot.user}, que está comendo a bunda da sua mã-" ,inline=True)
                
            embed.add_field(name="Meu prefixo",
                            value="Meu prefixo is `;`", inline=False)
            embed.add_field(name="Vota aí ",
                            value="Valeu agora me mama 👍", inline=False)
            embed.add_field(
                name="Help", value="Chega ae [https://github.com/WerG0D/WerBot---A-nextcord-bot](https://github.com/WerG0D/WerBot---A-nextcord-bot)", inline=True)
            embed.set_footer(text="By WerG0D#5376")

            await self.message.edit(content=f"Valeu, {interaction.user.mention} agora da uma sugada", embed=embed)

        else:
           button.disabled = True
           self.remove_item(self.on_thumbs_down)
           button.label = "Já votou mlk."
           await interaction.response.edit_message(view=self)

    @nextcord.ui.button(emoji="\N{THUMBS DOWN SIGN}")
    async def on_thumbs_down(self, button, interaction):
        status = await self.voteManage.check_user_vote_status(interaction.user.id)
        if not status:
            dictionary = {
                "_id": interaction.user.id,
                "voted": True
            }

            await self.voteManage.add_user_data(dictionary)
            await self.voteManage.add_dislike(self.__id)

            embed = nextcord.Embed(title="WerBot ",
                                   url="https://github.com/WerG0D/WerBot---A-nextcord-bot", description="O bot é open source, então você pode ver o código dele e até mesmo contribuir com ele!")
            embed.set_author(name="WerG0D#5376",
                             icon_url=self.bot.user.display_avatar)
            embed.add_field(
                name="Sobre mim", value=f"eu sou {self.bot.user} que está comendo sua mã-", inline=True)
            embed.add_field(name="Meu prefixo ",
                            value="Meu prefixo é `;`", inline=False)
            embed.add_field(name="Vota aí ",
                            value="VSFD MANO VC DEU DESLIKE EU SEI QUE SOU MAL FEITO MAS... ;-;", inline=False)
            embed.add_field(
                name="Help", value="Chega ae [https://github.com/WerG0D/WerBot---A-nextcord-bot](https://github.com/WerG0D/WerBot---A-nextcord-bot)", inline=True)
            embed.set_footer(text="By WerBot#5376")
            await self.message.edit(content=f"O MONGO {interaction.user.mention} ME DEU DESLIKE DESGRAÇA", embed=embed)

        else:
           button.disabled = True
           self.remove_item(self.on_thumbs_up)
           button.label = "Já votou mlk."
           await interaction.response.edit_message(view=self)

    @nextcord.ui.button(emoji=Emojis.trashcan)
    async def on_stop(self, button, interaction):
        await self.message.delete()



class About(commands.Cog, name="Informações do bot", description="Vem me conhecer"):

    COG_EMOJI = "👷"

    def __init__(self, bot):
        self.bot = bot


        
    @commands.command(name="vote", description="Vota em mim pff")    
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def vote_bot(self, ctx):
        await VoteButtonMenu(self.bot).start(ctx)

    @commands.command(name="Sobre", description="Mostra umas informações minhas", aliases=["botstats", "stats"])
    async def about(self, ctx):
        """
        Mostra umas informações minhas
        """
        view = DeletarMensagem(ctx)
        pythonVersion = platform.python_version()
        npyVersion = nextcord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        shard_id = ctx.guild.shard_id
        shard = self.bot.get_shard(shard_id)
        shard_ping = shard.latency
        shard_servers = len(
            [guild for guild in self.bot.guilds if guild.shard_id == shard_id])

        
        embed = nextcord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF',
                               colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Versão do bot', value=self.bot.bot_version, inline=False)
        embed.add_field(name='Versão do Python:', value=pythonVersion, inline=False)
        embed.add_field(name='Versão do nextcord:', value=npyVersion, inline=False)
        embed.add_field(name='Total de servers:', value=serverCount, inline=False)
        embed.add_field(name='Total de usuários:', value=memberCount, inline=False)
        embed.add_field(name='Shard ID:', value=shard_id, inline=False)
        embed.add_field(name='Shard Ping:', value=shard_ping, inline=False)
        embed.add_field(name='Shard Servers:', value=shard_servers, inline=False)
        embed.add_field(name="CPU CORE's:", value=os.cpu_count(), inline=False)
        embed.add_field(name="RAM:", value=convert_size.convert_size(psutil.virtual_memory().total), inline=False)
        embed.add_field(name="Uso de CPU:", value=f"{psutil.cpu_percent(interval=1)}%", inline=False)
        embed.add_field(name="Uso de RAM:", value=f"{psutil.virtual_memory().percent}%", inline=False)
        embed.add_field(name="\nUptime:", value=f"```elm\n{format_timespan(int(round(time.time()- self.bot.start_time)))}```\n", inline=False)
        embed.add_field(name='Bot Dev:', value=self.bot.owner_id, inline=False)
        embed.add_field(name='Código fonte:', value=f"[Clica aqui man]({Wer.github_bot_repo})", inline=False)

        embed.set_footer(
            text=f"{ctx.author.guild.name} | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)

        await ctx.send(embed=embed, view=view)


class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(
        name = "perfil",
        description = 'Mostra o perfil do usuário no servidor!'
    )
    async def perfil(self, interaction: nextcord.Interaction, membro: nextcord.Member = None):
        if membro == None:
            membro = interaction.user
        nome = membro.display_name  # Pega o nome do membro
        
        fp = membro.display_avatar  # Pega a foto de perfil
        
        criacao = membro.created_at  # Pega quando a conta foi criada
   
        tempo = membro.joined_at.strftime("%b %d, %Y, %T")  # pega o tempo que o usuário está no server
        
        roles = membro.roles  # Mostra as roles do usuário
        
        flags = membro.public_flags  # Mostra as flags do usuário
        
        atividades = membro.activities  # Mostra o que o usuário está fazendo
        
        status_usuario = membro.status  # Pega o status do usuário
        
        usuario_id = membro.id  # Pega o ID do usuário
        
        permissoes = membro.guild_permissions  # Permissões do usuário
        
        # criação da embed
        prof = nextcord.Embed(title='Esté o meu perfil.'
                            ,description='Seja livre pra ver um pouco mais sobre minha história aqui:'
                            ,colour=nextcord.Colour.random())  # Usa cor random
        
        prof.set_thumbnail(url=f'{fp}')
        
        prof.set_author(name=f'{nome}')
        
        prof.add_field(name='Criei minha conta no discord em'
                    ,value=f"{criacao}", inline=False)
        
        prof.add_field(name='Eu estou aqui desde:', value=f'{tempo}', inline=False)
        
        prof.add_field(name='Estes são os meus cargos (roles):'
                      ,value=f'{roles}', inline=False)
        
        prof.add_field(name='Estas são minhas medalhas (flags):'
                       ,value=f'{flags}', inline=False)
        
        prof.add_field(name='Agora eu estou fazendo isso:'
                       ,value=f'{atividades}', inline=False)
        
        prof.add_field(name='Este é o meu status atual:'
                       ,value=f'{status_usuario}', inline=False)
        
        prof.add_field(name='Este é o meu ID de usuário:'
                       ,value=f'ID: {usuario_id}', inline=False)
        
        prof.add_field(name='Estas são as minhas permissões neste server:'
                       ,value=f'{permissoes}', inline=False)

        await interaction.response.send_message(embed=prof)