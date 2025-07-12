# standard library imports
from datetime import datetime

# third party imports
import discord
import pytz
from discord import app_commands
from discord.ext import commands


class TimestampGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def timezone_autocomplete(self, interaction: discord.Interaction,
                                    current: str
                                    ) -> list[app_commands.Choice[str]]:
        current_lower = current.lower()
        matches = [tz for tz in pytz.all_timezones if current_lower in
                   tz.lower()][:25]
        return [app_commands.Choice(name=tz, value=tz) for tz in matches]

    async def format_autocomplete(self,
                                  interaction: discord.Interaction,
                                  current: str
                                  ) -> list[app_commands.Choice[str]]:
        # map descriptive options to the appropriate timestamp character
        options = {
            "DD/MM/YYYY (e.g. 15/07/2025)": "d",
            "DD Month YYYY (e.g. 15 July 2025)": "D",
            "HH:MM (e.g. 10:20)": "t",
            "HH:MM:SS (e.g. 10:20:15)": "T",
            "DD Month YYYY HH:MM (e.g. 15 July 2025 10:20)": "f",
            "Day, DD Month YYYY HH:MM (e.g. Tuesday, 15 July 2025, 10:20)": "F",
            "In <x> <time unit> (e.g. In 2 hours)": "R",
        }
        return [app_commands.Choice(name=key, value=val) for key, val in
                options.items()]

    @app_commands.command(name="timestamp",
                          description="Generate a dynamic timestamp")
    @app_commands.describe(date="Date in YYYY-MM-DD format",
                           time="Time in HH:MM format (24-hour)",
                           timezone="Your timezone (e.g. America/New_York)",
                           stamp_format="The timestamp format you want")
    @app_commands.autocomplete(timezone=timezone_autocomplete,
                               stamp_format=format_autocomplete)
    async def generate_timestamp(self,
                                 interaction: discord.Interaction,
                                 date: str,
                                 time: str,
                                 timezone: str,
                                 stamp_format: str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            error_message = ("Invalid date format.\n"
                             "Please use `YYYY-MM-DD`, e.g. `2025-07-15`.")
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )
            return

        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            error_message = ("Invalid time format.\n"
                             "Please use `HH:MM`, e.g. `13:45`.")
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )
            return

        if timezone not in pytz.all_timezones:
            error_message = (f"Invalid timezone: {timezone}. \n"
                             f"Go to https://zones.arilyn.cc/ to find your "
                             f"timezone.")
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )
            return

        valid_timestamp_formats = {"d", "D", "t", "T", "f", "F", "R"}
        if stamp_format not in valid_timestamp_formats:
            error_message = ("Invalid timestamp.\n"
                             "Please choose from the list provided.")
            await interaction.response.send_message(
                error_message,
                ephemeral=True
            )
            return

        date_str = f"{date} {time}"
        naive_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")

        timezone = pytz.timezone(timezone)
        local_datetime = timezone.localize(naive_date)

        unix_timestamp = int(local_datetime.timestamp())

        output = (f"Your timestamp is `<t:{unix_timestamp}:{stamp_format}>`\n"
                  f"It will show up as <t:{unix_timestamp}:{stamp_format}>")
        await interaction.response.send_message(
            output,
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(TimestampGenerator(bot))
