import os

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./noss.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # AI Services
    AI_SERVICE_TYPE: str = os.getenv("AI_SERVICE_TYPE", "hybrid")  # azure | ollama | hybrid
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "localhost")
    OLLAMA_PORT: int = int(os.getenv("OLLAMA_PORT", 11434))
    
    # Vector Database
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    
    # Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./upload")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024  # 50MB default
    ALLOWED_FILE_TYPES: list = ["pdf", "docx", "doc", "txt", "xlsx", "xls"]
    
    # CORS
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE: int = int(os.getenv("MAX_PAGE_SIZE", "100"))

settings = Settings()
