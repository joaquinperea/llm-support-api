from fastapi import APIRouter, HTTPException
from app.schemas import MessageRequest, MessageResponse
from app.services import ask_gpt

router = APIRouter()

@router.post("/ask", response_model=MessageResponse)
async def ask_endpoint(payload: MessageRequest):
    """
    Endpoint to ask a question to the GPT model.
    """
    try:
        # Generate a response using the ask_gpt function
        reply = await ask_gpt(payload.message)
        return MessageResponse(message=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
