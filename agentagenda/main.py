from datetime import datetime
import json
import os
from easycompletion import (
    openai_text_call,
    openai_function_call,
    compose_function,
    compose_prompt,
)
from agentmemory import (
    create_memory,
    get_memory,
    search_memory,
    get_memories,
    delete_memory,
    update_memory,
)

from agentlogger import log

planning_prompt = """\
{{goal}}
Based on the goal, generate a step-by-step plan for completing the task. Include all detail, including what resources need to be collected, what outputs need to be generated and what the conditions for knowing the task is complete are.
Be very thorough in your plan.
"""

step_creation_prompt = """\
Client's goal
{{goal}}

My plan
{{plan}}

Based on the goal and plan, generate a series of steps.
"""

step_creation_function = compose_function(
    name="create_steps",
    description="Based on the plan, create a list of steps to complete the task.",
    required_properties=["steps"],
    properties={
        "steps": {
            "type": "array",
            "description": "Array of steps to complete the task, based on the plan.",
            "items": {
                "type": "string",
                "description": "The text of the single step.",
            },
        }
    },
)

debug = os.environ.get("DEBUG", False)


def create_task(goal, plan=None, steps=None, model="gpt-3.5-turbo-0613"):
    """Create a task and store it in memory.

    Args:
        goal (str): The goal of the task.
        plan (str, optional): A plan to accomplish the task. Defaults to None.
        steps (list or dict, optional): Steps needed to complete the task. Defaults to None.
        model (str, optional): The OpenAI model to use for AI operations. Defaults to 'gpt-3.5-turbo-0613'.

    Returns:
        None
    """
    if plan is None:
        log("Creating plan for goal: {}".format(goal), log=debug)
        plan = create_plan(goal)
    if steps is None:
        response = openai_function_call(
            text=compose_prompt(step_creation_prompt, {"goal": goal, "plan": plan}),
            functions=[step_creation_function],
            function_call="create_steps",
            debug=debug,
            model=model,
        )

        steps = response["arguments"]["steps"]

    # if steps is a dict, json stringify it
    if isinstance(steps, dict) or isinstance(steps, list):
        steps = json.dumps(steps)

    # get timestamp
    created_at = datetime.timestamp(datetime.now())
    updated_at = datetime.timestamp(datetime.now())

    task = {
        "created_at": created_at,
        "updated_at": updated_at,
        "goal": goal,
        "plan": plan,
        "steps": steps,
        "status": "in_progress",
    }

    return get_task_by_id(create_memory("task", goal, metadata=task))


def list_tasks(status="in_progress"):
    """List all tasks with the given status.

    Args:
        status (str, optional): The status of the tasks to retrieve. Defaults to 'in_progress'.

    Returns:
        list: A list of tasks with the given status.
    """
    debug = os.environ.get("DEBUG", False)
    memories = get_memories(
        "task", filter_metadata={"status": status}, include_embeddings=False
    )
    log("Found {} tasks".format(len(memories)), log=debug)
    return memories


def search_tasks(search_term, status="in_progress"):
    """Search for tasks related to a given search term.

    Args:
        search_term (str): The search term to use.
        status (str, optional): The status of the tasks to retrieve. Defaults to 'in_progress'.

    Returns:
        list: A list of tasks related to the search term.
    """
    memories = search_memory(
        "task",
        search_term,
        filter_metadata={"status": status},
        include_embeddings=False,
        include_distances=False,
    )
    log("Found {} tasks".format(len(memories)), log=debug)
    return memories


def get_task_id(task):
    """Get the ID of a task.

    Args:
        task (dict or int or str): The task to get the ID of.

    Returns:
        str: The ID of the task.
    """
    if isinstance(task, dict):
        return task["id"]
    elif isinstance(task, int):
        return str(task)
    else:
        return task


def delete_task(task):
    """Delete a task.

    Args:
        task (dict or int or str): The task to delete.

    Returns:
        dict: The response from the memory deletion operation.
    """
    log("Deleting task: {}".format(task), log=debug)
    return delete_memory("task", get_task_id(task))


def finish_task(task):
    """Mark a task as complete.

    Args:
        task (dict or int or str): The task to finish.

    Returns:
        dict: The response from the memory update operation.
    """
    log("Finishing task: {}".format(task), log=debug)
    updated_at = datetime.timestamp(datetime.now())

    memory = get_memory("task", get_task_id(task))

    metadata = memory["metadata"]
    metadata["status"] = "complete"
    metadata["updated_at"] = updated_at

    return update_memory(
        "task",
        get_task_id(task),
        metadata=metadata,
    )


