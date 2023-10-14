from discord.ext import commands
from utils.get_steamid_info import get_steamid_info
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from models.models import SteamidData, DiscordServer, tracking
from settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Steamid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def steamid(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.subcommand_passed} is not valid.")

    @steamid.command(
        description="Add a steamid to track for updates.",
        brief="Add a steamid to track."
    )
    async def add(self, ctx, steamid: str):
        async with session_maker() as session:
            serverid = str(ctx.guild.id)
            channelid = str(ctx.channel.id)

            # Checking to see if this server is already tracking the software
            existing_tracking = await session.execute(
                select(SteamidData)
                .filter(SteamidData.steamid == steamid)
                .filter(SteamidData.servers.any(DiscordServer.serverid == serverid))
                .options(selectinload(SteamidData.servers))
            )
            existing_tracking = existing_tracking.scalars().first()

            if existing_tracking:
                await ctx.send(f"Already tracking {existing_tracking.name}.")
                return

            # Checking to see if the steamid is already in the database
            software = await session.execute(
                select(SteamidData).filter_by(steamid=steamid)
                .options(selectinload(SteamidData.servers))
            )
            software = software.scalar()

            if software is None:
                steamcmd_results = await get_steamid_info(steamid=steamid)

                if steamcmd_results is None:
                    await ctx.send("Invalid input.")
                    return

                software = SteamidData(
                    steamid=steamid,
                    name=steamcmd_results["name"],
                    buildid=steamcmd_results["buildid"],
                )

                session.add(software)
                await session.commit()

                # We now have to re-query software, since the above commit closes the query
                software = await session.execute(
                    select(SteamidData).filter_by(steamid=steamid)
                    .options(selectinload(SteamidData.servers))
                )
                software = software.scalar()

            # Checking to make sure that this server is already noted within the database
            existing_server = await session.execute(
                select(DiscordServer).filter_by(serverid=serverid)
            )

            existing_server = existing_server.scalar()

            # If a tracking channel isn't set, we're just going to use the channel the command was issued from
            if existing_server is None:
                server = DiscordServer(
                    serverid=serverid,
                    channelid=channelid
                )

                session.add(server)
                software.servers.append(server)
                software_name = software.name
                await session.commit()

                await ctx.send(f"Added {software_name} to tracked Steam packages.")
                await ctx.send(f"Using {ctx.channel.name} as the notification channel. Run 'set_channel' in the desired channel to change this.")
            else:
                software.servers.append(existing_server)
                software_name = software.name
                await session.commit()
                await ctx.send(f"Added {software_name} to tracked Steam packages.")

    @steamid.command(
        description="Remove a steamid from tracking in the DiscordServer table for the specific server.",
        brief="Remove a steamid from tracking in DiscordServer for this server."
    )
    async def remove(self, ctx, steamid: str):
        async with session_maker() as session:
            serverid = str(ctx.guild.id)

            steamid_data = await session.execute(select(SteamidData).filter_by(steamid=steamid))
            steamid_data = steamid_data.scalar()
            steamid_name = steamid_data.name

            if steamid_data is None:
                steamcmd_results = await get_steamid_info(steamid=steamid)

                if steamcmd_results is None:
                    await ctx.send("Invalid input.")
                    return

                await ctx.send(f"{steamcmd_results['name']} was not being tracked for this server.")
                return

            discord_server = await session.execute(select(DiscordServer).filter_by(serverid=serverid))
            discord_server = discord_server.scalar()

            remove_tracking = await session.execute(delete(tracking).where(
                (tracking.c.steamid == steamid_data.id) &
                (tracking.c.serverid == discord_server.id)
            ))
            deleted_count = remove_tracking.rowcount

            await session.commit()

            if deleted_count > 0:
                await ctx.send(f"Stopped tracking {steamid_name} for this server.")
            else:
                await ctx.send(f"{steamid_name} was not being tracked for this server.")

    @steamid.command(
        description="List tracked steamid's.",
        brief="List tracked steamids."
    )
    async def list(self, ctx):
        async with session_maker() as session:
            serverid = str(ctx.guild.id)

            tracked_software = await session.execute(
                select(SteamidData).filter(
                    SteamidData.servers.any(DiscordServer.serverid == serverid)
                )
            )
            tracked_software = tracked_software.scalars().all()

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
    async def set_channel(self, ctx):
        async with session_maker() as session:
            serverid = str(ctx.guild.id)
            channelid = str(ctx.channel.id)

            existing_channel = await session.execute(select(DiscordServer).filter_by(serverid=serverid))

            if existing_channel.first() is None:
                server = DiscordServer(
                    serverid=serverid,
                    channelid=channelid
                )

                session.add(server)
                await session.commit()
            else:
                existing_channel.channelid = channelid
                await session.commit()

        await ctx.send(f"Using {ctx.channel.name} for update notifications.")


async def setup(bot):
    await bot.add_cog(Steamid(bot))
