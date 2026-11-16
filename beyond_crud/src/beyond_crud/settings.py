from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    
    def get_database_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
settings = Settings()


