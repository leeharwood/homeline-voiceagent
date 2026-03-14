from sqlalchemy.orm import Session
from homeline.db import models
from homeline.schemas import lead as schemas

def create_lead(db: Session, request: schemas.CreateLeadRequest) -> str:
    db_lead = models.Lead(**request.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return f"Great, I've noted down the details for {request.name}. Thank you."

def create_callback_request(db: Session, request: schemas.CreateCallbackRequest) -> str:
    db_req = models.CallbackRequest(**request.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return f"I've requested a callback for {request.name}. An agent will call you at {request.phone} soon."

def create_showing_request(db: Session, request: schemas.CreateShowingRequest) -> str:
    db_req = models.ShowingRequest(**request.model_dump())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return f"I've submitted a showing request for listing ID {request.listing_id} for {request.preferred_time}. Someone will reach out to confirm."
