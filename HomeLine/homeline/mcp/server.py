from mcp.server.fastmcp import FastMCP
from homeline.db.database import SessionLocal
from homeline.schemas import listing, lead, faq
from homeline.services import listing_service, faq_service, lead_service

mcp = FastMCP("HomeLine Real Estate Assistant")

@mcp.tool()
def search_listings(city: str = None, min_price: float = None, max_price: float = None, min_beds: int = None) -> str:
    """Search for available real estate listings based on criteria."""
    db = SessionLocal()
    try:
        req = listing.SearchListingsRequest(
            city=city, min_price=min_price, max_price=max_price, min_beds=min_beds
        )
        return listing_service.search_listings(db, req)
    finally:
        db.close()

@mcp.tool()
def get_listing_details(listing_id: int) -> str:
    """Get detailed information about a specific listing by its ID."""
    db = SessionLocal()
    try:
        req = listing.GetListingDetailsRequest(listing_id=listing_id)
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
def create_lead(name: str, phone: str, query: str = None) -> str:
    """Create a new lead to save a caller's information."""
    db = SessionLocal()
    try:
        req = lead.CreateLeadRequest(name=name, phone=phone, query=query)
        return lead_service.create_lead(db, req)
    finally:
        db.close()

@mcp.tool()
def create_showing_request(listing_id: int, name: str, phone: str, preferred_time: str) -> str:
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
def create_callback_request(name: str, phone: str, reason: str = None) -> str:
    """Request a callback from a human agent."""
    db = SessionLocal()
    try:
        req = lead.CreateCallbackRequest(name=name, phone=phone, reason=reason)
        return lead_service.create_callback_request(db, req)
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
