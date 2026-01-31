"""RLS policies for tenant isolation.

Revision ID: 003
Revises: 002
Create Date: 2026-01-31

"""
from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    # Users: Super Admin sees all; School Admin/Staff see only their school
    op.execute("""
        CREATE POLICY users_super_admin_all ON users
        FOR ALL
        USING (
            current_setting('app.current_user_id', true) <> ''
            AND EXISTS (
                SELECT 1 FROM users u
                WHERE u.user_id = current_setting('app.current_user_id', true)::uuid
                AND u.role = 'SUPER_ADMIN'
            )
        )
    """)
    op.execute("""
        CREATE POLICY users_school_isolation ON users
        FOR ALL
        USING (school_id IS NOT NULL AND school_id = current_setting('app.current_school_id', true)::uuid)
    """)

    # Faculty: tenant isolation
    op.execute("""
        CREATE POLICY faculty_tenant_select ON faculty FOR SELECT
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY faculty_tenant_insert ON faculty FOR INSERT
        WITH CHECK (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY faculty_tenant_update ON faculty FOR UPDATE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY faculty_tenant_delete ON faculty FOR DELETE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)

    # Results: tenant isolation
    op.execute("""
        CREATE POLICY results_tenant_select ON results FOR SELECT
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY results_tenant_insert ON results FOR INSERT
        WITH CHECK (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY results_tenant_update ON results FOR UPDATE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY results_tenant_delete ON results FOR DELETE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)

    # Notices: tenant isolation
    op.execute("""
        CREATE POLICY notices_tenant_select ON notices FOR SELECT
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY notices_tenant_insert ON notices FOR INSERT
        WITH CHECK (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY notices_tenant_update ON notices FOR UPDATE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY notices_tenant_delete ON notices FOR DELETE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)

    # Gallery images: tenant isolation
    op.execute("""
        CREATE POLICY gallery_tenant_select ON gallery_images FOR SELECT
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY gallery_tenant_insert ON gallery_images FOR INSERT
        WITH CHECK (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY gallery_tenant_update ON gallery_images FOR UPDATE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY gallery_tenant_delete ON gallery_images FOR DELETE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)

    # Principal profiles: tenant isolation
    op.execute("""
        CREATE POLICY principal_tenant_select ON principal_profiles FOR SELECT
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY principal_tenant_insert ON principal_profiles FOR INSERT
        WITH CHECK (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY principal_tenant_update ON principal_profiles FOR UPDATE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)
    op.execute("""
        CREATE POLICY principal_tenant_delete ON principal_profiles FOR DELETE
        USING (school_id = current_setting('app.current_school_id', true)::uuid)
    """)


def downgrade():
    # Principal
    op.execute("DROP POLICY IF EXISTS principal_tenant_delete ON principal_profiles")
    op.execute("DROP POLICY IF EXISTS principal_tenant_update ON principal_profiles")
    op.execute("DROP POLICY IF EXISTS principal_tenant_insert ON principal_profiles")
    op.execute("DROP POLICY IF EXISTS principal_tenant_select ON principal_profiles")
    # Gallery
    op.execute("DROP POLICY IF EXISTS gallery_tenant_delete ON gallery_images")
    op.execute("DROP POLICY IF EXISTS gallery_tenant_update ON gallery_images")
    op.execute("DROP POLICY IF EXISTS gallery_tenant_insert ON gallery_images")
    op.execute("DROP POLICY IF EXISTS gallery_tenant_select ON gallery_images")
    # Notices
    op.execute("DROP POLICY IF EXISTS notices_tenant_delete ON notices")
    op.execute("DROP POLICY IF EXISTS notices_tenant_update ON notices")
    op.execute("DROP POLICY IF EXISTS notices_tenant_insert ON notices")
    op.execute("DROP POLICY IF EXISTS notices_tenant_select ON notices")
    # Results
    op.execute("DROP POLICY IF EXISTS results_tenant_delete ON results")
    op.execute("DROP POLICY IF EXISTS results_tenant_update ON results")
    op.execute("DROP POLICY IF EXISTS results_tenant_insert ON results")
    op.execute("DROP POLICY IF EXISTS results_tenant_select ON results")
    # Faculty
    op.execute("DROP POLICY IF EXISTS faculty_tenant_delete ON faculty")
    op.execute("DROP POLICY IF EXISTS faculty_tenant_update ON faculty")
    op.execute("DROP POLICY IF EXISTS faculty_tenant_insert ON faculty")
    op.execute("DROP POLICY IF EXISTS faculty_tenant_select ON faculty")
    # Users
    op.execute("DROP POLICY IF EXISTS users_school_isolation ON users")
    op.execute("DROP POLICY IF EXISTS users_super_admin_all ON users")
