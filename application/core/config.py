from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class JWTSettings(BaseModel):

    private_key_path: Path = BASE_DIR / "security" / "private.pem"
    public_key_path: Path = BASE_DIR / "security" / "public.pem"
    algorithm: str = "RSA256"

class Settings(BaseSettings):

    # JWT Settings
    jwt_settings: JWTSettings = JWTSettings()

    # Database Settings
    DB_USER: str
    DB_PASS: int
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # FastAPI Settings
    BASE_FASTAPI_URL: str

    @property
    def get_session(self):
        
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()