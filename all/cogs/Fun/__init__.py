import os, nextcord, asyncio, aiohttp, io,json, random, urllib, dotenv
from nextcord.ext import commands, tasks
import platform
from io import BytesIO
from Misc.utilidades import RapidApi
from Misc.carregadores import json
from craiyon import Craiyon
import time
import base64

dotenv.load_dotenv()

class MemeBtn(nextcord.ui.View):

   
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    async def interaction_check(self, interaction):
     if interaction.user != self.ctx.author:
         await interaction.response.send_message(":no_entry: Só pro Wer issae.", ephemeral=True)
         return False
     else:
         return True
        

    @nextcord.ui.button(label="Próximo meme", style=nextcord.ButtonStyle.green, emoji="⏩")
    async def nextmeme(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
        memeData = json.load(memeApi)

        memeUrl = memeData["url"]
        memeName = memeData["title"]
        memePoster = memeData["author"]
        memeReddit = memeData["subreddit"]
        memeLink = memeData["postLink"]

        memeEmbed = nextcord.Embed(title=memeName, color=0x14cccc)
        memeEmbed.set_author(
            name="WerBot", icon_url=interaction.client.user.display_avatar)
        memeEmbed.set_image(url=memeUrl)
        memeEmbed.set_footer(
            text=f"Meme por: {memePoster} | Subreddit: {memeReddit} | Post: {memeLink}")

        await interaction.response.edit_message(embed=memeEmbed) 

    @nextcord.ui.button(label="Finalizar", style=nextcord.ButtonStyle.secondary)
    async def end(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
         await interaction.response.send_message(f"{interaction.user.mention} Finalizamos a interação", ephemeral=True) 
         for child in self.children: 
            child.disabled = True 
            await interaction.message.edit(view=self)  


class Fun(commands.Cog, description="Faz umas coisas engraçadas."):

    COG_EMOJI  = "😄"

    def __init__(self, bot):
        self.bot = bot
        self.joke_api_key = RapidApi.joke_api
        
    
    @commands.command(name="echo", description=" Que? Para de me imitar", usage="<message>")
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Eu preciso que você digite algo para eu repetir."
        await ctx.message.delete()
        await ctx.send(message)
        
    @commands.command(name="8ball", aliases=["eightball", "8b", "bola8"], description="Um feedback supostamente aleatório. Supostamente\n", usage="<pergunta>")
    async def eightball(self, ctx, *, question):
        responses = [
            'Certamente.',
            'Foi decidido assim.',
            'Sem dúvidas.',
            "Sim - definitivamente.",
            'Sim sim.',
            'Provavelmente.',
            'Pode ser.',
            'Aparentemente sim né.',
            'Provável.',
            'Sim.',
            'Os sinais apontam para sim.',
            'Melhor não te contar agora.',
            'Se concentre e pergunte de novo.',
            "Conta com o ovo no anûs da galinha não.",
            'Não consigo prever agora.',
            'Minha resposta é não.',
            'Minhas fontes dizem que não.',
            'Não parece muito bem',
            'Bem duvidoso',
            'Todo mundo sabe que não.',
            'Talvez.',
            'Si.',
            'Positivo',
            'Do meu ponto de vista, sim',
            'Convincente.',
            'Provável que sim.',
            'Altas chances.',
            'Não.',
            'Negativo.',
            'Incovincente.',
            'Quem sabe?.',
            'Não tenho certeza.',
            'Beeemm talvez.',
            'O wer não me da comida a dias por favor eu não to com energias pra prever isso, volta mais tarde pff.'
        ]
        await ctx.send(f":8ball: Pergunta: {question}\n:8ball: Resposta: {random.choice(responses)}")

    @commands.command(name="meme", description="Responde com um meme.")
    async def meme(self, ctx):
        view = MemeBtn(ctx)
        memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
        memeData = json.load(memeApi)

        memeUrl = memeData["url"]
        memeName = memeData["title"]
        memePoster = memeData["author"]
        memeReddit = memeData["subreddit"]
        memeLink = memeData["postLink"]

        memeEmbed = nextcord.Embed(title=memeName, color=0x14cccc)
        memeEmbed.set_author(
            name="WerBot", icon_url=self.bot.user.display_avatar)
        memeEmbed.set_image(url=memeUrl)
        memeEmbed.set_footer(
            text=f"Meme by: {memePoster} | Subreddit: {memeReddit} | Post: {memeLink}")
        await ctx.send(embed=memeEmbed, view=view)
   
    @commands.command(
        name="paizao",
        description="Manda uma piada de pai",
        aliases=['dadjokes']
    )
    async def dadjoke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/jokes"

        headers = {
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
            'x-rapidapi-key': self.joke_api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                r = await response.json()
                r = r["body"][0]
                await ctx.send(f"**{r['setup']}**\n\n||{r['punchline']}||")

    @commands.command(name="emoji", aliases=["eadd"], description="Adiciona uma imagem como um gif no seu server, criando um emoji.", usage="<url do emoji> <nome>")
    async def emoji(self, ctx, url: str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgOrGif = BytesIO(await r.read())
                    eValue = imgOrGif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=eValue, name=name)
                        await ctx.send(f":{name}: emoji adicionado!")
                        await ses.close()
                    else:
                        await ctx.send(f'😞 **Emoji não pode ser adicionado** | {r.status}')
                except nextcord.HTTPException:
                    await ctx.send("📁 Nossa lobo mau, que arquivo grande em... você não pode adicionar um emoji com mais de 256kb, fica pra próxima.")


    @commands.command(name="emojify", description="Transforme seu texto em emoji", usage="<texto>") 
    @commands.cooldown(2, 30, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        emojis = []
        for beans in text:
            if beans.isdecimal():
                num2word = {
                    "0" : 'zero', 
                    "1": 'one', 
                    "2": "two", 
                    "3": "three", 
                    "4" : "four", 
                    "5":"five", 
                    "6":"six", 
                    "7":"seven", 
                    "8":"eight", 
                    "9": "nine"
                }
                emojis.append(f":{num2word.get(beans)}: ")

            elif beans.isalpha():
                text = beans.lower()
                emojis.append(f":regional_indicator_{text}: ")
            elif beans == "!":
                beans = ":grey_exclamation:"
                emojis.append(beans)
            elif beans == "?":
                beans = ":grey_question:"
                emojis.append(beans)
            elif beans == "*":
                beans = ":asterisk:"
                emojis.append(beans)
            else:
                emojis.append(beans)

        await ctx.send(' '.join(emojis))


    @commands.command(name="IAart", description="Crie imagens belas com uma inteligencia virtual.", usage="<Descreva detalhadamente o que voce quer ver.>")
    async def generate(self, ctx: commands.Context, *, prompt: str):
        ETA = int(time.time() + 60)
        mensagem = await ctx.send(f"🖌️ **Gerando imagem... Isso pode demorar um tempo. Tempo: <t:{ETA}:R>**")
        generator = Craiyon()
        result = generator.generate(prompt)
        images = result.images
        for i in images:
            image = BytesIO(base64.decodebytes(i.encode("utf-8")))
            return await mensagem.edit(content="🖌️ **Imagem gerada!**", file=nextcord.File(image, "image.png"))
            