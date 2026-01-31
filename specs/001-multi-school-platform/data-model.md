# Data Model: Multi-School Website Platform

**Feature**: 001-multi-school-platform | **Date**: 2026-01-31
**Status**: Draft
**Related**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md)

---

## Overview

This document defines the complete database schema for the multi-school website platform. The schema uses PostgreSQL 15+ with Row-Level Security (RLS) policies to enforce strict multi-tenant isolation. All tenant-specific entities include `school_id` foreign keys and RLS policies to prevent cross-school data access.

## Database Technology

- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+ (Backend)
- **Migrations**: Alembic
- **Key Features**:
  - Row-Level Security (RLS) for multi-tenant isolation
  - JSONB columns for flexible configuration storage
  - UUID primary keys for security and distribution
  - Audit logging triggers for compliance

---

## Multi-Tenant Isolation Strategy

### Row-Level Security Implementation

**Principle**: Database-level enforcement of tenant isolation. Application sets `app.current_school_id` session variable, and RLS policies automatically filter all queries.

**Application Flow**:
1. Middleware extracts subdomain from request (e.g., `schoolA.domain.com`)
2. Query `schools` table to resolve `school_id` from subdomain
3. Execute PostgreSQL command: `SET app.current_school_id = '{school_id}'`
4. All subsequent queries automatically filtered by RLS policies
5. Session variable cleared after request completion

**Security Requirements (FR-003, FR-004)**:
- School A admin CANNOT see School B data
- Direct SQL queries CANNOT bypass tenant isolation
- API endpoints MUST set tenant context before data access
- Security tests MUST verify 100% isolation (SC-005)

---

## Entity Relationship Diagram

```
┌─────────────────┐
│     schools     │ (Platform-wide, no RLS)
│  - school_id PK │
│  - subdomain UQ │
└────────┬────────┘
         │
         │ 1:N (school_id FK + RLS)
         │
    ┌────┴────────────────────────────────────────────────┐
    │                                                      │
    ▼                                                      ▼
┌──────────────┐  1:1    ┌─────────────────┐      ┌────────────────┐
│    users     │◄────────┤principal_profile│      │    faculty     │
│  - user_id PK│         │  - school_id PK │      │  - faculty_id  │
│  - school_id │         └─────────────────┘      │  - school_id   │
└──────────────┘                                   └────────────────┘
                                                            │
    │                                                       │
    │ 1:N                                                   │
    │                                                       │
    ▼                         ▼                             ▼
┌──────────────┐      ┌─────────────────┐       ┌──────────────────┐
│   notices    │      │    results      │       │  gallery_images  │
│  - notice_id │      │  - result_id    │       │  - image_id      │
│  - school_id │      │  - school_id    │       │  - school_id     │
│  - created_by│      │  - created_by   │       │  - uploaded_by   │
└──────────────┘      └─────────────────┘       └──────────────────┘
```

---

## Entities

### 1. School (Tenant)

Represents a school in the multi-tenant system. Each school is an isolated tenant.

**Table Name**: `schools`

**RLS Policy**: None (platform-wide table, accessible to Super Admin only)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `school_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_name` | VARCHAR(255) | NOT NULL | Official school name |
| `subdomain` | VARCHAR(100) | UNIQUE, NOT NULL | Subdomain (e.g., "schoolA") |
| `logo_url` | TEXT | NULLABLE | Logo file path or URL |
| `primary_color` | VARCHAR(7) | DEFAULT '#0A3D62' | Brand primary color (hex) |
| `secondary_color` | VARCHAR(7) | DEFAULT '#EAF2F8' | Brand secondary color (hex) |
| `contact_email` | VARCHAR(255) | NOT NULL | School contact email |
| `contact_phone` | VARCHAR(20) | NULLABLE | School contact phone |
| `address` | TEXT | NULLABLE | School physical address |
| `config_json` | JSONB | DEFAULT '{}' | Additional configuration |
| `is_active` | BOOLEAN | DEFAULT TRUE | School operational status |
| `storage_used_bytes` | BIGINT | DEFAULT 0 | Current storage usage |
| `storage_limit_bytes` | BIGINT | DEFAULT 10737418240 | Storage limit (10GB) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
```sql
CREATE UNIQUE INDEX idx_schools_subdomain ON schools(subdomain);
CREATE INDEX idx_schools_is_active ON schools(is_active) WHERE is_active = TRUE;
```

