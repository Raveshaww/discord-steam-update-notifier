import requests
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Valheim dedicated server steamid is 896660
class SteamidInfo:
    def __init__(self, steamid):
        url = f"https://api.steamcmd.net/v1/info/{steamid}"

        response = requests.get(
            url,
            headers={"Accept":"application/json"}
        )

        self.name = response.json()["data"][steamid]["common"]["name"]
        self.steamid = steamid
        self.buildid = response.json()["data"][steamid]["depots"]["branches"]["public"]["buildid"]


def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command(
        description="Add a steamid to track for updates.",
        brief="Add a steamid to track."
    )
    # CTX is context
    async def add_steamid(ctx, steamid):
        game = SteamidInfo(steamid=steamid)
        await ctx.send(f"Added `{game.name}` to tracked Steam packages. Current Build ID is `{game.buildid}`.")

        
    bot.run(TOKEN) 

if __name__ == "__main__":
    run()
