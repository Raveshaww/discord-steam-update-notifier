from discord.ext import commands
from utils.get_steamid_info import get_steamid_info
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models.models import SteamidData, DiscordServer, tracking
from settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine)

#session_maker = sessionmaker(bind=create_engine(DB_URL))


@commands.group()
async def steamid(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"{ctx.subcommand_passed} is not valid.")


@steamid.command(
    description="Add a steamid to track for updates.",
    brief="Add a steamid to track."
)
async def add(ctx, steamid: str):
    with session_maker() as session:
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)

        # Checking to see if this server is already tracking the software
        existing_tracking = session.query(SteamidData).\
            filter(SteamidData.steamid == steamid).\
            filter(SteamidData.servers.any(DiscordServer.serverid == serverid)).\
            first()
        
        if existing_tracking:
            await ctx.send(f"Already tracking {existing_tracking.name}.")
            return
        
        software = session.query(SteamidData).filter_by(steamid=steamid).first()

        if software is None:
            steamcmd_results = await get_steamid_info(steamid=steamid)
            
            if steamcmd_results is None:
                await ctx.send("Invalid input.")
                return
            
            software = SteamidData(
                steamid = steamid,
                name = steamcmd_results["name"],
                buildid = steamcmd_results["buildid"],
            )

            session.add(software)
            session.commit()

        # Add to tracking table
        existing_server = session.query(DiscordServer).filter_by(serverid = serverid).first()

        # If a tracking channel isn't set, we're just going to use the channel the command was issued from
        if existing_server is None:
            server = DiscordServer(
                serverid = serverid,
                channelid = channelid
            )

            session.add(server)
            # We need the DiscordServer record  to exist before tracking the software, so we'll create it
            session.commit()

            software.servers.append(server)
            session.commit()

            await ctx.send(f"Added {software.name} to tracked Steam packages.")
            await ctx.send(f"Using {ctx.channel.name} as the notification channel. Run 'set_channel' in the desired channel to change this.")
        else: 
            software.servers.append(existing_server)
            session.commit()
            await ctx.send(f"Added {software.name} to tracked Steam packages.")


@steamid.command(
    description="Remove a steamid from tracking in the DiscordServer table for the specific server.",
    brief="Remove a steamid from tracking in DiscordServer for this server."
)
async def remove(ctx, steamid: str):
    with session_maker() as session:
        serverid = str(ctx.guild.id)

        steamid_data = session.query(SteamidData).filter_by(steamid = steamid).first()

        if steamid_data is None:
            steamcmd_results = await get_steamid_info(steamid=steamid)
            
            if steamcmd_results is None:
                await ctx.send("Invalid input.")
                return
            
            await ctx.send(f"{steamcmd_results['name']} was not being tracked for this server.")
            return

        discord_server = session.query(DiscordServer).filter_by(serverid = serverid).first()
    
        remove_tracking = tracking.delete().where(
            (tracking.c.steamid == steamid_data.id) &
            (tracking.c.serverid == discord_server.id)
        )

        deleted_count = session.execute(remove_tracking).rowcount

        session.commit()
        
        if deleted_count > 0:
            await ctx.send(f"Stopped tracking {steamid_data.name} for this server.")
        else: 
            await ctx.send(f"{steamid_data.name} was not being tracked for this server.")


@steamid.command(
    description="List tracked steamid's.",
    brief="List tracked steamids."
)
async def list(ctx):
    with session_maker() as session:
        serverid = str(ctx.guild.id)

        tracked_software = session.query(SteamidData).\
            filter(SteamidData.servers.any(DiscordServer.serverid == serverid)).\
            all()
        
        if tracked_software:
            # Rather than a deluge of messages, we're going to send just one message
            output = ["Name - SteamID"]
            for package in tracked_software:
                output.append(f"{package.name} - {package.steamid}")

            await ctx.send("\n".join(output))
        else:
            await ctx.send("No Steam packages are currently being tracked for this server.")       


@steamid.command(
    description="Set notification channel.",
    brief="Set notification channel."
)
async def set_channel(ctx):
    async with session_maker() as session:
        serverid = str(ctx.guild.id)
        channelid = str(ctx.channel.id)
        
        existing_channel = await session.execute(select(DiscordServer).filter_by(serverid = serverid))
        #existing_channel = session.query(DiscordServer).filter_by(serverid = serverid).first()
        
        if existing_channel.first() is None:
            server = DiscordServer(
                serverid = serverid,
                channelid = channelid
            )

            session.add(server)
            await session.commit()
        else:
            existing_channel.channelid = channelid
            await session.commit()

    await ctx.send(f"Using {ctx.channel.name} for update notifications.")  

async def setup(bot):
    bot.add_command(steamid)
