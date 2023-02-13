import nextcord
from nextcord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import requests

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

def setup(client):
    client.add_cog(Fun(client))
