from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import uuid

app = FastAPI(
    title="Copilot Agent Data Quality Lab API",
    version="1.0.0",
    description="Synthetic REST API used by a Microsoft Copilot Studio portfolio agent."
)

BASE = Path(__file__).resolve().parents[1]
CUSTOMERS = BASE / "data" / "customers_clean.csv"
DEVICES = BASE / "data" / "devices.csv"

tickets = []

class TicketCreate(BaseModel):
    customer_id: int
    device_id: str
    issue: str
    severity: str = "normal"

class Ticket(BaseModel):
    ticket_id: str
    customer_id: int
    device_id: str
    issue: str
    severity: str
    status: str

@app.get("/health", operation_id="healthCheck")
def health():
    return {"status": "ok"}

@app.get("/customers/{customer_id}", operation_id="lookupCustomer")
def lookup_customer(customer_id: int):
    df = pd.read_csv(CUSTOMERS)
    row = df[df["customer_id"] == customer_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Customer not found")
    return row.iloc[0].where(pd.notnull(row.iloc[0]), None).to_dict()

@app.get("/devices/{device_id}", operation_id="lookupDevice")
def lookup_device(device_id: str):
    df = pd.read_csv(DEVICES)
    row = df[df["device_id"].str.upper() == device_id.upper()]
    if row.empty:
        raise HTTPException(status_code=404, detail="Device not found")
    return row.iloc[0].where(pd.notnull(row.iloc[0]), None).to_dict()

@app.post("/tickets", response_model=Ticket, operation_id="createSupportTicket")
def create_ticket(payload: TicketCreate):
    severity = payload.severity.lower()
    if severity not in {"low", "normal", "high", "critical"}:
        raise HTTPException(status_code=400, detail="Invalid severity")

    lookup_customer(payload.customer_id)
    device = lookup_device(payload.device_id)
    if int(device["customer_id"]) != payload.customer_id:
        raise HTTPException(status_code=400, detail="Device is not assigned to this customer")

    ticket = {
        "ticket_id": f"TKT-{uuid.uuid4().hex[:8].upper()}",
        "customer_id": payload.customer_id,
        "device_id": payload.device_id.upper(),
        "issue": payload.issue.strip(),
        "severity": severity,
        "status": "open",
    }
    tickets.append(ticket)
    return ticket

@app.get("/tickets", operation_id="listSupportTickets")
def list_tickets():
    return tickets
