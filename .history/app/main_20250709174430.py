from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv
import uuid
from app.codegen.util import generate_flask_app_structure, zip_app_directory

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "output": ""})

@app.post("/", response_class=HTMLResponse)
async def generate_app(request: Request, prompt: str = Form(...)):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Build this app: {prompt}"}]
    )
    output = response.choices[0].message.content
    return templates.TemplateResponse("index.html", {"request": request, "output": output})

@app.post("/generate")
async def generate_app_json(data: dict = Body(...)):
    prompt = data.get("prompt", "")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Build this app: {prompt}"}]
    )
    output = response.choices[0].message.content
    return JSONResponse({"output": output})

@app.post("/build")
async def build_app(data: dict = Body(...)):
    prompt = data.get("prompt", "")
    # Generate Flask app.py
    app_py_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate a minimal Flask app.py for: {prompt}. Use render_template for index.html."}]
    )
    app_py = app_py_response.choices[0].message.content
    # Generate index.html
    html_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate a minimal HTML for the main page of this Flask app: {prompt}. Only the HTML body, no Flask code."}]
    )
    html = html_response.choices[0].message.content
    # Save files
    app_id = str(uuid.uuid4())
    app_path = generate_flask_app_structure(app_id, app_py, html)
    zip_path = zip_app_directory(app_path)
    zip_filename = os.path.basename(zip_path)
    download_url = f"/download/{zip_filename}"
    return JSONResponse({"download_url": download_url})

@app.get("/download/{zip_filename}")
async def download_zip(zip_filename: str):
    from fastapi.responses import FileResponse
    zip_path = f"app/codegen/{zip_filename.replace('.zip','')}.zip"
    return FileResponse(zip_path, filename=zip_filename, media_type='application/zip')
