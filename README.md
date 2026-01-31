# Multi-School Website Platform

A modern, production-ready multi-tenant platform for managing multiple school websites with comprehensive admin features.

## 🎯 Features

### Public Features
- ✅ **School Homepage** - Customizable landing page with hero banner
- ✅ **Principal's Message** - Welcome message with photo
- ✅ **Faculty Directory** - Staff profiles with photos and qualifications
- ✅ **Exam Results** - Student results with JSONB data structure
- ✅ **Top Performers** - Display top 3 students on homepage
- ✅ **Notice Board** - Announcements with priority levels
- ✅ **Photo Gallery** - School events and activities
- ✅ **Responsive Design** - Mobile, tablet, and desktop support

### Admin Features
- ✅ **Dashboard** - Content management overview
- ✅ **Faculty Management** - Add/edit/delete staff profiles
- ✅ **Results Upload** - Publish exam results with student-wise marks
- ✅ **Notice Management** - Create and schedule announcements
- ✅ **Gallery Management** - Upload and organize photos
- ✅ **Branding** - Customize school logo, colors, and banner
- ✅ **Role-Based Access** - Super Admin, School Admin, Staff roles

### Technical Features
- ✅ **Multi-Tenant Architecture** - Single platform, multiple schools
- ✅ **JWT Authentication** - Secure with refresh tokens
- ✅ **PostgreSQL Database** - JSONB for flexible data structures
- ✅ **Redis Caching** - Per-school data caching
- ✅ **WCAG 2.1 Level AA** - Accessible design
- ✅ **Server-Side Rendering** - Next.js 14+ with App Router
- ✅ **Type Safety** - Full TypeScript implementation

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: React Context + Hooks
- **Forms**: React Hook Form + Zod validation

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL 14+
- **Cache**: Redis
- **Auth**: JWT with httpOnly cookies
- **ORM**: SQLAlchemy
- **Migrations**: Alembic

## 📦 Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 14+
- Redis (optional for caching)

### Installation

#### 1. Clone the repository
```bash
git clone <your-repo-url>
cd multi_school_website
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (when DB is set up)
alembic upgrade head

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: http://localhost:8000

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Start development server
npm run dev
```

Frontend will run at: http://localhost:3000

### 🎨 Demo Mode

The project includes demo data and HTML demos:

```bash
# Start backend (for API)
cd backend && python main.py

# Open demo files in browser
demo-improved.html  # Latest demo with all features
demo-fixed.html     # Demo with sticky header
```

Demo data includes:
- Greenfield International School
- 12 Class 10 students with detailed marks
- 8 Class 12 students
- 6 Class 9 students
- 6 faculty members
- Multiple notices and gallery images

## 📁 Project Structure

```
multi_school_website/
├── frontend/           # Next.js application
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   └── package.json
├── backend/            # FastAPI application
│   ├── src/
│   │   ├── api/       # API endpoints
│   │   ├── core/      # Core utilities
│   │   ├── db/        # Database models
│   │   └── services/
│   ├── alembic/       # Database migrations
│   ├── main.py        # Application entry
│   └── requirements.txt
├── specs/              # Feature specifications
├── docs/               # Documentation
├── images/             # Demo images
└── docker-compose.yml  # Docker setup
```

## 🔒 Security

- ✅ JWT tokens with refresh rotation
- ✅ Password hashing (bcrypt)
- ✅ CSRF protection
- ✅ XSS prevention
- ✅ SQL injection prevention (ORM)
- ✅ Rate limiting (production)
- ✅ Input validation (Zod + Pydantic)
- ✅ Secure headers (CORS, CSP)

See [SECURITY.md](SECURITY.md) for details.

## 📊 Database Schema

### Core Tables
- `schools` - Multi-tenant school data
- `users` - Authentication and roles
- `faculty` - Staff profiles
- `results` - Exam results (JSONB for student marks)
- `notices` - Announcements
- `gallery` - Photo gallery
- `principal_messages` - Welcome messages

See `backend/alembic/versions/` for full schema.

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- Vercel (Frontend)
- Railway/Render (Backend)
- PostgreSQL setup
- Redis configuration
- Environment variables

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test

# Backend tests
cd backend
pytest

# E2E tests
npm run test:e2e
```

## 📝 Documentation

- [SECURITY.md](SECURITY.md) - Security guidelines
- [PERFORMANCE.md](PERFORMANCE.md) - Performance optimization
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [PHASE_8_COMPLETE.md](PHASE_8_COMPLETE.md) - Implementation checklist
- [specs/](specs/) - Feature specifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Built with Claude Code
- Next.js documentation
- FastAPI documentation
- Tailwind CSS

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com

---

**Status**: ✅ Phase 8 Complete - Production Ready

**Version**: 1.0.0

**Last Updated**: February 2026
