import nextcord
from nextcord.ext import commands
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption

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
        prof = nextcord.Embed(title='Esté o meu perfil.',
                            description='Seja livre pra ver um pouco mais sobre minha história aqui:', colour=nextcord.Colour.random())  # Usa cor random
        prof.set_thumbnail(url=f'{fp}')
        prof.set_author(name=f'{nome}')
        prof.add_field(name='Criei minha conta no discord em',
                    value=f"{criacao}", inline=False)
        prof.add_field(name='Eu estou aqui desde:', value=f'{tempo}', inline=False)
        prof.add_field(name='Estes são os meus cargos (roles):',
                   value=f'{roles}', inline=False)
        prof.add_field(name='Estas são minhas medalhas (flags):',
                   value=f'{flags}', inline=False)
        prof.add_field(name='Agora eu estou fazendo isso:',
                   value=f'{atividades}', inline=False)
        prof.add_field(name='Este é o meu status atual:',
                   value=f'{status_usuario}', inline=False)
        prof.add_field(name='Este é o meu ID de usuário:',
                   value=f'ID: {usuario_id}', inline=False)
        prof.add_field(name='Estas são as minhas permissões neste server:',
                   value=f'{permissoes}', inline=False)

        await interaction.response.send_message(embed=prof)
       
    
def setup(bot: commands.Bot):
    bot.add_cog(Perfil(bot))
    
    