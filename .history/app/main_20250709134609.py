from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv

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
