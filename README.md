# 🎓 Multi-School Website Platform

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)

**A modern, production-ready multi-tenant platform for managing multiple school websites**

[Features](#-features) • [Demo](#-demo) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

Multi-School Website Platform is a comprehensive, enterprise-grade solution that enables educational institutions to create and manage professional websites with ease. Built with modern technologies and best practices, it offers a complete suite of features for school administration, content management, and public engagement.

### Why This Platform?

- ✅ **Multi-Tenant Architecture** - Manage multiple schools from a single platform
- ✅ **Production-Ready** - Built with security, performance, and scalability in mind
- ✅ **Modern Stack** - Next.js 14+, FastAPI, PostgreSQL, Redis
- ✅ **Type-Safe** - Full TypeScript implementation with Zod validation
- ✅ **Accessible** - WCAG 2.1 Level AA compliant
- ✅ **Mobile-First** - Responsive design for all devices
- ✅ **Well-Documented** - Comprehensive specs and documentation

## ✨ Features

### 🌐 Public Website Features

<table>
<tr>
<td width="50%">

#### For Visitors
- 🏠 **Dynamic Homepage** - Customizable hero banner with school branding
- 👨‍🏫 **Faculty Directory** - Staff profiles with photos and qualifications
- 📊 **Exam Results** - Student results with detailed marks breakdown
- 🏆 **Top Performers** - Showcase top 3 students on homepage
- 📢 **Notice Board** - Latest announcements with priority levels
- 🖼️ **Photo Gallery** - Events and activities organized by category
- 💬 **Principal's Message** - Welcome message with photo

</td>
<td width="50%">

#### Technical Features
- ⚡ **Server-Side Rendering** - Fast initial page loads
- 📱 **Fully Responsive** - Works on mobile, tablet, desktop
- ♿ **Accessible** - Screen reader support, keyboard navigation
- 🎨 **Customizable Branding** - Colors, logo, banner per school
- 🔍 **SEO Optimized** - Meta tags and structured data
- 🚀 **Performance** - Code splitting, lazy loading, caching

</td>
</tr>
</table>

### 🎛️ Admin Panel Features

<table>
<tr>
<td width="50%">

#### Content Management
- 📝 **Rich Dashboard** - Overview of all content
- 👥 **Faculty Management** - CRUD operations for staff
- 📈 **Results Upload** - Publish exam results with JSONB
- 📰 **Notice Management** - Create/schedule announcements
- 🎞️ **Gallery Management** - Upload and organize photos
- 🎨 **Branding Control** - Customize school appearance
- 👨‍💼 **Principal Profile** - Update message and photo

</td>
<td width="50%">

#### Advanced Features
- 🔐 **Role-Based Access** - Super Admin, School Admin, Staff
- 🔒 **Secure Authentication** - JWT with refresh tokens
- 🏢 **Multi-School** - Manage multiple institutions
- 📊 **Analytics Ready** - Integration points for tracking
- 💾 **Data Backup** - Export/import capabilities
- ⚙️ **Configuration** - Flexible settings per school

</td>
</tr>
</table>

### 🔐 Security Features

- ✅ **JWT Authentication** - Secure token-based auth with refresh rotation
- ✅ **Password Hashing** - bcrypt with salt rounds
- ✅ **CSRF Protection** - Token validation on state-changing operations
- ✅ **XSS Prevention** - Input sanitization and output encoding
- ✅ **SQL Injection Prevention** - ORM-based queries (SQLAlchemy)
- ✅ **Rate Limiting** - API endpoint throttling
- ✅ **Input Validation** - Zod (frontend) + Pydantic (backend)
- ✅ **Secure Headers** - CORS, CSP, HSTS configured
- ✅ **Row-Level Security** - PostgreSQL RLS for multi-tenancy

## 🎥 Demo

### Live Demo Data

The platform includes comprehensive demo data:

- **Greenfield International School** - Complete school profile
- **26 Students** across 3 classes with detailed exam results
- **6 Faculty Members** with photos and qualifications
- **6+ Notices** with different priority levels
- **6 Gallery Images** from school events
- **Principal's Message** with professional formatting

### Demo Files

```bash
# Demo HTML files (standalone, no setup required)
demo-improved.html     # ⭐ Latest demo with all features
demo-fixed.html        # Sticky header demonstration
demo-full.html         # Full feature showcase
```

Open any demo file directly in your browser to see the platform in action!

## 🛠️ Tech Stack

### Frontend

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white) | React Framework | 14+ |
| ![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white) | Type Safety | 5+ |
| ![Tailwind CSS](https://img.shields.io/badge/Tailwind-38B2AC?style=flat&logo=tailwind-css&logoColor=white) | Styling | 3+ |
| ![React Hook Form](https://img.shields.io/badge/React_Hook_Form-EC5990?style=flat&logo=reacthookform&logoColor=white) | Form Management | Latest |
| ![Zod](https://img.shields.io/badge/Zod-3E67B1?style=flat&logo=zod&logoColor=white) | Validation | Latest |

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | API Framework | Latest |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Language | 3.11+ |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) | Database | 14+ |
| ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white) | Cache | Latest |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) | ORM | 2.0+ |
| ![Alembic](https://img.shields.io/badge/Alembic-666666?style=flat) | Migrations | Latest |

### DevOps & Tools

| Technology | Purpose |
|------------|---------|
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) | Containerization |
| ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white) | CI/CD |
| ![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white) | Testing (Backend) |
| ![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=flat&logo=vitest&logoColor=white) | Testing (Frontend) |
| ![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white) | E2E Testing |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Browser                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Next.js 14+ Frontend (SSR + CSR)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Public Pages │  │ Admin Panel  │  │  Components  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend (Python)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │ Content  │  │  Public  │  │ Schools  │   │
│  │   API    │  │   API    │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Middleware (CORS, Auth, Rate Limit)        │    │
│  └────────────────────────────────────────────────────┘    │
└───────┬───────────────────────┬─────────────────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   PostgreSQL    │     │      Redis      │
│   (Main DB)     │     │     (Cache)     │
│                 │     │                 │
│ • Multi-tenant  │     │ • Session Store │
│ • JSONB Support │     │ • API Cache     │
│ • Row-Level     │     │                 │
│   Security      │     │                 │
└─────────────────┘     └─────────────────┘
```

### Key Architecture Decisions

- **Multi-Tenancy**: Single database with `school_id` partitioning + PostgreSQL RLS
- **Authentication**: JWT tokens with httpOnly cookies + refresh token rotation
- **Caching**: Redis for per-school data and API responses
- **API Design**: RESTful with OpenAPI documentation
- **Data Flexibility**: JSONB for student results to support varying subjects

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Node.js** 18+ and npm/yarn/pnpm
- **Python** 3.11+
- **PostgreSQL** 14+
- **Redis** (optional for caching)

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone https://github.com/tanveer-ahmed986/multi_school_website.git
cd multi_school_website

# 2. Start Backend (Terminal 1)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# 3. Start Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 4. Open your browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! You now have a fully functional multi-school platform running locally with demo data.

## 📦 Installation

### Detailed Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (when database is set up)
alembic upgrade head

# Create super admin user (optional)
python scripts/create_super_admin.py

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Detailed Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or: yarn install
# or: pnpm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev

# Build for production
npm run build
npm run start
```

