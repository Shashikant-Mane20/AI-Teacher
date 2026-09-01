from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Teacher API"
    environment: str = "development"
    debug: bool = True
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "ai_teacher"
    jwt_secret: str = "change-this-development-secret-use-a-longer-local-secret-2026"
    jwt_expire_minutes: int = 1440
    frontend_url: str = "http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
