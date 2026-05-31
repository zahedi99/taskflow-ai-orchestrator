# Testing Evidence

TaskFlow includes pytest coverage for the core workflow engine.

## Local Test Command

Run:

.\.venv\Scripts\python.exe -m pytest app/tests -v

## Latest Local Result

4 passed in 0.39s

## Covered Behaviour

- Rule-based planner selects the correct full workflow tools.
- Smaller task/prioritisation requests select only the relevant tools.
- Unclear requests fall back to the summariser.
- Executor and evaluator return valid outputs with no missing fields or empty outputs.

## Test File

app/tests/test_core_workflow.py
