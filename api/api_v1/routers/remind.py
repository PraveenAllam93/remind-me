from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.openai_service import genereate_response

router = APIRouter(
    prefix="/remind",
    tags=["remind"],
)


class MessageInput(BaseModel):
    message: str


@router.post("/task")
def tasks(request: MessageInput):
    """
    Endpoint to handle task creation requests.
    """
    try:
        result = genereate_response(request.message)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
