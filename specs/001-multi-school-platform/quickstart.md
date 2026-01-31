# Quickstart Guide: Multi-School Website Platform

**Feature**: 001-multi-school-platform | **Date**: 2026-01-31
**Status**: Draft
**Related**: [spec.md](./spec.md), [plan.md](./plan.md), [data-model.md](./data-model.md)

---

## Overview

This guide walks you through setting up the development environment for the multi-school website platform. After completing this guide, you'll have:

- PostgreSQL 15+ database with RLS policies
- FastAPI backend running on `http://localhost:8000`
- Next.js frontend running on `http://localhost:3000`
- Sample school tenant for testing

**Estimated Setup Time**: 30-45 minutes

---

## Prerequisites

Before starting, ensure you have the following installed:

### Required Software

| Software | Version | Download Link | Verification Command |
|----------|---------|---------------|----------------------|
| **Python** | 3.11+ | https://python.org | `python --version` |
| **Node.js** | 18+ | https://nodejs.org | `node --version` |
| **PostgreSQL** | 15+ | https://postgresql.org | `psql --version` |
| **Git** | 2.x+ | https://git-scm.com | `git --version` |

### Optional (Recommended)

- **Docker Desktop** (for containerized PostgreSQL): https://docker.com
- **VS Code** with extensions:
  - Python (Microsoft)
  - Pylance
  - ESLint
  - Prettier
  - PostgreSQL (Chris Kolkman)

---

## Step 1: Clone Repository and Setup

### 1.1 Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd multi_school_website

# Switch to feature branch
git checkout 001-multi-school-platform
```

### 1.2 Project Structure Verification

Verify the following directory structure exists:

```text
multi_school_website/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── specs/                # Feature specifications
│   └── 001-multi-school-platform/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── quickstart.md (this file)
│       └── contracts/
└── README.md
```

---

## Step 2: Database Setup

### Option A: Local PostgreSQL Installation

#### 2.1 Install PostgreSQL

**Windows**:
```bash
# Download installer from postgresql.org
# During installation:
# - Set password for 'postgres' user
# - Note the port (default: 5432)
# - Install pgAdmin 4 (recommended)
```

**macOS (Homebrew)**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install postgresql-15 postgresql-contrib-15
sudo systemctl start postgresql
```

#### 2.2 Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE multi_school_db;
CREATE USER school_admin WITH PASSWORD 'dev_password_2026';
GRANT ALL PRIVILEGES ON DATABASE multi_school_db TO school_admin;

# Exit psql
\q
```

### Option B: Docker PostgreSQL (Recommended)

#### 2.1 Create Docker Compose File

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: multi_school_postgres
    environment:
      POSTGRES_DB: multi_school_db
      POSTGRES_USER: school_admin
      POSTGRES_PASSWORD: dev_password_2026
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U school_admin"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

#### 2.2 Start PostgreSQL Container

```bash
# Start PostgreSQL
docker-compose up -d postgres

# Verify container is running
docker ps

# Check logs
docker-compose logs postgres
```

#### 2.3 Verify Database Connection

```bash
# Connect to database
psql -h localhost -U school_admin -d multi_school_db

# Should see:
# multi_school_db=>

# Exit
\q
```

---

## Step 3: Backend Setup (FastAPI)

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Python Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

Verify activation (prompt should show `(venv)`).

### 3.3 Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install backend dependencies
pip install -r requirements.txt

# If requirements.txt doesn't exist yet, install manually:
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 sqlalchemy==2.0.23 \
    alembic==1.12.1 psycopg2-binary==2.9.9 pydantic==2.5.0 \
    python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 \
    python-multipart==0.0.6 pytest==7.4.3 pytest-asyncio==0.21.1 \
    httpx==0.25.1 pytest-cov==4.1.0
```

### 3.4 Configure Environment Variables

Create `backend/.env` file:

```bash
# Database Configuration
DATABASE_URL=postgresql://school_admin:dev_password_2026@localhost:5432/multi_school_db

# JWT Configuration
SECRET_KEY=dev_secret_key_change_in_production_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Configuration
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# File Storage
STORAGE_PATH=../data/schools
MAX_FILE_SIZE_MB=5

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
```

**Security Note**: Never commit `.env` files to version control. Add to `.gitignore`.

### 3.5 Initialize Database Schema

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema with RLS policies"

# Apply migrations
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema with RLS policies
```

### 3.6 Seed Initial Data

Create `backend/scripts/seed_data.py`:

```python
import asyncio
from src.services.school_service import SchoolService
from src.services.auth_service import AuthService

