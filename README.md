# agentagenda <a href="https://discord.gg/qetWd7J9De"><img style="float: right" src="https://dcbadge.vercel.app/api/server/qetWd7J9De" alt=""></a>

An agenda and task manager for your agent.

<img src="resources/image.jpg">

[![Lint and Test](https://github.com/AutonomousResearchGroup/agentagenda/actions/workflows/test.yml/badge.svg)](https://github.com/AutonomousResearchGroup/agentagenda/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/agentagenda.svg)](https://badge.fury.io/py/agentagenda)

## Installation

```bash
pip install agentagenda
```

## Quickstart

This will create a new task with the goal "Write README.md file", and then mark it as completed.

```python
from agentagenda import create_task, finish_task

# Create a new task
task = create_task("Write README.md file")
print(task)

# Complete the task
finish_task(task)
```

### 1. Creating a Task:
To create a task, use the `create_task` method. You can optionally specify a plan and steps.
```python
task = create_task("Finish the project", plan="Plan for the project")
print(task)
```

### 2. List All Tasks:
Retrieve a list of all tasks that are in progress using the `list_tasks` method.
```python
tasks = list_tasks()
print(tasks)
```

### 3. Search for Tasks:
You can search for specific tasks using the `search_tasks` method.
```python
tasks = search_tasks("project")
print(tasks)
```

### 4. Deleting a Task:
To delete a task, use the `delete_task` method.
```python
delete_task(task)
```

### 5. Completing a Task:
Mark a task as complete using the `finish_task` method.
```python
finish_task(task)
```

### 6. Cancelling a Task:
If you want to cancel a task, use the `cancel_task` method.
```python
cancel_task(task)
```

### 7. Retrieve Task ID:
To get the ID of a specific task, use the `get_task_id` method.
```python
task_id = get_task_id(task)
print(task_id)
```

### 8. Working with Plans:
- To create a plan for a specific goal, use the `create_plan` method.
```python
plan = create_plan("Finish the project")
print(plan)
```
- To update the plan of a specific task, use the `update_plan` method.
```python
update_plan(task, "New plan for the project")
```

### 9. Working with Steps:
- To create a list of steps based on a given goal and plan, use the `create_steps` method.
```python
steps = create_steps("Finish the project", "Plan for the project")
print(steps)
```
- To add a new step to a task, use the `add_step` method.
```python
add_step(task, "New step for the project")
```
- To mark a specific step of a task as complete, use the `finish_step` method.
```python
finish_step(task, "Step to complete")
```

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

**`get_task_by_id(task_id: str) -> dict`**

    Returns the task with the given ID. If no task is found, None is returned.

    *Example:*

    ```python
    task = get_task_by_id(task_id)
    print(task)
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

**`get_task_as_formatted_string(task: dict, include_plan: bool = True, include_status: bool = True, include_steps: bool = True) -> str`**

    Returns a string representation of the task, including the plan, status, and steps based on the arguments provided.

    *Example:*

    ```python
    task_string = get_task_as_formatted_string(task, include_plan=True, include_status=True, include_steps=True)
    print(task_string)
    ```

**`list_tasks_as_formatted_string() -> str`**

    Retrieves and formats a list of all current tasks. Returns a string containing details of all current tasks.

    *Example:*

    ```python
    tasks_string = list_tasks_as_formatted_string()
    print(tasks_string)
    ```

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

<img src="resources/youcreatethefuture.jpg" width="100%">
