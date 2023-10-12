from discord.ext import tasks
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models.models import SteamidData, DiscordServer, tracking
from settings import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(engine)

@tasks.loop(seconds=60)
async def background_task():
    async with session_maker() as session:
        tracked_software = await session.execute(select(SteamidData))
    print(tracked_software.scalars().all())

async def setup(bot):
    await background_task.start()