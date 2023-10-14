from discord.ext import tasks, commands
from sqlalchemy import select
from models.models import SteamidData, DiscordServer, tracking
from settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from utils.get_steamid_info import mass_get_steamid_info

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine, class_=AsyncSession)


class UpdateCog(commands.Cog):
    '''Background task that checks for updates for all packages noted in SteamidData. 
        In the event that a package has been updated, it will then send a message to each server
        that is currently tracking that package.'''
    def __init__(self, bot):
        self.bot = bot
        self.check_buildid.start()

    def cog_unload(self):
        self.check_buildid.cancel()

    @tasks.loop(minutes=60)
    async def check_buildid(self):
        async with session_maker() as session:
            steamids = []
            existing_data = {}
            fresh_data = {}
            updated_software = {}

            # First we need to know what steamid's we need to look up
            tracked_software = await session.execute(select(SteamidData))
            tracked_software = tracked_software.scalars().all()

            # We'll need a list for the http requests, and a dict for later
            for package in tracked_software:
                existing_data[package.steamid] = package.buildid
                steamids.append(package.steamid)

            # Now that we know, we're going to get the current buildids for all steamids we are tracking
            steamid_data = await mass_get_steamid_info(steamids=steamids)

            for steamid in steamid_data:
                fresh_data[steamid["steamid"]] = steamid["buildid"]

            # There's no real point in moving forward if literally everything is the same
            if existing_data == fresh_data:
                return

            # Now we are creating a new dict with just the updated software included
            for key in existing_data:
                if existing_data[key] != fresh_data[key]:
                    updated_software[key] = fresh_data[key]

            # Now let's get the list of all tracked
            to_notify = await session.execute(
                select(tracking.c, SteamidData, DiscordServer)
                .join(SteamidData, tracking.c.steamid == SteamidData.id)
                .join(DiscordServer, tracking.c.serverid == DiscordServer.id)
                .filter(SteamidData.steamid.in_(updated_software.keys()))
            )
            to_notify = to_notify.all()

            for server in to_notify:
                # While we have to unpack the entire tuple, we don't actually care about the first two bits
                tracking_steamid, tracking_serverid, steamid_data, discord_server = server
                channel = self.bot.get_channel(int(discord_server.channelid))
                await channel.send(f"{steamid_data.name} has updated.")

            # Now that the relevant servers have been notified, we need to make sure our records are up to date
            steamids_to_update = await session.execute(
                select(SteamidData)
                .where(SteamidData.steamid.in_(updated_software.keys()))
            )
            steamids_to_update = steamids_to_update.scalars().all()

            for steamid in steamids_to_update:
                package = steamid.steamid
                new_buildid = updated_software[package]
                steamid.buildid = new_buildid

            await session.commit()


async def setup(bot):
    await bot.add_cog(UpdateCog(bot))
