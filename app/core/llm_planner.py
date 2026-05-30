import json
from typing import Optional, Tuple

import requests
from pydantic import ValidationError

from app.schemas.workflow_schema import WorkflowPlan, WorkflowStep
from app.schemas.result_schema import PlannerMetadata
from app.core.planner import create_workflow_plan


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2"


def build_llm_prompt(user_request: str) -> str:
    return f"""
You are a workflow planning assistant.

Convert the user's messy business request into a strict JSON workflow plan.

Available tools:
- summariser
- task_extractor
- priority_classifier
- plan_generator
- email_drafter

Return ONLY valid JSON. No markdown. No explanation.

JSON format:
{{
  "intent": "structured_business_workflow",
  "steps": [
    {{
      "step_id": 1,
      "tool_name": "summariser",
      "description": "Summarise the provided context."
    }}
  ]
}}

Rules:
- Use only the available tools.
- step_id must start at 1 and increase by 1.
- Include only tools that are relevant to the request.
- If the request is unclear, include summariser as the fallback tool.

User request:
{user_request}
""".strip()


def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> Optional[str]:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response")
    except requests.RequestException:
        return None


def parse_llm_plan(raw_response: str) -> Optional[WorkflowPlan]:
    try:
        cleaned_response = raw_response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.replace("```", "").strip()

        parsed = json.loads(cleaned_response)

        steps = [
            WorkflowStep(
                step_id=step["step_id"],
                tool_name=step["tool_name"],
                description=step["description"],
            )
            for step in parsed.get("steps", [])
        ]

        return WorkflowPlan(
            intent=parsed.get("intent", "structured_business_workflow"),
            steps=steps,
        )

    except (json.JSONDecodeError, KeyError, TypeError, ValidationError):
        return None


def create_llm_workflow_plan(user_request: str) -> Tuple[WorkflowPlan, PlannerMetadata]:
    prompt = build_llm_prompt(user_request)
    raw_response = call_ollama(prompt)

    if raw_response:
        llm_plan = parse_llm_plan(raw_response)
        if llm_plan and llm_plan.steps:
            return llm_plan, PlannerMetadata(
                mode="ollama",
                model=DEFAULT_MODEL,
                llm_available=True,
            )

        fallback_plan = create_workflow_plan(user_request)
        return fallback_plan, PlannerMetadata(
            mode="rule_based_fallback_invalid_llm_output",
            model=DEFAULT_MODEL,
            llm_available=True,
        )

    fallback_plan = create_workflow_plan(user_request)
    return fallback_plan, PlannerMetadata(
        mode="rule_based_fallback_ollama_unavailable",
        model=DEFAULT_MODEL,
        llm_available=False,
    )