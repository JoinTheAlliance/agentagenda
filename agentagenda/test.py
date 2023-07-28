from datetime import datetime
import json
from agentmemory import create_memory, get_memories, get_memory, wipe_category
from agentagenda import (
    create_task,
    delete_task,
    list_tasks,
    search_tasks,
    finish_task,
    cancel_task,
    create_plan,
    update_plan,
    create_steps,
    add_step,
    finish_step,
    cancel_step,
)
from agentagenda.main import get_next_step, get_task_as_formatted_string, list_tasks_as_formatted_string

goal = "Make a balogna sandwich"

plan = """Gather Ingredients and Equipment
Gather the following ingredients: two slices of bread (your choice), 2-3 slices of bologna, 1-2 slices of cheese (optional), lettuce leaves (optional), tomato slices (optional), mayonnaise, and mustard. Ensure you have a butter knife to spread the condiments and a plate to prepare your sandwich on.

Prepare Bread
Take the two slices of bread. Place them on the plate.

Spread the Condiments
Open the containers of mayonnaise and mustard. With your butter knife, spread a layer of mayonnaise on one slice of bread, and a layer of mustard on the other slice.

Add the Bologna
Take the slices of bologna and place them evenly on one of the slices of bread.

Add Optional Extras
If you're using cheese, place your cheese slices on top of the bologna. Then, add the lettuce leaves and tomato slices, if desired.

Complete the Sandwich
Pick up the slice of bread without the toppings and place it on top of the other slice, condiment-side down. Press gently.

Cutting (optional)
If you prefer, use a sharp knife to cut the sandwich in half, either diagonally or straight down the middle.

Cleanup
Make sure to put away your ingredients and clean your equipment, including the butter knife, plate, and any condiment spills.

Conditions for Task Completion
The task will be considered complete when the bologna sandwich has been fully assembled and all ingredients and tools have been cleaned up and put away. The final output will be a ready-to-eat bologna sandwich."""

steps = json.dumps(
    [
        {"content": "Gather Ingredients and Equipment", "completed": False},
        {"content": "Prepare Bread", "completed": False},
        {"content": "Spread the Condiments", "completed": False},
        {"content": "Add the Bologna", "completed": False},
        {"content": "Add Optional Extras", "completed": False},
        {"content": "Complete the Sandwich", "completed": False},
        {"content": "Cutting (optional)", "completed": False},
        {"content": "Cleanup", "completed": False},
    ]
)


# Custom setup and teardown
def setup():
    wipe_category("task")
    # get timestamp
    created_at = datetime.now()
    updated_at = datetime.now()

    task = {
        "created_at": created_at,
        "updated_at": updated_at,
        "goal": goal,
        "plan": plan,
        "steps": steps,
        "status": "in_progress",
    }

    create_memory("task", goal, metadata=task)
    memory = get_memories("task", goal)[0]
    return memory


def teardown():
    wipe_category("task")


# Test cases
def test_create_task():
    wipe_category("task")
    create_task(goal)
    # get memories
    task = get_memories("task")[0]

    assert isinstance(task, dict)
    assert "goal" in task["metadata"]
    assert "plan" in task["metadata"]
    assert "steps" in task["metadata"]
    assert "status" in task["metadata"]
    assert task["metadata"]["status"] == "in_progress"
    teardown()


def test_list_tasks():
    task = setup()
    tasks = list_tasks()
    assert isinstance(tasks, list)
    # check that the task document is in the list of tasks' docments
    assert task["document"] in [task["document"] for task in tasks]
    teardown()


def test_search_tasks():
    task = setup()
    search_result = search_tasks("Test")
    assert isinstance(search_result, list)
    # map search_result['document'] to documents
    documents = [result["document"] for result in search_result]
    assert task["document"] in documents
    teardown()


def test_delete_task():
    task = setup()
    delete_task(task)
    documents = [result["document"] for result in list_tasks()]
    assert task["document"] not in documents


