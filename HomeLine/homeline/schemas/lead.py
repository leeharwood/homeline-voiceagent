from pydantic import BaseModel, Field
from typing import Optional

class CreateLeadRequest(BaseModel):
    name: str = Field(..., description="The name of the caller/lead.")
    phone: str = Field(..., description="The phone number for the lead.")
    query: Optional[str] = Field(None, description="Optional notes on what the lead was looking for.")

class CreateShowingRequest(BaseModel):
    listing_id: int = Field(..., description="The ID of the listing to show.")
    name: str = Field(..., description="Name of the person requesting the showing.")
    phone: str = Field(..., description="Phone number.")
    preferred_time: str = Field(..., description="When they want to view the property.")

class CreateCallbackRequest(BaseModel):
    name: str = Field(..., description="Name of the requester.")
    phone: str = Field(..., description="Phone number to call back.")
    reason: Optional[str] = Field(None, description="Reason they want a callback.")
