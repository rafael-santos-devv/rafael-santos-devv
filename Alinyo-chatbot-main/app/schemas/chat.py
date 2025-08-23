from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    step: int = 0
    session_id: str
class ChatResponse(BaseModel):
    response: str
    login_required: bool = False