def cancel_task(task):
    """Cancel a task.

    Args:
        task (dict or int or str): The task to cancel.

    Returns:
        dict: The response from the memory update operation.
    """
    log("Cancelling task: {}".format(task), log=debug)
    updated_at = datetime.timestamp(datetime.now())

    memory = get_memory("task", get_task_id(task))

    metadata = memory["metadata"]
    metadata["status"] = "cancelled"
    metadata["updated_at"] = updated_at

    return update_memory(
        "task",
        get_task_id(task),
        metadata=metadata,
    )


def get_last_created_task():
    """
    Get the most recently created task.

    Returns
    -------
    dict or None
        The task with the most recent created_at date. If no tasks are found, None is returned.
    """
    tasks = get_memories("task", include_embeddings=False)
    sorted_tasks = sorted(
        tasks, key=lambda x: x["metadata"]["created_at"], reverse=True
    )
    log("Last created task: {}".format(len(sorted_tasks)), log=debug)
    return sorted_tasks[0] if sorted_tasks else None


def get_last_updated_task():
    """
    Get the most recently updated task.

    Returns
    -------
    dict or None
        The task with the most recent updated_at date. If no tasks are found, None is returned.
    """
    tasks = get_memories("task", include_embeddings=False)
    sorted_tasks = sorted(
        tasks, key=lambda x: x["metadata"]["updated_at"], reverse=True
    )
    log("Last updated task: {}".format(len(sorted_tasks)), log=debug)
    return sorted_tasks[0] if sorted_tasks else None


def get_task_by_id(task_id):
    """
    Get a task by its ID.

    Parameters
    ----------
    task_id : str
        The ID of the task to retrieve.

    Returns
    -------
    dict or None
        The task with the given ID. If no task is found, None is returned.
    """
    memory = get_memory("task", task_id)
    log("Task with ID {}: {}".format(task_id, memory), log=debug)
    return memory


def get_current_task():
    """
    Get the current active task.

    Returns
    -------
    dict or None
        The task marked as the current active task. If no current task is found, None is returned.
    """
    memory = get_memories(
        "task", filter_metadata={"current": True}, include_embeddings=False
    )
    if len(memory) > 0:
        log("Current task: {}".format(memory[0]), log=debug)
        return memory[0]
    else:
        log("No current task found", log=debug)
        return None


def set_current_task(task):
    """Set a task as the current task.

    Args:
        task (dict or int or str): The task to be set as current.

    Returns:
        dict: The response from the memory update operation.
    """
    task_id = get_task_id

    memories = get_memories(
        "task", filter_metadata={"current": True}, include_embeddings=False
    )

    for memory in memories:
        metadata = memory["metadata"]
        metadata["current"] = False
        update_memory("task", memory["id"], metadata=metadata)
    log("Setting current task: {}".format(task), log=debug)
    metadata = memory["metadata"]
    metadata["current"] = True
    return update_memory("task", task_id, metadata=metadata)


def create_plan(goal, model="gpt-3.5-turbo-0613"):
    """Create a plan for the goal using OpenAI API.

    Args:
        goal (str): The goal for which to create the plan.
        model (str, optional): The OpenAI model to use for AI operations. Defaults to 'gpt-3.5-turbo-0613'.

    Returns:
        str: The generated plan.
    """
    response = openai_text_call(
        compose_prompt(planning_prompt, {"goal": goal}), debug=debug, model=model
    )
    return response["text"]


def update_plan(task, plan):
    """Update the plan for a task.

    Args:
        task (dict or int or str): The task for which to update the plan.
        plan (str): The new plan.

    Returns:
        None
    """
    task_id = get_task_id(task)
    log("Updating plan for task: {}".format(task), log=debug)
    memory = get_memory("task", task_id)
    metadata = memory["metadata"]
    metadata["plan"] = plan
    metadata["updated_at"] = datetime.timestamp(datetime.now())
    update_memory("task", task_id, metadata=metadata)


def create_steps(goal, plan, model="gpt-3.5-turbo-0613"):
    """Create a series of steps based on the plan and the goal using OpenAI API.

    Args:
        goal (str): The goal for which to create the steps.
        plan (str): The plan based on which to create the steps.
        model (str, optional): The OpenAI model to use for AI operations. Defaults to 'gpt-3.5-turbo-0613'.

    Returns:
        list: The generated steps.
    """
    log("Creating steps for goal: {}".format(goal), log=debug)
    updated_at = datetime.timestamp(datetime.now())
    response = openai_function_call(
        text=compose_prompt(
            step_creation_prompt, {"goal": goal, "plan": plan, "updated_at": updated_at}
        ),
        functions=[step_creation_function],
        function_call="create_steps",
        debug=debug,
        model=model,
    )
    return response["arguments"]["steps"]


