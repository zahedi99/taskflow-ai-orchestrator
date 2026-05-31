# TaskFlow AI Orchestrator

TaskFlow AI Orchestrator is a clean-room LLM workflow automation API that converts messy business requests into structured, validated multi-step task plans.

It demonstrates practical AI workflow engineering using local LLM planning, schema validation, modular tool routing, workflow execution, and output evaluation.

## Demo UI

TaskFlow includes a built-in FastAPI browser UI for testing workflow orchestration locally.

![TaskFlow AI Orchestrator demo](docs/taskflow-ui-ollama-demo.png)

## Core Features

* Local LLM workflow planning with Ollama
* Rule-based fallback planner when the LLM is unavailable or returns invalid output
* Pydantic schema validation for workflow plans and results
* Modular tool execution pipeline
* Built-in workflow evaluator
* FastAPI API endpoints
* Built-in browser demo UI
* Pytest coverage for workflow and parser behaviour
* Example proof outputs for successful Ollama mode and fallback mode

## Tech Stack

Python | FastAPI | Pydantic | Ollama | Local LLMs | Uvicorn | Pytest | HTML/CSS/JavaScript

## What TaskFlow Does

A user can provide a messy business request such as:

```text
Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email.
```

TaskFlow then:

1. Generates a structured workflow plan.
2. Validates the workflow against strict schemas.
3. Routes each step to the correct internal tool.
4. Executes the workflow.
5. Evaluates the output for missing fields, invalid tools, and empty outputs.
6. Returns planner metadata, workflow steps, tool outputs, and evaluation results.

## Architecture

```text
User Request
    ↓
LLM Planner / Rule-Based Fallback
    ↓
Pydantic Workflow Schema Validation
    ↓
Tool Router
    ↓
Modular Tools
    ├── summariser
    ├── task_extractor
    ├── priority_classifier
    ├── plan_generator
    └── email_drafter
    ↓
Workflow Executor
    ↓
Output Evaluator
    ↓
Structured API / Browser UI Response
```

## Planner Modes

TaskFlow returns planner metadata so users can see how the workflow was generated.

```json
{
  "planner": {
    "mode": "ollama",
    "model": "llama3.2:1b",
    "llm_available": true
  }
}
```

Supported modes include:

* `ollama` — local Ollama model generated the workflow plan.
* `rule_based_fallback_invalid_llm_output` — Ollama responded, but the output was invalid.
* `rule_based_fallback_ollama_unavailable` — Ollama was unavailable, so TaskFlow used the rule-based planner.

## API Endpoints

| Method | Endpoint        | Purpose                    |
| ------ | --------------- | -------------------------- |
| GET    | `/`             | API information            |
| GET    | `/health`       | Health check               |
| GET    | `/ui`           | Built-in browser demo UI   |
| POST   | `/run-workflow` | Run workflow orchestration |

## Run Locally

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Optional: run Ollama locally

Install Ollama, then pull the local model:

```powershell
ollama pull llama3.2:1b
```

Confirm Ollama is running:

```powershell
curl.exe http://localhost:11434/api/tags
```

### 4. Start the FastAPI server

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

If port `8001` is busy, use:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### 5. Open the browser UI

```text
http://127.0.0.1:8001/ui
```

or, if using port `8002`:

```text
http://127.0.0.1:8002/ui
```

## Example API Request

```powershell
$body = @{
  user_request = "Extract the action items and prioritise them."
  context = "We need to review the API response. The team should prepare the client demo. Sarah must send the revised timeline by Friday."
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8001/run-workflow" -Method Post -Body $body -ContentType "application/json"

$response | ConvertTo-Json -Depth 10
```

## Testing

Run all tests:

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests -v
```

Latest local result:

```text
10 passed
```

Test coverage includes:

* Rule-based workflow planner behaviour
* Full workflow tool selection
* Smaller task/prioritisation workflow selection
* Unclear request fallback behaviour
* Executor and evaluator validity
* JSON extraction from plain JSON
* JSON extraction from markdown code blocks
* JSON extraction with text before/after JSON
* Parser rejection of invalid JSON
* Parser rejection of missing required fields

## Evidence and Proof Files

* Testing evidence: `docs/testing.md`
* Ollama planner proof: `docs/ollama_planner_proof.md`
* Successful Ollama example: `examples/ollama_success_response.json`
* Fallback example: `examples/fallback_response.json`

## Environment Configuration

TaskFlow supports environment-based Ollama configuration.

`.env.example`:

```env
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:1b
```

If no environment variables are provided, TaskFlow uses safe defaults.

## Portfolio Value

This project demonstrates applied AI engineering skills relevant to early-career AI Engineer, LLM Engineer, and AI Automation Engineer roles:

* Building local LLM-powered workflow systems
* Designing schema-validated AI outputs
* Implementing reliable fallback behaviour
* Creating tool-routing and execution pipelines
* Testing parser robustness for messy LLM responses
* Exposing AI workflows through both API and browser UI
* Keeping the project clean-room and independent

## Project Status

Strong portfolio MVP complete.

Implemented:

* API backend
* Local Ollama planner
* Fallback planner
* Planner metadata
* Parser robustness
* Core workflow tests
* Built-in demo UI
* Evidence documentation
