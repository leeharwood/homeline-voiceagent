# HomeLine

HomeLine is a Telnyx-powered real estate voice assistant built to handle common inbound office workflows: searching listings, capturing leads, requesting callbacks, and submitting showing requests. The project combines a Telnyx AI Assistant, a publicly deployed FastAPI backend, dynamic webhook variables, and a custom MCP-backed business-logic layer.

## Overview

The goal of this project was to build a practical voice AI system for a real-world business workflow. I chose residential real estate because it is still highly phone-driven and involves repetitive intake tasks that are well suited to automation.

HomeLine is designed for a solo real estate agent or small brokerage that wants to:
- answer listing questions after hours
- reduce missed inbound leads
- capture structured buyer interest
- collect callback requests
- collect showing requests for agent follow-up

The current MVP focuses on the highest-value workflows rather than trying to automate every part of a real-estate operation.

## Core Features

- Telnyx AI Assistant built in the Telnyx Assistant Builder
- Dynamic webhook variables for runtime personalization
- Public FastAPI backend deployed on Render
- Custom MCP server layer for AI-facing business tools
- Listing search
- Lead creation
- Callback request creation
- Showing request creation
- Publicly testable API endpoints

## Use Case

HomeLine acts as a real estate office front-desk assistant. A caller can:
- ask for properties by city, price, and bedroom count
- request a callback from an agent
- provide buyer details for lead capture
- request a showing time for a specific property

This is a strong fit for voice because many real-estate leads still begin with a phone call, and the first interaction is often repetitive qualification rather than deep consultation.

## Architecture

Caller or Telnyx Test Assistant
  ↓
Telnyx AI Assistant
  ↓
Dynamic Variables Webhook + Webhook Tools
  ↓
FastAPI Backend (Render)
  ↓
Custom MCP-backed business layer
  ↓
SQLite database / service modules

# HomeLine

HomeLine is a Telnyx-powered real estate voice assistant built to handle common inbound office workflows: searching listings, capturing leads, requesting callbacks, and submitting showing requests. The project combines a Telnyx AI Assistant, a publicly deployed FastAPI backend, dynamic webhook variables, and a custom MCP-backed business-logic layer.

## Overview

The goal of this project was to build a practical voice AI system for a real-world business workflow. I chose residential real estate because it is still highly phone-driven and involves repetitive intake tasks that are well suited to automation.

HomeLine is designed for a solo real estate agent or small brokerage that wants to:
- answer listing questions after hours
- reduce missed inbound leads
- capture structured buyer interest
- collect callback requests
- collect showing requests for agent follow-up

The current MVP focuses on the highest-value workflows rather than trying to automate every part of a real-estate operation.

## Core Features

- Telnyx AI Assistant built in the Telnyx Assistant Builder
- Dynamic webhook variables for runtime personalization
- Public FastAPI backend deployed on Render
- Custom MCP server layer for AI-facing business tools
- Listing search
- Lead creation
- Callback request creation
- Showing request creation
- Publicly testable API endpoints

## Use Case

HomeLine acts as a real estate office front-desk assistant. A caller can:
- ask for properties by city, price, and bedroom count
- request a callback from an agent
- provide buyer details for lead capture
- request a showing time for a specific property

This is a strong fit for voice because many real-estate leads still begin with a phone call, and the first interaction is often repetitive qualification rather than deep consultation.

## Architecture
Caller or Telnyx Test Assistant
  ↓
Telnyx AI Assistant
  ↓
Dynamic Variables Webhook + Webhook Tools
  ↓
FastAPI Backend (Render)
  ↓
Custom MCP-backed business layer
  ↓
SQLite database / service modules


