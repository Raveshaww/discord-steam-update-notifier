import requests
import settings
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        # Dynamically add all commands found in the cmds directory
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

    bot.run(settings.TOKEN) 

if __name__ == "__main__":
    run()
