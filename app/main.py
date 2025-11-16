from fastapi import FastAPI


def create_app():
    app = FastAPI(
        title="Clickjacking Detection API",
        description="API for detecting clickjacking vulnerabilities using headers + Selenium PoC",
        version="1.0.0",
    )

    # Routers will be added later
    # app.include_router(scan_router)

    return app


app = create_app()
