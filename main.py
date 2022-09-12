import discord
from discord.ext import commands, tasks
from itertools import cycle

class WerBot(commands.Bot):
    def __init__(self):
        super().__init__(
        command_prefix=";", #Define o prefixo do bot
        intents= discord.Intents.all(), #Seleciona as intents do bot. Não recomendo colocar all() por motivos de segurança
        application_id = 487009012689403904 # o ID da app que pode ser pego no mesmo site do token. Não sei pra que diabos isso serve, mas tá aí pra garantir pq a documentação pediu 
        )

        self.initial_extensions = ["cogs.fun.bola8_cog", #Uma lista para mencionar o diretorio das cogs.
                                   "cogs.admin.kick",
                                   "cogs.admin.ban",
                                   "cogs.misc.perfil",
                                   "cogs.misc.ping",
                                   "cogs.fun.api.anime_carinho",
                                   "cogs.fun.api.anime_abraco",
                                   "cogs.fun.api.anime_wink",
                                   "cogs.fun.api.shaco"]
    
    async def setup_hook(self): #def pra carregar as cogs
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        
        #await bot.tree.sync(guild= discord.Object(id = 714536008263401523)) --> Use esse comando para rodar o bot em um server específico. 
            
    
    async def on_ready(self): #Apenas convenções pra saber quando deu merda ou não e outras coisas importantes
        print(f'{self.user} está online')
        print(
            f"Conectado ao Discord (Latência: {round(bot.latency * 1000)}ms).")
        status_swap.start() #Inicia o trocador de atividades, que é explicado mais abaixo

bot = WerBot() 

# Trocador de atividade ---
frases = cycle(['a bunda lá no chão', 'Merda nos pombos!', 'League of Gays',
               'Não sei matemática básica', 'Wer me solta por favor'])  # Frases da atividade do bot, usando itertools pq preguiça de loopar isso, tnt faz perfomance. Sim eu sou péssimo.

@tasks.loop(seconds=10) #Usando o modulo de tasks do discord.py pra criar a função de swap da atividade. Coloque um valor
                        #maior ou igual a 10 segundos, para não travar o bot.
async def status_swap():
    await bot.change_presence(activity=discord.Game(next(frases)))

# Trocador de atividade ---

with open("secrets/token.txt", "r", encoding='utf-8') as f: #Reader da pasta secrets (que vc deveria criar) pra importar o
    token = f.read()                                        #Token do bot

bot.run(token) #acho que eh auto explicatório 

    