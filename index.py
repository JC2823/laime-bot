import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = nextcord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(intents=intents, default_guild_ids=os.getenv("TESTING_GUILDS"))

@client.event
async def on_ready():
    print("Hello World")

for file in os.listdir("./Cogs"):
    if file.endswith(".py"):
        client.load_extension(f"Cogs.{file[:-3]}")

for file in os.listdir("./Events"):
    if file.endswith(".py"):
        client.load_extension(f"Events.{file[:-3]}")

if __name__ == '__main__':
    client.run(os.getenv("DISCORD_TOKEN"))