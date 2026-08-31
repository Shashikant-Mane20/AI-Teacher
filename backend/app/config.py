try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:  # pragma: no cover
    from pydantic import BaseSettings as PydanticBaseSettings

    class SettingsConfigDict(dict):
        pass

    class BaseSettings(PydanticBaseSettings):
        class Config:
            env_file = ".env"


class Settings(BaseSettings):
    app_name: str = "AI Teacher"
    environment: str = "development"
    debug: bool = True

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "ai_teacher"

    qdrant_url: str = "https://a1651baa-8a02-493b-ae7d-6262c3958631.us-west-1-0.aws.cloud.qdrant.io"
    qdrant_collection: str = "ai_teacher_docs"
    qdrant_api_key: str = ""

    redis_url: str = "redis://localhost:6379/0"
    allowed_languages: list[str] = ["en", "hi", "hinglish"]

    if "SettingsConfigDict" in globals():
        model_config = SettingsConfigDict(env_file=".env")
    else:
        class Config:
            env_file = ".env"


settings = Settings()
