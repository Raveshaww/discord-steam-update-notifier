import settings
import discord
from discord.ext import commands, tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import SteamidData, DiscordServer
from utils import get_steamid_info

session_maker = sessionmaker(bind=create_engine('sqlite:///models.db'))


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        # Load all commands from cmds/steamcmd.py
        await bot.load_extension("cmds.steamcmd")
        
        await  background_task.start()

    @tasks.loop(seconds=60)
    async def background_task():
        print("Hi")

    bot.run(settings.TOKEN) 

if __name__ == "__main__":
    run()
