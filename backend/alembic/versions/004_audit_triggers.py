"""Update timestamp and audit log trigger functions.

Revision ID: 004
Revises: 003
Create Date: 2026-01-31

"""
from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    for table in ["schools", "users", "faculty", "results", "notices", "gallery_images", "principal_profiles"]:
        if table == "gallery_images":
            continue  # gallery_images has no updated_at
        op.execute(f"""
            CREATE TRIGGER trigger_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW
            EXECUTE PROCEDURE update_updated_at_column();
        """)


def downgrade():
    for table in ["schools", "users", "faculty", "results", "notices", "principal_profiles"]:
        op.execute(f"DROP TRIGGER IF EXISTS trigger_{table}_updated_at ON {table};")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
