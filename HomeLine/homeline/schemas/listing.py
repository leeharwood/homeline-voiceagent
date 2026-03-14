from pydantic import BaseModel, Field

class SearchListingsRequest(BaseModel):
    city: str | None = Field(None, description="City to search in.")
    min_price: float | None = Field(None, description="Minimum price filter.")
    max_price: float | None = Field(None, description="Maximum price filter.")
    min_beds: int | None = Field(None, description="Minimum number of beds.")

class GetListingDetailsRequest(BaseModel):
    listing_id: int = Field(..., description="The unique ID of the property listing.")
