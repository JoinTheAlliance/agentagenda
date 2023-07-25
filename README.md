# easytask

A simple task manager for your agent. Give it a goal, get a task with a plan and steps.

<img src="resources/image.jpg">

## Who is this for?

While you can use easytask from the command line, or integrate it into other types of applications, it is primarily useful for autonomous agents and generative AI applications which need to keep track of tasks.

## Installation

```bash
pip install easytask
```

## Quickstart

Here's a basic example of how to use easytask:

```python
from easytask import create_task, finish_task

# Create a new task
task = create_task("Write README.md file")
print(task)

# Complete the task
finish_task(task)
```

This will create a new task with the goal "Write README.md file", and then mark it as completed.

## Documentation

**`create_task(goal: str, plan: str = None, steps: dict = None) -> dict`**

    Creates a new task based on the given goal, as well as plan and steps optionally. If no plan or steps are provided they will be generated based on the goal. Returns a dictionary representing the task.

    *Example:*

    ```python
    task = create_task("Finish the project")
    print(task)
    ```

**`list_tasks() -> list`**

    Returns a list of all tasks that are currently in progress.

    *Example:*

    ```python
    tasks = list_tasks()
    print(tasks)
    ```

**`search_tasks(search_term: str) -> list`**

    Returns a list of tasks whose goal is most relevant to the search term.

    *Example:*

    ```python
    tasks = search_tasks("project")
    print(tasks)
    ```

**`delete_task(task: Union[dict, int, str]) -> None`**

    Deletes the specified task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    delete_task(task)
    ```

**`finish_task(task: Union[dict, int, str]) -> None`**

    Marks the specified task as complete.

    *Example:*

    ```python
    finish_task(task)
    ```

**`cancel_task(task: Union[dict, int, str]) -> None`**

    Marks the specified task as cancelled.

    *Example:*

    ```python
    cancel_task(task)
    ```

**`get_task_id(task: Union[dict, int, str]) -> str`**

    Returns the ID of the given task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    task_id = get_task_id(task)
    print(task_id)
    ```

**`get_last_created_task() -> dict`**

    Returns the most recently created task.

    *Example:*

    ```python
    task = get_last_created_task()
    print(task)
    ```

**`get_last_updated_task() -> dict`**

    Returns the most recently updated task.

    *Example:*

    ```python
    task = get_last_updated_task()
    print(task)
    ```

**`get_current_task() -> dict`**

    Returns the current task.

    *Example:*

    ```python
    task = get_current_task()
    print(task)
    ```

**`set_current_task(task: Union[dict, int, str]) -> dict`**

    Sets the specified task as the current task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    set_current_task(task)
    ```

**`create_plan(goal: str) -> str`**

    Creates a plan based on the given goal.

    *Example:*

    ```python
    plan = create_plan("Finish the project")
    print(plan)
    ```

**`update_plan(task: Union[dict, int, str], plan: str) -> dict`**

    Updates the plan of the specified task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    update_plan(task, "New plan for the project")
    ```

**`create_steps(goal: str, plan: str) -> list`**

    Creates a list of steps based on the given goal and plan.

    *Example:*

    ```python
    steps = create_steps("Finish the project", "Plan for the project")
    print(steps)
    ```

**`create_step(goal: str, steps: list, plan: str) -> list`**

    Adds a new step to the given steps based on the goal, and updates the plan. Returns the updated steps.

    *Example:*

    ```python
    steps = create_step("New step for the project", steps, "Plan for the project")
    print(steps)
    ```

**`update_step(task: Union[dict, int, str], step: dict) -> dict`**

    Updates the specified step of the specified task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    step = {"content": "New step", "completed": True}
    update_step(task, step)
    ```

**`add_step(task: Union[dict, int, str], step: str) -> dict`**

    Adds a new step to the specified task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    add_step(task, "New step for the project")
    ```

**`finish_step(task: Union[dict, int, str], step: str) -> dict`**

    Marks the specified step of the specified task as complete. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    finish_step(task, "Step to complete")
    ```

**`cancel_step(task: Union[dict, int, str], step: str) -> dict`**

    Cancels the specified step of the specified task. The task can be specified as a dictionary (as returned by `create_task`), an integer ID, or a string ID.

    *Example:*

    ```python
    cancel_step(task, "Step to cancel")
    ```

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

<img src="resources/youcreatethefuture.jpg" width="100%">