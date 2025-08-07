from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from utils import call_llm

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, user_input: str = Form(...)):
    print(f"收到用户输入: {user_input[:50]}...")  # 日志记录
    
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    print("开始调用LLM...")  # 日志记录
    result = call_llm(user_input, system_prompt)
    print(f"LLM响应完成，长度: {len(result)} 字符")  # 日志记录
    
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
