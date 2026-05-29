from app.schemas.workflow_schema import WorkflowPlan
from app.schemas.result_schema import StepResult, EvaluationResult
from app.core.tool_router import validate_tools


def evaluate_workflow(plan: WorkflowPlan, results: list[StepResult]) -> EvaluationResult:
    tool_names = [step.tool_name for step in plan.steps]

    missing_fields = []

    if not plan.intent:
        missing_fields.append("intent")

    if not plan.steps:
        missing_fields.append("steps")

    empty_outputs = []

    for result in results:
        if result.output in [None, "", [], {}]:
            empty_outputs.append(result.tool_name)

    return EvaluationResult(
        valid_json=True,
        all_tools_available=validate_tools(tool_names),
        missing_fields=missing_fields,
        empty_outputs=empty_outputs,
    )