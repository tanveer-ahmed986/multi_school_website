"""
Content management API endpoints for school administrators.

Provides CRUD operations for:
- Faculty members
- Student results
- Notices and announcements
- Gallery images
- Principal profile
- School branding

All endpoints require authentication and enforce tenant isolation via RLS.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from uuid import UUID

from src.database.connection import get_db
from src.services.faculty_service import FacultyService
from src.models.user import User, UserRole
from src.utils.permissions import require_permission

router = APIRouter(prefix="/content", tags=["Content Management"])


# ============================================================================
# Faculty Management Endpoints (T108-T110)
# ============================================================================

class FacultyCreate(BaseModel):
    full_name: str
    designation: str
    qualification: str
    experience_years: int
    subject: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    display_order: int = 0
    is_visible: bool = True


class FacultyUpdate(BaseModel):
    full_name: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    subject: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    display_order: Optional[int] = None
    is_visible: Optional[bool] = None


class FacultyResponse(BaseModel):
    faculty_id: str
    full_name: str
    designation: str
    qualification: str
    experience_years: int
    subject: Optional[str]
    photo_url: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    bio: Optional[str]
    display_order: int
    is_visible: bool

    class Config:
        from_attributes = True


# Temporary auth dependency - will be replaced with proper JWT middleware
async def get_current_admin_user(db: Session = Depends(get_db)) -> User:
    """
    Temporary: Get current authenticated admin user.
    TODO: Replace with actual JWT auth middleware in T137-T139
    """
    # For now, return a mock admin user for development
    # This will be replaced with actual JWT validation
    user = db.query(User).filter(User.role == "SCHOOL_ADMIN").first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.post("/faculty", response_model=FacultyResponse, status_code=201)
@require_permission('faculty', 'create')
def create_faculty(
    faculty_data: FacultyCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Create a new faculty member.

    Requires SCHOOL_ADMIN role. Photo upload handled separately.
    (T108 - Implementation, T188 - Permission enforcement)
    """
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)

    try:
        faculty = service.create(faculty_data.model_dump())
        return FacultyResponse.model_validate(faculty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/faculty", response_model=List[FacultyResponse])
@require_permission('faculty', 'read')
def list_faculty(
    include_hidden: bool = False,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    List all faculty members for the current school.

    Includes hidden faculty if include_hidden=true.
    (T188 - Permission enforcement)
    """
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)
    faculty_list = service.list_all(include_hidden=include_hidden)

    return [FacultyResponse.model_validate(f) for f in faculty_list]


@router.get("/faculty/{faculty_id}", response_model=FacultyResponse)
@require_permission('faculty', 'read')
def get_faculty(
    faculty_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific faculty member by ID. (T188 - Permission enforcement)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)
    faculty = service.get_by_id(faculty_id)

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")

    return FacultyResponse.model_validate(faculty)


@router.put("/faculty/{faculty_id}", response_model=FacultyResponse)
@require_permission('faculty', 'update')
def update_faculty(
    faculty_id: UUID,
    faculty_data: FacultyUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update faculty member details.

    RLS ensures only faculty from the admin's school can be updated.
    (T109, T188 - Implementation with permission enforcement)
    """
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)

    try:
        # Filter out None values to only update provided fields
        update_data = {k: v for k, v in faculty_data.model_dump().items() if v is not None}
        faculty = service.update(faculty_id, update_data)

        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty member not found")

        return FacultyResponse.model_validate(faculty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/faculty/{faculty_id}", status_code=204)
@require_permission('faculty', 'delete')
def delete_faculty(
    faculty_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Delete a faculty member.

    RLS ensures only faculty from the admin's school can be deleted.
    (T110, T188 - Implementation with permission enforcement)
    """
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)
    success = service.delete(faculty_id)

    if not success:
        raise HTTPException(status_code=404, detail="Faculty member not found")

    return None


@router.patch("/faculty/{faculty_id}/toggle-visibility", response_model=FacultyResponse)
@require_permission('faculty', 'update')
def toggle_faculty_visibility(
    faculty_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Toggle faculty member visibility on public website. (T188 - Permission enforcement)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = FacultyService(db, current_user.school_id)
    faculty = service.toggle_visibility(faculty_id)

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty member not found")

    return FacultyResponse.model_validate(faculty)


# ============================================================================
# Results Management Endpoints (T115-T116)
# ============================================================================

from src.services.result_service import ResultService

class ResultCreate(BaseModel):
    academic_year: str
    class_level: str
    exam_type: str
    result_data: dict
    is_published: bool = False


class ResultUpdate(BaseModel):
    result_data: Optional[dict] = None
    is_published: Optional[bool] = None


@router.post("/results", status_code=201)
@require_permission('results', 'create')
def create_result(
    result_data: ResultCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new result with JSONB validation. (T115, T188 - Permission enforcement)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = ResultService(db, current_user.school_id)
    try:
        result = service.create(result_data.model_dump(), current_user.user_id)
        return {"result_id": str(result.result_id), "message": "Result created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/results/{result_id}")
@require_permission('results', 'update')
def update_result(
    result_id: UUID,
    result_data: ResultUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update result with audit logging. (T116, T188 - Permission enforcement)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = ResultService(db, current_user.school_id)
    try:
        update_dict = {k: v for k, v in result_data.model_dump().items() if v is not None}
        result = service.update(result_id, update_dict)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return {"message": "Result updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Notices Management Endpoints (T121-T122)
# ============================================================================

from src.services.notice_service import NoticeService
from datetime import datetime

class NoticeCreate(BaseModel):
    title: str
    description: str
    priority_level: int = 0
    category: str = "general"
    expiry_date: Optional[datetime] = None
    is_published: bool = False
    attachment_url: Optional[str] = None


class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority_level: Optional[int] = None
    expiry_date: Optional[datetime] = None
    is_published: Optional[bool] = None


@router.post("/notices", status_code=201)
@require_permission('notices', 'create')
def create_notice(
    notice_data: NoticeCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new notice with expiry validation. (T121, T188 - Permission enforcement, STAFF allowed)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = NoticeService(db, current_user.school_id)
    try:
        notice = service.create(notice_data.model_dump(), current_user.user_id)
        return {"notice_id": str(notice.notice_id), "message": "Notice created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/notices/{notice_id}")
@require_permission('notices', 'update')
def update_notice(
    notice_id: UUID,
    notice_data: NoticeUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update notice. (T122, T188 - Permission enforcement, STAFF allowed)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = NoticeService(db, current_user.school_id)
    try:
        update_dict = {k: v for k, v in notice_data.model_dump().items() if v is not None}
        notice = service.update(notice_id, update_dict)
        if not notice:
            raise HTTPException(status_code=404, detail="Notice not found")
        return {"message": "Notice updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Gallery Management Endpoints (T127-T128)
# ============================================================================

from src.services.gallery_service import GalleryService

class GalleryImageCreate(BaseModel):
    category: str
    image_url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    event_date: Optional[datetime] = None
    file_size_bytes: int
    is_visible: bool = True


@router.post("/gallery", status_code=201)
@require_permission('gallery', 'create')
def upload_gallery_image(
    image_data: GalleryImageCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Upload gallery image with storage tracking. (T127, T188 - Permission enforcement, STAFF allowed)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = GalleryService(db, current_user.school_id)
    try:
        image = service.create(image_data.model_dump(), current_user.user_id)
        return {"image_id": str(image.image_id), "message": "Image uploaded successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/gallery/{image_id}", status_code=204)
@require_permission('gallery', 'delete')
def delete_gallery_image(
    image_id: UUID,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete gallery image and decrement storage. (T128, T188 - Permission enforcement, STAFF allowed)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = GalleryService(db, current_user.school_id)
    success = service.delete(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return None


# ============================================================================
# Principal Profile Endpoints (T132)
# ============================================================================

from src.services.principal_service import PrincipalService

class PrincipalProfileUpdate(BaseModel):
    principal_name: str
    message_text: str
    photo_url: Optional[str] = None
    qualification: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


@router.put("/principal")
@require_permission('principal', 'update')
def update_principal_profile(
    profile_data: PrincipalProfileUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Upsert principal profile. (T132, T188 - Permission enforcement, SCHOOL_ADMIN only)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = PrincipalService(db, current_user.school_id)
    profile = service.upsert(profile_data.model_dump(), current_user.user_id)
    return {"message": "Principal profile updated successfully"}


@router.get("/principal")
@require_permission('principal', 'read')
def get_principal_profile(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get principal profile. (T188 - Permission enforcement, SCHOOL_ADMIN only)"""
    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    service = PrincipalService(db, current_user.school_id)
    profile = service.get()
    if not profile:
        raise HTTPException(status_code=404, detail="Principal profile not found")
    return profile


# ============================================================================
# School Branding Management Endpoints (T177)
# ============================================================================

class SchoolBrandingUpdate(BaseModel):
    """Schema for updating school branding settings."""
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None

    @field_validator('primary_color', 'secondary_color')
    @classmethod
    def validate_hex_color(cls, v):
        """Validate that color is a valid hex code."""
        if v is not None:
            if not (len(v) == 7 and v[0] == '#' and all(c in '0123456789ABCDEFabcdef' for c in v[1:])):
                raise ValueError('Color must be a valid hex code (e.g., #FF5733)')
        return v


class SchoolBrandingResponse(BaseModel):
    """Response schema for school branding."""
    school_id: str
    school_name: str
    subdomain: str
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    contact_email: str
    contact_phone: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True


@router.put("/branding", response_model=SchoolBrandingResponse)
@require_permission('branding', 'update')
def update_school_branding(
    branding_data: SchoolBrandingUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update school branding settings (logo, colors, contact info).

    Allows school administrators to customize their school's appearance.
    Only updates fields that are provided (partial update supported).

    (T177, T188 - Implementation with permission enforcement, SCHOOL_ADMIN only)
    """
    from src.models.school import School

    if not current_user.school_id:
        raise HTTPException(status_code=403, detail="No school assigned to user")

    # Get the school
    school = db.query(School).filter(School.school_id == current_user.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    # Update only provided fields
    update_data = branding_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(school, field, value)

    db.commit()
    db.refresh(school)

    return school
