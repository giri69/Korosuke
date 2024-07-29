from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
