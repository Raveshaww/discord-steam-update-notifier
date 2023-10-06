from discord.ext import commands
from utils.get_steamid_info import get_steamid_info
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import SteamidData

session_maker = sessionmaker(bind=create_engine('sqlite:///models.db'))

@commands.group()
async def steamid(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"{ctx.subcommand_passed} is not valid.")


@steamid.command(
    description="Add a steamid to track for updates.",
    brief="Add a steamid to track."
)
async def add(ctx, steamid):
    steamcmd_results = get_steamid_info(steamid=steamid)

    with session_maker() as session:
        software = SteamidData(
            steamid = steamid,
            name = steamcmd_results["name"],
            buildid = steamcmd_results["buildid"],
            serverid = ctx.guild.id
        )
        session.add(software)
        session.commit()
    await ctx.send(f"Added {steamcmd_results['name']} to tracked Steam packages.")


@steamid.command(
    description="Remove a steamid to track for updates.",
    brief="Remove a steamid from tracking."
)
async def remove(ctx, steamid):
    with session_maker() as session:
        tracked_software = session.query(SteamidData).filter_by(steamid = steamid)
        session.delete(tracked_software)
        session.commit
    await ctx.send(f"Removed {steamid} from tracked Steam packages.")

async def setup(bot):
    bot.add_command(steamid)


@steamid.command(
    description="List tracked steamid's.",
    brief="List tracked steamids."
)
async def list(ctx):
    with session_maker() as session:
        tracked_software = session.query(SteamidData).filter_by(serverid = ctx.guild.id)
        
        # Rather than a deluge of messages, we're going to send just one message
        output = []
        for package in tracked_software:
            output.append(package.name)

        await ctx.send("\n".join(output))       


async def setup(bot):
    bot.add_command(steamid)