def test_finish_task():
    task = setup()
    finish_task(task)
    updated_task = get_memory("task", task["id"])
    assert updated_task["metadata"]["status"] == "complete"
    teardown()


def test_cancel_task():
    task = setup()
    cancel_task(task)
    updated_task = get_memory("task", task["id"])
    assert updated_task["metadata"]["status"] == "cancelled"
    teardown()


def test_create_plan():
    goal = "Test goal"
    plan = create_plan(goal)
    assert isinstance(plan, str)
    assert len(plan) > 0


def test_update_plan():
    task = setup()
    plan = "New plan"
    update_plan(task, plan)
    updated_task = get_memory("task", task["id"])
    print('updated_task')
    print(updated_task)
    assert updated_task["metadata"]["plan"] == plan
    teardown()


def test_create_steps():
    goal = "Test goal"
    plan = "Write a test plan, then outline what the steps are, then print them out."
    steps = create_steps(goal, plan)
    assert isinstance(steps, list)
    assert len(steps) > 0


def test_add_step():
    task = setup()
    step = "New step"
    add_step(task, step)
    updated_task = get_memory("task", task["id"])
    assert {"content": step, "completed": False} in json.loads(
        updated_task["metadata"]["steps"]
    )
    teardown()


def test_finish_step():
    task = setup()
    steps = json.loads(task["metadata"]["steps"])
    step = steps[0]["content"]
    finish_step(task, step)
    updated_task = get_memory("task", task["id"])
    updated_steps = json.loads(updated_task["metadata"]["steps"])
    step_data = next((s for s in updated_steps if s["content"] == step), None)
    assert step_data and step_data["completed"] == True
    teardown()


def test_cancel_step():
    task = setup()
    step = json.loads(task["metadata"]["steps"])[0]["content"]
    cancel_step(task, step)
    updated_task = get_memory("task", task["id"])
    updated_steps = json.loads(updated_task["metadata"]["steps"])
    step_data = next((s for s in updated_steps if s["content"] == step), None)
    assert step_data == None
    teardown()


def test_get_next_step():
    task = {
        "metadata": {
            "steps": json.dumps(
                [
                    {"content": "Step 1", "completed": False},
                    {"content": "Step 2", "completed": False},
                ]
            )
        }
    }

    next_step = get_next_step(task)
    assert next_step == {"content": "Step 1", "completed": False}


def test_get_task_as_formatted_string():
    task = {
        "metadata": {
            "plan": "Plan 1",
            "status": "in_progress",
            "steps": json.dumps(
                [
                    {"content": "Step 1", "completed": False},
                    {"content": "Step 2", "completed": False},
                ]
            ),
        }
    }

    task_string = get_task_as_formatted_string(task)
    expected_string = (
        "Plan: Plan 1\n"
        "Status: in_progress\n"
        "Steps: Step 1: Not completed, Step 2: Not completed"
    )
    assert task_string == expected_string


def test_list_tasks_as_formatted_string():
    # Setup: Create multiple tasks
    tasks = [
        {
            "plan": "Plan 1",
            "status": "in_progress",
            "steps": json.dumps([
                {"content": "Step 1", "completed": False},
                {"content": "Step 2", "completed": False}
            ])
        },
        {
            "plan": "Plan 2",
            "status": "Completed",
            "steps": json.dumps([
                {"content": "Step 3", "completed": True},
                {"content": "Step 4", "completed": True}
            ])
        },
    ]
    for task in tasks:
        create_task("some goal", task["plan"], task["steps"])

    tasks = get_memories("task", unique=False)

    # Execute
    tasks_string = list_tasks_as_formatted_string()

    # Check if tasks_string includes all tasks
    for task in tasks:
        task_string = get_task_as_formatted_string(task)
        print("*** task_string is")
        print(task_string)
        print("***  tasks_string")
        print(tasks_string)
        assert task_string in tasks_string

    # Teardown: Remove all tasks
    wipe_category("task")
