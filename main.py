import settings
import discord
import os
from discord.ext import commands


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        # Load all commands from cmds directory
        #for filename in os.listdir("./cmds"):
        #    if filename.endswith(".py"):
        #        await bot.load_extension(f"cmds.{filename[:-3]}")

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run(settings.TOKEN)


if __name__ == "__main__":
    run()
