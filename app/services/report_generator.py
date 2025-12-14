import os
import uuid
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.config import settings

try:
    from weasyprint import HTML  # type: ignore

    WEASYPRINT_AVAILABLE = True
except Exception:
    WEASYPRINT_AVAILABLE = False


BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # app/
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
REPORT_DIR = settings.REPORT_DIR

os.makedirs(REPORT_DIR, exist_ok=True)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
)


def generate_report(scan_data: dict) -> dict:
    """
    Generate a beautiful HTML report (and a PDF if possible) for a scan.

    scan_data is expected to have:
        - target_url
        - headers
        - selenium
        - final_vulnerable
    """

    report_id = str(uuid.uuid4())
    html_filename = f"{report_id}.html"
    pdf_filename = f"{report_id}.pdf"

    html_path = os.path.join(REPORT_DIR, html_filename)
    pdf_path = os.path.join(REPORT_DIR, pdf_filename)

    template = env.get_template("report.html")

    context = {
        "report_id": report_id,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "target_url": scan_data.get("target_url"),
        "headers": scan_data.get("headers", {}),
        "selenium": scan_data.get("selenium", {}),
        "final_vulnerable": scan_data.get("final_vulnerable", False),
        "screenshot_url": None,
    }

    screenshot_name = (
        context["selenium"].get("screenshot") if context["selenium"] else None
    )
    if screenshot_name:
        context["screenshot_url"] = f"/reports/{screenshot_name}"

    rendered_html = template.render(**context)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    pdf_created = False
    if WEASYPRINT_AVAILABLE:
        try:
            HTML(string=rendered_html, base_url=BASE_DIR).write_pdf(pdf_path)
            pdf_created = True
        except Exception:
            pdf_created = False

    return {
        "report_id": report_id,
        "html_filename": html_filename,
        "pdf_filename": pdf_filename if pdf_created else None,
    }
