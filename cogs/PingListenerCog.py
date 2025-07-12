# standard library imports
import os
from pathlib import Path

# third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv


# Load env vars as module constants
SCRIPT_DIR = Path(__file__).parent  # finds this script's folder
PARENT_DIR = SCRIPT_DIR.parent  # goes up once again (to the DiscordBot folder)

load_dotenv(PARENT_DIR / ".env")

GUCCI_SERVER_ID = int(os.getenv("GUCCI_SERVER_ID"))

BIRTHDAY_ROLE_ID = int(os.getenv("BIRTHDAY_ROLE_ID"))
BIRTHDAY_CHANNEL_ID = int(os.getenv("BIRTHDAY_CHANNEL_ID"))
BIRTHDAY_BOT_ID = int(os.getenv("BIRTHDAY_BOT_ID"))

GO_LIVE_CHANNEL_ID = int(os.getenv("GO_LIVE_CHANNEL_ID"))
GUCCI_USER_ID = int(os.getenv("GUCCI_USER_ID"))
STREAM_PING_ID = int(os.getenv("STREAM_PING_ID"))

required_env_vars = {
    "GUCCI_SERVER_ID": GUCCI_SERVER_ID,
    "BIRTHDAY_ROLE_ID": BIRTHDAY_ROLE_ID,
    "BIRTHDAY_CHANNEL_ID": BIRTHDAY_CHANNEL_ID,
    "BIRTHDAY_BOT_ID": BIRTHDAY_BOT_ID,
    "GO_LIVE_CHANNEL_ID": GO_LIVE_CHANNEL_ID,
    "GUCCI_USER_ID": GUCCI_USER_ID,
    "STREAM_PING_ID": STREAM_PING_ID
}

# check if all vars are loaded properly
for key in required_env_vars:
    if not required_env_vars[key]:
        raise ValueError(f"PingListenerCog: Variable {key} did not load.")


ALLOW_ALL = discord.AllowedMentions(everyone=True,
                                    roles=True,
                                    users=True)


class PingListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user:
            print(f"[DEBUG] Ignored - message from self")
            return

        if isinstance(message.channel, discord.DMChannel):
            print(f"[DEBUG] Received a DM from {message.author}:"
                  f" {message.content}")
            response = ("I'm sorry, I'm not programmed to respond to DMs.\n"
                        "Please use my commands in the server.")
            await message.channel.send(response)
            return

        print(f"[DEBUG] Received message in {message.guild} / "
              f"{message.channel.name}")

        if message.guild.id != GUCCI_SERVER_ID:
            print("[DEBUG] Ignored - Message not in Gucci's server")
            return
        else:
            print("[DEBUG] Message in Gucci's server. Checking conditions...")
            if self.should_trigger_birthday_ping(message):
                print("[DEBUG] BirthdayPing trigger conditions met. "
                      "Sending birthday ping.")
                await message.channel.send(f"<@&{BIRTHDAY_ROLE_ID}>",
                                           allowed_mentions=ALLOW_ALL)
                return
            if self.should_trigger_go_live_ping(message):
                print(f"[DEBUG] StreamPing conditions met. "
                      f"Sending stream ping.")
                await message.channel.send(f"<@&{STREAM_PING_ID}>",
                                           allowed_mentions=ALLOW_ALL)
                return
            print("[DEBUG] Ignored - Conditions not met.")

    # check conditions for birthday ping
    @staticmethod
    def should_trigger_birthday_ping(message) -> bool:
        if message.channel.id != BIRTHDAY_CHANNEL_ID:
            return False
        if message.author.id != BIRTHDAY_BOT_ID:
            return False
        return True

    # check conditions for go live ping
    @staticmethod
    def should_trigger_go_live_ping(message) -> bool:
        mentioned_role_ids = [role.id for role in message.role_mentions]
        if message.channel.id != GO_LIVE_CHANNEL_ID:
            return False
        if message.author.id != GUCCI_USER_ID:
            return False
        if STREAM_PING_ID in mentioned_role_ids:
            return False
        return True


async def setup(bot):
    await bot.add_cog(PingListenerCog(bot))
