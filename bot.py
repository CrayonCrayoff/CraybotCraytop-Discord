# standard library imports
import asyncio
import logging
import os
from pathlib import Path

# third party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv


# load bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# double check presence of bot token
if not TOKEN:
    raise ValueError("Bot token not found in .env")

logging.basicConfig(level=logging.INFO)

# set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

# create bot instance
bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   allowed_mentions=discord.AllowedMentions(everyone=True,
                                                            users=True,
                                                            roles=True))


async def load_cogs():
    print("Loading in cogs...")
    try:
        cog_dir = Path(__file__).parent / "cogs"
        all_cogs = [x.name for x in cog_dir.iterdir() if x.name.endswith(
                    "Cog.py")]
        print("Attempting to load cogs: ", all_cogs)
    except (FileNotFoundError, PermissionError) as e:
        print(e)
        raise
    else:
        failed = False
        for filename in all_cogs:
            extension = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"Loaded {extension}")
            except commands.ExtensionAlreadyLoaded:
                print(f"{extension} is already loaded")
            except commands.NoEntryPointError:
                print(f"{extension} is missing a setup(bot) function")
                failed = True
            except commands.ExtensionFailed as e:
                print(f"Failed to load {extension}: {e.original}")
                failed = True
            except Exception as e:
                print(f"Unexpected error while loading {extension}: {e}")
                failed = True

            if failed:
                raise RuntimeError


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        print(f"Syncing global slash commands...")
        await bot.tree.sync()
        print("Successfully synced slash commands globally")
    except discord.app_commands.CommandSyncFailure as e:
        print(f"General command sync failure: {e}")
    except discord.HTTPException as e:
        print(f"HTTP error during sync: {e}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


async def main():
    try:
        await load_cogs()
    except RuntimeError:
        return
    try:
        await bot.start(TOKEN)
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
