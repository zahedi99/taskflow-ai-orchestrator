from app.core.llm_planner import extract_json_object, parse_llm_plan

VALID_PLAN_JSON = '''
{
  "intent": "structured_business_workflow",
  "steps": [
    {
      "step_id": 1,
      "tool_name": "summariser",
      "description": "Summarise the provided context."
    }
  ]
}
'''


def test_extract_json_object_from_plain_json():
    extracted = extract_json_object(VALID_PLAN_JSON)
    assert extracted is not None
    assert '"tool_name": "summariser"' in extracted


def test_extract_json_object_from_markdown_json_block():
    raw_response = '`json' + VALID_PLAN_JSON + '`'
    extracted = extract_json_object(raw_response)
    assert extracted is not None
    assert '"tool_name": "summariser"' in extracted


def test_extract_json_object_with_text_before_and_after_json():
    raw_response = 'Here is the workflow:' + VALID_PLAN_JSON + 'Done.'
    extracted = extract_json_object(raw_response)
    assert extracted is not None
    assert extracted.strip().startswith('{')
    assert extracted.strip().endswith('}')


def test_parse_llm_plan_accepts_messy_markdown_response():
    raw_response = 'Sure, here is the JSON: `json' + VALID_PLAN_JSON + '`'
    plan = parse_llm_plan(raw_response)
    assert plan is not None
    assert plan.intent == 'structured_business_workflow'
    assert len(plan.steps) == 1
    assert plan.steps[0].tool_name == 'summariser'


def test_parse_llm_plan_rejects_invalid_json():
    plan = parse_llm_plan('This is not JSON.')
    assert plan is None


def test_parse_llm_plan_rejects_missing_required_fields():
    raw_response = '''
{
  "intent": "structured_business_workflow",
  "steps": [
    {
      "step_id": 1,
      "tool_name": "summariser"
    }
  ]
}
'''
    plan = parse_llm_plan(raw_response)
    assert plan is None
