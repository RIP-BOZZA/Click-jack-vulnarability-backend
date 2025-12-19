from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
import os

from app.services.header_scanner import scan_headers
from app.services.selenium_scanner import run_selenium_poc
from app.services.report_generator import generate_report

router = APIRouter(prefix="/scan", tags=["Scan"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


class ScanRequest(BaseModel):
    target_url: HttpUrl


def perform_scan(target: str) -> dict:
    """Run the header + selenium checks and generate a report. Returns the same
    response shape used by the JSON API.
    """
    header_result = scan_headers(target)
    if "error" in header_result:
        return {"error": header_result["error"]}

    xfo = header_result.get("x_frame_options")
    csp = header_result.get("content_security_policy")

    header_vulnerable = False
    if not xfo and not csp:
        header_vulnerable = True
    elif xfo and xfo.upper() in ["ALLOW-FROM", "ALLOWALL"]:
        header_vulnerable = True

    selenium_result = run_selenium_poc(target)

    vulnerable = header_vulnerable or selenium_result.get("iframe_worked", False)

    report_meta = generate_report(
        {
            "target_url": str(target),
            "headers": header_result,
            "selenium": selenium_result,
            "final_vulnerable": vulnerable,
        }
    )

    download_file = report_meta["pdf_filename"] or report_meta["html_filename"]
    report_url = f"/reports/{download_file}"
    response_data = {
        "target": str(target),
        "header_scan": header_result,
        "selenium_test": selenium_result,
        "vulnerable": vulnerable,
        "report_id": report_meta["report_id"],
        "report_url": report_url,
        "report_files": {
            "html": f"/reports/{report_meta['html_filename']}",
            "pdf": (
                f"/reports/{report_meta['pdf_filename']}"
                if report_meta["pdf_filename"]
                else None
            ),
        },
    }

    return response_data


@router.post("/")
async def scan_clickjacking(request: ScanRequest):
    result = perform_scan(str(request.target_url))
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/ui", response_class=HTMLResponse)
async def scan_ui(request: Request):
    return templates.TemplateResponse("scan_ui.html", {"request": request, "result": None, "error": None})


@router.post("/ui", response_class=HTMLResponse)
async def scan_ui_post(request: Request, target_url: str = Form(...)):
    result = perform_scan(target_url)
    if "error" in result:
        return templates.TemplateResponse("scan_ui.html", {"request": request, "result": None, "error": result["error"], "target": target_url})
    return templates.TemplateResponse("scan_ui.html", {"request": request, "result": result, "error": None, "target": target_url})


