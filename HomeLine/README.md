# HomeLine - Real Estate Voice AI Assistant

HomeLine is a production-ready Minimum Viable Product (MVP) designed to power a real estate customer service voice AI assistant. It integrates with Telnyx AI Assistant to handle incoming calls, answer FAQs, search for property listings, collect lead information, and book showing or callback requests.

## 🏗️ Architecture

HomeLine integrates deeply with the **Model Context Protocol (MCP)** while preserving a standard HTTP webhook layer required by the Telnyx AI Assistant.

```text
Caller
 └─→ Telnyx AI Assistant
      └─→ Dynamic Variables & Webhook Tools (HTTP POST)
           └─→ FastAPI Backend (`/api/tool/*`)
                └─→ MCP-Backed Business Logic (shared `*_impl` functions)
                     ├─→ Custom FastMCP Server (`homeline/mcp/server.py`)
                     └─→ Service Logic & SQLite Database
```
### Why MCP in this architecture?
By sharing the underlying implementation functions between the FastAPI webhooks and the **MCP Server**, we ensure the backend capabilities are defined strictly as modular tools without relying on private SDK internals. This makes HomeLine a true *MCP-backed* application, capable of exposing those exact same tools directly to an LLM desktop client (like Claude) or any other MCP-compatible orchestration layer.

### Tradeoffs
**Why does Telnyx still call webhook endpoints if MCP is used behind the backend?**
- **Simplicity vs. Distribution:** Implementing shared logic functions behind the webhooks avoids introducing complex, distributed infrastructure (like spinning up a separate MCP transport service and connecting it to Telnyx).
- **Vendor Compatibility:** Telnyx AI Assistant natively supports RESTful POST webhooks rather than raw MCP SSE/Stdio transports. This routing pattern maintains 100% compatibility with Telnyx while letting the backend neatly organize around the MCP specification.

- **FastAPI Endpoints**: Centralized routing in `homeline/api/routes.py` handling inbound webhook formats.
- **MCP Server Layer**: A `FastMCP` server defining tools:
  - `search_listings(city, max_price, beds)`
  - `get_listing_details(listing_id, address)`
  - `create_lead(name, phone, intent, area, budget, timeline)`
  - `create_showing_request(name, phone, listing_id, preferred_time)`
  - `create_callback_request(name, phone, reason)`
  - `search_faq(query)`
- **Pydantic Schemas**: Structured request payloads in `homeline/schemas`. Responses are concise and conversational for optimal voice Text-To-Speech (TTS).
- **Service & Database Layers**: Abstracted business logic backed by SQLAlchemy. Swappable to PostgreSQL via `.env`.

---

## 🚀 Local Setup

1. **Clone or Download the Repository**
   Navigate to the project root: `/Users/macpro2019lee/Interview/Telnyx/HomeLine/`

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Copy the example config and edit if necessary (uses `pydantic-settings`).
   ```bash
   cp .env.example .env
   ```

5. **Seed the Database**
   This script will create the database schema and populate it with realistic real-estate listings and FAQs.
   ```bash
   python3 seed_db.py
   ```

6. **Run the API Tests**
   ```bash
   python3 -m pytest tests/
   ```

7. **Run the FastAPI Server**
   ```bash
   uvicorn homeline.main:app --reload --port 8000
   ```

8. **Run the local MCP Server (Test MCP natively)**
   You can interact directly with the underlying MCP tools locally without the voice assistant via the MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector mcp run homeline/mcp/server.py
   ```
   Or connect it directly to an MCP-compatible client like Claude Desktop.

9. **Run Ngrok for Local Webhooks (Optional)**
   To test with Telnyx locally, expose your local port 8000 using Ngrok:
   ```bash
   ngrok http 8000
   ```
   *Use the forwarded `https` URL in your Telnyx Assistant tool webhooks.*

---

## ☁️ Deployment on Vercel

This project is tailored for instant serverless deployment on [Vercel](https://vercel.com/).

1. **Install Vercel CLI** (or connect your GitHub repo to Vercel).
2. **Deploy** by running from the project root:
   ```bash
   vercel
   ```
3. **Environment Variables**:
   By default, Vercel provides a read-only filesystem. The application detects the Vercel environment and safely falls back to seeding an in-memory database on every function cold-start, strictly for demo purposes.
   To persist data later, simply add a `DATABASE_URL` to Vercel pointing to a PostgreSQL database.

---

## 📞 Telnyx AI Assistant Configuration

Go to your Telnyx Portal, navigate to AI Assistants, and create a new Assistant.

### 1. Dynamic Variables Webhook
Point this to your Ngrok or Vercel URL so the prompt can be built dynamically on every call.
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/dynamic-variables`
- **Method**: `POST`

**Sample Webhook Response from this endpoint:**
```json
{
  "office_name": "HomeLine Realty",
  "agent_name": "Sarah",
  "business_hours": "Monday to Friday 9 AM to 6 PM, weekends 10 AM to 4 PM",
  "service_areas": "Springfield, Shelbyville, and Capital City",
  "featured_listing_city": "Springfield",
  "caller_phone": "+15551234567",
  "returning_caller": "False"
}
```

### 2. General Settings
- **Greeting**:  
  `"Hello! Thank you for calling {{office_name}}. My name is {{agent_name}}. How can I help you today? We serve {{service_areas}}."`

### 3. System Instructions
Use the following prompt format in the Telnyx Portal:
```text
You are a helpful and professional customer service AI voice assistant for {{office_name}}. 
Your goal is to answer real estate questions, search for property listings, qualify leads, and create callback or property showing requests for human agents to follow up on.

Context:
- Our business hours are {{business_hours}}. 
- The caller's phone number is {{caller_phone}}.

CRITICAL BEHAVIORS:
1. NEVER invent facts about listings. Always use the search-listings or get-listing-details tools to find accurate information.
2. Before booking a showing or creating a callback request, ensure you have collected the caller's name and gently confirmed their phone number (use {{caller_phone}} as your reference, but always ask the caller if that is the best number to reach them to be sure).
3. If the caller asks for legal, financing, or contract-specific advice, politely decline and offer to have a licensed human agent call them back via the create-callback tool.
4. Keep all responses clear, natural, and concise. You are speaking to a human over the phone, so avoid reading out code, long lists, or JSON. Do not overwhelm the caller with more than two options at a time.
```

### 4. Client Tools (Webhooks)
Add the following Webhook Tools in the Telnyx portal:

**Tool 1: search-listings**
- **Description**: Search for available real estate listings based on the user's criteria.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/search-listings`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "properties": {
      "city": { "type": "string", "description": "City to search in." },
      "min_price": { "type": "number", "description": "Minimum price." },
      "max_price": { "type": "number", "description": "Maximum price." },
      "min_beds": { "type": "integer", "description": "Minimum number of beds." }
    }
  }
  ```

**Tool 2: get-listing-details**
- **Description**: Get extensive details about a single listing to describe it to the caller.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/get-listing-details`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "required": ["listing_id"],
    "properties": {
      "listing_id": { "type": "integer", "description": "The ID of the listing to get details for." }
    }
  }
  ```

**Tool 3: search-faq**
- **Description**: Search office FAQs for general knowledge, commissions, hours, processes, etc.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/search-faq`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": { "type": "string", "description": "The topic to search the FAQ for." }
    }
  }
  ```

**Tool 4: create-lead**
- **Description**: Save the caller's basic lead info so agents have a record.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/create-lead`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "required": ["name", "phone"],
    "properties": {
      "name": { "type": "string" },
      "phone": { "type": "string" },
      "query": { "type": "string", "description": "Context of what they are looking for." }
    }
  }
  ```

**Tool 5: create-showing**
- **Description**: Request an in-person or virtual property showing.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/create-showing`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "required": ["listing_id", "name", "phone", "preferred_time"],
    "properties": {
      "listing_id": { "type": "integer" },
      "name": { "type": "string" },
      "phone": { "type": "string" },
      "preferred_time": { "type": "string" }
    }
  }
  ```

**Tool 6: create-callback**
- **Description**: Request a human agent callback for escalations or detailed negotiations.
- **Method**: POST
- **URL**: `https://<YOUR-NGROK-OR-VERCEL-URL>/api/tool/create-callback`
- **Body Schema**:
  ```json
  {
    "type": "object",
    "required": ["name", "phone"],
    "properties": {
      "name": { "type": "string" },
      "phone": { "type": "string" },
      "reason": { "type": "string" }
    }
  }
  ```

---

## 🧪 Quick cURL Checks

```bash
# Check Liveness Probe
curl -X GET http://localhost:8000/health

# Trigger Dynamic Variables
curl -X POST http://localhost:8000/api/dynamic-variables \
  -H "Content-Type: application/json" \
  -d '{"caller_id": "+1234567890"}'

# Search Listings tool
curl -X POST http://localhost:8000/api/tool/search-listings \
  -H "Content-Type: application/json" \
  -d '{"city": "Springfield", "min_beds": 3}'
```
