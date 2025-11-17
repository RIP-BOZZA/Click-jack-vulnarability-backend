import os
import uuid
import tempfile
from selenium.webdriver.common.by import By
from app.utils.selenium_driver import get_driver
from app.core.config import settings
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader("app/templates"))


def run_selenium_poc(target_url: str):
    driver = None
    try:
        driver = get_driver(headless=settings.SELENIUM_HEADLESS)

        # ---- Create fake attacker page ----
        template = env.get_template("attacker_template.html")
        html = template.render(target_url=target_url)

        temp_html = os.path.join(tempfile.gettempdir(), f"poc_{uuid.uuid4()}.html")
        with open(temp_html, "w") as f:
            f.write(html)

        driver.get(f"file:///{temp_html}")

        # ---- Check if iframe loads ----
        iframe_working = True
        try:
            driver.switch_to.frame(0)
            title = driver.title
            driver.switch_to.default_content()
        except Exception:
            iframe_working = False
            title = None

        # ---- Screenshot Evidence ----
        screenshot_name = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.join(settings.REPORT_DIR, screenshot_name)
        driver.save_screenshot(screenshot_path)

        return {
            "iframe_worked": iframe_working,
            "page_title": title,
            "screenshot": screenshot_name,
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if driver:
            driver.quit()
