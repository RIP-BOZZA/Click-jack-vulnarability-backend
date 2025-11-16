import requests


def scan_headers(url: str):
    try:
        r = requests.get(url, timeout=10)
        headers = r.headers

        return {
            "x_frame_options": headers.get("X-Frame-Options"),
            "content_security_policy": headers.get("Content-Security-Policy"),
        }
    except Exception as e:
        return {"error": str(e)}
