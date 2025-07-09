from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import requests
from dotenv import load_dotenv
import uuid
from app.codegen.util import generate_flask_app_structure, zip_app_directory
import traceback

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "meta-llama/llama-3-70b-instruct"

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "output": ""})

@app.post("/", response_class=HTMLResponse)
async def generate_app(request: Request, prompt: str = Form(...)):
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": f"Build this app: {prompt}"}]
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    data = res.json()
    output = data["choices"][0]["message"]["content"] if "choices" in data and data["choices"] else ""
    return templates.TemplateResponse("index.html", {"request": request, "output": output})

@app.post("/generate")
async def generate_app_json(data: dict = Body(...)):
    prompt = data.get("prompt", "")
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": f"Build this app: {prompt}"}]
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    data = res.json()
    output = data["choices"][0]["message"]["content"] if "choices" in data and data["choices"] else ""
    return JSONResponse({"output": output})

@app.post("/build")
async def build_app(data: dict = Body(...)):
    try:
        print("/build called with data:", data)
        prompt = data.get("prompt", "")
        print("Prompt:", prompt)
        # Generate Flask app.py
        print("Calling OpenAI for app.py...")
        # Generate Flask app.py
        payload_app = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": f"Generate a minimal Flask app.py for: {prompt}. Use render_template for index.html."}]
        }
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        app_py_res = requests.post(OPENROUTER_API_URL, json=payload_app, headers=headers)
        app_py_data = app_py_res.json()
        app_py = app_py_data["choices"][0]["message"]["content"] if "choices" in app_py_data and app_py_data["choices"] else ""
        print("app.py generated.")
        # Generate index.html
        print("Calling OpenRouter for index.html...")
        payload_html = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": f"Generate a minimal HTML for the main page of this Flask app: {prompt}. Only the HTML body, no Flask code."}]
        }
        html_res = requests.post(OPENROUTER_API_URL, json=payload_html, headers=headers)
        html_data = html_res.json()
        html = html_data["choices"][0]["message"]["content"] if "choices" in html_data and html_data["choices"] else ""
        print("index.html generated.")
        # Save files
        app_id = str(uuid.uuid4())
        print("Saving files to:", app_id)
        app_path = generate_flask_app_structure(app_id, app_py, html)
        print("Files saved.")
        zip_path = zip_app_directory(app_path)
        print("App zipped at:", zip_path)
        zip_filename = os.path.basename(zip_path)
        download_url = f"/download/{zip_filename}"
        print("Returning download URL:", download_url)
        return JSONResponse({"download_url": download_url})
    except Exception as e:
        print("/build error:", e)
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download/{zip_filename}")
async def download_zip(zip_filename: str):
    from fastapi.responses import FileResponse
    zip_path = f"app/codegen/{zip_filename.replace('.zip','')}.zip"
    return FileResponse(zip_path, filename=zip_filename, media_type='application/zip')
