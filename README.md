# AI App Builder

Python FastAPI app that lets users describe an app and get an AI-generated layout using OpenAI.

## Setup

1. Add `.env` file with your OpenAI key:
OPENAI_API_KEY=your_key_here

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
uvicorn app.main:app --reload
```

4. Open in browser: http://localhost:8000

## Deployment

Deploy on Render: https://render.com


---

## Supabase Auth Setup

1. Create a project at https://supabase.com
2. Go to project settings → API and get the `SUPABASE_URL` and `SUPABASE_KEY`
3. Add to your `.env` file:

```
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=your_anon_or_service_role_key
```

---

## Code Generation (React)

Use the `generate_react_app_structure(name, code)` function to turn GPT output into actual downloadable React code files.



---

## Exporting Generated Code

To generate and zip a React app from AI output:

```python
from app.codegen.util import generate_react_app_structure, zip_app_directory

code = """import React from 'react';

export default function App() {
    return <h1>Hello from AI</h1>;
}
"""

folder = generate_react_app_structure("my_ai_app", code)
zip_path = zip_app_directory(folder)

print("Zipped app at:", zip_path)
```
