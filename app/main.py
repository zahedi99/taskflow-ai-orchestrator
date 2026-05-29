from fastapi import FastAPI

from app.schemas.request_schema import WorkflowRequest
from app.schemas.result_schema import WorkflowResult

from app.core.planner import create_workflow_plan
from app.core.executor import execute_workflow
from app.core.evaluator import evaluate_workflow


app = FastAPI(
    title="TaskFlow AI Orchestrator",
    description=(
        "A clean-room structured workflow automation API that converts "
        "messy business requests into validated multi-step task plans."
    ),
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "TaskFlow AI Orchestrator API is running.",
        "docs": "/docs",
        "health": "/health",
        "workflow_endpoint": "/run-workflow",
    }
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TaskFlow AI Orchestrator",
    }


@app.post("/run-workflow", response_model=WorkflowResult)
def run_workflow(request: WorkflowRequest):
    workflow_plan = create_workflow_plan(request.user_request)
    results = execute_workflow(workflow_plan, request.context)
    evaluation = evaluate_workflow(workflow_plan, results)

    return WorkflowResult(
        intent=workflow_plan.intent,
        workflow=workflow_plan,
        results=results,
        evaluation=evaluation,
    )