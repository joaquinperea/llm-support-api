import os
import openai
from dotenv import load_dotenv
from openai import AsyncOpenAI
from app.models import ChatHistory
from app.db import database

# Load environment variables from .env file
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
