from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    ENV:str
    DATABASE_URL:str
    REDIS_URL:str
    JWT_PUBLIC_KEY:str
    JWT_ALGORITHM: str =  "RS256"
    
    class Config:
        env_file = ".env"
        
settings = Settings()