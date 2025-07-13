from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config.settings import settings
from exceptions import RedisServiceException, TaskServiceException
from services.openai_service import genereate_response
from services.redis_service import get_redis_hash_values

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

    previous_response_ids = get_redis_hash_values(
        f"{settings.REDIS_RESPONSES_ID_KEY}",
        settings.DEFAULT_USER_ID,
    )
    previous_response_id = previous_response_ids[-1] if previous_response_ids else None

    try:
        result = genereate_response(request.message, previous_response_id, loop=1)
        return {"result": result}
    except (TaskServiceException, RedisServiceException) as e:
        raise HTTPException(status_code=500, detail=e.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
