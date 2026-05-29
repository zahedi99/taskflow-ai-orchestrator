from app.schemas.workflow_schema import WorkflowPlan
from app.schemas.result_schema import StepResult

from app.tools.summariser import summarise_text
from app.tools.task_extractor import extract_tasks
from app.tools.priority_classifier import classify_priorities
from app.tools.plan_generator import generate_plan
from app.tools.email_drafter import draft_email


def execute_workflow(plan: WorkflowPlan, context: str) -> list[StepResult]:
    results = []

    summary = ""
    tasks = []
    prioritised_tasks = []

    for step in plan.steps:
        if step.tool_name == "summariser":
            summary = summarise_text(context)
            output = summary

        elif step.tool_name == "task_extractor":
            tasks = extract_tasks(context)
            output = tasks

        elif step.tool_name == "priority_classifier":
            if not tasks:
                tasks = extract_tasks(context)

            prioritised_tasks = classify_priorities(tasks)
            output = prioritised_tasks

        elif step.tool_name == "plan_generator":
            if prioritised_tasks:
                plan_tasks = [item["task"] for item in prioritised_tasks]
            elif tasks:
                plan_tasks = tasks
            else:
                plan_tasks = extract_tasks(context)

            output = generate_plan(plan_tasks)

        elif step.tool_name == "email_drafter":
            if not summary:
                summary = summarise_text(context)

            if not tasks:
                tasks = extract_tasks(context)

            output = draft_email(summary, tasks)

        else:
            output = f"Tool '{step.tool_name}' is not implemented."

        results.append(
            StepResult(
                step_id=step.step_id,
                tool_name=step.tool_name,
                output=output,
            )
        )

    return results