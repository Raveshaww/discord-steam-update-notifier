from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()

tracking = Table(
    "tracking",
    Base.metadata,
    Column("steamid", ForeignKey("steamid_data.id")),
    Column("serverid", ForeignKey("discord_server.id"))
)


class SteamidData(Base):
    __tablename__ = "steamid_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    steamid: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    buildid: Mapped[str] = mapped_column(nullable=False)

    servers = relationship(
        "DiscordServer",
        secondary=tracking,
        # This needs to be the name of the "column" in the other table
        back_populates="steamids"
    )


class DiscordServer(Base):
    __tablename__ = "discord_server"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    serverid: Mapped[str] = mapped_column(unique=True, nullable=False)
    channelid: Mapped[str] = mapped_column(unique=True, nullable=False)

    steamids = relationship(
        "SteamidData",
        secondary=tracking,
        back_populates="servers"
    )
