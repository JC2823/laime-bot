import nextcord
from nextcord.ext import commands
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from Utils.Images import round_avatar

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        if os.getenv("GOODBYE_CHANNEL") is not None:
            img = Image.open("Statics/Images/goodbye-base.png")
            font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
            font2 = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

            draw = ImageDraw.Draw(img)

            draw.text(((img.size[0]/2)-(font.getlength("Adios, nos vemos")/2), 459), "Adios, nos vemos", (255, 255, 255), font=font)
            draw.text(((img.size[0]/2)-(font2.getlength(member.name)/2), 577), member.name, (255, 255, 255), font=font2)

            pfp = await round_avatar(member, (300, 300))
            img.paste(pfp[0], (658, 134), mask=pfp[1])
            
            bytes = BytesIO()
            img.save(bytes, "png")
            bytes.seek(0)

            channel = self.client.get_channel(int(os.getenv("GOODBYE_CHANNEL")))

            await channel.send(content=f"😢 **Adios {member.mention}, esperamos que la hayas pasado bien en nuestro servidor**", file=nextcord.File(fp=bytes, filename="goodbye.png"))
        else:
            pass

def setup(client):
    client.add_cog(Goodbye(client))