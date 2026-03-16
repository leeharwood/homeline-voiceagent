from sqlalchemy.orm import Session
from homeline.db.models import Listing, FAQ

def seed_database(db: Session):
    # Check if we already have data
    if db.query(Listing).first():
        return

    # 8 Sample Listings
    listings = [
        Listing(
            address="123 Maple Street", city="Springfield", price=450000, beds=3, baths=2.0, sqft=1800,
            property_type="Single Family",
            description="A beautiful single-family home with a large backyard and newly renovated kitchen.",
            status="Active"
        ),
        Listing(
            address="456 Oak Avenue", city="Springfield", price=320000, beds=2, baths=1.5, sqft=1200,
            property_type="Townhouse",
            description="Cozy townhouse close to downtown, perfect for first-time buyers.",
            status="Active"
        ),
        Listing(
            address="789 Pine Road", city="Shelbyville", price=650000, beds=4, baths=3.0, sqft=2500,
            property_type="Single Family",
            description="Spacious 4-bedroom home in a quiet neighborhood with a two-car garage.",
            status="Active"
        ),
        Listing(
            address="101 Elm Street", city="Capital City", price=850000, beds=5, baths=4.0, sqft=3200,
            property_type="Single Family",
            description="Luxury estate with a pool, open floor plan, and premium finishes.",
            status="Active"
        ),
        Listing(
            address="202 Birch Blvd", city="Springfield", price=275000, beds=2, baths=2.0, sqft=1100,
            property_type="Condo",
            description="Modern condo with stunning city views and gym access.",
            status="Active"
        ),
        Listing(
            address="303 Cedar Lane", city="Shelbyville", price=500000, beds=3, baths=2.5, sqft=2000,
            property_type="Single Family",
            description="Charming suburban house with a large deck and fenced yard.",
            status="Active"
        ),
        Listing(
            address="404 Walnut Drive", city="Capital City", price=410000, beds=3, baths=2.0, sqft=1600,
            property_type="Townhouse",
            description="Newly built townhouse with smart home features.",
            status="Active"
        ),
        Listing(
            address="505 Ash Court", city="Springfield", price=550000, beds=4, baths=2.5, sqft=2200,
            property_type="Single Family",
            description="Family home located in a top-rated school district.",
            status="Active"
        )
    ]
    
    # 12 Sample FAQs
    faqs = [
        FAQ(question="What are your office hours?", answer="We are open Monday to Friday from 9 AM to 6 PM, and on weekends from 10 AM to 4 PM."),
        FAQ(question="What areas do you serve?", answer="We serve Springfield, Shelbyville, and Capital City."),
        FAQ(question="How do I schedule a showing?", answer="You can request a showing over the phone with me, and I will collect your details and preferred time."),
        FAQ(question="Do you help with financing?", answer="Our team can connect you with trusted local lenders, but I recommend speaking directly with a human agent for specific financing advice."),
        FAQ(question="What is the standard commission rate?", answer="Commission rates vary by property and agreement. Please speak with an agent for detailed information."),
        FAQ(question="Can I sell my home through your office?", answer="Absolutely! We handle both buying and selling. An agent can provide a free market analysis of your home."),
        FAQ(question="Are pets allowed in the listings?", answer="Pet policies depend on the specific property or HOA. I'd be happy to check the details of a specific listing for you."),
        FAQ(question="How long does it typically take to close?", answer="On average, closing takes 30 to 45 days after an offer is accepted, depending on financing and inspections."),
        FAQ(question="Do I need to be pre-approved before viewing homes?", answer="While not strictly required for a first showing, being pre-approved makes you a stronger buyer when you're ready to make an offer."),
        FAQ(question="Can I get a virtual tour?", answer="Many of our listings offer virtual tours. If you're interested in a specific property, an agent can set that up."),
        FAQ(question="What should I do to prepare my house for sale?", answer="Decluttering, minor repairs, and staging make a big difference. An agent can walk through and give personalized recommendations."),
        FAQ(question="How can I speak to a human agent?", answer="I can create a callback request for you right now, and one of our agents will reach out to you shortly.")
    ]

    db.add_all(listings)
    db.add_all(faqs)
    db.commit()
