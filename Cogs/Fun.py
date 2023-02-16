import nextcord
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import random
import requests

from Utils.Images import round_avatar

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command()
    async def howgay(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if member is None:
            member = interaction.user
            
        howgay = int(random.random()*10) / 10.0
            
        image = Image.open("Statics/Images/howgay-base.png")
        font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 150)
        draw = ImageDraw.Draw(image)    
        
        draw.text((616, 115), f"Es {int(howgay*100)}% gay", (255, 255, 255), font=font)    
        
        def new_bar(x, y, width, height, progress, bg=(129, 66, 97), fg=(255,122,0), fg2=(29,29,29)):
            draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg2, width=10)
            draw.ellipse((x+width, y, x+height+width, y+height), fill=fg2)
            draw.ellipse((x, y, x+height, y+height), fill=fg2)
            width = int(width*progress)

            draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg, width=10)
            draw.ellipse((x+width, y, x+height+width, y+height), fill=fg)
            draw.ellipse((x, y, x+height, y+height), fill=fg)
            
        new_bar(414, 344, 1100, 163, howgay)
        
        bytes = BytesIO()
        image.save(bytes, "png")
        bytes.seek(0)
        
        await interaction.send(content=f"{member.mention} es un {int(howgay*100)}% gay!!", file=nextcord.File(fp=bytes, filename="howgay.png"))

    @nextcord.slash_command()
    async def cat(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="\🐱 MEEEOOWWW", color=0xffc01e)
        embed.set_image(url=requests.get("https://aws.random.cat/meow").json()["file"])
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def dog(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="\🐶 WOFF", color=0xffc01e)
        embed.set_image(url=requests.get("https://dog.ceo/api/breeds/image/random").json()["message"])
        await interaction.send(embed=embed)

    @nextcord.slash_command(name="8ball")
    async def _ball(self, interaction: nextcord.Interaction, question: str):
        answers = ["Sí", "No", "¿Quien sabe?", "Tal vez", "Nunca sabremos", "Vuelve a preguntar, no te escuche bien"]
        
        embed = nextcord.Embed(title="\🎩 Bola mágica!", color=0xffc01e)
        embed.add_field(name="\❔ Tu pregunta:", value=f"```{question}```", inline=False)
        embed.add_field(name="\📄 Mi respuesta: ", value=f"```{random.choice(answers)}```")
        
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def love(self, interaction: nextcord.Interaction, first: nextcord.Member, second: nextcord.Member):
        image = Image.open("Statics/Images/love-base.png")
        font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 80)
        
        love = random.randint(0, 101)
        messages = ["Wow, creo que deberian distanciarse un poco...", "No creo que esten destinados a estar juntos", "Mejor se quedan como amigos", "Que bonita pareja formarian!", "WOW! que buena compatibilidad tienen!", "Son la pareja perfecta..."]
        message = None
        emote_list_100 = ["Statics/Emotes/enamorado.png", "Statics/Emotes/superestrella.png", "Statics/Emotes/sonrisa.png"]
        emote_list_50 = ["Statics/Emotes/confundido.png", "Statics/Emotes/muerto.png"]
        if love > 50:
            emote = Image.open(random.choice(emote_list_100))
            message = random.choice(messages[3:])
        elif love < 50:
            emote = Image.open(random.choice(emote_list_50))
            message = random.choice(messages[:3])
        emote = emote.resize((150, 150))
        image.paste(emote, (971, 129), emote.convert("RGBA"))
        
        draw = ImageDraw.Draw(image)
        length = font.getlength(f"{love}%")
        draw.text(((image.size[0]/2)-(length/2), 339), f"{love}%", (255, 255, 255), font=font)
        
        pfp1 = await round_avatar(first, (349, 349))
        pfp2 = await round_avatar(second, (349, 349))
        
        image.paste(im=pfp1[0], box=(511, 136), mask=pfp1[1])
        image.paste(im=pfp2[0], box=(1231, 136), mask=pfp2[1])
        
        bytes = BytesIO()
        image.save(bytes, "png")
        bytes.seek(0)
        
        await interaction.send(content=f"Su compatibilidad es de {love}%! {message}", file=nextcord.File(fp=bytes, filename="love.png"))
        

def setup(client):
    client.add_cog(Fun(client))
