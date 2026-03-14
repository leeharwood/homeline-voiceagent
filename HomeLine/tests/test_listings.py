from homeline.db.models import Listing

def test_search_listings_empty(client):
    response = client.post("/tool/search-listings", json={"city": "Nowhere"})
    assert response.status_code == 200
    assert "I couldn't find any listings matching those criteria right now." in response.json()["response"]

def test_search_listings_with_data(client, db_session):
    # Setup test data
    test_listing = Listing(
        address="101 Test Ave", 
        city="Testville", 
        price=150000, 
        beds=3, 
        baths=2, 
        property_type="House"
    )
    db_session.add(test_listing)
    db_session.commit()
    
    # Query via API
    response = client.post("/tool/search-listings", json={"city": "Testville"})
    assert response.status_code == 200
    assert "Testville" in response.json()["response"]
    assert "150,000" in response.json()["response"]

def test_get_listing_details(client, db_session):
    response = client.post("/tool/get-listing-details", json={"listing_id": 9999})
    assert response.status_code == 200
    assert "couldn't find a listing with that ID" in response.json()["response"]
