def draft_email(summary: str, tasks: list[str]) -> str:
    task_lines = "\n".join(f"- {task}" for task in tasks)

    return f"""Subject: Follow-up and Next Steps

Hi,

Thank you for the discussion. Here is a brief summary:

{summary}

Key next steps:
{task_lines}

Best regards,
TaskFlow AI Orchestrator
"""