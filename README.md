# TaskFlow AI Orchestrator

TaskFlow AI Orchestrator is a clean-room AI engineering portfolio project that converts messy business requests into structured, validated, multi-step workflows.

The project demonstrates workflow planning, tool routing, schema validation, modular execution, and output evaluation using FastAPI and Pydantic.

## Example Use Case

Input:

> Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email.

Output:

- Request interpretation
- Multi-step workflow plan
- Tool routing
- Structured execution results
- Evaluation checks for workflow validity

## Core Features

- FastAPI backend
- Pydantic request and response schemas
- Rule-based workflow planner
- Tool router
- Modular task tools
- Workflow executor
- Output evaluator
- Example business productivity workflows

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
app/
  main.py
  schemas/
  core/
  tools/
  tests/
examples/
docs/