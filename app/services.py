import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sqlalchemy import select
from app.models import ChatHistory, User
from app.auth import hash_password, verify_password, create_access_token
from app.schemas import UserCreate, UserLogin
from app.db import database

# Load environment variables from .env file
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def register_user(payload: UserCreate):
    # Verifica si existe
    query = select(User).where(User.username == payload.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise ValueError("Username already exists")

    hashed = hash_password(payload.password)
    insert_query = User.__table__.insert().values(username=payload.username, hashed_password=hashed)
    await database.execute(insert_query)
    return {"message": "User created successfully"}

async def authenticate_user(payload: UserLogin):
    query = select(User).where(User.username == payload.username)
    db_user = await database.fetch_one(query)
    if not db_user or not verify_password(payload.password, db_user.hashed_password):
        raise ValueError("Invalid username or password")

    token = create_access_token({"sub": payload.username})
    return {"access_token": token, "token_type": "bearer"}

async def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Asynchronously ask a question to the GPT model and return the response.
    """
    # Call the OpenAI API with the provided prompt:
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    # Store the prompt and response in the database:
    await database.execute(query=ChatHistory.__table__.insert().values(
        prompt=prompt,
        response=response.choices[0].message.content,
        model=model,
    ))
    # Return the response text from the API response:
    return response.choices[0].message.content
