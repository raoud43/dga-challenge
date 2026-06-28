import os

class Settings:
   
   raw_url = os.getenv("BACKEND_URL", "https://dga-backend-production-ea1f.up.railway.app")
   BACKEND_URL = raw_url.rstrip('/')
settings = Settings()