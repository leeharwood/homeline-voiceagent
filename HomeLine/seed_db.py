import os
from sqlalchemy.orm import Session
from homeline.db import models
from homeline.db.database import engine, SessionLocal, init_db

# Auto-create all tables
init_db()

def seed():
    db = SessionLocal()
    
    # Check if DB is already seeded to prevent duplicates
    if db.query(models.Listing).first():
        print("Database already seeded")
        return
        
    print("Seeding realistic real-estate listings...")
    listings = [
        {"address": "1234 Maplewood Drive", "city": "Springfield", "price": 450000, "beds": 3, "baths": 2, "sqft": 1850, "description": "Beautiful mid-century modern family home with a fully fenced large backyard and newly renovated kitchen.", "property_type": "Single Family"},
        {"address": "4501 Oak Avenue", "city": "Springfield", "price": 525000, "beds": 4, "baths": 3, "sqft": 2400, "description": "Spacious two-story house located near downtown. Features a finished basement, hardwood floors, and a two-car garage.", "property_type": "Single Family"},
        {"address": "789 Pine Road, Unit 4B", "city": "Shelbyville", "price": 310000, "beds": 2, "baths": 1.5, "sqft": 1200, "description": "Cozy starter condo in a quiet, well-maintained neighborhood. HOA includes water, trash, and exterior maintenance.", "property_type": "Condo"},
        {"address": "321 Elm Street", "city": "Springfield", "price": 650000, "beds": 5, "baths": 3.5, "sqft": 3200, "description": "Luxury executive home with modern amenities, smart home integrations, an open floor plan, and a private pool.", "property_type": "Single Family"},
        {"address": "654 Cedar Lane, Loft 12", "city": "Shelbyville", "price": 275000, "beds": 1, "baths": 1, "sqft": 900, "description": "Modern downtown loft featuring exposed brick walls, high ceilings, and industrial design elements.", "property_type": "Condo"},
        {"address": "987 Birch Boulevard", "city": "Capital City", "price": 890000, "beds": 4, "baths": 4, "sqft": 3600, "description": "Stunning estate perched on a hill with panoramic views of the city. Includes a gourmet chef's kitchen and home theater.", "property_type": "Single Family"},
        {"address": "159 Cherry Court", "city": "Capital City", "price": 425000, "beds": 3, "baths": 2.5, "sqft": 1650, "description": "Recently renovated townhouse with an attached garage, quartz countertops, and a private back patio.", "property_type": "Townhouse"},
        {"address": "753 Ash Drive", "city": "Springfield", "price": 380000, "beds": 2, "baths": 2, "sqft": 1400, "description": "Charming historic bungalow with original woodwork, stained glass details, and a cozy front porch.", "property_type": "Single Family"}
    ]
    
    for l in listings:
        db.add(models.Listing(**l))
        
    print("Seeding realistic FAQs...")
    faqs = [
        {"question": "What are your business hours?", "answer": "Our agents are available Monday through Friday from 9 AM to 6 PM, and weekends from 10 AM to 4 PM. We also have an on-call agent for emergencies outside those hours."},
        {"question": "Do you handle rentals or just sales?", "answer": "At HomeLine Realty, we currently focus exclusively on residential and commercial sales. We do not handle rentals or property management at this time."},
        {"question": "How much does it cost to list a home with you?", "answer": "Our standard commission is typically 6%, which is split evenly between the buyer's agent and the seller's agent. However, commissions can sometimes be negotiated depending on the property. We'd love to schedule a listing appointment to discuss specifics."},
        {"question": "Do you operate outside of Springfield?", "answer": "Yes! Our core service areas include Springfield, Shelbyville, and Capital City. We have specialists familiar with the market trends in all three regions."},
        {"question": "How do I schedule a showing?", "answer": "I can actually help you with that right now directly over the phone! Just let me know the address or Listing ID and your preferred time, and I will submit a showing request for an agent to confirm with you."},
        {"question": "Can I get a human agent to call me back?", "answer": "Absolutely. I can take down your name, phone number, and the reason for your call, and I'll have an agent return your call as soon as possible."},
        {"question": "How long does it typically take to close on a house?", "answer": "A typical closing takes 30 to 45 days after an offer is accepted. This timeline depends heavily on the buyer's financing process and how quickly the bank can complete the appraisal and underwriting."},
        {"question": "Do I need to be pre-approved for a mortgage before looking at houses?", "answer": "While not strictly required by law, we highly recommend getting a mortgage pre-approval first. It helps you understand exactly what you can afford, and makes your offer much stronger when you find the home you love."},
        {"question": "What is earnest money?", "answer": "Earnest money is a deposit made by the buyer to the seller when signing a contract to show good faith. It is typically 1% to 3% of the purchase price and is held in escrow until closing."},
        {"question": "Are your agents licensed?", "answer": "Yes, all of our agents are fully licensed REALTORS® in the state and adhere to a strict ethical code."},
        {"question": "Can you help me find a real estate lawyer?", "answer": "Yes, we have a network of trusted standard and commercial real estate attorneys that we collaborate with heavily during the contracting phase. We can provide recommendations upon request."},
        {"question": "What is a home inspection?", "answer": "A home inspection is a professional, third-party examination of the condition of a home. We strongly recommend that all our buyers get one before finalizing their purchase to uncover any hidden electrical, plumbing, or structural issues."}
    ]
    
    for f in faqs:
        db.add(models.FAQ(**f))
        
    db.commit()
    print("Database seeded successfully.")
    db.close()

if __name__ == "__main__":
    seed()
