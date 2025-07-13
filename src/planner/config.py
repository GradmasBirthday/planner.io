from typing import List

class Settings:
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000"
    ]
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

settings = Settings() 