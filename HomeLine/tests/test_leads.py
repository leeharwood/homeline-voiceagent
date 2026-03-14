from homeline.db.models import Lead, CallbackRequest

def test_create_lead(client, db_session):
    payload = {
        "name": "Alice Tester",
        "phone": "+15551234567",
        "query": "Looking for a nice condo"
    }
    response = client.post("/tool/create-lead", json=payload)
    assert response.status_code == 200
    assert "Alice Tester" in response.json()["response"]
    
    # Verify in DB
    lead = db_session.query(Lead).filter_by(name="Alice Tester").first()
    assert lead is not None
    assert lead.phone == "+15551234567"

def test_create_callback(client, db_session):
    payload = {
        "name": "Bob NeedsCall",
        "phone": "+19998887777",
        "reason": "Need legal advice on mortgage"
    }
    response = client.post("/tool/create-callback", json=payload)
    assert response.status_code == 200
    assert "requested a callback for Bob" in response.json()["response"]
    
    req = db_session.query(CallbackRequest).filter_by(name="Bob NeedsCall").first()
    assert req is not None
    assert req.reason == "Need legal advice on mortgage"
