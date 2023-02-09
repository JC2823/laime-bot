import nextcord
from nextcord.ext import commands
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

class Goodbye(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        img = Image.open("Statics/Images/goodbye-base.png")
        font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
        font2 = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

        draw = ImageDraw.Draw(img)

        draw.text(((img.size[0]/2)-(font.getlength("Adios, nos vemos")/2), 459), "Adios, nos vemos", (255, 255, 255), font=font)
        draw.text(((img.size[0]/2)-(font2.getlength(member.name)/2), 577), member.name, (255, 255, 255), font=font2)

        data = BytesIO(await member.display_avatar.read())
        pfp = Image.open(data)
        pfp = pfp.resize((300, 300))
        h, w = pfp.size


        x = (w - h)//2
        pfp = pfp.crop((x, 0, x+h, h))

        mask = Image.new('L', pfp.size)
        mask_draw = ImageDraw.Draw(mask)
        width, height = pfp.size
        mask_draw.ellipse((0, 0, width, height), fill=255)

        pfp = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        pfp.putalpha(mask)
        
        img.paste(pfp, (658, 134), mask=mask)
        bytes = BytesIO()
        img.save(bytes, "png")
        bytes.seek(0)

        channel = self.client.get_channel(int(os.getenv("GOODBYE_CHANNEL")))

        await channel.send(content=f"😢 **Adios {member.mention}, esperamos que la hayas pasado bien en nuestro servidor**", file=nextcord.File(fp=bytes, filename="goodbye.png"))

def setup(client):
    client.add_cog(Goodbye(client))