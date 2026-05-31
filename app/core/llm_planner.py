import json
import os
from typing import Optional, Tuple

import requests
from pydantic import ValidationError

from app.schemas.workflow_schema import WorkflowPlan
from app.schemas.result_schema import PlannerMetadata
from app.core.planner import create_workflow_plan


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


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
- Do not wrap the JSON in markdown.
- Do not add text before or after the JSON.

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


def strip_markdown_fences(raw_response: str) -> str:
    cleaned = raw_response.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()

    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()

    return cleaned


def extract_json_object(raw_response: str) -> Optional[str]:
    cleaned = strip_markdown_fences(raw_response)

    start_index = cleaned.find("{")
    if start_index == -1:
        return None

    brace_depth = 0
    in_string = False
    escape_next = False

    for index in range(start_index, len(cleaned)):
        char = cleaned[index]

        if escape_next:
            escape_next = False
            continue

        if char == "\\" and in_string:
            escape_next = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1

            if brace_depth == 0:
                return cleaned[start_index : index + 1]

    return None


def parse_llm_plan(raw_response: str) -> Optional[WorkflowPlan]:
    try:
        json_text = extract_json_object(raw_response)

        if not json_text:
            return None

        parsed = json.loads(json_text)

        return WorkflowPlan.model_validate(parsed)

    except (json.JSONDecodeError, TypeError, ValidationError):
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
