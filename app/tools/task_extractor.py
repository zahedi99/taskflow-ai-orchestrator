def extract_tasks(context: str) -> list[str]:
    if not context.strip():
        return ["Review the request and gather more context."]

    tasks = []

    keywords = [
        "need to",
        "must",
        "should",
        "follow up",
        "prepare",
        "send",
        "review",
        "complete",
    ]

    for sentence in context.split("."):
        sentence_clean = sentence.strip()
        if any(keyword in sentence_clean.lower() for keyword in keywords):
            tasks.append(sentence_clean)

    if not tasks:
        tasks.append("Review the provided context and identify next steps.")

    return tasks