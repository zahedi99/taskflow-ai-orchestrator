def generate_plan(tasks: list[str]) -> dict:
    return {
        "day_1": tasks[:2],
        "day_2": tasks[2:4],
        "day_3": tasks[4:] if len(tasks) > 4 else ["Review progress and finalise outputs."],
    }