from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://korosuke_owner:a8KJEhfi0vgX@ep-floral-sun-a1v35x0f.ap-southeast-1.aws.neon.tech/korosuke?sslmode=require"
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
