"""
This is database connection module
For some reason credentials for connection are stored in public
"""

from .imports import sessionmaker, declarative_base, URL, create_engine

# import os
# from .imports import load_dotenv, AsyncSession, create_async_engine, DeclarativeBase
# load_dotenv()

connection_string = URL.create(
    drivername='postgresql',
    username="lethalmaks",
    password="xrpAqm06UadH",
    host="ep-sparkling-fog-87757951.eu-central-1.aws.neon.tech",
    database="client"
)

engine = create_engine(connection_string)

PGHOST = 'ep-sparkling-fog-87757951.eu-central-1.aws.neon.tech'
PGDATABASE = 'client'
PGUSER = 'lethalmaks'
PGPASSWORD = 'xrpAqm06UadH'

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# drivername = os.getenv("DRIVERNAME")
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")
# host = os.getenv("HOST")
# database = os.getenv("DATABASE")

# DATABASE_URL = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}'
# engine = create_async_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# class Base(DeclarativeBase):
#     pass
