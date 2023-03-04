import nextcord
from nextcord.ext import commands

from random import randint
from Utils.Economy import checkIfUserExists, createUserAccount, addMoneyWallet, getUserMoney

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command()
    async def work(self, interaction: nextcord.Interaction):
        result = checkIfUserExists(interaction.user.id)
        money = randint(0, 1000)
        if result is False:
            createUserAccount(interaction.user.id, money)
        elif result is True:
            addMoneyWallet(interaction.user.id, money)
        await interaction.send(f"Trabajaste y ganaste {money} dolares!!!")
    
    @nextcord.slash_command()
    async def balance(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if member is None:
            member = interaction.user
        
        result = getUserMoney(int(member.id))
        embed = nextcord.Embed(title=f"Balance de {member.name}")
        embed.add_field(name="Cartera", value=f"{result[0] if result is not None else '0'}$")
        embed.add_field(name="Banco", value=f"{result[1] if result is not None else '0'}$")
        await interaction.send(embed=embed)
    
def setup(client):
    client.add_cog(Economy(client))