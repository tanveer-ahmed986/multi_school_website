"""
Public API endpoints for school website visitors.

Endpoints provide read-only access to:
- School information and branding
- Faculty members
- Published results
- Active notices
- Gallery images
- Principal profile

All endpoints require tenant context (subdomain) via Host header.
"""
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from src.database.connection import get_db
from src.models.school import School
from src.models.faculty import Faculty
from src.models.result import Result
from src.models.notice import Notice
from src.models.gallery import GalleryImage
from src.models.principal import PrincipalProfile

router = APIRouter(prefix="/public", tags=["Public"])


def get_school_from_subdomain(host: str, db: Session) -> School:
    """
    Extract subdomain from Host header and resolve to School.

    Args:
        host: Host header value (e.g., "schoolA.domain.com")
        db: Database session

    Returns:
        School object

    Raises:
        HTTPException: If subdomain invalid or school not found
    """
    if not host:
        raise HTTPException(status_code=400, detail="Host header required")

    # Extract subdomain (first part before first dot)
    subdomain = host.split(".")[0]

    # Query school by subdomain
    school = db.query(School).filter(
        School.subdomain == subdomain,
        School.is_active == True
    ).first()

    if not school:
        raise HTTPException(status_code=404, detail=f"School not found or not active")

    return school


@router.get("/school")
def get_school_info(
    host: str = Header(..., alias="Host"),
    db: Session = Depends(get_db)
):
    """
    Get school information and branding.

    Returns school configuration for customizing public website appearance.
    (T056 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    return {
        "school_id": str(school.school_id),
        "school_name": school.school_name,
        "subdomain": school.subdomain,
        "logo_url": school.logo_url,
        "primary_color": school.primary_color,
        "secondary_color": school.secondary_color,
        "contact_email": school.contact_email,
        "contact_phone": school.contact_phone,
        "address": school.address
    }


@router.get("/faculty")
def get_faculty(
    host: str = Header(..., alias="Host"),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get visible faculty members for the school.

    Only returns faculty with is_visible=true, ordered by display_order.
    (T058 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    faculty_list = db.query(Faculty).filter(
        Faculty.school_id == school.school_id,
        Faculty.is_visible == True
    ).order_by(Faculty.display_order).all()

    return [
        {
            "faculty_id": str(f.faculty_id),
            "full_name": f.full_name,
            "designation": f.designation,
            "qualification": f.qualification,
            "experience_years": f.experience_years,
            "subject": f.subject,
            "photo_url": f.photo_url,
            "email": f.email,
            "phone": f.phone,
            "bio": f.bio
        }
        for f in faculty_list
    ]


@router.get("/results")
def get_results(
    host: str = Header(..., alias="Host"),
    year: Optional[str] = Query(None, description="Academic year filter (e.g., 2024-25)"),
    class_level: Optional[str] = Query(None, description="Class level filter (e.g., Class 10)"),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get published results with optional year/class filtering.

    Returns list of results matching filters. Use GET /results/{year}/{class} for full data.
    (T061 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    query = db.query(Result).filter(
        Result.school_id == school.school_id,
        Result.is_published == True
    )

    if year:
        query = query.filter(Result.academic_year == year)
    if class_level:
        query = query.filter(Result.class_level == class_level)

    results = query.order_by(Result.published_date.desc()).all()

    return [
        {
            "result_id": str(r.result_id),
            "academic_year": r.academic_year,
            "class_level": r.class_level,
            "exam_type": r.exam_type,
            "published_date": r.published_date.isoformat()
        }
        for r in results
    ]


@router.get("/results/{year}/{class_level}")
def get_specific_result(
    year: str,
    class_level: str,
    host: str = Header(..., alias="Host"),
    db: Session = Depends(get_db)
):
    """
    Get full result data for specific year and class.

    Returns complete result_data JSONB with student details and statistics.
    (T062 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    result = db.query(Result).filter(
        Result.school_id == school.school_id,
        Result.academic_year == year,
        Result.class_level == class_level,
        Result.is_published == True
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "result_id": str(result.result_id),
        "academic_year": result.academic_year,
        "class_level": result.class_level,
        "exam_type": result.exam_type,
        "result_data": result.result_data,
        "published_date": result.published_date.isoformat()
    }


@router.get("/notices")
def get_notices(
    host: str = Header(..., alias="Host"),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get active notices sorted by priority.

    Filters out expired notices (expiry_date < NOW) and unpublished notices.
    Sorts by priority_level DESC, then published_date DESC.
    (T064 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    now = datetime.now()
    notices = db.query(Notice).filter(
        Notice.school_id == school.school_id,
        Notice.is_published == True,
        (Notice.expiry_date == None) | (Notice.expiry_date > now)
    ).order_by(
        Notice.priority_level.desc(),
        Notice.published_date.desc()
    ).all()

    return [
        {
            "notice_id": str(n.notice_id),
            "title": n.title,
            "description": n.description,
            "priority_level": n.priority_level,
            "category": n.category,
            "published_date": n.published_date.isoformat(),
            "expiry_date": n.expiry_date.isoformat() if n.expiry_date else None,
            "attachment_url": n.attachment_url
        }
        for n in notices
    ]


@router.get("/gallery")
def get_gallery(
    host: str = Header(..., alias="Host"),
    category: Optional[str] = Query(None, description="Category filter (sports, cultural, academics, etc.)"),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Get gallery images with optional category filtering.

    Returns visible images ordered by display_order.
    (T066 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    query = db.query(GalleryImage).filter(
        GalleryImage.school_id == school.school_id,
        GalleryImage.is_visible == True
    )

    if category:
        query = query.filter(GalleryImage.category == category)

    images = query.order_by(
        GalleryImage.category,
        GalleryImage.display_order
    ).all()

    return [
        {
            "image_id": str(img.image_id),
            "category": img.category,
            "image_url": img.image_url,
            "thumbnail_url": img.thumbnail_url,
            "caption": img.caption,
            "event_date": img.event_date.isoformat() if img.event_date else None
        }
        for img in images
    ]


@router.get("/principal")
def get_principal(
    host: str = Header(..., alias="Host"),
    db: Session = Depends(get_db)
):
    """
    Get principal profile.

    Returns principal's name, photo, message, and contact information.
    (T068 - Implementation)
    """
    school = get_school_from_subdomain(host, db)

    principal = db.query(PrincipalProfile).filter(
        PrincipalProfile.school_id == school.school_id
    ).first()

    if not principal:
        raise HTTPException(status_code=404, detail="Principal profile not found")

    return {
        "principal_name": principal.principal_name,
        "photo_url": principal.photo_url,
        "message_text": principal.message_text,
        "qualification": principal.qualification,
        "email": principal.email,
        "phone": principal.phone
    }
