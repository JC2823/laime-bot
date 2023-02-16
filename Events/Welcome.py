import nextcord
from nextcord.ext import commands
import os
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from Utils.Images import round_avatar

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if os.getenv("WELCOME_CHANNEL") is not None:
            img = Image.open("Statics/Images/welcome-base.png")
            font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
            font2 = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

            draw = ImageDraw.Draw(img)
            size = font2.getlength(member.name)

            draw.text((558, 459), "Bienvenid@", (255, 255, 255), font=font)
            draw.text(((img.size[0]/2)-(size/2), 577), member.name, (255, 255, 255), font=font2)

            pfp = await round_avatar(member, (300, 300))
            
            img.paste(pfp[0], (658, 134), mask=pfp[1])
            
            bytes = BytesIO()
            img.save(bytes, "png")
            bytes.seek(0)

            channel = self.client.get_channel(int(os.getenv("WELCOME_CHANNEL")))

            await channel.send(content=f"👋 **Bienvenid@ {member.mention}!!!**", file=nextcord.File(fp=bytes, filename="welcome.png"))

            roles = [int(role) for role in os.getenv("WELCOME_ROLES").split(' ')]

            if roles is not None:
                for r in roles:
                    role = member.guild.get_role(r)
                    await member.add_roles(role)
        else:
            pass

def setup(client):
    client.add_cog(Welcome(client))