**Validation Rules**:
- `subdomain`: lowercase alphanumeric, 3-50 chars, no special chars except hyphens
- `primary_color`, `secondary_color`: valid hex color codes (#RRGGBB)
- `contact_email`: valid email format
- `storage_used_bytes`: must not exceed `storage_limit_bytes`

**Sample Data**:
```json
{
  "school_id": "550e8400-e29b-41d4-a716-446655440001",
  "school_name": "Springfield High School",
  "subdomain": "springfield",
  "logo_url": "/data/schools/550e8400-e29b-41d4-a716-446655440001/config/logo.png",
  "primary_color": "#0A3D62",
  "secondary_color": "#EAF2F8",
  "contact_email": "admin@springfieldhigh.edu",
  "contact_phone": "+1-555-0100",
  "is_active": true
}
```

---

### 2. User

Represents administrators and staff with role-based access.

**Table Name**: `users`

**RLS Policy**: Super Admin sees all; School Admin/Staff see only their school's users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `user_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `email` | VARCHAR(255) | NOT NULL | User email (NOT unique - multi-school) |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt password hash |
| `role` | VARCHAR(50) | NOT NULL | SUPER_ADMIN, SCHOOL_ADMIN, STAFF |
| `school_id` | UUID | NULLABLE, FK schools(school_id) | Assigned school (NULL for Super Admin) |
| `full_name` | VARCHAR(255) | NOT NULL | User full name |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account status |
| `last_login` | TIMESTAMP | NULLABLE | Last successful login |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes**:
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_school_id ON users(school_id);
CREATE INDEX idx_users_role ON users(role);
CREATE UNIQUE INDEX idx_users_email_school_unique ON users(email, school_id) WHERE school_id IS NOT NULL;
```

**RLS Policies**:
```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Super Admin sees all users
CREATE POLICY users_super_admin_all ON users
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM users u
      WHERE u.user_id = current_setting('app.current_user_id')::uuid
      AND u.role = 'SUPER_ADMIN'
    )
  );

-- School Admin/Staff see only their school's users
CREATE POLICY users_school_isolation ON users
  FOR ALL
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Validation Rules**:
- `email`: valid email format, max 255 chars
- `password_hash`: bcrypt format (60 chars)
- `role`: ENUM ('SUPER_ADMIN', 'SCHOOL_ADMIN', 'STAFF')
- `school_id`: required for SCHOOL_ADMIN and STAFF, must be NULL for SUPER_ADMIN

**Permissions by Role** (FR-016 to FR-022):

| Role | Permissions |
|------|-------------|
| **SUPER_ADMIN** | Create schools, assign school admins, view all schools |
| **SCHOOL_ADMIN** | Manage all content for assigned school (faculty, results, notices, gallery, principal, branding) |
| **STAFF** | Publish notices, upload gallery images (read-only for other content) |

---

### 3. Faculty

Represents teaching staff at a school.

**Table Name**: `faculty`

