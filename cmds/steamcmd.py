from discord.ext import commands
from utils.get_steamid_info import get_steamid_info
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import SteamidData, DiscordServer

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
        )

        # Basically, we're telling SQL Alchemy to update the DiscordServer table
        # as well as the SteamidData table
        discord_server = DiscordServer(serverid=ctx.guild.id)
        software.servers.append(discord_server)

        # .merge will add the record if it doesn't exist, and update it if it does
        # This is great here, since we will only need to update the SteamidData table if
        # the Steamid in question doesn't already exist there, but we will always need to
        # update the DiscordServer table
        session.merge(software)
        session.commit()
    await ctx.send(f"Added {steamcmd_results['name']} to tracked Steam packages.")


@steamid.command(
    description="Remove a steamid from tracking in the DiscordServer table for the specific server.",
    brief="Remove a steamid from tracking in DiscordServer for this server."
)
async def remove(ctx, steamid):
    with session_maker() as session:
        discord_server = session.query(DiscordServer).join(SteamidData).filter(
            DiscordServer.steamid == steamid,
        ).first()

        if discord_server:
            session.delete(discord_server)
            session.commit()
            await ctx.send(f"Stopped tracking {steamid} for this server.")
        else: 
            await ctx.send(f"{steamid} was not being tracked for this server.")


@steamid.command(
    description="List tracked steamid's.",
    brief="List tracked steamids."
)
async def list(ctx):
    with session_maker() as session:
        tracked_software = session.query(SteamidData.name, SteamidData.steamid).join(DiscordServer).filter(
            DiscordServer.serverid == ctx.guild.id
        )
        
        if tracked_software:
            # Rather than a deluge of messages, we're going to send just one message
            output = ["Name - SteamID"]
            for package in tracked_software:
                output.append(f"{package.name} - {package.steamid}")

            await ctx.send("\n".join(output))
        else:
            await ctx.send("No Steam packages are currently being tracked for this server.")       


async def setup(bot):
    bot.add_command(steamid)
