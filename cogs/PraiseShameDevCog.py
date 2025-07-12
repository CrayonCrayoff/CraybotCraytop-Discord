# standard library imports
import os
from pathlib import Path

# third party imports
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


SCRIPT_DIR = Path(__file__).resolve().parent  # finds this script's folder
PARENT_DIR = SCRIPT_DIR.parent  # goes up once again (to the DiscordBot folder)

load_dotenv(PARENT_DIR / ".env")
CRAYON_USER_ID = int(os.getenv("CRAYON_USER_ID"))


class PraiseShameDevCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # good bot slash command
    @app_commands.command(name="praisedev",
                          description="Tell my dev he's doing a good job")
    async def good_bot(self, interaction: discord.Interaction) -> None:
        bot_response = (f"Hey <@{CRAYON_USER_ID}>, "
                        f"{interaction.user.display_name} likes your work!")
        await interaction.response.send_message(bot_response)

    # bad bot slash command
    @app_commands.command(name="shamedev",
                          description="Tell my dev he's doing a bad job")
    async def bad_bot(self, interaction: discord.Interaction) -> None:
        bot_response = (f"Hey <@{CRAYON_USER_ID}>, "
                        f"{interaction.user.display_name} is calling shame "
                        f"upon you. You must've messed something up!")
        await interaction.response.send_message(bot_response)


async def setup(bot: commands.Bot):
    await bot.add_cog(PraiseShameDevCog(bot))
