from pydantic import BaseModel
from typing import List


class WorkflowStep(BaseModel):
    step_id: int
    tool_name: str
    description: str


class WorkflowPlan(BaseModel):
    intent: str
    steps: List[WorkflowStep]