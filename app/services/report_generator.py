import uuid
from app.core.config import settings
import os


def generate_report(data: dict):
    report_id = str(uuid.uuid4()) + ".txt"
    report_path = os.path.join(settings.REPORT_DIR, report_id)

    with open(report_path, "w") as f:
        f.write("Clickjacking Scan Report\n")
        f.write(str(data))

    return report_id
