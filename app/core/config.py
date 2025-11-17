from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    REPORT_DIR: str = "app/static/reports"
    SELENIUM_HEADLESS: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
