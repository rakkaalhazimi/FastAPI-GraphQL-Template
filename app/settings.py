from functools import lru_cache
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


# This default read from env variables first
# then env file
class Settings(BaseSettings):
    api_key: str
    secret_key: str  # for JWT
    
    temp_folder: str = "temp"
    
    sqlite_db_name: str = "second.db"
    database_url: str
    
    # Load env variables from multiple files
    # ../.env for local
    # /volume/.env for GCP Cloud Run
    model_config = SettingsConfigDict(env_file=[".env", "../.env", "/volume/.env"], extra="ignore")

# Cache settings on every request
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

if not os.path.exists(settings.temp_folder):
    os.mkdir(settings.temp_folder)
    
if not os.path.exists(settings.sqlite_db_name):
    open(settings.sqlite_db_name, "w").close()