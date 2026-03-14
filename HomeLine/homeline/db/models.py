from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from homeline.db.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, nullable=False)
    city = Column(String, index=True)
    price = Column(Float, nullable=False)
    beds = Column(Integer)
    baths = Column(Float)
    sqft = Column(Integer)
    description = Column(Text)
    property_type = Column(String)
    status = Column(String, default="Active")

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True, nullable=False)
    answer = Column(Text, nullable=False)

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    query = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CallbackRequest(Base):
    __tablename__ = "callback_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    reason = Column(Text)
    status = Column(String, default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ShowingRequest(Base):
    __tablename__ = "showing_requests"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    preferred_time = Column(String, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
