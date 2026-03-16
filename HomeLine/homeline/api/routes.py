from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from homeline.schemas import common, listing, lead, faq
from homeline.services import listing_service, lead_service, faq_service
from homeline.api.dependencies import get_db
from homeline.config import settings

api_router = APIRouter()

@api_router.get("/health")
def health_check():
    """Liveness probe."""
    return {"status": "healthy"}

@api_router.post("/dynamic-variables")
async def dynamic_variables(request: Request):
    """
    Webhook handler for Telnyx Dynamic Variables.
    """
    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
        
    return {
        "office_name": settings.OFFICE_NAME,
        "agent_name": settings.AGENT_NAME,
        "business_hours": settings.BUSINESS_HOURS,
        "service_areas": settings.SERVICE_AREAS,
        "featured_listing_city": settings.FEATURED_LISTING_CITY,
        "caller_phone": body.get("from") or body.get("caller_id") or "Unknown caller",
        "returning_caller": "False" 
    }

# Listings
@api_router.post("/tool/search-listings", response_model=common.WebhookResponse)
def search_listings(req: listing.SearchListingsRequest):
    from homeline.mcp.adapter import call_mcp_tool
    result = call_mcp_tool(
        "search_listings", 
        city=req.city, 
        max_price=req.max_price, 
        beds=req.min_beds
    )
    return common.WebhookResponse(response=result)

@api_router.post("/tool/get-listing-details", response_model=common.WebhookResponse)
def get_listing_details(req: listing.GetListingDetailsRequest):
    from homeline.mcp.adapter import call_mcp_tool
    result = call_mcp_tool(
        "get_listing_details", 
        listing_id=req.listing_id
    )
    return common.WebhookResponse(response=result)

# Leads & Activity
@api_router.post("/tool/create-lead", response_model=common.WebhookResponse)
def create_lead(req: lead.CreateLeadRequest):
    from homeline.mcp.adapter import call_mcp_tool
    # The webhook schema 'req.query' encompasses intent/area/budget. 
    # We map 'query' to 'intent' to fulfill the MCP signature requirement gracefully.
    result = call_mcp_tool(
        "create_lead", 
        name=req.name, 
        phone=req.phone, 
        intent=req.query or "General Inquiry"
    )
    return common.WebhookResponse(response=result)

@api_router.post("/tool/create-showing", response_model=common.WebhookResponse)
def create_showing(req: lead.CreateShowingRequest):
    from homeline.mcp.adapter import call_mcp_tool
    result = call_mcp_tool(
        "create_showing_request", 
        name=req.name, 
        phone=req.phone, 
        listing_id=req.listing_id, 
        preferred_time=req.preferred_time
    )
    return common.WebhookResponse(response=result)

@api_router.post("/tool/create-callback", response_model=common.WebhookResponse)
def create_callback(req: lead.CreateCallbackRequest):
    from homeline.mcp.adapter import call_mcp_tool
    result = call_mcp_tool(
        "create_callback_request", 
        name=req.name, 
        phone=req.phone, 
        reason=req.reason or "Callback requested by User"
    )
    return common.WebhookResponse(response=result)

# FAQ
@api_router.post("/tool/search-faq", response_model=common.WebhookResponse)
def search_faq(req: faq.SearchFAQRequest):
    from homeline.mcp.adapter import call_mcp_tool
    result = call_mcp_tool(
        "search_faq", 
        query=req.query
    )
    return common.WebhookResponse(response=result)
