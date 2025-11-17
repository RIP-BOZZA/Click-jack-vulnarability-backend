from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.services.header_scanner import scan_headers
from app.services.selenium_scanner import run_selenium_poc
from app.services.report_generator import generate_report

router = APIRouter(prefix="/scan", tags=["Scan"])


class ScanRequest(BaseModel):
    target_url: HttpUrl


@router.post("/")
async def scan_clickjacking(request: ScanRequest):
    target = request.target_url

    # ---- Stage 1: Header Scan ----
    header_result = scan_headers(target)
    if "error" in header_result:
        raise HTTPException(status_code=400, detail=header_result["error"])

    xfo = header_result.get("x_frame_options")
    csp = header_result.get("content_security_policy")

    header_vulnerable = False
    if not xfo and not csp:
        header_vulnerable = True
    elif xfo and xfo.upper() in ["ALLOW-FROM", "ALLOWALL"]:
        header_vulnerable = True

    # ---- Stage 2: Selenium PoC ----
    selenium_result = run_selenium_poc(target)

    # ---- Final verdict ----
    vulnerable = header_vulnerable or selenium_result.get("iframe_worked", False)

    # ---- Generate report (HTML + PDF) ----
    report_meta = generate_report(
        {
            "target_url": str(target),
            "headers": header_result,
            "selenium": selenium_result,
            "final_vulnerable": vulnerable,
        }
    )

    # Prefer PDF if exists, otherwise HTML
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
