import os
import openai
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_gpt(prompt: str) -> str:
    """
    Asynchronously ask a question to the GPT model and return the response.
    """
    # Call the OpenAI API with the provided prompt:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # o "gpt-4"
        messages=[{"role": "user", "content": prompt}]
    )
    # Return the response text from the API response:
    return response.choices[0].message.content
