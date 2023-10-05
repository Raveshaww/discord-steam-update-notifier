from discord.ext import commands
import requests

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

@commands.group()
async def steamid(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"{ctx.subcommand_passed} is not valid.")

@steamid.command(
    description="Add a steamid to track for updates.",
    brief="Add a steamid to track."
)
async def add(ctx, steamid):
    game = SteamidInfo(steamid=steamid)
    await ctx.send(f"Added `{game.name}` to tracked Steam packages. Current Build ID is `{game.buildid}`.")

async def setup(bot):
    bot.add_command(steamid)