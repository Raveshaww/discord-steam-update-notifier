from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SteamidData(Base):
    __tablename__ = "steamid_data"

    steamid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    buildid = Column(String, nullable=False)
    serverid = Column(String, nullable=False)
