from app.core.planner import create_workflow_plan
from app.core.executor import execute_workflow
from app.core.evaluator import evaluate_workflow


def test_rule_based_planner_full_workflow_tools():
    plan = create_workflow_plan(
        "Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email."
    )

    tool_names = [step.tool_name for step in plan.steps]

    assert "summariser" in tool_names
    assert "task_extractor" in tool_names
    assert "priority_classifier" in tool_names
    assert "plan_generator" in tool_names
    assert "email_drafter" in tool_names


def test_rule_based_planner_small_workflow_tools():
    plan = create_workflow_plan("Extract the action items and prioritise them.")

    tool_names = [step.tool_name for step in plan.steps]

    assert "task_extractor" in tool_names
    assert "priority_classifier" in tool_names
    assert "email_drafter" not in tool_names
    assert "plan_generator" not in tool_names


def test_unclear_request_defaults_to_summariser():
    plan = create_workflow_plan("Help me understand this.")

    tool_names = [step.tool_name for step in plan.steps]

    assert tool_names == ["summariser"]


def test_executor_and_evaluator_return_valid_outputs():
    plan = create_workflow_plan(
        "Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email."
    )

    context = (
        "Today we discussed the product launch. The testing phase is delayed. "
        "We need to review the documentation. Sarah should send the client update by Friday. "
        "The team must prepare the final launch checklist."
    )

    results = execute_workflow(plan, context)
    evaluation = evaluate_workflow(plan, results)

    assert len(results) == len(plan.steps)
    assert evaluation.valid_json is True
    assert evaluation.all_tools_available is True
    assert evaluation.missing_fields == []
    assert evaluation.empty_outputs == []