async def seed_development_data():
    """Seed database with development data"""

    # Create Super Admin
    auth_service = AuthService()
    super_admin = await auth_service.create_user({
        "email": "admin@platform.com",
        "password": "SuperAdmin123!",
        "role": "SUPER_ADMIN",
        "full_name": "Platform Administrator"
    })
    print(f"✓ Created Super Admin: {super_admin.email}")

    # Create Demo School
    school_service = SchoolService()
    demo_school = await school_service.create_school({
        "school_name": "Springfield High School",
        "subdomain": "springfield",
        "contact_email": "admin@springfield.edu",
        "contact_phone": "+1-555-0100",
        "address": "123 Education St, Springfield, IL 62701",
        "primary_color": "#0A3D62",
        "secondary_color": "#EAF2F8"
    })
    print(f"✓ Created Demo School: {demo_school.school_name} ({demo_school.subdomain})")

    # Create School Admin for Demo School
    school_admin = await auth_service.create_user({
        "email": "admin@springfield.edu",
        "password": "SchoolAdmin123!",
        "role": "SCHOOL_ADMIN",
        "full_name": "John Smith",
        "school_id": demo_school.school_id
    })
    print(f"✓ Created School Admin: {school_admin.email}")

    # Create Staff for Demo School
    staff = await auth_service.create_user({
        "email": "staff@springfield.edu",
        "password": "Staff123!",
        "role": "STAFF",
        "full_name": "Jane Doe",
        "school_id": demo_school.school_id
    })
    print(f"✓ Created Staff: {staff.email}")

    print("\n=== Development Data Seed Complete ===")
    print("\nLogin Credentials:")
    print("  Super Admin: admin@platform.com / SuperAdmin123!")
    print("  School Admin: admin@springfield.edu / SchoolAdmin123!")
    print("  Staff: staff@springfield.edu / Staff123!")

if __name__ == "__main__":
    asyncio.run(seed_development_data())
```

Run seed script:

```bash
python scripts/seed_data.py
```

### 3.7 Start Backend Server

```bash
# Start FastAPI with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn src.main:app --reload
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3.8 Verify Backend API

Open browser and navigate to:

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/health

Test login endpoint:
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@platform.com","password":"SuperAdmin123!"}'
```

**Expected Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "user_id": "...",
    "email": "admin@platform.com",
    "role": "SUPER_ADMIN",
    "full_name": "Platform Administrator",
    "schools": []
  }
}
```

---

## Step 4: Frontend Setup (Next.js)

### 4.1 Navigate to Frontend Directory

Open a **new terminal** (keep backend running) and navigate to frontend:

```bash
cd frontend
```

### 4.2 Install Node.js Dependencies

```bash
# Install all dependencies
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

**Expected Dependencies** (check `package.json`):
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.3.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@testing-library/react": "^14.0.0",
    "vitest": "^1.0.0",
    "playwright": "^1.40.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### 4.3 Configure Environment Variables

Create `frontend/.env.local` file:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/v1

# Application Configuration
NEXT_PUBLIC_APP_NAME=Multi-School Platform
NEXT_PUBLIC_ENVIRONMENT=development

# Feature Flags
NEXT_PUBLIC_ENABLE_DEBUG=true
```

### 4.4 Configure Subdomain Routing (Development)

For local development, we need to simulate subdomain routing. Add to `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts` on Windows):

```
127.0.0.1    springfield.localhost
127.0.0.1    demo.localhost
```

**Note**: You may need admin/sudo privileges to edit hosts file.

### 4.5 Start Frontend Development Server

```bash
# Start Next.js with dev server
npm run dev

# Or using yarn
yarn dev

# Or using pnpm
pnpm dev
```

**Expected Output**:
```
  ▲ Next.js 14.0.0
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.100:3000

 ✓ Ready in 2.5s
```

### 4.6 Verify Frontend

Open browser and navigate to:

- **Main Domain**: http://localhost:3000
- **Springfield School**: http://springfield.localhost:3000
- **Admin Login**: http://localhost:3000/admin/login

**Troubleshooting Subdomain Routing**:

If subdomain routing doesn't work in development, use query parameter fallback:
- http://localhost:3000?school=springfield

---

## Step 5: Onboard Test School

### 5.1 Login as Super Admin

Navigate to: http://localhost:3000/admin/login

```
Email: admin@platform.com
Password: SuperAdmin123!
```

### 5.2 Create New School

Using API directly (or admin UI if implemented):

```bash
# Get access token first (from login response)
ACCESS_TOKEN="<your-access-token>"

# Create school
curl -X POST http://localhost:8000/v1/schools \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "school_name": "Greenwood Academy",
    "subdomain": "greenwood",
    "contact_email": "admin@greenwood.edu",
    "contact_phone": "+1-555-0200",
    "address": "456 Learning Ave, Greenwood, CA 90210",
    "primary_color": "#2C3E50",
    "secondary_color": "#ECF0F1"
  }'
```

### 5.3 Create School Admin

```bash
# Create admin for Greenwood Academy
curl -X POST http://localhost:8000/v1/schools/{school_id}/admins \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@greenwood.edu",
    "password": "GreenAdmin123!",
    "role": "SCHOOL_ADMIN",
    "full_name": "Alice Johnson"
  }'
```

### 5.4 Verify New School

