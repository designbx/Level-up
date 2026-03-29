from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.database import get_db
from core.security import require_admin
from models.lead import Lead, LeadStatus
from models.user import User

router = APIRouter()

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    total_leads     = db.query(func.count(Lead.id)).scalar()
    new_leads       = db.query(func.count(Lead.id)).filter(Lead.status == LeadStatus.new).scalar()
    converted_leads = db.query(func.count(Lead.id)).filter(Lead.status == LeadStatus.converted).scalar()
    total_users     = db.query(func.count(User.id)).scalar()

    conversion_rate = round((converted_leads / total_leads * 100), 1) if total_leads else 0

    # Leads by source
    by_source = db.query(Lead.source, func.count(Lead.id)).group_by(Lead.source).all()

    # Leads by status
    by_status = db.query(Lead.status, func.count(Lead.id)).group_by(Lead.status).all()

    return {
        "total_leads":      total_leads,
        "new_leads":        new_leads,
        "converted_leads":  converted_leads,
        "conversion_rate":  conversion_rate,
        "total_users":      total_users,
        "leads_by_source":  {s: c for s, c in by_source},
        "leads_by_status":  {s: c for s, c in by_status},
    }

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    users = db.query(User).order_by(User.id.desc()).all()
    return [
        {"id": u.id, "name": u.name, "email": u.email,
         "is_admin": u.is_admin, "is_active": u.is_active,
         "created_at": u.created_at}
        for u in users
    ]

@router.patch("/users/{user_id}/toggle-admin")
def toggle_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == current_admin.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Cannot modify your own admin status")
    user.is_admin = not user.is_admin
    db.commit()
    return {"message": f"Admin status set to {user.is_admin}", "is_admin": user.is_admin}
