import nextcord
import os

class ReportModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "🟢 Comparte tu opinion sobre nuestro bot",
            timeout=5 * 60,
        )

        self.opinion = nextcord.ui.TextInput(
            label="¿Cómo calificaría su experiencia?",
            min_length=2
        )
        self.add_item(self.opinion)

        self.description = nextcord.ui.TextInput(
            label="Cuentanos mas acerca de tu experiencia",
            style=nextcord.TextInputStyle.paragraph,
            required=True
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.send(f"Gracias **{interaction.user.name}**!! nos encargaremos leer tu reseña para poder seguir mejorando nuestro bot 😄")
        channel = interaction.client.get_channel(os.environ.get("FEEDBACK_CHANNEL"))
        embed = nextcord.Embed(title="\✅ Nueva Reseña!!", color=0xffc01e)
        embed.add_field(name="\👤 Autor:", value=f"```{interaction.user.name}```")
        embed.add_field(name="\💬 Clasificacion:", value=f"```{self.opinion.value}```", inline=False)
        embed.add_field(name="\📄 Opinion:", value=f"```{self.description.value}```")
        embed.set_image(url="https://bnz05pap001files.storage.live.com/y4mFDNGNSHaKkrDbB1cGXqhLElV0b9DfatvE_bgOWrNqycKK7yuZf1yF2MV7ikkkvOrGCfwHtSapqF50-S9jTD34awEYgyiamHKYCn_2cndWSM_v1yGK2Ofd3lNCaoBCo4nEyeg3xpwHD1gMpvd8nAdqbjQ40LMP6e7xlpDSHUkBXmxouTgY_DwuXoutY3X9ghp?width=1430&height=371&cropmode=none")
        await channel.send(embed=embed)