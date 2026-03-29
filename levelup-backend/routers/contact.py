from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.database import get_db
from models.lead import Lead
from services.email_service import send_lead_confirmation, send_admin_lead_alert

router = APIRouter()

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    message: str | None = None

@router.post("/", status_code=201)
def submit_contact(
    body: ContactRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save as a lead
    lead = Lead(
        name    = body.name,
        email   = body.email,
        phone   = body.phone,
        company = body.company,
        message = body.message,
        source  = "contact_form"
    )
    db.add(lead)
    db.commit()

    # Fire emails in the background
    background_tasks.add_task(send_lead_confirmation, body.name, body.email)
    background_tasks.add_task(send_admin_lead_alert, body.name, body.email, body.message or "")

    return {"message": "Thanks! We'll be in touch within 24 hours."}
