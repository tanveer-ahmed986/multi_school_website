"""Enable RLS on all tenant tables.

Revision ID: 002
Revises: 001
Create Date: 2026-01-31

"""
from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE faculty ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE results ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE notices ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE gallery_images ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE principal_profiles ENABLE ROW LEVEL SECURITY")


def downgrade():
    op.execute("ALTER TABLE principal_profiles DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE gallery_images DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE notices DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE results DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE faculty DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE users DISABLE ROW LEVEL SECURITY")