**RLS Policy**: School-specific (all users see only their school's faculty)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `faculty_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_id` | UUID | NOT NULL, FK schools(school_id) ON DELETE CASCADE | School tenant |
| `full_name` | VARCHAR(255) | NOT NULL | Faculty member name |
| `designation` | VARCHAR(100) | NOT NULL | Position (Principal, Vice Principal, Teacher, etc.) |
| `qualification` | VARCHAR(255) | NOT NULL | Academic qualifications |
| `experience_years` | INTEGER | NOT NULL, CHECK (experience_years >= 0) | Years of experience |
| `subject` | VARCHAR(100) | NULLABLE | Teaching subject (if applicable) |
| `photo_url` | TEXT | NULLABLE | Faculty photo file path |
| `email` | VARCHAR(255) | NULLABLE | Faculty email |
| `phone` | VARCHAR(20) | NULLABLE | Faculty phone |
| `bio` | TEXT | NULLABLE | Short biography |
| `display_order` | INTEGER | DEFAULT 0 | Display order on website |
| `is_visible` | BOOLEAN | DEFAULT TRUE | Visibility on public website |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes**:
```sql
CREATE INDEX idx_faculty_school_id ON faculty(school_id);
CREATE INDEX idx_faculty_display_order ON faculty(school_id, display_order, is_visible);
```

**RLS Policies**:
```sql
ALTER TABLE faculty ENABLE ROW LEVEL SECURITY;

CREATE POLICY faculty_tenant_isolation_select ON faculty
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY faculty_tenant_isolation_insert ON faculty
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY faculty_tenant_isolation_update ON faculty
  FOR UPDATE
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY faculty_tenant_isolation_delete ON faculty
  FOR DELETE
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Validation Rules**:
- `full_name`: 2-255 chars, required
- `designation`: 2-100 chars, required
- `qualification`: 2-255 chars, required
- `experience_years`: non-negative integer
- `email`: valid email format if provided
- `photo_url`: valid file path, must be jpg/png/webp

---

### 4. Result

Represents academic results for a class.

**Table Name**: `results`

**RLS Policy**: School-specific (all users see only their school's results)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `result_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_id` | UUID | NOT NULL, FK schools(school_id) ON DELETE CASCADE | School tenant |
| `academic_year` | VARCHAR(20) | NOT NULL | Academic year (e.g., "2024-25") |
| `class_level` | VARCHAR(50) | NOT NULL | Class/grade (e.g., "Class 10", "Grade 12") |
| `exam_type` | VARCHAR(100) | NOT NULL | Exam type (e.g., "Annual", "Midterm", "Board") |
| `result_data` | JSONB | NOT NULL | Structured result data (see format below) |
| `published_date` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Publication timestamp |
| `is_published` | BOOLEAN | DEFAULT FALSE | Visibility on public website |
| `created_by` | UUID | NOT NULL, FK users(user_id) | Admin who created result |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes**:
```sql
CREATE INDEX idx_results_school_id ON results(school_id);
CREATE INDEX idx_results_published ON results(school_id, is_published, academic_year, class_level);
CREATE INDEX idx_results_year_class ON results(academic_year, class_level);
```

**RLS Policies**:
```sql
ALTER TABLE results ENABLE ROW LEVEL SECURITY;

CREATE POLICY results_tenant_isolation_select ON results
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY results_tenant_isolation_insert ON results
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY results_tenant_isolation_update ON results
  FOR UPDATE
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY results_tenant_isolation_delete ON results
  FOR DELETE
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Result Data Format** (JSONB):
```json
{
  "students": [
    {
      "roll_number": "101",
      "student_name": "John Doe",
      "total_marks": 450,
      "percentage": 90.0,
      "grade": "A+",
      "rank": 1,
      "subjects": [
        {
          "subject_name": "Mathematics",
          "marks_obtained": 95,
          "max_marks": 100,
          "grade": "A+"
        },
        {
          "subject_name": "Science",
          "marks_obtained": 92,
          "max_marks": 100,
          "grade": "A+"
        }
      ]
    }
  ],
  "statistics": {
    "total_students": 50,
    "pass_percentage": 98.0,
    "highest_marks": 495,
    "average_percentage": 82.5
  }
}
```

**Validation Rules**:
- `academic_year`: format "YYYY-YY" (e.g., "2024-25")
- `class_level`: non-empty string, max 50 chars
- `exam_type`: non-empty string, max 100 chars
- `result_data`: valid JSON structure with required fields (students array, statistics)
- `created_by`: must be SCHOOL_ADMIN role for the same school

**Audit Logging** (FR-026):
- All updates logged to `audit_log` table with timestamp, user, reason, before/after values

---

### 5. Notice

Represents announcements and notices.

**Table Name**: `notices`

**RLS Policy**: School-specific (all users see only their school's notices)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `notice_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_id` | UUID | NOT NULL, FK schools(school_id) ON DELETE CASCADE | School tenant |
| `title` | VARCHAR(500) | NOT NULL | Notice title |
| `description` | TEXT | NOT NULL | Notice content (Markdown supported) |
| `priority_level` | INTEGER | DEFAULT 0, CHECK (priority_level BETWEEN 0 AND 5) | Priority (0=low, 5=urgent) |
| `category` | VARCHAR(100) | DEFAULT 'general' | Category (general, academic, events, etc.) |
| `published_date` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Publication timestamp |
| `expiry_date` | TIMESTAMP | NULLABLE | Auto-hide after this date (FR-014) |
| `is_published` | BOOLEAN | DEFAULT FALSE | Visibility on public website |
| `created_by` | UUID | NOT NULL, FK users(user_id) | Admin/staff who created notice |
| `attachment_url` | TEXT | NULLABLE | Optional attachment file path |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes**:
```sql
CREATE INDEX idx_notices_school_id ON notices(school_id);
CREATE INDEX idx_notices_published ON notices(school_id, is_published, expiry_date, priority_level);
CREATE INDEX idx_notices_expiry ON notices(expiry_date) WHERE expiry_date IS NOT NULL;
```

**RLS Policies**:
```sql
ALTER TABLE notices ENABLE ROW LEVEL SECURITY;

CREATE POLICY notices_tenant_isolation_select ON notices
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY notices_tenant_isolation_insert ON notices
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY notices_tenant_isolation_update ON notices
  FOR UPDATE
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY notices_tenant_isolation_delete ON notices
  FOR DELETE
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Validation Rules**:
- `title`: 5-500 chars, required
- `description`: non-empty, max 10,000 chars
- `priority_level`: 0-5 (0=low, 1=normal, 2=important, 3=high, 4=very high, 5=urgent)
- `expiry_date`: must be in the future (if provided)
- `created_by`: must be SCHOOL_ADMIN or STAFF role for the same school

**Auto-Hide Logic** (FR-014):
```sql
-- Query to fetch only active notices
SELECT * FROM notices
WHERE is_published = TRUE
  AND (expiry_date IS NULL OR expiry_date > CURRENT_TIMESTAMP)
ORDER BY priority_level DESC, published_date DESC;
```

---

### 6. Gallery Image

Represents photos in the school gallery.

**Table Name**: `gallery_images`

**RLS Policy**: School-specific (all users see only their school's images)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `image_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_id` | UUID | NOT NULL, FK schools(school_id) ON DELETE CASCADE | School tenant |
| `category` | VARCHAR(100) | NOT NULL | Category (sports, cultural, academics, events) |
| `image_url` | TEXT | NOT NULL | Image file path or URL |
| `thumbnail_url` | TEXT | NULLABLE | Optimized thumbnail path |
| `caption` | TEXT | NULLABLE | Image description/caption |
| `event_date` | DATE | NULLABLE | Date when photo was taken |
| `display_order` | INTEGER | DEFAULT 0 | Display order in gallery |
| `is_visible` | BOOLEAN | DEFAULT TRUE | Visibility on public website |
| `file_size_bytes` | INTEGER | NOT NULL | File size for storage tracking |
| `uploaded_by` | UUID | NOT NULL, FK users(user_id) | Admin/staff who uploaded |
| `upload_date` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Upload timestamp |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

**Indexes**:
```sql
CREATE INDEX idx_gallery_school_id ON gallery_images(school_id);
CREATE INDEX idx_gallery_category ON gallery_images(school_id, category, is_visible);
CREATE INDEX idx_gallery_display_order ON gallery_images(school_id, category, display_order);
```

**RLS Policies**:
```sql
ALTER TABLE gallery_images ENABLE ROW LEVEL SECURITY;

CREATE POLICY gallery_tenant_isolation_select ON gallery_images
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY gallery_tenant_isolation_insert ON gallery_images
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY gallery_tenant_isolation_update ON gallery_images
  FOR UPDATE
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY gallery_tenant_isolation_delete ON gallery_images
  FOR DELETE
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Validation Rules**:
- `category`: non-empty, max 100 chars, recommended values: sports, cultural, academics, events, infrastructure
- `image_url`: valid file path, must be jpg/png/webp (FR-030)
- `file_size_bytes`: max 5MB (5,242,880 bytes) (FR-030)
- `caption`: max 500 chars
- `uploaded_by`: must be SCHOOL_ADMIN or STAFF role for the same school

**Storage Tracking**:
- On image upload, increment `schools.storage_used_bytes`
- On image delete, decrement `schools.storage_used_bytes`
- Reject upload if `storage_used_bytes + file_size_bytes > storage_limit_bytes`

---

### 7. Principal Profile

Represents the school principal's profile.

**Table Name**: `principal_profiles`

**RLS Policy**: School-specific (all users see only their school's principal profile)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `school_id` | UUID | PRIMARY KEY, FK schools(school_id) ON DELETE CASCADE | School tenant (1:1 relationship) |
| `principal_name` | VARCHAR(255) | NOT NULL | Principal's full name |
| `photo_url` | TEXT | NULLABLE | Principal's photo file path |
| `message_text` | TEXT | NOT NULL | Principal's message (Markdown supported) |
| `qualification` | VARCHAR(255) | NULLABLE | Academic qualifications |
| `email` | VARCHAR(255) | NULLABLE | Principal's email |
| `phone` | VARCHAR(20) | NULLABLE | Principal's phone |
| `updated_by` | UUID | NOT NULL, FK users(user_id) | Last admin who updated profile |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Indexes**:
```sql
CREATE UNIQUE INDEX idx_principal_school_id ON principal_profiles(school_id);
```

**RLS Policies**:
```sql
ALTER TABLE principal_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY principal_tenant_isolation_select ON principal_profiles
  FOR SELECT
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY principal_tenant_isolation_insert ON principal_profiles
  FOR INSERT
  WITH CHECK (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY principal_tenant_isolation_update ON principal_profiles
  FOR UPDATE
  USING (school_id = current_setting('app.current_school_id')::uuid);

CREATE POLICY principal_tenant_isolation_delete ON principal_profiles
  FOR DELETE
  USING (school_id = current_setting('app.current_school_id')::uuid);
```

**Validation Rules**:
- `principal_name`: 2-255 chars, required
- `message_text`: non-empty, max 5,000 chars, Markdown format
- `email`: valid email format if provided
- `photo_url`: valid file path, must be jpg/png/webp

---

## Supporting Tables

### 8. Audit Log

Tracks all data modifications for compliance (FR-045, FR-050).

**Table Name**: `audit_logs`

**RLS Policy**: Super Admin only

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `log_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `school_id` | UUID | NULLABLE, FK schools(school_id) | Related school (NULL for platform-wide) |
| `user_id` | UUID | NOT NULL, FK users(user_id) | User who performed action |
| `action` | VARCHAR(50) | NOT NULL | Action type (CREATE, UPDATE, DELETE) |
| `entity_type` | VARCHAR(100) | NOT NULL | Entity affected (faculty, result, notice, etc.) |
| `entity_id` | UUID | NOT NULL | ID of affected entity |
| `before_value` | JSONB | NULLABLE | Entity state before change |
| `after_value` | JSONB | NULLABLE | Entity state after change |
| `reason` | TEXT | NULLABLE | Reason for change (optional) |
| `ip_address` | VARCHAR(45) | NULLABLE | User's IP address |
| `user_agent` | TEXT | NULLABLE | User's browser/client |
| `timestamp` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Action timestamp |

**Indexes**:
```sql
CREATE INDEX idx_audit_school_id ON audit_logs(school_id);
CREATE INDEX idx_audit_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp DESC);
```

**Implementation**:
- Trigger functions on all tenant tables to insert audit log entries
- Application-level logging for complex multi-table operations

---

### 9. Refresh Tokens

Stores JWT refresh tokens for revocation support (FR-017).

**Table Name**: `refresh_tokens`

**RLS Policy**: None (internal security table)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `token_id` | UUID | PRIMARY KEY, DEFAULT uuid_generate_v4() | Unique identifier |
| `user_id` | UUID | NOT NULL, FK users(user_id) ON DELETE CASCADE | Token owner |
| `token_hash` | VARCHAR(255) | UNIQUE, NOT NULL | SHA-256 hash of refresh token |
| `expires_at` | TIMESTAMP | NOT NULL | Token expiration (7 days) |
| `is_revoked` | BOOLEAN | DEFAULT FALSE | Revocation status |
| `revoked_at` | TIMESTAMP | NULLABLE | Revocation timestamp |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Token creation |

**Indexes**:
```sql
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
CREATE INDEX idx_refresh_tokens_expires ON refresh_tokens(expires_at) WHERE is_revoked = FALSE;
```

**Cleanup Job**:
```sql
-- Delete expired tokens daily
DELETE FROM refresh_tokens
WHERE expires_at < CURRENT_TIMESTAMP - INTERVAL '1 day';
```

---

## Database Initialization

### 1. Extensions

```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Password hashing (if using pgcrypto)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

### 2. Custom Types

```sql
-- User roles
CREATE TYPE user_role AS ENUM ('SUPER_ADMIN', 'SCHOOL_ADMIN', 'STAFF');

-- Audit log actions
CREATE TYPE audit_action AS ENUM ('CREATE', 'UPDATE', 'DELETE');
```

### 3. Triggers

**Update Timestamp Trigger**:
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at column
CREATE TRIGGER update_schools_updated_at BEFORE UPDATE ON schools
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ... (repeat for all tables)
```

**Audit Log Trigger**:
```sql
CREATE OR REPLACE FUNCTION audit_log_trigger()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_logs (
    school_id,
    user_id,
    action,
    entity_type,
    entity_id,
    before_value,
    after_value
  ) VALUES (
    COALESCE(NEW.school_id, OLD.school_id),
    current_setting('app.current_user_id')::uuid,
    TG_OP,
    TG_TABLE_NAME,
    COALESCE(NEW.result_id, OLD.result_id),  -- Adjust based on table
    CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END
  );
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Apply to tenant tables
CREATE TRIGGER audit_results AFTER INSERT OR UPDATE OR DELETE ON results
  FOR EACH ROW EXECUTE FUNCTION audit_log_trigger();

-- ... (repeat for critical tables)
```

---

## Migration Strategy

### Initial Migration (Alembic)

**File**: `backend/alembic/versions/001_initial_schema.py`

```python
"""Initial schema with RLS policies

Revision ID: 001
Revises:
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # Create enums
    op.execute("CREATE TYPE user_role AS ENUM ('SUPER_ADMIN', 'SCHOOL_ADMIN', 'STAFF')")
    op.execute("CREATE TYPE audit_action AS ENUM ('CREATE', 'UPDATE', 'DELETE')")

    # Create schools table
    op.create_table('schools',
        sa.Column('school_id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('school_name', sa.String(255), nullable=False),
        sa.Column('subdomain', sa.String(100), nullable=False),
        # ... (all columns)
        sa.PrimaryKeyConstraint('school_id'),
        sa.UniqueConstraint('subdomain')
    )

    # Create users table
    op.create_table('users',
        sa.Column('user_id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
        # ... (all columns)
        sa.ForeignKeyConstraint(['school_id'], ['schools.school_id']),
        sa.PrimaryKeyConstraint('user_id')
    )

    # Enable RLS on users
    op.execute('ALTER TABLE users ENABLE ROW LEVEL SECURITY')

    # Create RLS policies
    op.execute('''
        CREATE POLICY users_super_admin_all ON users
          FOR ALL
          USING (
            EXISTS (
              SELECT 1 FROM users u
              WHERE u.user_id = current_setting('app.current_user_id')::uuid
              AND u.role = 'SUPER_ADMIN'
            )
          )
    ''')

    # ... (repeat for all tables and policies)

def downgrade():
    # Drop tables in reverse order
    op.drop_table('refresh_tokens')
    op.drop_table('audit_logs')
    # ... (all tables)

    # Drop enums
    op.execute('DROP TYPE audit_action')
    op.execute('DROP TYPE user_role')
```

---

## Performance Optimization

### Query Optimization Guidelines

1. **Tenant Context Caching**:
   - Cache `subdomain → school_id` mapping in Redis (TTL: 1 hour)
   - Avoid repeated database lookups for same subdomain

2. **Index Usage**:
   - All foreign keys have indexes
   - Composite indexes for common query patterns (school_id + is_published + date)
   - Partial indexes for filtered queries (WHERE is_active = TRUE)

3. **Query Patterns**:
```sql
-- Good: Uses index on (school_id, is_published, expiry_date)
SELECT * FROM notices
WHERE school_id = '...'
  AND is_published = TRUE
  AND (expiry_date IS NULL OR expiry_date > CURRENT_TIMESTAMP)
ORDER BY priority_level DESC;

-- Bad: Full table scan without school_id filter
SELECT * FROM notices
WHERE is_published = TRUE;
```

4. **Connection Pooling**:
   - SQLAlchemy connection pool: min=10, max=50
   - Connection recycling after 1 hour to prevent stale connections

---

## Data Integrity Constraints

### Foreign Key Cascades

- **ON DELETE CASCADE**: Used for tenant data (deleting school deletes all related data)
- **ON DELETE RESTRICT**: Used for users (cannot delete user if they created content)

### Check Constraints

```sql
-- Ensure storage limits are not exceeded
ALTER TABLE schools ADD CONSTRAINT check_storage_limit
  CHECK (storage_used_bytes <= storage_limit_bytes);

-- Ensure expiry date is in future
ALTER TABLE notices ADD CONSTRAINT check_expiry_future
  CHECK (expiry_date IS NULL OR expiry_date > published_date);

-- Ensure experience is non-negative
ALTER TABLE faculty ADD CONSTRAINT check_experience_positive
  CHECK (experience_years >= 0);
```

---

## Security Testing

### Tenant Isolation Tests

**Test Case**: School A admin cannot access School B data

```python
# backend/tests/security/test_tenant_isolation.py

import pytest
from sqlalchemy import text

@pytest.mark.asyncio
async def test_school_a_cannot_see_school_b_faculty(db_session):
    # Set tenant context to School A
    await db_session.execute(text(f"SET app.current_school_id = '{school_a_id}'"))

    # Query faculty - should only return School A faculty
    result = await db_session.execute(text("SELECT * FROM faculty"))
    faculty_list = result.fetchall()

    # Assert: No School B faculty in results
    for faculty in faculty_list:
        assert faculty.school_id == school_a_id
```

**Test Case**: Direct SQL injection attempt

```python
@pytest.mark.asyncio
async def test_rls_prevents_sql_injection(db_session):
    # Attempt to bypass RLS with malicious school_id
    malicious_id = "'; DROP TABLE faculty; --"

    with pytest.raises(Exception):
        await db_session.execute(text(f"SET app.current_school_id = '{malicious_id}'"))
```

---

## Next Steps

1. **Implement Migrations**: Create Alembic migration files for this schema
2. **Seed Data**: Create seed scripts for development/testing
3. **API Contracts**: Define OpenAPI specifications based on this data model
4. **ORM Models**: Implement SQLAlchemy models matching this schema
5. **Security Testing**: Write comprehensive tenant isolation tests
