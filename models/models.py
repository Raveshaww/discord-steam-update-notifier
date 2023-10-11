from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

tracking = Table(
    "tracking",
    Base.metadata,
    Column("steamid", ForeignKey("steamid_data.id")),
    Column("serverid", ForeignKey("discord_server.id"))
)

class SteamidData(Base):
    __tablename__ = "steamid_data"

    id = Column(Integer,primary_key=True, autoincrement=True)
    steamid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    buildid = Column(String, nullable=False)

    servers = relationship(
        "DiscordServer", 
        secondary = tracking,
        back_populates = "steamids" # This needs to be the name of the "column" in the other table
    )


class DiscordServer(Base):
    __tablename__ = "discord_server"

    id = Column(Integer,primary_key=True, autoincrement=True)
    serverid = Column(String, nullable=False)
    channelid = Column(String, nullable=False)

    steamids = relationship(
        "SteamidData",
        secondary = tracking,
        back_populates="servers"
    )