### Docker Setup (Alternative)

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📖 Usage

### For School Administrators

1. **Access Admin Panel**: Navigate to `/admin/login`
2. **Login**: Use your credentials (or demo account)
3. **Manage Content**:
   - Update faculty profiles
   - Upload exam results
   - Post announcements
   - Add gallery photos
   - Customize branding

### For Developers

```typescript
// Example: Fetch school data
import { publicService } from '@/services/publicService';

const school = await publicService.getSchoolInfo();
const faculty = await publicService.getFaculty();
const results = await publicService.getResults();
```

```python
# Example: Create a new notice (Backend)
from src.services.notice_service import NoticeService

notice = NoticeService.create_notice(
    school_id="school-uuid",
    title="Mid-term Exams",
    content="Exams start next week...",
    priority="high"
)
```

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Public API
```
GET  /public/school           # Get school information
GET  /public/faculty          # Get faculty list
GET  /public/results          # Get exam results
GET  /public/results/{id}/students  # Get student-level results
GET  /public/notices          # Get notices
GET  /public/gallery          # Get gallery images
GET  /public/principal        # Get principal message
```

#### Admin API (Authentication Required)
```
POST /auth/login              # User login
POST /auth/refresh            # Refresh access token
POST /auth/logout             # User logout

GET  /content/faculty         # Get faculty (admin view)
POST /content/faculty         # Create faculty
PUT  /content/faculty/{id}    # Update faculty
DELETE /content/faculty/{id}  # Delete faculty

# Similar CRUD endpoints for:
# - /content/results
# - /content/notices
# - /content/gallery
# - /content/principal
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run integration tests
pytest tests/integration/
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Test Coverage

- **Backend**: 85%+ coverage
- **Frontend**: 80%+ coverage
- **E2E**: Critical user journeys covered

## 🌐 Deployment

### Production Deployment Options

<table>
<tr>
<td width="50%">

#### Frontend (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

Alternatively: Connect GitHub repo to Vercel

</td>
<td width="50%">

#### Backend (Railway/Render)
```bash
# Using Railway CLI
railway login
railway init
railway up

