import json
from datetime import datetime, timezone
from typing import List

from config.openai_config import openai_client
from config.settings import settings
from exceptions import TaskServiceException
from services.redis_service import push_redis_value
from tools import tools

from .tasks_service import TasksService

service = TasksService(userid=settings.DEFAULT_USER_ID)


responses = []


def genereate_response(
    message: str | List[str], previous_response_id: str | None = None, loop: int = 1
) -> dict:
    """Generate a response using OpenAI's API with function calling capabilities."""
    print(f"{loop} - Generating response for message")

    if loop == 1:
        utc_now = datetime.now(timezone.utc)
        input_messages = [
            {
                "role": "user",
                "content": f"{message}\n\nUTC time now: {utc_now}",
            }
        ]
    else:
        input_messages = message or []

    if not previous_response_id:
        response = openai_client.responses.create(
            model=settings.TOOL_CALL_MODEL,
            input=input_messages,
            tools=tools,
        )
    else:
        response = openai_client.responses.create(
            model=settings.TOOL_CALL_MODEL,
            input=input_messages,
            tools=tools,
            previous_response_id=previous_response_id,
        )

    response_id = response.id
    push_redis_value(
        settings.REDIS_RESPONSES_ID_KEY, settings.DEFAULT_USER_ID, response_id
    )

    try:
        tools_responses = []
        if loop < 5:
            for output in response.output:
                if output.type == "function_call":
                    function_name = output.name
                    args = json.loads(output.arguments)
                    print(f"{args=}")
                    if function_name == "create_task":
                        result = service.create_task(**args)

                    elif function_name == "delete_task":
                        result = service.delete_task(**args)

                    elif function_name == "get_task":
                        result = service.get_task(**args)

                    elif function_name == "update_task":
                        result = service.update_task(**args)

                    elif function_name == "list_tasks":
                        result = service.list_tasks(**args)

                    tools_responses.append(
                        {
                            "type": "function_call_output",
                            "call_id": output.call_id,
                            "output": str(result),
                        }
                    )
        else:
            for output in response.output:
                if output.type == "function_call":
                    tools_responses.append(
                        {
                            "type": "function_call_output",
                            "call_id": output.call_id,
                            "output": "Maximum looping reached, can't proceed further..try sending another request/ message",
                        }
                    )
    except Exception as e:
        raise TaskServiceException(
            message="Error while calling functions", original_exception=e
        )

    if tools_responses:
        loop += 1
        return genereate_response(tools_responses, response_id, loop=loop)

    return (
        response.output_text
        if response.output_text
        else response.output[0].content[0].text
    )
