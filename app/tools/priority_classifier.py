def classify_priorities(tasks: list[str]) -> list[dict]:
    prioritised_tasks = []

    for task in tasks:
        task_lower = task.lower()

        if "urgent" in task_lower or "deadline" in task_lower or "friday" in task_lower:
            priority = "high"
        elif "review" in task_lower or "prepare" in task_lower:
            priority = "medium"
        else:
            priority = "low"

        prioritised_tasks.append(
            {
                "task": task,
                "priority": priority,
            }
        )

    return prioritised_tasks