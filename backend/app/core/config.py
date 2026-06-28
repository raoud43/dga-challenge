from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    BACKEND_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

    # الطريقة الحديثة لتعريف ملف الـ env
    model_config = SettingsConfigDict(env_file=".env")

# نقوم بإنشاء كائن واحد
settings = Settings()