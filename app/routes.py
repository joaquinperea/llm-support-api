import logging
from fastapi import APIRouter, HTTPException, Depends
from app.schemas import MessageRequest, MessageResponse, UserCreate, UserLogin, Token
from app.services import register_user, authenticate_user, ask_gpt
from app.auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register")
async def register(payload: UserCreate):
    try:
        return await register_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    try:
        return await authenticate_user(payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/ask", response_model=MessageResponse)
async def ask_endpoint(payload: MessageRequest, username: str = Depends(get_current_user)):
    """
    Endpoint to ask a question to the GPT model.
    """
    try:
        logger.info(f"User {username} asked: {payload.message}")
        # Generate a response using the ask_gpt function
        reply = await ask_gpt(payload.message, model=payload.model)
        logger.info(f"Generated response: {reply}")
        return MessageResponse(message=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
