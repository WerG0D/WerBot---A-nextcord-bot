import nextcord
from nextcord.ext import commands, activities


class MakeLink(nextcord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Entrar no game", url=f"{link}"))


class Activities(commands.Cog, name="Atividades Discord", description="Cria atividades no Discord"):

    COG_EMOJI = "🚀"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, description="Cria atividades no Discord")
    async def activity(self, ctx):
        return

    @activity.command(name="SkecthHeads", description="Cria um `Skecth Heads crew` no seu canal.")
    async def skecth_heads(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.sketch)

        except nextcord.HTTPException:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        embed = nextcord.Embed(
            title="Skecth Heads Crew Game", description=f"{ctx.author.mention} crou um jogo em: {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="Que p*rr@ é essa?", value="É tipo o skribble.io só que mal feito e feito no canal de voz. Alguem desenha alguma merda e o resto tem que adivinhar.")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4503731144471/Discord_SketchHeads_Lobby.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="poker", description="Cria um `poker` no seu canal.")
    async def poker(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.poker)

        except nextcord.HTTPException:
            msg = await ctx.send("Por favor, fala um canal aí..", delete_after=45)
            return msg

        embed = nextcord.Embed(
            title="Poker", description=f"{ctx.author.mention} criou em {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="Que p*rr@ é essa?", value="Este é um poker em  Texas hold 'em,  Podem jogar 8 pessoas ao mesmo tempo, e ainda ter 17 espectadores.")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/1500015218941/Screen_Shot_2021-05-06_at_1.46.50_PM.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="Xadrez", description="Cria  `Xadrez` no canal.")
    async def chess(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.chess)

        except nextcord.HTTPException:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Chess in the park Game (Xadrez)",
                               description=f"{ctx.author.mention} criou em {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="Que p*rr@ é essa?", value="Um xadrez no canal do discord para você pagar de intelectual!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4404615637015/chess_banner.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))


    @activity.command(name="youtube", description="Cria um `Youtube Watch Together` no canal.")
    async def youtube(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.youtube)

        except nextcord.HTTPException:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Youtube Watch Together",
                               description=f"{ctx.author.mention} criou em {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="Que p*rr@ é essa?", 
                        value=
                        "É uma atividade pra rodar o Youtube dentro de um canal do discord.")
        embed.set_thumbnail(
            url="https://www.youtube.com/s/desktop/6007d895/img/favicon_32x32.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))


    @activity.command(name="fishington", description="Cria `Fishington` no seu canal.")
    async def fishington(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.fishington)

        except nextcord.HTTPException:
            msg = await ctx.send("Por favor, fala um canal aí.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Fishington",
                               description=f"{ctx.author.mention} criou em {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="Que p*rr@ é essa?", 
                        value=
                        "Um jogo de pescaria no canal do discord, suporta outros 24 players.")
        embed.set_thumbnail(
            url="https://betrayal.io/asset/image/share-card-fishington.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))


