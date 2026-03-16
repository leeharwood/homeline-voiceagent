from mcp.server.fastmcp import FastMCP
from homeline.db.database import SessionLocal
from homeline.schemas import listing, lead, faq
from homeline.services import listing_service, faq_service, lead_service

mcp = FastMCP("HomeLine Real Estate Assistant")

@mcp.tool()
def search_listings(city: str | None = None, max_price: float | None = None, beds: int | None = None) -> str:
    """Search for available real estate listings based on criteria."""
    db = SessionLocal()
    try:
        req = listing.SearchListingsRequest(
            city=city, max_price=max_price, min_beds=beds
        )
        return listing_service.search_listings(db, req)
    finally:
        db.close()

@mcp.tool()
def get_listing_details(listing_id: int | None = None, address: str | None = None) -> str:
    """Get detailed information about a specific listing by its ID or address."""
    db = SessionLocal()
    try:
        # Note: listing_service expects listing_id currently. If address is passed and no ID, we fetch ID first.
        # But for stability with existing code, we will rely on ID for now, or you could extend the service.
        _id = listing_id
        if _id is None and address is not None:
            from homeline.db import models
            loc_listing = db.query(models.Listing).filter(models.Listing.address.ilike(f"%{address}%")).first()
            if loc_listing:
                 _id = loc_listing.id
            else:
                 return "I'm sorry, I couldn't find a listing at that address."
                
        if _id is None:
            return "Please provide a valid listing ID or address."

        req = listing.GetListingDetailsRequest(listing_id=_id)
        return listing_service.get_listing_details(db, req)
    finally:
        db.close()

@mcp.tool()
def search_faq(query: str) -> str:
    """Search the office FAQ for answers to common questions about hours, services, commissions, etc."""
    db = SessionLocal()
    try:
        req = faq.SearchFAQRequest(query=query)
        return faq_service.search_faqs(db, req)
    finally:
        db.close()

@mcp.tool()
def create_lead(name: str, phone: str, intent: str, area: str | None = None, budget: str | None = None, timeline: str | None = None) -> str:
    """Create a new lead to save a caller's information."""
    db = SessionLocal()
    try:
        query_details = f"Intent: {intent}"
        if area: query_details += f", Area: {area}"
        if budget: query_details += f", Budget: {budget}"
        if timeline: query_details += f", Timeline: {timeline}"

        req = lead.CreateLeadRequest(name=name, phone=phone, query=query_details)
        return lead_service.create_lead(db, req)
    finally:
        db.close()

@mcp.tool()
def create_showing_request(name: str, phone: str, listing_id: int, preferred_time: str) -> str:
    """Request a property showing for a specific listing."""
    db = SessionLocal()
    try:
        req = lead.CreateShowingRequest(
            listing_id=listing_id, name=name, phone=phone, preferred_time=preferred_time
        )
        return lead_service.create_showing_request(db, req)
    finally:
        db.close()

@mcp.tool()
def create_callback_request(name: str, phone: str, reason: str) -> str:
    """Request a callback from a human agent."""
    db = SessionLocal()
    try:
        req = lead.CreateCallbackRequest(name=name, phone=phone, reason=reason)
        return lead_service.create_callback_request(db, req)
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
