-- Multi-School Website Platform - Database initialization
-- Run once after creating the database (e.g. after Docker/postgres is up).
-- Extensions required for UUID generation and crypto (e.g. gen_random_uuid).

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Optional: pgcrypto for gen_random_uuid and other crypto helpers
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Note: Full schema (tables, RLS, triggers) is managed by Alembic migrations.
-- Run: alembic upgrade head
