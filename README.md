## Local LLM Planning with Ollama

TaskFlow supports local LLM-based workflow planning through Ollama. A user can provide a messy business request, and the system attempts to convert it into a structured workflow plan using a local model.

The current default local model is:

```text
llama3.2:1b
```

TaskFlow does not require paid cloud API access. If Ollama is unavailable or the model output cannot be parsed into the expected schema, the system safely falls back to the rule-based planner.

### Planner Modes

The API response includes planner metadata so the user can see exactly how the workflow plan was generated.

Example successful Ollama planning mode:

```json
{
  "planner": {
    "mode": "ollama",
    "model": "llama3.2:1b",
    "llm_available": true
  }
}
```

Example fallback mode when Ollama is unavailable:

```json
{
  "planner": {
    "mode": "rule_based_fallback_ollama_unavailable",
    "model": "llama3.2:1b",
    "llm_available": false
  }
}
```

This makes the system transparent: it clearly shows whether the workflow plan came from the local LLM or from the safe fallback planner.

## Running with Ollama

Install Ollama and pull the lightweight local model:

```powershell
ollama pull llama3.2:1b
```

Confirm Ollama is running:

```powershell
curl.exe http://localhost:11434/api/tags
```

Start the TaskFlow API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

Open the API docs:

```text
http://127.0.0.1:8001/docs
```

Or test from PowerShell:

```powershell
$body = @{
  user_request = "Summarise this meeting transcript, extract tasks, prioritise them, create a 3-day plan, and draft a follow-up email."
  context = "Today we discussed the product launch. The testing phase is delayed. We need to review the documentation. Sarah should send the client update by Friday. The team must prepare the final launch checklist."
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8001/run-workflow" -Method Post -Body $body -ContentType "application/json"

$response | ConvertTo-Json -Depth 10
```

Example proof outputs are included in:

```text
examples/ollama_success_response.json
examples/fallback_response.json
```
