# backend/routes/doctor_reviews.py
# Doctor review workflow endpoints
# POST /api/reviews/share/{screening_id}   — ASHA shares report to a doctor
# GET  /api/reviews/pending                — Doctor sees reports pending review
# POST /api/reviews/{screening_id}         — Doctor submits full review
# GET  /api/reviews/my-reports             — ASHA sees their reports + doctor responses

import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from db.models   import Screening, User, DoctorReview, Patient
from auth.jwt    import get_current_user, TokenData

logger = logging.getLogger(__name__)
router = APIRouter()

GRADE_LABELS = {0: "No DR", 1: "Mild DR", 2: "Moderate DR", 3: "Severe DR", 4: "Proliferative DR"}


class ShareReportRequest(BaseModel):
    doctor_id: str
    notes:     Optional[str] = None  # ASHA's notes to doctor

class SubmitReviewRequest(BaseModel):
    confirmed_grade:          int         # 0–4
    review_description:       str         # full clinical review text
    treatment_recommendation: Optional[str] = None
    urgency:                  str = "routine"   # routine | urgent | emergency


def _screening_summary(s: Screening) -> dict:
    patient = s.patient
    return {
        "screening_id":    s.id,
        "patient_id":      s.patient_id,
        "patient_name":    patient.name if patient else "Unknown",
        "patient_age":     patient.age if patient else s.patient_age,
        "patient_gender":  patient.gender if patient else None,
        "grade":           s.grade,
        "grade_label":     s.grade_label,
        "confidence":      s.confidence,
        "findings":        s.findings,
        "action":          s.action,
        "image_url":       s.image_url,
        "heatmap_url":     s.heatmap_url,
        "asha_notes":      s.asha_notes,
        "report_status":   s.report_status,
        "screened_by":     s.screened_by,
        "created_at":      s.created_at.isoformat() if s.created_at else None,
        "doctor_review":   _review_dict(s.doctor_review) if s.doctor_review else None,
    }


def _review_dict(r: DoctorReview) -> dict:
    return {
        "review_id":               r.id,
        "confirmed_grade":         r.confirmed_grade,
        "confirmed_grade_label":   r.confirmed_grade_label,
        "review_description":      r.review_description,
        "treatment_recommendation": r.treatment_recommendation,
        "urgency":                 r.urgency,
        "doctor_name":             r.doctor.name if r.doctor else None,
        "reviewed_at":             r.reviewed_at.isoformat() if r.reviewed_at else None,
    }


# ── POST /api/reviews/share/{screening_id} ───────────────────
@router.post("/share/{screening_id}", summary="ASHA shares a report to a doctor")
def share_report(
    screening_id: str,
    body:   ShareReportRequest,
    caller: TokenData = Depends(get_current_user),
    db:     Session   = Depends(get_db),
):
    if caller.role not in ("asha", "field_worker", "admin"):
        raise HTTPException(
            status_code=403,
            detail={"error": "FORBIDDEN", "message": "Only ASHA workers can share reports"}
        )

    screening = db.query(Screening).filter(Screening.id == screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail={"error": "NOT_FOUND", "message": "Screening not found"})

    doctor = db.query(User).filter(User.id == body.doctor_id, User.role == "doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail={"error": "NOT_FOUND", "message": "Doctor not found"})

    if screening.report_status == "reviewed":
        raise HTTPException(status_code=400, detail={"error": "ALREADY_REVIEWED", "message": "Report has already been reviewed"})

    screening.shared_to_doctor_id = body.doctor_id
    screening.asha_notes          = body.notes
    screening.report_status       = "pending_review"
    db.commit()

    logger.info(f"ASHA {caller.user_id} shared screening {screening_id} to Dr. {doctor.name}")
    return {"message": f"Report shared to Dr. {doctor.name}", "report_status": "pending_review"}


# ── GET /api/reviews/pending ──────────────────────────────────
@router.get("/pending", summary="Doctor sees reports pending their review")
def pending_reviews(
    caller: TokenData = Depends(get_current_user),
    db:     Session   = Depends(get_db),
):
    if caller.role not in ("doctor", "admin"):
        raise HTTPException(
            status_code=403,
            detail={"error": "FORBIDDEN", "message": "Only doctors can access the review queue"}
        )

    query = db.query(Screening).filter(Screening.report_status == "pending_review")

    # Doctors only see reports assigned to them (unless admin)
    if caller.role == "doctor":
        query = query.filter(Screening.shared_to_doctor_id == caller.user_id)

    screenings = query.order_by(Screening.created_at.desc()).all()
    return [_screening_summary(s) for s in screenings]


# ── POST /api/reviews/{screening_id} ─────────────────────────
@router.post("/{screening_id}", summary="Doctor submits full review")
def submit_review(
    screening_id: str,
    body:   SubmitReviewRequest,
    caller: TokenData = Depends(get_current_user),
    db:     Session   = Depends(get_db),
):
    if caller.role not in ("doctor", "admin"):
        raise HTTPException(
            status_code=403,
            detail={"error": "FORBIDDEN", "message": "Only doctors can submit reviews"}
        )

    if body.confirmed_grade not in range(5):
        raise HTTPException(status_code=422, detail={"error": "INVALID_GRADE", "message": "Grade must be 0–4"})

    if body.urgency not in ("routine", "urgent", "emergency"):
        raise HTTPException(status_code=422, detail={"error": "INVALID_URGENCY", "message": "Urgency must be routine/urgent/emergency"})

    screening = db.query(Screening).filter(Screening.id == screening_id).first()
    if not screening:
        raise HTTPException(status_code=404, detail={"error": "NOT_FOUND", "message": "Screening not found"})

    if screening.report_status == "reviewed":
        raise HTTPException(status_code=400, detail={"error": "ALREADY_REVIEWED", "message": "This report has already been reviewed"})

    # Resolve doctor DB user (if DB user)
    doctor_db_id = None
    if not caller.user_id.startswith("demo_"):
        doc_user = db.query(User).filter(User.id == caller.user_id).first()
        if doc_user:
            doctor_db_id = doc_user.id

    review = DoctorReview(
        screening_id             = screening_id,
        doctor_id                = doctor_db_id,
        confirmed_grade          = body.confirmed_grade,
        confirmed_grade_label    = GRADE_LABELS.get(body.confirmed_grade, "Unknown"),
        review_description       = body.review_description,
        treatment_recommendation = body.treatment_recommendation,
        urgency                  = body.urgency,
        reviewed_at              = datetime.now(timezone.utc),
    )

    screening.report_status = "reviewed"
    screening.validated     = True

    db.add(review)
    db.commit()
    db.refresh(review)

    logger.info(f"Doctor {caller.user_id} reviewed screening {screening_id} | grade={body.confirmed_grade} | urgency={body.urgency}")

    return {
        "message":       "Review submitted successfully",
        "review_id":     review.id,
        "report_status": "reviewed",
        "review":        _review_dict(review),
    }


# ── GET /api/reviews/my-reports ───────────────────────────────
@router.get("/my-reports", summary="ASHA worker sees their own reports + doctor responses")
def my_reports(
    caller: TokenData = Depends(get_current_user),
    db:     Session   = Depends(get_db),
):
    if caller.role not in ("asha", "field_worker", "admin"):
        raise HTTPException(
            status_code=403,
            detail={"error": "FORBIDDEN", "message": "Only ASHA workers can view their reports"}
        )

    screenings = (
        db.query(Screening)
        .filter(Screening.screened_by == caller.user_id)
        .order_by(Screening.created_at.desc())
        .all()
    )
    return [_screening_summary(s) for s in screenings]
