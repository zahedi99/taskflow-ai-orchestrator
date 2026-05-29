AVAILABLE_TOOLS = {
    "summariser",
    "task_extractor",
    "priority_classifier",
    "email_drafter",
    "plan_generator",
}


def validate_tools(tool_names: list[str]) -> bool:
    return all(tool_name in AVAILABLE_TOOLS for tool_name in tool_names)


def get_missing_tools(tool_names: list[str]) -> list[str]:
    return [tool_name for tool_name in tool_names if tool_name not in AVAILABLE_TOOLS]