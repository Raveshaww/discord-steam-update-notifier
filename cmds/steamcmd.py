from discord.ext import commands
from utils.get_steamid_info import get_steamid_info
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine
from models.models import SteamidData, DiscordServer, tracking

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
    with session_maker() as session:
        # Checking to see if this server is already tracking the software
        existing_tracking = session.query(SteamidData).\
            filter(SteamidData.steamid == steamid).\
            filter(SteamidData.servers.any(DiscordServer.serverid == ctx.guild.id)).\
            first()
        
        if existing_tracking:
            await ctx.send(f"Already tracking {existing_tracking.name}.")
        else:
            software = session.query(SteamidData).filter_by(steamid=steamid).first()

            if software is None:
                steamcmd_results = get_steamid_info(steamid=steamid)

                software = SteamidData(
                    steamid = steamid,
                    name = steamcmd_results["name"],
                    buildid = steamcmd_results["buildid"],
                )

                session.add(software)
                session.commit()

            # Add to tracking table
            existing_server = session.query(DiscordServer).filter_by(serverid = ctx.guild.id).first()

            # If a tracking channel isn't set, we're just going to use the channel the command was issued from
            if existing_server is None:
                server = DiscordServer(
                    serverid = ctx.guild.id,
                    channelid = ctx.channel.id
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

@steamid.command(
    description="Set notification channel.",
    brief="Set notification channel."
)
async def set_channel(ctx):
    with session_maker() as session:
        existing_channel = session.query(DiscordServer).filter_by(serverid = ctx.guild.id).first()

        
        if existing_channel is None:
            server = DiscordServer(
                serverid = ctx.guild.id,
                channelid = ctx.channel.id
            )

            session.add(server)
            session.commit()
        else:
            existing_channel.channelid = ctx.channel.id
            session.commit()

    await ctx.send(f"Using {ctx.channel.name} for update notifications.")  

async def setup(bot):
    bot.add_command(steamid)
