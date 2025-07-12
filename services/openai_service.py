import json
from typing import List

from config.openai_client import openai_client
from config.settings import settings
from tools import tools

from .tasks_service import TasksService

service = TasksService(userid="default_user")


responses = []


def genereate_response(
    message: str | List[str], previous_response_id: str | None = None, loop: int = 1
) -> dict:
    """Generate a response using OpenAI's API with function calling capabilities."""
    print(f"{loop} - Generating response for message")
    if loop == 1:
        input_messages = [
            {
                "role": "user",
                "content": message,
            }
        ]
    else:
        input_messages = message or []

    response = openai_client.responses.create(
        model=settings.TOOL_CALL_MODEL,
        input=input_messages,
        tools=tools,
    )

    function_call = False
    if loop < 5:
        for output in response.output:
            if output.type == "function_call":
                function_call = True
                input_messages.append(output)
                function_name = output.name
                args = json.loads(output.arguments)

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

                input_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": str(result),
                    }
                )

    if function_call:
        loop += 1
        function_call = False

        return genereate_response(input_messages, loop=loop)

    return (
        response.output_text
        if response.output_text
        else response.output[0].content[0].text
    )
