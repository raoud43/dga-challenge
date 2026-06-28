import os

class Settings:
   
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

settings = Settings()