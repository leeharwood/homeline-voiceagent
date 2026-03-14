from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from homeline.db import models
from homeline.schemas import listing as schemas

def search_listings(db: Session, request: schemas.SearchListingsRequest) -> str:
    query = db.query(models.Listing).filter(models.Listing.status == "Active")
    if request.city:
        query = query.filter(models.Listing.city.ilike(f"%{request.city}%"))
    if request.min_price is not None:
        query = query.filter(models.Listing.price >= request.min_price)
    if request.max_price is not None:
        query = query.filter(models.Listing.price <= request.max_price)
    if request.min_beds is not None:
        query = query.filter(models.Listing.beds >= request.min_beds)
        
    listings = query.limit(5).all()
    
    if not listings:
        return "I couldn't find any listings matching those criteria right now."
        
    results = []
    for l in listings:
        results.append(f"Listing ID {l.id} is a {l.beds} bed {l.property_type} in {l.city} for ${l.price:,.0f}.")
    return "Here is what I found:\n" + "\n".join(results)

def get_listing_details(db: Session, request: schemas.GetListingDetailsRequest) -> str:
    listing = db.query(models.Listing).filter(models.Listing.id == request.listing_id).first()
    if not listing:
        return "I'm sorry, I couldn't find a listing with that ID."
    
    # Concise TTS friendly format
    details = f"Listing {listing.id} is located at {listing.address}, {listing.city}. " \
              f"It is a {listing.property_type} with {listing.beds} bedrooms and {listing.baths} bathrooms, " \
              f"spanning {listing.sqft} square feet. The asking price is ${listing.price:,.0f}. " \
              f"Description: {listing.description}"
    return details
