import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Centralized application configuration settings."""
    APP_NAME: str = "FAQ Management System"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(24).hex())
    DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://valentin:root@db:5432/faq_db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CACHE_TIMEOUT: int = int(os.getenv("CACHE_TIMEOUT", "300"))
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", os.urandom(24).hex())
    JWT_ACCESS_TOKEN_EXPIRES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))
    UPLOAD_FOLDER: Path = Path(os.getenv("UPLOAD_FOLDER", "uploads"))
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16MB
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_ENDPOINT", "http://ollama:11434")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")

    @classmethod
    def ensure_upload_folder_exists(cls) -> None:
        """Ensure the upload folder exists with correct permissions."""
        cls.UPLOAD_FOLDER.mkdir(exist_ok=True, parents=True)
        os.chmod(cls.UPLOAD_FOLDER, 0o755)

settings = Settings()
settings.ensure_upload_folder_exists()