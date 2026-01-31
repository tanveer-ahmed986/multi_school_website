"""Initial schema: all tables, indexes, foreign keys.

Revision ID: 001
Revises:
Create Date: 2026-01-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "schools",
        sa.Column("school_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_name", sa.String(255), nullable=False),
        sa.Column("subdomain", sa.String(100), nullable=False),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("primary_color", sa.String(7), server_default="#0A3D62", nullable=False),
        sa.Column("secondary_color", sa.String(7), server_default="#EAF2F8", nullable=False),
        sa.Column("contact_email", sa.String(255), nullable=False),
        sa.Column("contact_phone", sa.String(20), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("config_json", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("storage_used_bytes", sa.BigInteger(), server_default="0", nullable=False),
        sa.Column("storage_limit_bytes", sa.BigInteger(), server_default="10737418240", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("school_id"),
    )
    op.create_index("idx_schools_subdomain", "schools", ["subdomain"], unique=True)
    op.create_index("idx_schools_is_active", "schools", ["is_active"], postgresql_where=sa.text("is_active = true"))

    op.create_table(
        "users",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_users_school_id", "users", ["school_id"])
    op.create_index("idx_users_role", "users", ["role"])
    op.create_index("idx_users_email_school_unique", "users", ["email", "school_id"], unique=True, postgresql_where=sa.text("school_id IS NOT NULL"))

    op.create_table(
        "faculty",
        sa.Column("faculty_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("designation", sa.String(100), nullable=False),
        sa.Column("qualification", sa.String(255), nullable=False),
        sa.Column("experience_years", sa.Integer(), nullable=False),
        sa.Column("subject", sa.String(100), nullable=True),
        sa.Column("photo_url", sa.Text(), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_visible", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("faculty_id"),
        sa.CheckConstraint("experience_years >= 0", name="check_faculty_experience_positive"),
    )
    op.create_index("idx_faculty_school_id", "faculty", ["school_id"])
    op.create_index("idx_faculty_display_order", "faculty", ["school_id", "display_order", "is_visible"])

    op.create_table(
        "results",
        sa.Column("result_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("academic_year", sa.String(20), nullable=False),
        sa.Column("class_level", sa.String(50), nullable=False),
        sa.Column("exam_type", sa.String(100), nullable=False),
        sa.Column("result_data", postgresql.JSONB(), nullable=False),
        sa.Column("published_date", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("is_published", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("result_id"),
    )
    op.create_index("idx_results_school_id", "results", ["school_id"])
    op.create_index("idx_results_published", "results", ["school_id", "is_published", "academic_year", "class_level"])
    op.create_index("idx_results_year_class", "results", ["academic_year", "class_level"])

    op.create_table(
        "notices",
        sa.Column("notice_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("priority_level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("category", sa.String(100), server_default="general", nullable=False),
        sa.Column("published_date", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("expiry_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_published", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attachment_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("notice_id"),
        sa.CheckConstraint("priority_level BETWEEN 0 AND 5", name="check_notice_priority"),
    )
    op.create_index("idx_notices_school_id", "notices", ["school_id"])
    op.create_index("idx_notices_published", "notices", ["school_id", "is_published", "expiry_date", "priority_level"])
    op.create_index("idx_notices_expiry", "notices", ["expiry_date"], postgresql_where=sa.text("expiry_date IS NOT NULL"))

    op.create_table(
        "gallery_images",
        sa.Column("image_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("thumbnail_url", sa.Text(), nullable=True),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("display_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_visible", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False),
        sa.Column("uploaded_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("upload_date", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("image_id"),
    )
    op.create_index("idx_gallery_school_id", "gallery_images", ["school_id"])
    op.create_index("idx_gallery_category", "gallery_images", ["school_id", "category", "is_visible"])
    op.create_index("idx_gallery_display_order", "gallery_images", ["school_id", "category", "display_order"])

    op.create_table(
        "principal_profiles",
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("principal_name", sa.String(255), nullable=False),
        sa.Column("photo_url", sa.Text(), nullable=True),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("qualification", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["updated_by"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("school_id"),
    )
    op.create_index("idx_principal_school_id", "principal_profiles", ["school_id"], unique=True)

    op.create_table(
        "audit_logs",
        sa.Column("log_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("before_value", postgresql.JSONB(), nullable=True),
        sa.Column("after_value", postgresql.JSONB(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.school_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("log_id"),
    )
    op.create_index("idx_audit_school_id", "audit_logs", ["school_id"])
    op.create_index("idx_audit_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_entity", "audit_logs", ["entity_type", "entity_id"])
    op.create_index("idx_audit_timestamp", "audit_logs", ["timestamp"], postgresql_ops={"timestamp": "DESC"})

    op.create_table(
        "refresh_tokens",
        sa.Column("token_id", postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("token_id"),
    )
    op.create_index("idx_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("idx_refresh_tokens_hash", "refresh_tokens", ["token_hash"])
    op.create_index("idx_refresh_tokens_expires", "refresh_tokens", ["expires_at"], postgresql_where=sa.text("is_revoked = false"))


def downgrade():
    op.drop_table("refresh_tokens")
    op.drop_table("audit_logs")
    op.drop_table("principal_profiles")
    op.drop_table("gallery_images")
    op.drop_table("notices")
    op.drop_table("results")
    op.drop_table("faculty")
    op.drop_table("users")
    op.drop_table("schools")
    op.execute('DROP EXTENSION IF EXISTS "pgcrypto"')
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
