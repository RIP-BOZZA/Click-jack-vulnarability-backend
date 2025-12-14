import os
import uuid
import json
import time
import tempfile
from selenium.webdriver.common.by import By
from app.utils.selenium_driver import get_driver
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader("app/templates"))

def run_selenium_poc(target_url):
    driver = None
    try:
        target_url = str(target_url)

        driver = get_driver(headless=settings.SELENIUM_HEADLESS)

        driver.get(target_url)
        time.sleep(4)

        logs = driver.get_log("performance")

        xfo = None
        csp = None

        for entry in logs:
            message = json.loads(entry["message"])["message"]

            if message["method"] == "Network.responseReceived":
                response = message["params"]["response"]
                response_url = response.get("url", "")

                if response_url.startswith(target_url):
                    headers = response.get("headers", {})

                    xfo = headers.get("x-frame-options")
                    csp = headers.get("content-security-policy")
                    break

        clickjacking_vulnerable = not (
            (xfo and xfo.lower() in ["deny", "sameorigin"]) or
            (csp and "frame-ancestors" in csp.lower())
        )

        template = env.get_template("attacker_template.html")
        html = template.render(target_url=target_url)

        temp_html = os.path.join(tempfile.gettempdir(), f"poc_{uuid.uuid4()}.html")
        with open(temp_html, "w") as f:
            f.write(html)

        driver.get(f"file:///{temp_html}")
        time.sleep(3)

        screenshot_name = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.join(settings.REPORT_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)

        return {
            "target": target_url,
            "iframe_worked": clickjacking_vulnerable,
            "x_frame_options": xfo,
            "content_security_policy": csp,
            "screenshot": screenshot_name,
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if driver:
            driver.quit()
