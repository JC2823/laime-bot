from io import BytesIO
from PIL import Image, ImageDraw, ImageOps
import nextcord

async def round_avatar(member: nextcord.Interaction, wh: tuple):
    data = BytesIO(await member.display_avatar.read())
    pfp = Image.open(data)
    pfp = pfp.resize(wh)
    h, w = pfp.size


    x = (w - h)//2
    pfp = pfp.crop((x, 0, x+h, h))

    mask = Image.new('L', pfp.size)
    mask_draw = ImageDraw.Draw(mask)
    width, height = pfp.size
    mask_draw.ellipse((0, 0, width, height), fill=255)
    
    pfp = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
    pfp.putalpha(mask)
    return (pfp, mask)

def new_bar(draw, x, y, width, height, progress, bg=(129, 66, 97), fg=(255,122,0), fg2=(29,29,29)):
    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg2, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height), fill=fg2)
    draw.ellipse((x, y, x+height, y+height), fill=fg2)
    width = int(width*progress)

    draw.rectangle((x+(height/2), y, x+width+(height/2), y+height), fill=fg, width=10)
    draw.ellipse((x+width, y, x+height+width, y+height), fill=fg)
    draw.ellipse((x, y, x+height, y+height), fill=fg)