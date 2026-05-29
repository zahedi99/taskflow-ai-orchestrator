from pydantic import BaseModel, Field


class WorkflowRequest(BaseModel):
    user_request: str = Field(..., min_length=5)
    context: str = Field(default="")