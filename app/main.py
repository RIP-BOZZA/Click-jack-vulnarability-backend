from fastapi import FastAPI
from app.routers.scanner import router as scan_router
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI(
        title="Clickjacking Detection API",
        description="API for detecting clickjacking vulnerabilities using headers + Selenium PoC",
        version="1.0.0",
    )
    app.include_router(scan_router)
    return app


app = create_app()
app.mount("/reports", StaticFiles(directory="app/static/reports"), name="reports")
