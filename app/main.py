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
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

        await bot.tree.sync()

    bot.run(settings.TOKEN)


if __name__ == "__main__":
    run()
