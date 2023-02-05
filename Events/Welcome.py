import nextcord
from nextcord.ext import commands
import os
from PIL import Image, ImageFont, ImageOps, ImageDraw
from io import BytesIO

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if os.environ.get("WELCOME_CHANNEL") is not None:
            img = Image.open("Statics/Images/welcome-base.png")
            font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
            font2 = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

            draw = ImageDraw.Draw(img)
            size = font2.getlength(member.name)

            draw.text((558, 459), "Bienvenid@", (255, 255, 255), font=font)
            draw.text(((img.size[0]/2)-(size/2), 577), member.name, (255, 255, 255), font=font2)

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

            channel = self.client.get_channel(os.environ.get("WELCOME_CHANNEL"))

            await channel.send(content=f"👋 **Bienvenid@ {member.mention}!!!**", file=nextcord.File(fb=bytes, filename="welcome.png"))

            roles = os.environ.get("WELCOME_ROLES")

            if roles is not None:
                for r in roles:
                    role = member.guild.get_role(r)
                    await member.add_roles(role)

def setup(client):
    client.add_cog(Welcome(client))