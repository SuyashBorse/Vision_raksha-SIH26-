# backend/routes/admin.py
# Admin-only user management endpoints
# GET    /api/admin/users        — list all users
# POST   /api/admin/users        — create new user
# PUT    /api/admin/users/{id}   — update user (password, role, status)
# DELETE /api/admin/users/{id}   — deactivate user
# GET    /api/admin/doctors      — list only doctors (for ASHA dropdown)

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from db.models   import User
from auth.jwt    import hash_password, get_current_user, TokenData

logger = logging.getLogger(__name__)
router = APIRouter()


def _require_admin(caller: TokenData = Depends(get_current_user)) -> TokenData:
    if caller.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "FORBIDDEN", "message": "Admin access required"}
        )
    return caller


class CreateUserRequest(BaseModel):
    name:     str
    username: str
    password: str
    role:     str               # "asha" | "doctor" | "admin"
    phc_id:   Optional[str] = None
    email:    Optional[str] = None

class UpdateUserRequest(BaseModel):
    name:      Optional[str] = None
    password:  Optional[str] = None
    role:      Optional[str] = None
    phc_id:    Optional[str] = None
    is_active: Optional[bool] = None


def _user_dict(u: User) -> dict:
    return {
        "user_id":    u.id,
        "username":   u.username,
        "name":       u.name,
        "email":      u.email,
        "role":       u.role,
        "phc_id":     u.phc_id,
        "is_active":  u.is_active,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


# ── GET /api/admin/users ──────────────────────────────────────
@router.get("/users", summary="List all users")
def list_users(
    role: Optional[str] = None,
    caller: TokenData = Depends(_require_admin),
    db: Session = Depends(get_db),
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    users = q.order_by(User.created_at.desc()).all()
    return [_user_dict(u) for u in users]


# ── GET /api/admin/doctors ────────────────────────────────────
@router.get("/doctors", summary="List all doctors (for ASHA report sharing)")
def list_doctors(
    caller: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Any authenticated user can get the list of doctors to share reports."""
    doctors = db.query(User).filter(
        User.role == "doctor",
        User.is_active == True
    ).all()
    return [{"user_id": d.id, "name": d.name, "phc_id": d.phc_id} for d in doctors]


# ── POST /api/admin/users ─────────────────────────────────────
@router.post("/users", summary="Create a new user account", status_code=201)
def create_user(
    body:   CreateUserRequest,
    caller: TokenData = Depends(_require_admin),
    db:     Session   = Depends(get_db),
):
    allowed_roles = {"asha", "doctor", "admin", "field_worker", "officer"}
    if body.role not in allowed_roles:
        raise HTTPException(
            status_code=422,
            detail={"error": "INVALID_ROLE", "message": f"Role must be one of: {allowed_roles}"}
        )

    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(
            status_code=409,
            detail={"error": "USERNAME_TAKEN", "message": f"Username '{body.username}' is already taken"}
        )

    email = body.email or f"{body.username}@visionraksha.local"
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=409,
            detail={"error": "EMAIL_TAKEN", "message": f"Email '{email}' is already registered"}
        )

    user = User(
        name          = body.name,
        username      = body.username,
        email         = email,
        password_hash = hash_password(body.password),
        role          = body.role,
        phc_id        = body.phc_id,
        is_active     = True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"Admin {caller.user_id} created {body.role} account: {body.username}")
    return _user_dict(user)


# ── PUT /api/admin/users/{id} ─────────────────────────────────
@router.put("/users/{user_id}", summary="Update user (password / role / status)")
def update_user(
    user_id: str,
    body:    UpdateUserRequest,
    caller:  TokenData = Depends(_require_admin),
    db:      Session   = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": "NOT_FOUND", "message": "User not found"})

    if body.name      is not None: user.name      = body.name
    if body.role      is not None: user.role      = body.role
    if body.phc_id    is not None: user.phc_id    = body.phc_id
    if body.is_active is not None: user.is_active = body.is_active
    if body.password  is not None: user.password_hash = hash_password(body.password)

    db.commit()
    db.refresh(user)
    logger.info(f"Admin {caller.user_id} updated user {user_id}")
    return _user_dict(user)


# ── DELETE /api/admin/users/{id} ──────────────────────────────
@router.delete("/users/{user_id}", summary="Deactivate a user account")
def deactivate_user(
    user_id: str,
    caller:  TokenData = Depends(_require_admin),
    db:      Session   = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail={"error": "NOT_FOUND", "message": "User not found"})
    if user_id == caller.user_id:
        raise HTTPException(status_code=400, detail={"error": "SELF_DELETE", "message": "Cannot deactivate your own account"})

    user.is_active = False
    db.commit()
    logger.info(f"Admin {caller.user_id} deactivated user {user_id}")
    return {"message": f"User '{user.name}' deactivated successfully"}
