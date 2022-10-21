#Importa os modulos:
import nextcord, os, json, datetime, random, time, logging, sys
from nextcord.ext import commands, tasks
from itertools import cycle
from pathlib import Path
from Misc.messages import DeletarMensagem
from time import sleep

#importa os Miscs:
from Misc.utilidades import Wer



#Setando as Intents / Permissões do bot
intents = nextcord.Intents.all() #Não recomendo colocar todas as intents, prefira o parametro default()
intents.members = True #Permite que o bot veja os membros do servidor
intents.message_content = True #Permite que o bot veja o conteúdo das mensagens






#Carregando prefixo do bot:
async def pega_prefixo(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(Wer.prefixo)(bot, message)
    
    try:
        dados = await WerBot.config.find(message.guild.id)
        
        if not dados or "prefixo" not in dados:
            return commands.when_mentioned_or(Wer.prefixo)(bot, message)
        return commands.when_mentioned_or(dados["prefixo"])(bot, message)
    except:
        return commands.when_mentioned_or(Wer.prefixo)(bot, message)
    
    
    
    
    
    
#Bot instânciado:
WerBot = commands.AutoShardedBot(command_prefix=pega_prefixo, intents=intents)






#Deixando a atividade do bot em loop
activity = cycle(['a bunda lá no chão', 'Merda nos pombos!',
               'Não sei matemática básica', 'Wer me solta por favor'])

@tasks.loop(seconds=10) #Esta função troca automaticamente o status do bot, recomendo botar um valor min de 10s.
async def status_swap():
    await WerBot.change_presence(activity=nextcord.Game(next(activity)))
    
    
    
    
    
    
WerBot.bot_version = Wer.bot_versão #Pega a versão do bot na tupla 




diretorio = Path(__file__).parents[0] #Pega o diretório atual do arquivo main.py (Não mexa nisso)
diretorio = str(diretorio)


def slowprint(text, time): #Uma função para printar o texto lentamente.
	for c in text:
		sys.stdout.write(c)
		sys.stdout.flush()
		sleep(time/10)


#Todos os eventos do bot:
@WerBot.event
async def on_ready():
    
    slowprint('\n-=-=-=-=-=-=-=-=🎉Bot iniciado!🎉-=-=-=-=-=-=-=-=\n', 1)
    
    slowprint(f'✨ Entrou como: {WerBot.user.name}#{WerBot.user.discriminator}\n💾User ID :{WerBot.user.id}\n', 0.1)
    
    slowprint(f'⚓ Meu prefixo atual é: {Wer.prefixo}\n', 0.1)
    
    
    
   
    slowprint(f"📄 O diretório atual é: {diretorio}\n=================================================================================================\n", 0.1)

 
    
    #Carrega os cogs:
    for cog in WerBot.cogs:
        slowprint(f'📦 A cog: {cog} foi carregada com sucesso! ✔\n', 0.1)
    
    
    
    #MongoDB:
    #WerBot.db = DataB.db
    #WerBot.config = Doc(WerBot.db, "config")
   #for document in await WerBot.config.get_all():
   #     slowprint(f'ID: {document["_id"]} | Prefixo: {document["prefixo"]}\n',0.1)
        
    #slowprint('\n-=-=-=-=-=🍃 MongoDB conectado com sucesso! ✔-=-=-=-=-=\n', 1)
    
    
    
    #Chama a função de troca de status do bot
    status_swap.start()





#TroubleShooting:
@WerBot.event
async def on_command_error(ctx, error):
    ver = DeletarMensagem(ctx)
    
    embederror = nextcord.Embed(
        title="💢 Erro no comando.", description="Ocorreu um erro, tente novamente mais tarde 🤫", color=0xff4500)
    
    embederror.set_author(
        name="WerBot"
        )
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embederror.add_field(name="Argumento faltando", value=f" **Tipo:** {type(error)}\n\n```Você esqueceu de colocar um argumento no comando, tente novamente.```", inline=False)
    else:
        embederror.add_field(name="Erro abaixo:", value=f" **Tipo:** {type(error)}\n\n```{error}```", inline=False)
        
    embederror.add_field(name="__**O que fazer?**__"
                         ,value=f"```Não se preocupe, o Wer já recebeu uma mensagem sobre o erro e logo logo ele vai resolver... Se ele não tiver preguiça.\n\nAs vezes ele já até resolveu e tá lá no github do bot. **[clique aqui](https://github.com/WerG0D/WerBot---A-nextcord-bot)```"
                         ,inline=False)
    
    
    await ctx.send(embed=embederror, view=ver)




@WerBot.event
async def on_application_command_error(interaction, error):
    
    embederror = nextcord.Embed(
        title='💢 Erro no comando.'
        ,description="Ocorreu um erro, tente novamente mais tarde 🤫"
        ,color=0xff4500
    )
    
    embederror.set_author(
        name='WerBot'
        ,icon_url=interaction.user.display_avatar
    )
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        embederror.add_field(
            name='Argumento faltando'
            ,value=f' **Tipo:** {type(error)}\n\n```Você esqueceu de colocar um argumento no comando, tente novamente.```'
            ,inline=False
        )
        
    else:
        embederror.add_field(
            name='Erro abaixo:'
            ,value=f' **Tipo:** {type(error)}\n\n```{error}```'
            ,inline=False
        )
        
        embederror.add_field(
            name="__**O que fazer?**__"
            ,value=f"```Não se preocupe, o Wer já recebeu uma mensagem sobre o erro e logo logo ele vai resolver... Se ele não tiver preguiça.\n\nAs vezes ele já até resolveu e tá lá no github do bot. **[clique aqui](https://github.com/WerG0D/WerBot---A-nextcord-bot)```"
            ,inline=False
        )
        
        embederror.set_footer(text=f"Versão do bot: {WerBot.bot_version}"
                          ,value=f'comando pedido por: {interaction.author.name}#{interaction.author.discriminator}'
                          ,icon_url=interaction.author.avatar_url
                        )
        await interaction.response.send_message(embed=embederror, ephemeral=True)
        

if __name__ == '__main__':
    
    for file in os.listdir(diretorio + "/cogs"):
        if file.endswith(".py"):
            try:
                WerBot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"Erro ao carregar a cog: {file[:-3]}")
                print(f"Erro: {e}")
            
WerBot.run(Wer.token)