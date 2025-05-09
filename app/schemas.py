from pydantic import BaseModel


class MessageRequest(BaseModel):
    """Schema for the request payload."""
    message: str

class MessageResponse(BaseModel):
    """Schema for the response payload."""
    message: str