Add to `/etc/hosts`:
```
127.0.0.1    greenwood.localhost
```

Navigate to: http://greenwood.localhost:3000

---

## Step 6: Run Tests

### 6.1 Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_school_service.py

# Run integration tests
pytest tests/integration/

# Run security tests
pytest tests/security/test_tenant_isolation.py -v
```

**Expected Coverage**: ≥90% for business logic

### 6.2 Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run unit tests with coverage
npm run test:coverage

# Run E2E tests (requires backend running)
npm run test:e2e

# Run specific E2E test
npm run test:e2e -- tests/e2e/public-visitor.spec.ts
```

**Expected Coverage**: ≥70% for critical user journeys

---

## Step 7: Development Workflow

### 7.1 Daily Development Setup

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

**Terminal 3 - Database (Docker)**:
```bash
docker-compose up postgres
```

### 7.2 Database Migrations

**Create New Migration**:
```bash
cd backend
alembic revision --autogenerate -m "Add new column to faculty table"
```

**Apply Migration**:
```bash
alembic upgrade head
```

**Rollback Migration**:
```bash
alembic downgrade -1
```

### 7.3 TDD Workflow (Red-Green-Refactor)

**Step 1 - Red**: Write failing test
```python
# backend/tests/unit/test_faculty_service.py

@pytest.mark.asyncio
async def test_create_faculty_validates_email():
    service = FacultyService()

    with pytest.raises(ValidationError):
        await service.create_faculty({
            "full_name": "John Doe",
            "email": "invalid-email",  # Invalid format
            # ... other fields
        })
```

**Step 2 - Green**: Implement minimal code to pass
```python
# backend/src/services/faculty_service.py

from pydantic import EmailStr, ValidationError

async def create_faculty(self, data: dict):
    # Validate email format
    if "email" in data:
        EmailStr.validate(data["email"])

    # ... create faculty
```

**Step 3 - Refactor**: Improve code quality
```python
# Extract to validator utility
from src.utils.validators import validate_email

async def create_faculty(self, data: dict):
    if "email" in data:
        validate_email(data["email"])
    # ... create faculty
```

---

## Troubleshooting

### Issue: Database Connection Failed

**Error**: `psycopg2.OperationalError: connection to server failed`

**Solution**:
1. Verify PostgreSQL is running:
   ```bash
   # Docker
   docker ps | grep postgres

   # Local installation (Linux/Mac)
   pg_isready
   ```

2. Check connection string in `.env`:
   ```bash
   DATABASE_URL=postgresql://school_admin:dev_password_2026@localhost:5432/multi_school_db
   ```

3. Verify database exists:
   ```bash
   psql -U school_admin -d multi_school_db -c "\l"
   ```

### Issue: Port Already in Use

**Error**: `Address already in use: port 8000`

**Solution**:
```bash
# Find process using port
# Linux/Mac
lsof -i :8000

# Windows
netstat -ano | findstr :8000

# Kill process (replace PID)
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows
```

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Next.js Build Errors

**Error**: `Module parse failed: Unexpected token`

**Solution**:
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Restart dev server
npm run dev
```

### Issue: CORS Errors in Browser

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:

Update `backend/.env`:
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://springfield.localhost:3000
```

Update `backend/src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://springfield.localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Next Steps

After completing this setup:

1. **Review Specifications**:
   - Read [spec.md](./spec.md) for feature requirements
   - Review [plan.md](./plan.md) for architecture decisions
   - Study [data-model.md](./data-model.md) for database schema

2. **Explore API Contracts**:
   - Review OpenAPI specs in [contracts/](./contracts/)
   - Test endpoints using Swagger UI at http://localhost:8000/docs

3. **Begin Implementation**:
   - Run `/sp.tasks` command to generate implementation tasks
   - Follow TDD workflow (Red-Green-Refactor)
   - Start with P1 user stories (public website visitor, school admin content management)

4. **Join Development Workflow**:
   - Create feature branches from `001-multi-school-platform`
   - Write tests first, then implementation
   - Run full test suite before committing
   - Follow commit message conventions

---

## Useful Commands Reference

### Backend Commands
```bash
# Start server
uvicorn src.main:app --reload

# Run tests
pytest --cov=src

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

### Frontend Commands
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Run tests
npm run test

# Run E2E tests
npm run test:e2e

# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check
```

### Database Commands
```bash
# Connect to database
psql -h localhost -U school_admin -d multi_school_db

# Backup database
pg_dump -U school_admin multi_school_db > backup.sql

# Restore database
psql -U school_admin multi_school_db < backup.sql

# View tables
\dt

# Describe table
\d table_name

# View RLS policies
\d+ table_name
```

---

## Support

For issues or questions:

1. Check troubleshooting section above
2. Review [spec.md](./spec.md) for requirements
3. Check API documentation at http://localhost:8000/docs
4. Review test cases for usage examples

---

**Last Updated**: 2026-01-31
**Next Review**: After implementation tasks are generated
