from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
import os
from .scanner import perform_scan

from app.services.header_scanner import scan_headers
from app.services.selenium_scanner import run_selenium_poc
from app.services.report_generator import generate_report



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)



ui_router = APIRouter(prefix="", tags=["UI"])



@ui_router.get("/", response_class=HTMLResponse)
async def scan_ui(request: Request):
    return templates.TemplateResponse("scan_ui.html", {"request": request, "result": None, "error": None})


@ui_router.post("/", response_class=HTMLResponse)
async def scan_ui_post(request: Request, target_url: str = Form(...)):
    result = perform_scan(target_url)
    if "error" in result:
        return templates.TemplateResponse("scan_ui.html", {"request": request, "result": None, "error": result["error"], "target": target_url})
    return templates.TemplateResponse("scan_ui.html", {"request": request, "result": result, "error": None, "target": target_url})
