from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME:str
    ENV:str
    DATABASE_URL:str
    REDIS_URL:str
    JWT_PUBLIC_KEY:str
    JWT_ALGORITHM: str =  "RS256"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_URL: str 
    
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid",
    )
        
settings = Settings()