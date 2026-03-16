import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # If running on Vercel, default to in-memory SQLite, else local file
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", 
        "sqlite:///:memory:" if os.environ.get("VERCEL") else "sqlite:///./homeline.db"
    )
    
    # Defaults for dynamic variables
    OFFICE_NAME: str = "HomeLine Realty"
    AGENT_NAME: str = "Sarah"
    BUSINESS_HOURS: str = "Monday to Friday 9 AM to 6 PM, weekends 10 AM to 4 PM"
    SERVICE_AREAS: str = "Springfield, Shelbyville, and Capital City"
    FEATURED_LISTING_CITY: str = "Springfield"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
