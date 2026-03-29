from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from core.database import get_db
from core.security import require_admin
from models.lead import Lead, LeadStatus
from models.user import User

router = APIRouter()

class LeadOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    message: Optional[str]
    source: str
    status: LeadStatus

    class Config:
        from_attributes = True

class LeadStatusUpdate(BaseModel):
    status: LeadStatus

# ── Admin: list all leads ──────────────────────────────────
@router.get("/", response_model=list[LeadOut])
def list_leads(
    status: Optional[LeadStatus] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    q = db.query(Lead)
    if status:
        q = q.filter(Lead.status == status)
    return q.order_by(Lead.id.desc()).offset(skip).limit(limit).all()

# ── Admin: get single lead ─────────────────────────────────
@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

# ── Admin: update lead status ──────────────────────────────
@router.patch("/{lead_id}/status", response_model=LeadOut)
def update_lead_status(
    lead_id: int,
    body: LeadStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = body.status
    db.commit()
    db.refresh(lead)
    return lead

# ── Admin: delete lead ─────────────────────────────────────
@router.delete("/{lead_id}", status_code=204)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
