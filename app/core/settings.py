from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic import computed_field

load_dotenv()

class Settings(BaseSettings):
    DB_NAME: str    
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    ALG: str
    SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    OPENAI_API_KEY: str
    

    @computed_field
    @property
    def DB_URL(self) -> str:
        password = quote_plus(self.DB_PASS)
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
