create_task_tools = {
    "type": "function",
    "name": "create_task",
    "description": "Creates multiple tasks by adding each task from task_data if its task_id does not already exist. Returns false immediately if a duplicate is found; otherwise returns true after adding all tasks.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "task_data": {
                "type": "array",
                "description": "List of task objects to be created.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the task.",
                        },
                        "priority": {
                            "type": ["string", "null"],
                            "enum": ["low", "medium", "high"],
                            "description": "Optional priority level of the task defaulting to low.",
                        },
                        "deadline": {
                            "type": ["string", "null"],
                            "description": "Optional deadline for the task defaulting to null.",
                        },
                    },
                    "required": ["name", "priority", "deadline"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["task_data"],
        "additionalProperties": False,
    },
}

delete_task_tools = {
    "type": "function",
    "name": "delete_task",
    "description": "Deletes a task by its ID. Returns false if the task does not exist; otherwise returns true after deletion.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to be deleted.",
            }
        },
        "required": ["task_id"],
        "additionalProperties": False,
    },
}

get_task_tools = {
    "type": "function",
    "name": "get_task",
    "description": "Retrieves a task by its ID. Returns the task object if found; otherwise returns null.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to be retrieved.",
            }
        },
        "required": ["task_id"],
        "additionalProperties": False,
    },
}

update_task_tools = {
    "type": "function",
    "name": "update_task",
    "description": "Updates an existing task by its ID. Returns false if the task does not exist; otherwise returns true after updating the task.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "The ID of the task to be updated.",
            },
            "task_data": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the task.",
                    },
                    "priority": {
                        "type": ["string", "null"],
                        "enum": ["low", "medium", "high"],
                        "description": "Optional priority level of the task defaulting to low.",
                    },
                    "deadline": {
                        "type": ["string", "null"],
                        "description": "Optional deadline for the task defaulting to null.",
                    },
                },
                "required": ["name", "priority", "deadline"],
                "additionalProperties": False,
            },
        },
        "required": ["task_id", "task_data"],
        "additionalProperties": False,
    },
}

list_tasks_tools = {
    "type": "function",
    "name": "list_tasks",
    "description": "Lists all tasks, optionally filtered by priority. Returns a list of task objects.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "all"],
                "description": "Optional priority level to filter tasks by. If null or not provided, all tasks are returned.",
            }
        },
        "required": ["priority"],
        "additionalProperties": False,
    },
}

tools = [
    create_task_tools,
    delete_task_tools,
    get_task_tools,
    update_task_tools,
    list_tasks_tools,
]