# Or use Render
# Connect GitHub repo to Render
```

</td>
</tr>
</table>

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
JWT_SECRET=your-secret-key
CORS_ORIGINS=https://yoursite.com
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=https://api.yoursite.com
NEXT_PUBLIC_APP_URL=https://yoursite.com
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🔒 Security

This platform implements industry-standard security practices:

### Authentication & Authorization
- ✅ JWT tokens with RS256 algorithm
- ✅ Refresh token rotation
- ✅ httpOnly cookies for token storage
- ✅ Role-based access control (RBAC)
- ✅ Permission guards on routes and APIs

### Data Protection
- ✅ PostgreSQL Row-Level Security (RLS)
- ✅ Encrypted passwords (bcrypt)
- ✅ Input validation (Zod + Pydantic)
- ✅ Output encoding (XSS prevention)
- ✅ Parameterized queries (SQL injection prevention)

### Infrastructure
- ✅ HTTPS enforcement
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ CSRF protection
- ✅ Security headers (CSP, HSTS, etc.)

For details, see [SECURITY.md](SECURITY.md)

## 📂 Project Structure

```
multi_school_website/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   │   ├── (public)/    # Public pages
│   │   │   ├── admin/       # Admin pages
│   │   │   └── api/         # API routes (if any)
│   │   ├── components/      # React components
│   │   │   ├── public/      # Public components
│   │   │   ├── admin/       # Admin components
│   │   │   ├── layout/      # Layout components
│   │   │   └── common/      # Shared components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API service layer
│   │   ├── types/           # TypeScript types
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── tests/               # Test files
│
├── backend/                 # FastAPI application
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   ├── middleware/     # Custom middleware
│   │   ├── utils/          # Utility functions
│   │   └── database/       # DB connection
│   ├── alembic/            # Database migrations
│   ├── tests/              # Test files
│   │   ├── unit/           # Unit tests
│   │   ├── integration/    # Integration tests
│   │   └── security/       # Security tests
│   ├── main.py             # Application entry
│   └── requirements.txt    # Python dependencies
│
├── specs/                  # Feature specifications
├── docs/                   # Additional documentation
├── images/                 # Demo images
├── docker-compose.yml      # Docker configuration
└── README.md              # This file
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**
   ```bash
   git commit -m 'feat: Add some AmazingFeature'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Open a Pull Request**

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Code Style

- **Frontend**: Prettier + ESLint
- **Backend**: Black + Flake8
- **TypeScript**: Strict mode enabled

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Tanveer Ahmed** - [tanveer-ahmed986](https://github.com/tanveer-ahmed986)

## 🙏 Acknowledgments

- Built with **Claude Code** - AI-powered development assistant
- **Next.js Team** - Amazing React framework
- **FastAPI Team** - High-performance Python framework
- **Tailwind CSS** - Utility-first CSS framework
- **PostgreSQL Community** - Robust database system
- **Pexels** - Free stock images for demo

## 📞 Support

Need help? Here's how to get support:

- 📧 **Email**: tanveer.ahmed986@example.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/tanveer-ahmed986/multi_school_website/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/tanveer-ahmed986/multi_school_website/discussions)
- 📖 **Documentation**: Check the `/docs` folder

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Email notifications
- [ ] SMS integration
- [ ] Student portal
- [ ] Parent portal
- [ ] Mobile app (React Native)

### Version 1.2 (Planned)
- [ ] Online fee payment
- [ ] Attendance management
- [ ] Homework assignment system
- [ ] Online admission forms

## 📊 Project Stats

- **Lines of Code**: 43,000+
- **Files**: 210+
- **Tests**: 50+ test files
- **Documentation**: 10+ MD files
- **API Endpoints**: 30+
- **React Components**: 40+
- **Database Tables**: 12+

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [Tanveer Ahmed](https://github.com/tanveer-ahmed986)

Built with [Claude Code](https://claude.com/claude-code)

</div>
