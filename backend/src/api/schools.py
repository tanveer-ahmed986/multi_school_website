"""
Schools management API (Super Admin only).

Endpoints for school onboarding and administration.
(T165-T170 - Implementation)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID

from src.database.connection import get_db
from src.services.school_service import SchoolService
from src.models.user import User, UserRole

router = APIRouter(prefix="/schools", tags=["Schools Management"])


# Pydantic models for request/response
class SchoolCreate(BaseModel):
    school_name: str
    subdomain: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    primary_color: str = "#0A3D62"
    secondary_color: str = "#EAF2F8"


class SchoolUpdate(BaseModel):
    school_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    is_active: Optional[bool] = None
    storage_limit_bytes: Optional[int] = None


class SchoolResponse(BaseModel):
    school_id: str
    school_name: str
    subdomain: str
    contact_email: str
    contact_phone: Optional[str]
    address: Optional[str]
    logo_url: Optional[str]
    primary_color: str
    secondary_color: str
    is_active: bool
    storage_used_bytes: int
    storage_limit_bytes: int

    class Config:
        from_attributes = True


class AdminAssignment(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    school_id: Optional[str]

    class Config:
        from_attributes = True


# Temporary super admin dependency
async def get_current_super_admin(db: Session = Depends(get_db)) -> User:
    """
    Get current authenticated super admin user.
    TODO: Replace with actual JWT validation
    """
    # For development, return first super admin user
    user = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return user


@router.post("/", response_model=SchoolResponse, status_code=status.HTTP_201_CREATED)
def create_school(
    school_data: SchoolCreate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new school (Super Admin only).

    Initializes complete school structure including folder hierarchy.
    (T165 - Implementation)
    """
    service = SchoolService(db)

    try:
        school = service.create_school(
            school_name=school_data.school_name,
            subdomain=school_data.subdomain,
            contact_email=school_data.contact_email,
            contact_phone=school_data.contact_phone,
            address=school_data.address,
            primary_color=school_data.primary_color,
            secondary_color=school_data.secondary_color,
        )

        return SchoolResponse.model_validate(school)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[SchoolResponse])
def list_schools(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    List all schools with pagination and filtering (Super Admin only).

    (T166 - Implementation)
    """
    service = SchoolService(db)
    schools = service.list_schools(
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active
    )

    return [SchoolResponse.model_validate(s) for s in schools]


@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(
    school_id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Get school details by ID (Super Admin only).

    (T167 - Implementation)
    """
    service = SchoolService(db)
    school = service.get_school_by_id(school_id)

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"School with ID {school_id} not found"
        )

    return SchoolResponse.model_validate(school)


@router.put("/{school_id}", response_model=SchoolResponse)
def update_school(
    school_id: UUID,
    school_data: SchoolUpdate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Update school configuration (Super Admin only).

    (T168 - Implementation)
    """
    service = SchoolService(db)

    update_dict = {k: v for k, v in school_data.model_dump().items() if v is not None}
    school = service.update_school(school_id, update_dict)

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"School with ID {school_id} not found"
        )

    return SchoolResponse.model_validate(school)


@router.post("/{school_id}/admins", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def assign_school_admin(
    school_id: UUID,
    admin_data: AdminAssignment,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Create and assign a school administrator (Super Admin only).

    (T170 - Implementation)
    """
    service = SchoolService(db)

    try:
        admin_user = service.assign_school_admin(
            school_id=school_id,
            email=admin_data.email,
            password=admin_data.password,
            full_name=admin_data.full_name,
        )

        return UserResponse.model_validate(admin_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_school(
    school_id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """
    Deactivate a school (Super Admin only).

    Soft delete - sets is_active to False.
    """
    service = SchoolService(db)
    success = service.deactivate_school(school_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"School with ID {school_id} not found"
        )

    return None
