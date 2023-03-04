import nextcord
import asyncio

from Utils.Poll import createPoll

class CreatePollModal(nextcord.ui.Modal):
    def __init__(self, channel: nextcord.TextChannel):
        super().__init__(
            "Test"
        )
        
        self.channel = channel
        
        self.titulo = nextcord.ui.TextInput(label="Titulo de la encuesta", placeholder="Ej: Te gusta Minecraft?")
        self.add_item(self.titulo)
        
        self.options = nextcord.ui.TextInput(label="Opciones", placeholder="Separadas por '|'. Ej: Si | No", style=nextcord.TextInputStyle.paragraph)
        self.add_item(self.options)
        
    async def callback(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title=f"NUEVA ENCUESTA! {self.titulo.value}", color=0xffc01e)
        emojis = ['\u0031\u20E3', '\u0032\u20E3', '\u0033\u20E3', '\u0034\u20E3', '\u0035\u20E3', '\u0036\u20E3', '\u0037\u20E3', '\u0038\u20E3', '\u0039\u20E3', '\uD83D\uDD1F']
        
        i = 1
        option = self.options.value.split(" | ") and self.options.value.split("|")
        for o in option:
            o = o.replace('\n', ' ').strip()
            
            embed.add_field(name=f"{emojis[i-1]} Opcion {i}", value=f"**```{o}```**", inline=False if i % 3 == 0 else True)

            i += 1
            
        message = await self.channel.send(embed=embed)
        
        createPoll(self.titulo.value, interaction.guild_id,  self.channel.id, message.id, self.options.value)
        
        for i in range(len(option)):
            await message.add_reaction(emojis[i])
            i += 1