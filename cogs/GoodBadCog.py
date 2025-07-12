# standard library imports

# third party imports
import discord
from discord import app_commands
from discord.ext import commands


class GoodBadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # good bot slash command
    @app_commands.command(name="goodbot",
                          description="Tell Craybot it's doing a good job")
    async def good_bot(self, interaction: discord.Interaction) -> None:
        bot_response = (f"Thanks for telling me I'm doing a good job, "
                        f"{interaction.user.mention}! :D ")
        await interaction.response.send_message(bot_response)

    # bad bot slash command
    @app_commands.command(name="badbot",
                          description="Tell Craybot it's doing a bad job")
    async def bad_bot(self, interaction: discord.Interaction) -> None:
        bot_response = (f"Oh no! I'll try to do better, "
                        f"{interaction.user.mention} :(")
        await interaction.response.send_message(bot_response)


async def setup(bot: commands.Bot):
    await bot.add_cog(GoodBadCog(bot))

