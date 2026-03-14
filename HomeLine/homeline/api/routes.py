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
        "caller_phone": body.get("caller_id", "Unknown caller"),
        "returning_caller": "False" 
    }

# Listings
@api_router.post("/tool/search-listings", response_model=common.WebhookResponse)
def search_listings(req: listing.SearchListingsRequest, db: Session = Depends(get_db)):
    result = listing_service.search_listings(db, req)
    return common.WebhookResponse(response=result)

@api_router.post("/tool/get-listing-details", response_model=common.WebhookResponse)
def get_listing_details(req: listing.GetListingDetailsRequest, db: Session = Depends(get_db)):
    result = listing_service.get_listing_details(db, req)
    return common.WebhookResponse(response=result)

# Leads & Activity
@api_router.post("/tool/create-lead", response_model=common.WebhookResponse)
def create_lead(req: lead.CreateLeadRequest, db: Session = Depends(get_db)):
    result = lead_service.create_lead(db, req)
    return common.WebhookResponse(response=result)

@api_router.post("/tool/create-showing", response_model=common.WebhookResponse)
def create_showing(req: lead.CreateShowingRequest, db: Session = Depends(get_db)):
    result = lead_service.create_showing_request(db, req)
    return common.WebhookResponse(response=result)

@api_router.post("/tool/create-callback", response_model=common.WebhookResponse)
def create_callback(req: lead.CreateCallbackRequest, db: Session = Depends(get_db)):
    result = lead_service.create_callback_request(db, req)
    return common.WebhookResponse(response=result)

# FAQ
@api_router.post("/tool/search-faq", response_model=common.WebhookResponse)
def search_faq(req: faq.SearchFAQRequest, db: Session = Depends(get_db)):
    result = faq_service.search_faqs(db, req)
    return common.WebhookResponse(response=result)
