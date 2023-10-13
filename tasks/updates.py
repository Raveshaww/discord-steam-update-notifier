from discord.ext import tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models.models import SteamidData, DiscordServer, tracking
from settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from utils.get_steamid_info import mass_get_steamid_info

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine, class_= AsyncSession)

@tasks.loop(seconds=60)
async def background_task():
    async with session_maker() as session:
        tracked_software = await session.execute(select(SteamidData))
        tracked_software = tracked_software.scalars().all()

        steamids = []
        existing_data = {}
        fresh_data = {}
        updated_software = {}
        
        
        for package in tracked_software:
            print(f"{package.name} has buildid: {package.buildid}")
            existing_data[package.steamid] = package.buildid
            steamids.append(package.steamid)

        steamid_data = await mass_get_steamid_info(steamids = steamids)

        print()

        for steamid in steamid_data:
            print(f"{steamid['name']} is on buildid {steamid['buildid']}")
            fresh_data[steamid["steamid"]] = steamid["buildid"]

        if existing_data == fresh_data:
            print("These are the same")
            return
        
        print("These are not the same")

        for key in existing_data:
            if existing_data[key] != fresh_data[key]:
                updated_software[key] = fresh_data[key]
        print(updated_software)
 
    # get list of servers to notify
    # create notify table
    # add notfiy list to table


async def setup(bot):
    await background_task.start()