from sqlalchemy.orm import Session
from sqlalchemy import or_

from homeline.db import models
from homeline.schemas import faq as schemas

def search_faqs(db: Session, request: schemas.SearchFAQRequest) -> str:
    # Basic keyword search on question or answer
    faqs = db.query(models.FAQ).filter(
        or_(
            models.FAQ.question.ilike(f"%{request.query}%"),
            models.FAQ.answer.ilike(f"%{request.query}%")
        )
    ).limit(3).all()

    if not faqs:
        return "I don't have an immediate answer to that question in my knowledge base. Would you like me to have an agent call you back?"
    
    return faqs[0].answer
