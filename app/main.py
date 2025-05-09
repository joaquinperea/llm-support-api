from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.db import database
from app.routes import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="LLM Support API",
    version="0.1.0",
    lifespan=lifespan,
    )

app.include_router(api_router)
