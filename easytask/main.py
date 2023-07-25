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


def create_task(goal, plan=None, steps=None):
    if plan is None:
        log("Creating plan for goal: {}".format(goal), log=debug)
        plan = create_plan(goal)
    if steps is None:
        response = openai_function_call(
            text=compose_prompt(step_creation_prompt, {"goal": goal, "plan": plan}),
            functions=[step_creation_function],
            function_call="create_steps",
            debug=debug,
        )

        steps = response["arguments"]["steps"]

    # if steps is a dict, json stringify it
    if isinstance(steps, dict) or isinstance(steps, list):
        steps = json.dumps(steps)

    # get timestamp
    created_at = datetime.now()
    updated_at = datetime.now()

    task = {
        "created_at": created_at,
        "updated_at": updated_at,
        "goal": goal,
        "plan": plan,
        "steps": steps,
        "status": "in progress",
    }

    create_memory("task", goal, metadata=task)

    return


def list_tasks():
    debug = os.environ.get("DEBUG", False)
    memories = get_memories("task", filter_metadata={"status": "in progress"})
    log("Found {} tasks".format(len(memories)), log=debug)
    return memories


def search_tasks(search_term):
    # return tasks whose goal is most relevant to the search term
    memories = search_memory("task", search_term)
    log("Found {} tasks".format(len(memories)), log=debug)
    return memories


def get_task_id(task):
    if isinstance(task, dict):
        return task["id"]
    elif isinstance(task, int):
        return str(task)
    else:
        return task


def delete_task(task):
    log("Deleting task: {}".format(task), log=debug)
    return delete_memory("task", get_task_id(task))


def finish_task(task):
    log("Finishing task: {}".format(task), log=debug)
    return update_memory("task", get_task_id(task), metadata={"status": "complete"})


def cancel_task(task):
    log("Cancelling task: {}".format(task), log=debug)
    return update_memory("task", get_task_id(task), metadata={"status": "cancelled"})


# Get Last Created Task
def get_last_created_task():
    # return the task with the most recent created_at date
    tasks = get_memories("task")
    sorted_tasks = sorted(
        tasks, key=lambda x: x["metadata"]["created_at"], reverse=True
    )
    log("Last created task: {}".format(len(sorted_tasks)), log=debug)
    return sorted_tasks[0] if sorted_tasks else None


# Get Last Updated Task
def get_last_updated_task():
    # return the task with the most recent updated_at date
    tasks = get_memories("task")
    sorted_tasks = sorted(
        tasks, key=lambda x: x["metadata"]["updated_at"], reverse=True
    )
    log("Last updated task: {}".format(len(sorted_tasks)), log=debug)
    return sorted_tasks[0] if sorted_tasks else None


def get_current_task():
    memory = get_memories("task", filter_metadata={"current": True})
    if len(memory) > 0:
        log("Current task: {}".format(memory[0]), log=debug)
        return memory[0]
    else:
        log("No current task found", log=debug)
        return None


def set_current_task(task):
    task_id = get_task_id

    memories = get_memories("task", filter_metadata={"current": True})

    for memory in memories:
        update_memory("task", memory["id"], metadata={"current": False})
    log("Setting current task: {}".format(task), log=debug)
    return update_memory("task", task_id, metadata={"current": True})


# Plans
def create_plan(goal):
    response = openai_text_call(
        compose_prompt(planning_prompt, {"goal": goal}), debug=debug
    )
    return response["text"]


def update_plan(task, plan):
    task_id = get_task_id(task)
    log("Updating plan for task: {}".format(task), log=debug)
    update_memory("task", task_id, metadata={"plan": plan})


# Create Steps
def create_steps(goal, plan):
    log("Creating steps for goal: {}".format(goal), log=debug)
    response = openai_function_call(
        text=compose_prompt(step_creation_prompt, {"goal": goal, "plan": plan}),
        functions=[step_creation_function],
        function_call="create_steps",
        debug=debug,
    )
    return response["arguments"]["steps"]


# Create Step
def create_step(goal, steps, plan):
    steps.append({"content": goal, "completed": False})
    update_plan(goal, steps, plan)
    log("Creating step for goal: {}".format(goal), log=debug)
    return steps


# Update Step
def update_step(task, step):
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    steps = task["metadata"]["steps"]
    steps = json.loads(steps)

    for s in steps:
        if s["content"] == step["content"]:
            s["completed"] = step["completed"]

    steps = json.dumps(steps)
    log("Updating step for task: {}\nSteps are: {}".format(task, steps), log=debug)
    return update_memory("task", task_id, metadata={"steps": steps})


# Add Step
def add_step(task, step):
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    steps = task["metadata"]["steps"]
    steps = json.loads(steps)
    steps.append({"content": step, "completed": False})
    steps = json.dumps(steps)
    log("Adding step for task: {}\nSteps are: {}".format(task, steps), log=debug)
    return update_memory("task", task_id, metadata={"steps": steps})


# Finish Step
def finish_step(task, step):
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    steps = task["metadata"]["steps"]
    steps = json.loads(steps)
    for s in steps:
        if s["content"] == step:
            s["completed"] = True
    steps = json.dumps(steps)
    log("Finishing step for task: {}\nSteps are: {}".format(task, steps), log=debug)
    return update_memory("task", task_id, metadata={"steps": steps})


# Cancel Step
def cancel_step(task, step):
    task_id = get_task_id(task)
    task = get_memory("task", task_id)
    steps = task["metadata"]["steps"]
    steps = json.loads(steps)
    steps = [s for s in steps if s["content"] != step]
    steps = json.dumps(steps)
    log("Cancelling step for task: {}\nSteps are: {}".format(task, steps), log=debug)
    return update_memory("task", task_id, metadata={"steps": steps})
