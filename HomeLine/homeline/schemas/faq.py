from pydantic import BaseModel, Field

class SearchFAQRequest(BaseModel):
    query: str = Field(..., description="The topic to search the FAQ for.")
