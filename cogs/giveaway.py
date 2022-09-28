import nextcord
from nextcord.ext import commands, tasks, application_checks
from nextcord.abc import GuildChannel
from nextcord import Interaction, ChannelType, SlashOption
import asyncio
import humanfriendly
import time as pyTime
import json
import random

#Essa cog foi feita usando como base o canal "Glowstik"
#https://github.com/Glowstik-YT/giveawayBot/blob/main/cogs/giveaway.py 

class JoinGiveaway(nextcord.ui.View):
    def __init__(self, time, name, guild, epochEnd, bot):
        super().__init__(timeout=time)
        self.name = name
        self.guild = guild
        self.time = epochEnd
        self.bot = bot

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @nextcord.ui.button(label="Entre no giveaway", style=nextcord.ButtonStyle.blurple, custom_id="join"
                        )
    async def Join(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT participants FROM giveaways WHERE guild = ? AND prize = ? AND time = ?", (self.guild, self.name, self.time))
            data = await cursor.fetchone()
            if data:
                participants = data[0]
                try:
                    participants = json.loads(participants)
                except:
                    participants = []
                if interaction.user.id in participants:
                    return await interaction.response.send_message("Você já entrou no giveaway", ephemeral=True)
                else:
                    participants.append(interaction.user.id)
                await cursor.execute("UPDATE giveaways SET participants = ? WHERE guild = ? AND prize = ? AND time = ?", (json.dumps(participants), self.guild, self.name, self.time))
                await interaction.response.send_message("Opa, você entrou no giveaway", ephemeral=True)
            else:
                await interaction.response.send_message("Esse giveaway não existe ou já acabou.", ephemeral=True)
        await self.bot.db.commit()


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=5)
    async def giveawayCheck(self):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT time, prize, message, channel, guild, participants, winners, finished FROM giveaways")
            data = await cursor.fetchall()
            if data:
                for table in data:
                    time, prize, message, channel, guild, participants, winners, finished = table[
                        0], table[1], table[2], table[3], table[4], table[5], table[6], table[7]
                    if not finished:
                        if pyTime.time() >= time:
                            guild = self.bot.get_guild(guild)
                            channel = guild.get_channel(channel)
                            if guild or channel is not None:
                                try:
                                    participants = json.loads(table[5])
                                except:
                                    participants = []
                                if not len(participants) == 0:
                                    if len(participants) < winners:
                                        winner = random.choices(
                                            participants, k=len(participants))
                                    else:
                                        winner = random.choices(
                                            participants, k=winners)
                                    winners = []
                                    for user in winner:
                                        winners.append(
                                            guild.get_member(int(user)).name)
                                    if winner is not None:
                                        em = nextcord.Embed(
                                            title="Resultado do Giveaway", description=f"Parabens, o corno `{', '.join(winners)}` ganhou o giveaway, o premio é >> `{prize}` :tada:")
                                        await channel.send(embed=em)
                                        await cursor.execute("UPDATE giveaways SET finished = ? WHERE guild = ? AND prize = ? AND message = ?", (True, guild.id, prize, message))
                                        msg = await channel.fetch_message(message)
                                        newEm = nextcord.Embed(
                                            title="Giveaway Finalizado", description=f"`{', '.join(winners)}` ganhou `{prize}` :tada: :tada: :tada:", color=nextcord.Color.blurple())
                                        newEm.set_footer(
                                            text=f"Participantes: {len(participants)}")
                                        await msg.edit(embed=newEm)
                                else:
                                    await cursor.execute("UPDATE giveaways SET finished = ? WHERE guild = ? AND prize = ? AND message = ?", (True, guild.id, prize, message))
                                    msg = await channel.fetch_message(message)
                                    newEm = nextcord.Embed(
                                        title=f"{prize} Giveaway finalizado", description=f"Ninguém entrou neste giveaway <:cri:796075215741255691>", color=nextcord.Color.blurple())
                                    await msg.edit(embed=newEm)
                                    em = nextcord.Embed(
                                        title=f"{prize} Giveaway finalizado", description="Ninguém entrou no giveaway")
                                    await channel.send(embed=em)
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(2)
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS giveaways (time INTEGER, prize TEXT, message INTEGER, channel INTEGER, guild INTEGER, participants TEXT, winners INTEGER, finished BOOL)")
        await self.bot.db.commit()
        print("Status do banco de dados: Online")
        self.giveawayCheck.start()
        print("Loop do Giveaway: Online")

    @nextcord.slash_command(name="ping", description="Vê o ping do bot")
    async def ping(self, interaction: Interaction):
        em = nextcord.Embed(title="Ping")
        em.add_field(
            name="Minha latência é:", value=f"{round(self.bot.latency*1000)} ms"
        )
        em.set_footer(
            text=f"Ping pedido por >> {interaction.user}", icon_url=interaction.user.display_avatar
        )
        await interaction.response.send_message(embed=em)

    @nextcord.slash_command(name="giveaway", description="Giveaway comando mestre [Sem funcão]")
    async def giveaway(self, interaction: Interaction):
        return

    @giveaway.subcommand(name="iniciar", description="Começa um giveaway")
    @application_checks.has_permissions(manage_messages=True)
    async def start(self, interaction: Interaction, prêmio: str = SlashOption(description="O prêmio do giveaway", required=True), canal: GuildChannel = SlashOption(channel_types=[ChannelType.text], description="Em qual canal o giveaway vai acontecer??", required=True), time: str = SlashOption(description="A quantidade de tempo que o giveaway vai durar, exemplo: 5d, 6h, 30m", required=True), winners: int = SlashOption(description="O número de vencedores do giveaway", required=True)):
        time = humanfriendly.parse_timespan(time)
        epochEnd = pyTime.time() + time
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO giveaways (time, prize, message, channel, guild, participants, winners, finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                 (epochEnd, prêmio, "", canal.id,
                                  interaction.guild.id, "", winners, False)
                                 )
            embed = nextcord.Embed(
                title=f"🎉{prêmio}🎉", description=f"Termina em: <t:{int(epochEnd)}:R>\nVencedor(es): `{winners}`\nClique em `Entre no giveaway` para entrar :p", color=nextcord.Color.blurple())
            await interaction.response.send_message(f"Giveaway começou no canal: {canal.mention}", ephemeral=True)
            view = JoinGiveaway(
                time, prêmio, interaction.guild.id, epochEnd, self.bot)
            msg = await canal.send(embed=embed, view=view)
            view.message = msg
            await cursor.execute("UPDATE giveaways SET message = ? WHERE guild = ? AND prize = ? AND time = ?", (msg.id, interaction.guild.id, prêmio, epochEnd))
        await self.bot.db.commit()

    @giveaway.subcommand(name="refazer", description="Refaz o giveaway com um novo vencedor")
    @application_checks.has_permissions(manage_messages=True)
    async def reroll(self, interaction: Interaction, messageid: str = SlashOption(description="O ID da mensagem do Giveaway", required=True)):
        try:
            message = int(messageid)
        except ValueError:
            return interaction.response.send_message("Só aceitamos numeros inteiros como ID pogchamp. Sem sacanear")
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT participants, channel, prize, winners FROM giveaways WHERE message = ? AND finished = ?", (message, True))
            data = await cursor.fetchone()
            if data:
                try:
                    participants = json.loads(data[0])
                except:
                    participants = []
                if len(participants) == 0:
                    return await interaction.response.send_message("Não é possivel refazer o giveaway porquê ninguém entrou nele")
                if not len(participants) == 0:
                    if len(participants) < data[3]:
                        winner = random.choices(
                            participants, k=len(participants))
                    else:
                        winner = random.choices(participants, k=data[3])
                    winners = []
                    for user in winner:
                        winners.append(
                            interaction.guild.get_member(int(user)).name)
                channel = interaction.guild.get_channel(data[1])
                if winners and channel is not None:
                    em = nextcord.Embed(title="Resultado do reroll do giveaway",
                                        description=f"PARÁBENS CORNO(S): `{', '.join(winners)}`  Vocês ganharam o giveaway `{data[2]}` :tada:")
                    await channel.send(embed=em)
                    await channel.send(f"PARABÉNS SEGUNDAS OPÇÕES DE MERDA: {winner.mention} Vocês ganharam o giveaway `{data[2]}` :tada: [REFEITO]")
                    msg = await channel.fetch_message(data[0])
                    newEm = nextcord.Embed(
                        title="Giveaway finalizado", description=f"`{winner}` ganhou `{data[2]}` :tada: :tada: :tada:", color=nextcord.Color.blurple())
                    newEm.set_footer(
                        text=f"Participantes: {len(participants)}")
                    await msg.edit(embed=newEm)
                else:
                    return await interaction.response.send_message("Não é possível refazer o giveaway porquê o canal ou o vencedor não existem mais")
            else:
                return await interaction.response.send_message("Não é possível refazer um giveaway que não existe bocó")


def setup(bot):
    bot.add_cog(Giveaway(bot))
