from pydantic import BaseModel
from typing import Any, List

from app.schemas.workflow_schema import WorkflowPlan


class StepResult(BaseModel):
    step_id: int
    tool_name: str
    output: Any


class EvaluationResult(BaseModel):
    valid_json: bool
    all_tools_available: bool
    missing_fields: List[str]
    empty_outputs: List[str]


class PlannerMetadata(BaseModel):
    mode: str
    model: str
    llm_available: bool


class WorkflowResult(BaseModel):
    intent: str
    planner: PlannerMetadata
    workflow: WorkflowPlan
    results: List[StepResult]
    evaluation: EvaluationResult