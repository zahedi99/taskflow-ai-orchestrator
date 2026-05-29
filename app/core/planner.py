from app.schemas.workflow_schema import WorkflowPlan, WorkflowStep


def create_workflow_plan(user_request: str) -> WorkflowPlan:
    request_lower = user_request.lower()
    steps = []
    step_id = 1

    if "summarise" in request_lower or "summarize" in request_lower or "summary" in request_lower:
        steps.append(
            WorkflowStep(
                step_id=step_id,
                tool_name="summariser",
                description="Summarise the provided context."
            )
        )
        step_id += 1

    if "task" in request_lower or "action item" in request_lower or "extract" in request_lower:
        steps.append(
            WorkflowStep(
                step_id=step_id,
                tool_name="task_extractor",
                description="Extract action items from the provided context."
            )
        )
        step_id += 1

    if "priority" in request_lower or "prioritise" in request_lower or "prioritize" in request_lower:
        steps.append(
            WorkflowStep(
                step_id=step_id,
                tool_name="priority_classifier",
                description="Assign priority levels to extracted tasks."
            )
        )
        step_id += 1

    if "plan" in request_lower:
        steps.append(
            WorkflowStep(
                step_id=step_id,
                tool_name="plan_generator",
                description="Create a short execution plan."
            )
        )
        step_id += 1

    if "email" in request_lower:
        steps.append(
            WorkflowStep(
                step_id=step_id,
                tool_name="email_drafter",
                description="Draft a professional follow-up email."
            )
        )

    if not steps:
        steps.append(
            WorkflowStep(
                step_id=1,
                tool_name="summariser",
                description="Provide a general summary of the request."
            )
        )

    return WorkflowPlan(
        intent="structured_business_workflow",
        steps=steps
    )