import nextcord
from nextcord.ext import commands
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests

class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command()
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(embed=nextcord.Embed(description="🛰 Pong!", color=0xffc01e))

    @nextcord.slash_command()
    async def userinfo(self, interaction: nextcord.Interaction, member: nextcord.Member):
        img = Image.open("Statics/Images/user-info-base.png")
        main_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
        sub_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 36)
        date_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

        draw = ImageDraw.Draw(img)
        draw.text((823, 240), f"{member.name if len(member.name) < 13 else f'{member.name[:13]}...'}", (255, 255, 255), font=main_font)
        draw.text((644, 602), str(member.id), (178, 178, 178), font=sub_font)
        draw.text((800, 683), member.status.capitalize(), (178, 178, 178), font=sub_font)
        draw.text((789, 764), f"{member.display_name if len(member.display_name) < 13 else f'{member.display_name[:13]}...'}", (178, 178, 178), font=sub_font)
        draw.text((1681, 65), str(member.created_at.strftime("%b %d, %Y")), (255, 255, 255), font=date_font)

        draw.text((1257, 641), f"{str(0)}$", (178, 178, 178), font=sub_font)
        draw.text((1257, 786), f"{str(0)}$", (178, 178, 178), font=sub_font)

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

        img.paste(pfp, (456, 167), mask=mask)

        bytes = BytesIO()
        img.save(bytes, "png")
        bytes.seek(0)

        await interaction.send(files=[nextcord.File(fp=bytes, filename="userinfo-test.png")])

    @nextcord.slash_command()
    async def serverinfo(self, interaction: nextcord.Interaction):
        img = Image.open("Statics/Images/server-info-base.png")
        main_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 96)
        sub_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 40)
        date_font = ImageFont.FreeTypeFont("Statics/Fonts/Inter.ttf", 48)

        draw = ImageDraw.Draw(img)
        draw.text((836, 259), interaction.guild.name if len(interaction.guild.name) <= 20 else f"{interaction.guild.name[:13]}...", (255, 255, 255), font=main_font)
        draw.text((521, 668), str(interaction.guild_id), (178, 178, 178), font=sub_font)
        draw.text((521, 804), str(interaction.guild.owner.name), (178, 178, 178), font=sub_font)
        draw.text((1239, 624), str(len(list(interaction.guild.channels))), (178, 178, 178), font=sub_font)
        draw.text((1239, 748), str(interaction.guild.member_count), (178, 178, 178), font=sub_font)
        draw.text((1239, 872), str(len(list(interaction.guild.roles))), (178, 178, 178), font=sub_font)
        draw.text((1683, 65), str(interaction.guild.created_at.strftime("%b %d, %Y")), (255, 255, 255), font=date_font)

        data = BytesIO(await interaction.guild.icon.read())
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

        img.paste(pfp, (456, 167), mask=mask)

        bytes = BytesIO()
        img.save(bytes, "png")
        bytes.seek(0)

        await interaction.send(file=nextcord.File(fp=bytes, filename="serverinfo.png"))

    @nextcord.slash_command()
    async def avatar(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if member is None:
            member = interaction.user
        embed = nextcord.Embed(title=f"👤 Avatar de {member.name}", color=0xffc01e)
        embed.add_field(name="\✅ Descargar:", value=f"[PNG]({member.display_avatar.with_format('png').url}) | [JPG]({member.display_avatar.with_format('jpg').url}) | [WEBP]({member.display_avatar.with_format('webp').url})")
        embed.set_image(member.display_avatar.url)
        await interaction.send(embed=embed)

    @nextcord.slash_command()
    async def feedback(self, interaction: nextcord.Interaction):
        await interaction.send("En desarrollo...69")

def setup(client):
    client.add_cog(Utils(client))