import nextcord
from nextcord.ext import commands
from tabulate import tabulate
import matplotlib.pyplot as plt
from io import BytesIO

from Components.Poll import CreatePollModal
from Utils.Poll import setPollResults, getPollResults, getPollList, getPollHistory, deletePoll, getPollById

class Poll(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        
    @nextcord.slash_command()
    async def poll(self, interaction: nextcord.Interaction):
        pass
    
    @poll.subcommand(name="create")
    async def create(self, interaction: nextcord.Interaction, ch: nextcord.TextChannel):
        await interaction.response.send_modal(modal=CreatePollModal(channel=ch))
        
    @poll.subcommand(name="list")
    async def list(self, interaction: nextcord.Interaction):
        result = getPollList(interaction.guild_id)
        embed = nextcord.Embed(title="Poll List", description=f"```{tabulate(result, headers=['', 'Title'], tablefmt='fancy_grid')}```", color=0xffc01e)
        await interaction.send(embed=embed)
        
    @poll.subcommand(name="end")
    async def end(self, interaction: nextcord.Interaction, id: int):
        result = getPollById(interaction.guild_id, id)
        if result is None:
            await interaction.send(":x: Encuesta no encontrada!")
            return
        
        channel = self.client.get_channel(int(result["channel"]))
        message = await channel.fetch_message(int(result["message"]))
        
        count = []
        emojis = ['\u0031\u20E3', '\u0032\u20E3', '\u0033\u20E3', '\u0034\u20E3', '\u0035\u20E3', '\u0036\u20E3', '\u0037\u20E3', '\u0038\u20E3', '\u0039\u20E3', '\uD83D\uDD1F']
        
        for reaction in message.reactions:
            if reaction.emoji in emojis:
                count.append(float(reaction.count - 1))
                    
        activities = list(o.replace('\n', ' ').strip() for o in result["options"].split("|"))

        colors = ['#ffc01e', '#313131']

        plt.bar(range(len(count)), count, color=colors)
        plt.xticks(range(len(count)), activities)
        plt.title(result["title"])
        
        bytes = BytesIO()
        plt.savefig(bytes, format="png")
        bytes.seek(0)
        
        await message.edit(file=nextcord.File(fp=bytes, filename="results.png"), embed=None)
        await message.clear_reactions()
        
        setPollResults(interaction.guild_id, id, bytes)
        deletePoll(id)
        
        await interaction.send("Encuesta borrada!")
        
    @poll.subcommand(name="history")
    async def history(self, interaction: nextcord.Interaction):
        result = getPollHistory(interaction.guild_id)
        embed = nextcord.Embed(title="Poll List", description=f"```{tabulate(result, headers=['', 'Title', 'Ended'], tablefmt='fancy_grid')}```", color=0xffc01e)
        await interaction.send(embed=embed)
        
    @poll.subcommand(name="get-results")
    async def results(self, interaction: nextcord.Interaction, id: int):
        bytes = getPollResults(interaction.guild_id, id)
        await interaction.send(file=nextcord.File(fp=BytesIO(bytes["results"]), filename="results.png"))
            
        
def setup(client):
    client.add_cog(Poll(client))