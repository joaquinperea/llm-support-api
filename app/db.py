import os
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine

database = Database(os.getenv("DATABASE_URL"))
engine = create_async_engine(os.getenv("DATABASE_URL"))
