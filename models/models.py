from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SteamidData(Base):
    __tablename__ = "steamid_data"

    steamid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    buildid = Column(String, nullable=False)

    servers = relationship("DiscordServer")

class DiscordServer(Base):
    __tablename__ = "discord_server"

    id = Column(Integer,primary_key=True, autoincrement=True)
    serverid = Column(String, nullable=False)
    steamid = Column(String, ForeignKey("steamid_data.steamid"))