def update_step(task, step):
    """
    Update a step in a task.

    Parameters
    ----------
    task : dict
        The task in which the step is to be updated.
    step : dict
        The step which is to be updated.

    Returns
    -------
    dict
        The updated task after updating the step.
    """
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    metadata = task["metadata"]
    metadata["steps"] = json.loads(metadata["steps"])

    for s in metadata["steps"]:
        if s["content"] == step["content"]:
            s["completed"] = step["completed"]

    metadata["steps"] = json.dumps(metadata["steps"])
    metadata["updated_at"] = datetime.timestamp(datetime.now())
    log(
        "Updating step for task: {}\nSteps are: {}".format(task, metadata["steps"]),
        log=debug,
    )
    return update_memory("task", task_id, metadata=metadata)


def add_step(task, step):
    """
    Add a step to a task.

    Parameters
    ----------
    task : dict
        The task to which the step is to be added.
    step : str
        The step which is to be added to the task.

    Returns
    -------
    dict
        The updated task after adding the step.
    """
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    metadata = task["metadata"]
    steps = json.loads(metadata["steps"])
    steps.append({"content": step, "completed": False})
    metadata["steps"] = json.dumps(steps)
    log(
        "Adding step for task: {}\nSteps are: {}".format(task, metadata["steps"]),
        log=debug,
    )
    metadata["updated_at"] = datetime.timestamp(datetime.now())
    return update_memory("task", task_id, metadata=metadata)


def finish_step(task, step):
    """
    Mark a step in a task as completed.

    Parameters
    ----------
    task : dict
        The task containing the step to be marked as completed.
    step : str
        The step which is to be marked as completed.

    Returns
    -------
    dict
        The updated task after marking the step as completed.
    """
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    metadata = task["metadata"]
    steps = json.loads(metadata["steps"])
    for s in steps:
        if s["content"] == step:
            s["completed"] = True
    metadata["steps"] = json.dumps(steps)
    log(
        "Finishing step for task: {}\nSteps are: {}".format(task, metadata["steps"]),
        log=debug,
    )
    metadata["updated_at"] = datetime.timestamp(datetime.now())
    return update_memory("task", task_id, metadata=metadata)


def cancel_step(task, step):
    """
    Remove a step from a task.

    Parameters
    ----------
    task : dict
        The task from which the step is to be removed.
    step : str
        The step which is to be removed from the task.

    Returns
    -------
    dict
        The updated task after removing the step.
    """
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    metadata = task["metadata"]
    steps = metadata["steps"]
    steps = json.loads(steps)
    steps = [s for s in steps if s["content"] != step]
    metadata["steps"] = json.dumps(steps)
    metadata["updated_at"] = datetime.timestamp(datetime.now())
    log(
        "Cancelling step for task: {}\nSteps are: {}".format(task, metadata["steps"]),
        log=debug,
    )
    return update_memory("task", task_id, metadata=metadata)


def get_next_step(task):
    """
    This function will get the task, unpack the string to a dict from the
    "steps" object in task["metadata"], find the first step in the list
    that hasn't been completed and return it
    """

    # First, get the steps from the task metadata
    steps = json.loads(task["metadata"]["steps"])

    # Loop through each step to find the first one that isn't completed
    for step in steps:
        if not step["completed"]:
            # If a step is not completed, return it
            return step

    # If all steps are completed, return None
    return None


def get_task_as_formatted_string(
    task, include_plan=True, include_status=True, include_steps=True
):
    """
    This function will return a string representation of the task,
    including the plan, status and steps based on the arguments provided
    """

    # Define an empty list to store the task details
    task_details = []

    # Append each detail to the list based on the arguments
    if include_plan:
        task_details.append("Plan: {}".format(task["metadata"]["plan"]))

    if include_status:
        task_details.append("Status: {}".format(task["metadata"]["status"]))

    if include_steps:
        # For the steps, since it's a list, we need to format each step separately
        steps = json.loads(task["metadata"]["steps"])
        formatted_steps = ", ".join(
            [
                "{}: {}".format(
                    step["content"],
                    "Completed" if step["completed"] else "Not completed",
                )
                for step in steps
            ]
        )
        task_details.append("Steps: {}".format(formatted_steps))

    # Finally, join all the task details into a single string and return it
    return "\n".join(task_details)


def list_tasks_as_formatted_string():
    """
    Retrieve and format a list of all current tasks.

    Returns:
        str: Formatted string containing details of all current tasks.
    """

    # Get all tasks
    tasks = list_tasks()

    # Define an empty list to store the task details
    task_details = []

    # Loop through each task and append the formatted string to the list
    for task in tasks:
        task_details.append(get_task_as_formatted_string(task))

    # Finally, join all the task details into a single string and return it
    return "\n".join(task_details)
