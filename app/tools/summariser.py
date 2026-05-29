def summarise_text(context: str) -> str:
    if not context.strip():
        return "No context was provided to summarise."

    sentences = context.split(".")
    short_summary = ". ".join(sentences[:2]).strip()

    if short_summary:
        return short_summary + "."

    return context[:300]