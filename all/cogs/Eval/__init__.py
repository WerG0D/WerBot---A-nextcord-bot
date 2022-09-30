import nextcord, asyncio, os, io, contextlib, textwrap, traceback
from typing import Any, Optional

from nextcord.ext import commands
from nextcord.ui import Modal, TextInput

from Misc.utilidades import Wer, Emojis
from Misc.messages import DeleteMessageSlash

class SnekBox_Eval(nextcord.ui.Modal):
    def __init__(self) -> None:
     super().__init__(title="Avalia seu código", custom_id="evaluate_code")

     self._last_result: Optional[Any] = None

     self.add_item(
            nextcord.ui.TextInput(
                label="Seu código",
                placeholder="print('Hello')",
                custom_id="Código avaliado",
                style=nextcord.TextInputStyle.paragraph,
                min_length=10
            ),
     )

    async def callback(self, inter: nextcord.Interaction) -> None:

        view = DeleteMessageSlash(inter)

        vars = {
            'bot' : inter.client,
            'ctx': commands.Context,
            'interaction': inter,
            'channel': inter.channel,
            'author': inter.user,
            'guild': inter.guild,
            'message': inter.message,
            '_':  self._last_result,
            'nextcord': nextcord
             
        }

        vars.update(globals())

        
        embed = nextcord.Embed(title="Seu código", description="✅ Seu código foi avaliado e aqui está o julgamento:", color=0x00FF00)
        code = self.children[0].value
        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'
        stdout = io.StringIO()

        try:
            exec(to_compile, vars)
        except Exception as e:
             return await inter.response.send_message(f'```py\n{e.__class__.__name__}: {e}\n```')  

        func = vars['func']       

        try:
            with contextlib.redirect_stdout(stdout):
                res = await func()

        except Exception as e:
            value = stdout.getvalue()
            await inter.response.send_message(f'```py\n{value}{traceback.format_exc()}\n```')
            
        else:
            value = stdout.getvalue()
            try:
                await inter.message.add_reaction(Emojis.check)
            except:
                pass

        if Wer.token in value:
            value = ":warning: Nenhuma informação sensível foi encontrada no seu código."


        embed.add_field(name="Input Code", value=f"```py\n{value}\n```", inline=False)

        if res is None:
           if not value:
               embed.add_field(name="Código avaliado:", value=f"{Emojis.decline} A execução do código não retornou nada.", inline=False) 
        else:
            self._last_result = res
            embed.add_field(f'```py\n{value}{res}\n```')
        await inter.response.send_message(embed=embed,view=view)

    async def on_error(self, error, interaction: nextcord.Interaction):
        view = DeleteMessageSlash(interaction)
        embed = nextcord.Embed(title="Code Status", description=":x: Um erro ocorreu.", color=0xFF0000)
        embed.add_field(name=":warning: O erro", value=f"```{error}```", inline=False)
        await interaction.response.send_message(embed=embed,view=view)     
 
class Eval(commands.Cog, description='Avalia seu código.'):

    
    COG_EMOJI = "💻"

    def __init__(self, bot):
        self.bot = bot
        

    @nextcord.slash_command(name="eval", description="Avalia o código Python")
    async def eval(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(modal=SnekBox_Eval())
  
                   
