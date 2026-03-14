from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./homeline.db"
    
    # Defaults for dynamic variables
    OFFICE_NAME: str = "HomeLine Realty"
    AGENT_NAME: str = "Sarah"
    BUSINESS_HOURS: str = "Monday to Friday 9 AM to 6 PM, weekends 10 AM to 4 PM"
    SERVICE_AREAS: str = "Springfield, Shelbyville, and Capital City"
    FEATURED_LISTING_CITY: str = "Springfield"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
