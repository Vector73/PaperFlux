```
paperflux/
├── .env.example
├── pyproject.toml
├── poetry.lock
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── hf_tools/
│   │   │   ├── __init__.py
│   │   │   ├── paper_pdf_tool.py
│   │   │   └── summarization_tool.py
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   ├── redis_client.py       # Core Redis operations
│   │   │   └── cache_interface.py    # Abstract base class
│   │   └── cache_manager.py          # High-level cache operations
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── model.py           # Pydantic models for data validation
│   │── scheduler.py                 # Scheduled cache updates
|   └── app.py                       # gradio web app
```

``` Above is agentic workflow design, initial workflow will be using gemini api key and will be extended to agentic system ```