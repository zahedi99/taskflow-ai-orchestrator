from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.schemas.request_schema import WorkflowRequest
from app.schemas.result_schema import WorkflowResult

from app.core.llm_planner import create_llm_workflow_plan
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
    workflow_plan, planner_metadata = create_llm_workflow_plan(request.user_request)
    results = execute_workflow(workflow_plan, request.context)
    evaluation = evaluate_workflow(workflow_plan, results)

    return WorkflowResult(
    intent=workflow_plan.intent,
    planner=planner_metadata,
    workflow=workflow_plan,
    results=results,
    evaluation=evaluation,
    )
@app.get("/ui", response_class=HTMLResponse)
def taskflow_ui():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>TaskFlow AI Orchestrator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f6f7fb;
            margin: 0;
            padding: 30px;
            color: #1f2937;
        }
        .container {
            max-width: 1100px;
            margin: auto;
            background: white;
            padding: 28px;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        }
        h1 {
            margin-top: 0;
            color: #111827;
        }
        textarea {
            width: 100%;
            min-height: 130px;
            margin-top: 8px;
            margin-bottom: 18px;
            padding: 12px;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            font-size: 14px;
            resize: vertical;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 10px;
            font-size: 15px;
            cursor: pointer;
        }
        button:hover {
            background: #1d4ed8;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-top: 24px;
        }
        .card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 18px;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background: #111827;
            color: #e5e7eb;
            padding: 16px;
            border-radius: 12px;
            overflow-x: auto;
        }
        .meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 18px;
        }
        .pill {
            background: #eef2ff;
            color: #3730a3;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: 13px;
        }
        .status {
            margin-top: 16px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TaskFlow AI Orchestrator</h1>
        <p>Convert messy business requests into structured workflow plans with planner metadata, tool execution, and evaluation.</p>

        <label><strong>Messy business request</strong></label>
        <textarea id="user_request">Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email.</textarea>

        <label><strong>Context / transcript / notes</strong></label>
        <textarea id="context">Today we discussed the product launch. The testing phase is delayed. We need to review the documentation. Sarah should send the client update by Friday. The team must prepare the final launch checklist.</textarea>

        <button onclick="runTaskFlow()">Run TaskFlow</button>

        <div id="status" class="status"></div>
        <div id="metadata" class="meta"></div>

        <div class="grid">
            <div class="card">
                <h2>Workflow Plan</h2>
                <pre id="workflow">No workflow generated yet.</pre>
            </div>

            <div class="card">
                <h2>Tool Results</h2>
                <pre id="results">No results generated yet.</pre>
            </div>
        </div>

        <div class="card" style="margin-top: 18px;">
            <h2>Evaluation</h2>
            <pre id="evaluation">No evaluation generated yet.</pre>
        </div>

        <div class="card" style="margin-top: 18px;">
            <h2>Raw Response</h2>
            <pre id="raw">No response yet.</pre>
        </div>
    </div>

    <script>
        async function runTaskFlow() {
            const status = document.getElementById("status");
            const metadata = document.getElementById("metadata");

            status.innerText = "Running TaskFlow...";
            metadata.innerHTML = "";

            const payload = {
                user_request: document.getElementById("user_request").value,
                context: document.getElementById("context").value
            };

            try {
                const response = await fetch("/run-workflow", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(JSON.stringify(data, null, 2));
                }

                status.innerText = "Workflow completed.";

                metadata.innerHTML = `
                    <span class="pill">Planner: ${data.planner.mode}</span>
                    <span class="pill">Model: ${data.planner.model}</span>
                    <span class="pill">LLM available: ${data.planner.llm_available}</span>
                `;

                document.getElementById("workflow").innerText = JSON.stringify(data.workflow, null, 2);
                document.getElementById("results").innerText = JSON.stringify(data.results, null, 2);
                document.getElementById("evaluation").innerText = JSON.stringify(data.evaluation, null, 2);
                document.getElementById("raw").innerText = JSON.stringify(data, null, 2);

            } catch (error) {
                status.innerText = "Error running workflow.";
                document.getElementById("raw").innerText = error.message;
            }
        }
    </script>
</body>
</html>
"""