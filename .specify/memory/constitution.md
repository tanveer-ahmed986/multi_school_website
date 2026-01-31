<!--
Sync Impact Report:
- Version Change: 1.6.0 → 1.7.0
- Modified Principles: None (core principles remain stable)
- Added Sections:
  - School Websites & Student Management Systems (comprehensive educational requirements)
    - Multi-tenant architecture for multiple schools
    - Role-based access control (RBAC) for education stakeholders
    - Student data privacy & compliance (FERPA, COPPA, GDPR)
    - Educational features (student management, gradebook, attendance, reporting)
    - Communication features (parent-teacher, announcements, emergency alerts)
    - Academic management (grades, assignments, schedules, transcripts)
    - Integration requirements (SIS, LMS, SSO)
    - Enhanced accessibility, security, and testing for educational context
    - AI-powered enhancements for school platforms
    - Recommended tech stacks for school websites (Next.js, Django, FastAPI options)
    - Database schema design for multi-tenant school platforms
- Previous Additions (v1.6.0):
  - API Design Standards (REST/GraphQL best practices, versioning, documentation, security, performance, testing)
  - Database Design & Data Layer (schema design, indexing, migrations, multi-tenancy, ORM best practices, backup/recovery)
  - Email, SMS & Notifications Infrastructure (email deliverability, SMS best practices, push notifications, in-app notifications, compliance)
- Previous Additions (v1.5.0):
  - Portfolio Websites, Entertainment Websites, Social Media Platforms
  - AI-Powered Enhancements for all website types
  - AI Features & Machine Learning Integration section
- Removed Sections: None
- Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md (Add school website planning considerations)
  ✅ .specify/templates/spec-template.md (Add school-specific requirements sections)
  ✅ .specify/templates/tasks-template.md (Add school platform implementation tasks)
  ⚠️ Need to create: school-website-checklist.md, ferpa-compliance-checklist.md, multi-tenant-testing-checklist.md
- Follow-up TODOs:
  - Create school website launch checklist
  - Create FERPA/COPPA compliance verification checklist
  - Create multi-tenant security testing guide
  - Add school database schema template
  - Add role-based access control (RBAC) implementation guide
  - Add student data privacy policy template
  - Add school website user guides (admin, teacher, parent, student roles)
-->

# Universal Website Constitution

**Purpose**: This constitution provides comprehensive engineering standards for ALL types of websites including portfolios, e-commerce, SaaS applications, marketing sites, blogs, web applications, and community platforms.

## Core Principles

### I. Test-Driven Development (TDD) - NON-NEGOTIABLE

**All code MUST be developed using strict Test-Driven Development methodology:**

- Tests MUST be written BEFORE any implementation code
- Tests MUST fail initially (Red phase)
- Implementation code MUST be written to make tests pass (Green phase)
- Code MUST be refactored while keeping tests green (Refactor phase)
- All tests MUST pass before any commit or pull request
- Zero tolerance for untested code - test coverage MUST be comprehensive
- Tests MUST be run in CI/CD pipeline and MUST pass for deployment

**Test Pyramid & Coverage:**

- MUST follow test pyramid: ~70% unit tests, ~20% integration tests, ~10% e2e tests
- Unit test coverage MUST be ≥90% for business logic and utilities
- Component test coverage MUST be ≥85% for UI components
- Integration test coverage MUST be ≥70% for critical user journeys
- E2E tests MUST cover all P1 (critical) user flows
- Performance regression tests MUST block deployments if thresholds exceeded
- Accessibility tests MUST run on every component

**Rationale**: TDD ensures code quality, prevents regressions, validates requirements
before implementation, and creates living documentation through tests. The test pyramid
prevents slow, flaky test suites.

### II. Component-Based Architecture

**Website MUST be built as modular, reusable components:**

- Each component MUST have a single, clear responsibility
- Components MUST be independently testable
- Components MUST follow consistent naming conventions
- Shared components MUST be documented with usage examples
- Components MUST handle their own state where appropriate
- Component APIs MUST be explicit and well-defined

**Rationale**: Component-based architecture enables scalability, reusability, and
parallel development. Makes the codebase easier to maintain and extend with new features.

### III. Responsive & Accessible Design with Design System

**Website MUST be accessible and usable across all devices and by all users:**

- MUST be mobile-first responsive (320px to 4K+)
- MUST meet WCAG 2.1 Level AA accessibility standards (minimum)
- MUST support keyboard navigation for all interactive elements
- MUST provide appropriate ARIA labels and semantic HTML
- MUST be tested across major browsers (Chrome, Firefox, Safari, Edge)
- MUST provide alternative text for all images
- MUST maintain readable contrast ratios (minimum 4.5:1 for normal text, 3:1 for large)
- MUST provide touch targets minimum 44px x 44px (WCAG 2.5.5)

**Design System Requirements:**

- MUST define design tokens for colors, spacing, typography, shadows
- MUST maintain consistent component styling across the site
- MUST document style guide or design system
- MUST implement visual regression testing to prevent inconsistencies
- MUST use CSS variables or design token system for theming
- MUST define reusable animation and transition patterns
- MUST specify responsive breakpoints: mobile (320-767px), tablet (768-1023px),
  desktop (1024-1919px), wide (1920px+)

**Accessibility Audit Requirements:**

- MUST run automated a11y tests (axe-core) on every build
- MUST perform manual accessibility audit quarterly
- MUST test with screen readers (NVDA on Windows, VoiceOver on macOS/iOS)
- MUST test keyboard-only navigation
- MUST remediate Critical/Serious accessibility issues within 1 sprint

**Rationale**: Accessibility is both ethical and practical - it expands reach,
improves SEO, and demonstrates professional web development standards. Responsive
design ensures optimal experience regardless of device. A design system maintains
visual consistency and accelerates development.

### IV. Performance & Optimization

**Website MUST be performant and optimized for user experience:**

- Initial page load MUST be under 3 seconds on 3G connections
- Core Web Vitals MUST meet Google's "Good" thresholds:
  - LCP (Largest Contentful Paint): < 2.5s
  - INP (Interaction to Next Paint): < 200ms
  - CLS (Cumulative Layout Shift): < 0.1
  - FCP (First Contentful Paint): < 1.8s
- Images MUST be optimized and served in modern formats (WebP, AVIF with fallbacks)
- Assets MUST be minified and compressed (gzip/brotli)
- Critical CSS MUST be inlined; non-critical CSS deferred
- JavaScript MUST be code-split and lazy-loaded where appropriate
- MUST use CDN for static assets
- MUST implement resource hints (preload, prefetch, preconnect)

**Performance Budgets:**

- JavaScript bundle size: < 150KB (gzipped) for initial load
- CSS bundle size: < 50KB (gzipped) for critical styles
- Total page weight: < 2MB for initial load
- Time to Interactive (TTI): < 5 seconds on 3G

**Uptime & Reliability:**

- MUST maintain 99.9% uptime SLO (Service Level Objective)
- MUST implement health check endpoints
- MUST have monitoring and alerting for downtime
- MUST have incident response procedures (see Production Operations section)

**Rationale**: Performance directly impacts user experience, SEO rankings, and
conversion rates. Performance budgets prevent regression.

### V. Clean Code & Maintainability

**Code MUST be clean, readable, and maintainable:**

- MUST follow established style guides for chosen technologies
- MUST use meaningful variable and function names
- MUST include comments for complex logic only (code should be self-documenting)
- MUST avoid code duplication (DRY principle)
- MUST keep functions small and focused (Single Responsibility Principle)
- MUST use consistent formatting (enforced by linters/formatters)
- MUST follow semantic versioning for releases

**Rationale**: Clean code reduces technical debt, facilitates collaboration, and
makes future updates easier.

### VI. Security & Privacy

**Website MUST implement security best practices:**

- MUST use HTTPS for all traffic with HSTS headers (max-age=31536000)
- MUST sanitize all user inputs (contact forms, etc.)
- MUST implement Content Security Policy (CSP) headers
- MUST protect against common vulnerabilities (XSS, CSRF, injection, SSRF)
- MUST NOT expose sensitive information in client-side code
- MUST comply with privacy regulations (GDPR, CCPA, PIPEDA where applicable)
- MUST use secure, up-to-date dependencies
- MUST implement rate limiting for form submissions and API endpoints
- MUST scan dependencies for vulnerabilities in CI

**Secret Management:**

- MUST use environment variables for all secrets and API keys
- MUST NOT commit secrets to repository (enforce with git-secrets or similar)
- MUST rotate secrets quarterly (API keys, tokens)
- MUST use secret management service (e.g., GitHub Secrets, AWS Secrets Manager, Vault)

**Security Headers:**

- MUST implement: Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options,
  Referrer-Policy, Permissions-Policy

**Rationale**: Security protects both the site owner and visitors. Demonstrates
professional awareness of web security fundamentals.

### VII. Documentation & Knowledge Sharing

**Project MUST maintain comprehensive documentation:**

- README MUST include setup, development, and deployment instructions
- Each feature MUST have accompanying documentation
- API contracts (if applicable) MUST be documented
- Architecture decisions MUST be recorded in ADRs
- Code MUST include JSDoc/TSDoc comments for public APIs
- MUST maintain a changelog following Keep a Changelog format

**Rationale**: Documentation enables collaboration, reduces onboarding time, and
serves as reference for future maintenance.

### VIII. SEO & Discoverability

**Website MUST be optimized for search engines and social sharing:**

- MUST use semantic HTML with proper heading hierarchy (h1 → h6)
- MUST include meta tags (title, description, keywords)
- MUST implement Open Graph tags for social media sharing
- MUST implement Twitter Card tags
- MUST include structured data using JSON-LD (Schema.org)
  - Website schema (for all sites)
  - Organization/Person schema (as applicable)
  - BreadcrumbList schema for navigation
  - Article schema (for blogs)
  - Product schema (for e-commerce)
  - FAQ schema (as applicable)
- MUST generate XML sitemap and robots.txt
- MUST optimize page titles and meta descriptions (unique per page)
- MUST ensure fast indexing and crawlability
- MUST implement canonical URLs to prevent duplicate content
- MUST optimize images with alt text and descriptive filenames
- MUST create SEO-friendly URLs (readable, keyword-rich)

**Rationale**: Proper SEO ensures the site reaches its intended audience. Social
sharing optimization extends reach organically.

### IX. Analytics & Observability

**Website MUST implement monitoring and analytics to enable data-driven improvements:**

- MUST implement privacy-respecting analytics (e.g., Plausible, Fathom, Google Analytics)
- MUST track Core Web Vitals in production (Real User Monitoring)
- MUST implement error tracking and reporting (e.g., Sentry, LogRocket, Bugsnag)
- MUST monitor user journeys and conversion funnels
- MUST track key metrics: page views, bounce rate, time on page, conversions
- MUST NOT collect PII without explicit consent
- MUST provide cookie consent mechanism if using tracking cookies
- MUST respect Do Not Track (DNT) headers where applicable
- MUST log errors and warnings for debugging
- MUST implement uptime monitoring for production

**Alerting Thresholds:**

- MUST alert on error rate > 5% of requests
- MUST alert on uptime < 99.9% over 24-hour period
- MUST alert on Core Web Vitals degradation > 20% from baseline
- MUST alert on 5xx errors (server errors)

**Data Retention:**

- Analytics data: Retain for 13 months minimum (year-over-year comparison)
- Error logs: Retain for 90 days
- Access logs: Retain for 30 days
- Audit logs: Retain for 1 year minimum (or longer for compliance)

**Rationale**: Data-driven insights enable continuous improvement. Error tracking
catches issues before they impact user experience.

### X. Content Management Strategy

**Content MUST be structured, version-controlled, and easy to update:**

- Content items MUST be defined as structured data (JSON, YAML, or Markdown with frontmatter)
- MUST define clear schema for content metadata
- Content MUST be version-controlled alongside code
- Content updates MUST NOT require code changes
- MUST implement content validation in CI (schema validation, required fields)
- MUST separate content from presentation logic
- MUST support multiple content types as needed
- MUST provide templates for new content items
- MUST include content contribution guidelines in documentation

**Rationale**: Separating content from code makes updates faster and enables
non-technical content management. Structured data ensures consistency.

### XI. UI/UX Implementation Techniques

**User interface and experience MUST follow best practices for engagement and usability:**

**Interaction Patterns:**

- MUST provide immediate visual feedback for all user interactions
- MUST implement smooth transitions and micro-interactions (hover states, focus
  indicators, loading states)
- MUST use progressive disclosure to manage complexity
- MUST implement skeleton screens or loading indicators for async content
- MUST provide clear error states with actionable guidance
- MUST use consistent interaction patterns throughout the site

**Navigation & Wayfinding:**

- MUST include clear, persistent navigation
- MUST show current location/active page in navigation
- MUST implement breadcrumbs for deep hierarchies
- MUST provide skip-to-content links for accessibility
- MUST include back-to-top functionality on long pages

**Visual Hierarchy & Typography:**

- MUST establish clear visual hierarchy using size, weight, color, spacing
- MUST use typography scale for consistent sizing (e.g., 1.25 ratio)
- MUST maintain optimal line length (45-75 characters per line)
- MUST use adequate line height (1.5-1.8 for body text)
- MUST ensure sufficient white space between elements

**Forms & Input:**

- MUST provide inline validation with clear error messages
- MUST show field requirements upfront (required, format expectations)
- MUST implement sensible tab order
- MUST disable submit buttons during processing to prevent double submission
- MUST show success/failure states clearly
- MUST preserve user input on validation errors

**Performance Perception:**

- MUST implement optimistic UI updates where appropriate
- MUST use skeleton screens instead of spinners for content loading
- MUST prioritize above-the-fold content rendering
- MUST implement smooth scrolling for anchor links
- MUST lazy-load images and heavy components

**Emotional Design:**

- MUST use animations purposefully to guide attention
- MUST maintain consistent personality in copy and visuals
- MUST celebrate user actions (subtle success animations)
- MUST use appropriate imagery that supports content

**Rationale**: Superior UI/UX differentiates websites and directly impacts user
engagement and conversion.

## Technical Architecture & Programming Structure

### Technology Stack Requirements

**Core Technologies:**

- **Frontend Framework**: Modern framework with strong ecosystem (React, Vue, Svelte, Solid, Angular)
- **Language**: TypeScript for type safety and developer experience
- **Styling**: Multiple options based on team preference and project needs
- **Build Tool**: Modern build tooling (Vite, Next.js, Turbopack, etc.)
- **Testing**: Comprehensive testing stack for all test levels
- **Linting**: ESLint with strict configuration, Prettier for formatting
- **Git Hooks**: Husky for pre-commit hooks (lint, test, type-check)

### Comprehensive Stack Options

**Choose based on project requirements, team expertise, and website type:**

**Option 1: Next.js + TypeScript + Tailwind CSS (Recommended for most projects)**
- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS with custom design tokens
- **Testing**: Vitest + Testing Library + Playwright
- **Best for**: Full-stack apps, marketing sites, e-commerce, SaaS, blogs
- **Pros**: Built-in SSR/SSG, API routes, image optimization, excellent DX
- **Cons**: Vercel-centric, learning curve for App Router

**Option 2: React + Vite + TypeScript + CSS-in-JS (Styled Components/Emotion)**
- **Framework**: React 18+ with Vite
- **Styling**: Styled Components or Emotion with design tokens
- **Testing**: Vitest + Testing Library + Cypress
- **Best for**: SPAs, design-system-heavy projects, web applications
- **Pros**: Component-scoped styles, dynamic theming, TypeScript integration
- **Cons**: Runtime cost, bundle size consideration

**Option 3: React + Vite + TypeScript + CSS Modules**
- **Framework**: React 18+ with Vite
- **Styling**: CSS Modules with PostCSS
- **Testing**: Vitest + Testing Library + Cypress
- **Best for**: Projects prioritizing performance, traditional CSS workflows
- **Pros**: Zero runtime cost, familiar CSS syntax, scoped by default
- **Cons**: Less dynamic theming, separate files

**Option 4: Astro + TypeScript + Tailwind CSS (For content-heavy sites)**
- **Framework**: Astro with islands architecture
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Playwright
- **Best for**: Blogs, documentation sites, marketing sites, portfolios
- **Pros**: Ultra-fast static generation, minimal JavaScript, component framework agnostic
- **Cons**: Limited interactivity without islands, newer ecosystem

**Option 5: Remix + TypeScript + Tailwind CSS**
- **Framework**: Remix with React
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Testing Library + Playwright
- **Best for**: Full-stack apps prioritizing web standards, progressive enhancement
- **Pros**: Excellent data loading, nested routing, web platform focus
- **Cons**: Smaller ecosystem than Next.js, deployment considerations

**Option 6: SvelteKit + TypeScript + Tailwind CSS**
- **Framework**: SvelteKit
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Playwright
- **Best for**: Performance-critical apps, teams preferring Svelte syntax
- **Pros**: No virtual DOM, reactive by default, small bundle sizes
- **Cons**: Smaller ecosystem, fewer third-party components

**Option 7: Vue 3 + Vite + TypeScript + Tailwind CSS**
- **Framework**: Vue 3 with Composition API
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Testing Library + Playwright
- **Best for**: Teams with Vue expertise, progressive web apps
- **Pros**: Gentle learning curve, excellent tooling, flexible architecture
- **Cons**: Smaller ecosystem than React, TypeScript integration improving

**Option 8: Python + FastAPI + React (Full-Stack AI-Powered Applications)**
- **Backend**: FastAPI with Python 3.11+ and async/await
- **Frontend**: React 18+ with TypeScript
- **Styling**: Tailwind CSS or Material-UI
- **Testing**: pytest + pytest-asyncio + Testing Library + Playwright
- **Best for**: AI/ML applications, data science platforms, intelligent automation, chatbots
- **Pros**: Superior AI/ML ecosystem (TensorFlow, PyTorch, scikit-learn, Hugging Face), fast async performance, automatic OpenAPI documentation, type safety with Pydantic
- **Cons**: Fewer frontend integrations than Next.js, requires separate frontend and backend deployment
- **AI Libraries**: LangChain, OpenAI SDK, Anthropic SDK, Hugging Face Transformers, spaCy, NLTK

**Option 9: Python + Django + HTMX (Traditional Full-Stack with Modern UX)**
- **Backend**: Django 5+ with Python 3.11+
- **Frontend**: HTMX for dynamic interactions without heavy JavaScript
- **Styling**: Tailwind CSS
- **Testing**: pytest + pytest-django + Playwright
- **Best for**: Content management systems, admin-heavy applications, AI-powered content platforms
- **Pros**: Batteries-included framework, robust ORM, excellent admin interface, mature AI integration ecosystem
- **Cons**: Monolithic architecture, steeper learning curve, less modern frontend patterns
- **AI Integration**: Easy integration with TensorFlow, PyTorch, scikit-learn, Celery for background ML tasks

**Option 10: Python + Flask + React (Microservices AI Backend)**
- **Backend**: Flask with Python 3.11+ for lightweight microservices
- **Frontend**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **Testing**: pytest + Testing Library + Playwright
- **Best for**: Microservices architecture, ML model serving, API-first applications, AI prototypes
- **Pros**: Minimal and flexible, easy to learn, excellent for ML model deployment, microservice-friendly
- **Cons**: Less batteries-included than Django/FastAPI, requires more manual setup, async support limited

**Design-System-Heavy Projects:**

For teams building and maintaining extensive design systems:

- **Primary Stack**: React + TypeScript + Styled Components/Emotion OR CSS-in-JS
- **Component Development**: Storybook for component library development and documentation
- **Design Tokens**: Style Dictionary or Theo for cross-platform design tokens
- **Documentation**: Docusaurus or Storybook Docs for comprehensive component docs
- **Testing**: Chromatic for visual regression testing of component library
- **Package Management**: Monorepo with Turborepo or Nx for multi-package design systems
- **CI/CD**: Automated component releases with Changesets
- **Best Practices**:
  - Atomic design methodology for component organization
  - Comprehensive Storybook stories for all components and variants
  - Design token documentation with usage examples
  - Accessibility props and documentation for all components
  - TypeScript prop interfaces for all components
  - Version all design system packages semantically
  - Automated visual regression testing on every PR
  - Component usage analytics to track adoption

**Hosting & Deployment:**

- MUST support CI/CD (GitHub Actions, GitLab CI, CircleCI, or equivalent)
- MUST use modern hosting (Vercel, Netlify, Cloudflare Pages, AWS Amplify, Render, Fly.io, or similar)
- MUST support preview deployments for pull requests
- MUST have production and staging environments
- SHOULD have development environment for testing

### Project Structure

**MUST follow this folder organization (adapt based on framework):**

**Frontend-Only or Next.js/React Projects:**

```
project_root/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── common/           # Shared components (Button, Card, etc.)
│   │   ├── layout/           # Layout components (Header, Footer, etc.)
│   │   ├── forms/            # Form components
│   │   └── sections/         # Page-specific sections
│   ├── pages/ (or app/)      # Page components or routes (framework-specific)
│   ├── content/              # Structured content (if applicable)
│   ├── styles/               # Global styles and design tokens
│   │   ├── tokens/           # Design tokens (colors, spacing, etc.)
│   │   └── global/           # Global styles and resets
│   ├── utils/                # Utility functions
│   ├── hooks/                # Custom hooks (React/Vue)
│   ├── types/                # TypeScript type definitions
│   ├── lib/                  # Third-party integrations
│   ├── services/             # API services and data fetching
│   ├── contexts/             # React Context providers (if using Context)
│   ├── store/                # State management (Redux, Zustand, Pinia, etc.)
│   └── assets/               # Static assets (images, fonts, icons)
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   ├── e2e/                  # End-to-end tests
│   ├── visual/               # Visual regression tests
│   └── load/                 # Load and performance tests
├── public/                   # Static files (favicon, robots.txt, etc.)
├── docs/                     # Documentation
├── specs/                    # Feature specifications (SDD)
├── history/                  # PHRs and ADRs
├── .specify/                 # SDD infrastructure
└── scripts/                  # Build and deployment scripts
```

**Python Backend Projects (FastAPI/Django/Flask):**

```
project_root/
├── backend/                  # Python backend (if separate from frontend)
│   ├── app/                  # Main application package
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry point (or wsgi.py for Django/Flask)
│   │   ├── api/              # API routes and endpoints
│   │   │   ├── __init__.py
│   │   │   ├── v1/           # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── routes/   # Route handlers
│   │   │   │   └── schemas/  # Pydantic schemas (request/response models)
│   │   │   └── deps.py       # Shared dependencies (auth, database, etc.)
│   │   ├── core/             # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── config.py     # Configuration (environment variables)
│   │   │   ├── security.py   # Authentication and authorization
│   │   │   └── middleware.py # Custom middleware
│   │   ├── models/           # Database models (SQLAlchemy, Django ORM)
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── services/         # Business logic and AI services
│   │   │   ├── __init__.py
│   │   │   ├── ai/           # AI/ML services
│   │   │   │   ├── chatbot.py
│   │   │   │   ├── embeddings.py
│   │   │   │   ├── llm.py    # LLM integration (OpenAI, Anthropic, etc.)
│   │   │   │   └── models.py # ML model loading and inference
│   │   │   └── ...
│   │   ├── utils/            # Utility functions
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── db/               # Database setup and migrations
│   │   │   ├── __init__.py
│   │   │   ├── base.py       # Database base classes
│   │   │   └── session.py    # Database session management
│   │   └── tasks/            # Background tasks (Celery, etc.)
│   │       ├── __init__.py
│   │       └── ...
│   ├── tests/                # Backend tests
│   │   ├── __init__.py
│   │   ├── unit/             # Unit tests
│   │   ├── integration/      # Integration tests
│   │   ├── e2e/              # API e2e tests
│   │   └── conftest.py       # pytest fixtures
│   ├── alembic/              # Database migrations (Alembic)
│   │   └── versions/
│   ├── scripts/              # Utility scripts
│   ├── requirements/         # Python dependencies
│   │   ├── base.txt          # Base requirements
│   │   ├── dev.txt           # Development requirements
│   │   └── prod.txt          # Production requirements
│   ├── pyproject.toml        # Poetry/setuptools configuration
│   ├── pytest.ini            # pytest configuration
│   └── .env.example          # Example environment variables
├── frontend/                 # Frontend application (if separate)
│   └── [Same structure as frontend-only projects]
├── docs/                     # Documentation
├── specs/                    # Feature specifications (SDD)
├── history/                  # PHRs and ADRs
├── .specify/                 # SDD infrastructure
└── docker-compose.yml        # Multi-service orchestration
```

**Naming Conventions:**

- Components: PascalCase (e.g., `ProjectCard.tsx`)
- Files: kebab-case for non-components (e.g., `use-scroll-position.ts`)
- Folders: kebab-case (e.g., `project-card/`)
- Constants: UPPER_SNAKE_CASE
- Functions/Variables: camelCase
- CSS classes: kebab-case (for Tailwind, BEM, etc.)
- React hooks: camelCase prefixed with `use` (e.g., `useAuth`)

### Architectural Patterns

**MUST implement:**

- **Composition over inheritance**: Favor component composition
- **Single Source of Truth**: One authoritative data source per entity
- **Separation of Concerns**: Logic, presentation, and data separate
- **Dependency Injection**: Avoid tight coupling, enable testing
- **Error Boundaries**: Graceful error handling at component boundaries (React)
- **Code Splitting**: Route-based and component-based code splitting
- **Static Generation**: Pre-render pages where possible for performance
- **Server-Side Rendering**: Use SSR for dynamic, personalized content
- **Incremental Static Regeneration**: Use ISR for frequently updated content (Next.js)

**State Management:**

- MUST keep state as local as possible
- MUST use URL state for shareable/bookmarkable state
- MUST use context or state management library only when truly needed
- MUST avoid prop drilling with composition or context
- For complex apps: Use Redux Toolkit, Zustand, Jotai, or Pinia (Vue)
- For server state: Use TanStack Query (React Query), SWR, or Apollo Client (GraphQL)

**API Integration:**

- MUST use environment variables for configuration
- MUST implement request/response interceptors
- MUST handle errors consistently
- MUST implement retry logic with exponential backoff
- MUST cache responses where appropriate
- MUST implement request deduplication
- MUST handle loading and error states in UI

### API Design Standards

**For projects building REST or GraphQL APIs (SaaS, e-commerce backends, web apps):**

**REST API Best Practices:**

**MUST implement:**

- **Versioning**: Use URI versioning (e.g., `/api/v1/users`) or header versioning (`Accept: application/vnd.api.v1+json`)
- **HTTP Methods**: Use correctly (GET for read, POST for create, PUT/PATCH for update, DELETE for delete)
- **Status Codes**: Use appropriate HTTP status codes:
  - 200 OK (successful GET, PUT, PATCH)
  - 201 Created (successful POST)
  - 204 No Content (successful DELETE)
  - 400 Bad Request (validation errors)
  - 401 Unauthorized (authentication required)
  - 403 Forbidden (authenticated but not authorized)
  - 404 Not Found (resource doesn't exist)
  - 409 Conflict (resource conflict, e.g., duplicate email)
  - 422 Unprocessable Entity (semantic validation errors)
  - 429 Too Many Requests (rate limit exceeded)
  - 500 Internal Server Error (server errors)
  - 503 Service Unavailable (maintenance, overload)
- **Consistent Response Format**:
  ```json
  {
    "data": { ... },           // Successful response data
    "error": {                 // Error details (if error)
      "code": "VALIDATION_ERROR",
      "message": "Invalid input",
      "details": [ ... ]
    },
    "meta": {                  // Pagination, timestamps, etc.
      "page": 1,
      "per_page": 20,
      "total": 100
    }
  }
  ```
- **Pagination**: Implement for list endpoints (offset/limit or cursor-based)
  - Offset-based: `GET /api/v1/users?page=1&per_page=20`
  - Cursor-based: `GET /api/v1/users?cursor=abc123&limit=20` (better for large datasets)
- **Filtering**: Support query parameters for filtering (e.g., `GET /api/v1/users?status=active&role=admin`)
- **Sorting**: Support sort parameter (e.g., `GET /api/v1/users?sort=-created_at,name` for descending created_at, ascending name)
- **Field Selection**: Support sparse fieldsets (e.g., `GET /api/v1/users?fields=id,name,email`)
- **Search**: Support search parameter (e.g., `GET /api/v1/users?search=john`)
- **Rate Limiting**: Implement rate limits with headers:
  - `X-RateLimit-Limit: 1000`
  - `X-RateLimit-Remaining: 999`
  - `X-RateLimit-Reset: 1640000000`
- **Authentication**: Use JWT tokens, OAuth 2.0, or API keys
- **CORS**: Configure properly for frontend access
- **Request/Response Logging**: Log all API requests for debugging and audit
- **Input Validation**: Validate all inputs (types, formats, ranges, required fields)
- **Idempotency**: Support idempotency keys for POST/PUT/PATCH to prevent duplicate operations
- **Webhooks**: If offering webhooks, implement:
  - Webhook URL registration and validation
  - Retry logic with exponential backoff (3-5 retries)
  - Webhook signature verification (HMAC)
  - Event types and payload documentation

**API Documentation Requirements:**

- MUST provide OpenAPI/Swagger specification (auto-generated or manual)
- MUST document all endpoints with:
  - Description and purpose
  - Request parameters (path, query, body)
  - Request/response examples
  - Possible error responses
  - Authentication requirements
  - Rate limits
- MUST provide interactive API explorer (Swagger UI, Redoc, Postman collection)
- SHOULD provide SDK/client libraries for popular languages
- SHOULD provide quickstart guide and code examples

**GraphQL Best Practices (if using GraphQL):**

**MUST implement:**

- **Schema Design**: Design schema around business domain (types, queries, mutations, subscriptions)
- **Versioning**: Avoid versioning; use schema evolution (deprecate fields, add new fields)
- **N+1 Problem**: Implement DataLoader for batching and caching
- **Query Complexity**: Limit query complexity and depth to prevent abuse
- **Pagination**: Use cursor-based pagination (Relay-style connections)
- **Error Handling**: Return structured errors with codes and messages
- **Authentication**: Use context for authentication (JWT in headers)
- **Rate Limiting**: Implement based on query complexity or cost
- **Introspection**: Disable in production (security) or restrict access
- **Persisted Queries**: Use for performance and security (whitelist queries)

**API Security:**

- MUST use HTTPS only (TLS 1.2+)
- MUST validate and sanitize all inputs (prevent injection attacks)
- MUST implement authentication and authorization
- MUST implement rate limiting (per user, per IP, per API key)
- MUST implement CORS with specific origins (not wildcard in production)
- MUST use API keys or tokens (never basic auth passwords)
- MUST rotate secrets regularly
- MUST log security events (failed auth, rate limit violations)
- MUST implement request size limits (prevent DoS)
- MUST implement timeout limits (prevent long-running requests)

**API Performance:**

- MUST implement caching (Redis, CDN) for read-heavy endpoints
- MUST use database indexing for query performance
- MUST implement compression (gzip, brotli)
- MUST optimize payload size (avoid over-fetching)
- MUST implement request/response streaming for large data
- SHOULD implement ETags for conditional requests (304 Not Modified)
- SHOULD implement background jobs for long-running operations
- SHOULD use CDN for API endpoints (if global distribution needed)

**API Testing:**

- MUST write integration tests for all endpoints
- MUST test authentication and authorization
- MUST test error handling (validation errors, server errors)
- MUST test rate limiting
- MUST test pagination and filtering
- MUST load test API endpoints (expected load + 2-3x spike)
- SHOULD use contract testing (Pact, Postman) for API versioning

### Database Design & Data Layer

**Database design principles for production applications:**

**Schema Design Best Practices:**

**MUST implement:**

- **Normalization**: Normalize to 3NF (Third Normal Form) for transactional data to reduce redundancy
- **Denormalization**: Strategically denormalize for read-heavy workloads (e.g., user profile with post counts)
- **Primary Keys**: Use auto-incrementing integers or UUIDs (UUIDs for distributed systems, integers for simpler systems)
- **Foreign Keys**: Define foreign key constraints for referential integrity
- **Indexes**: Create indexes for:
  - Columns frequently used in WHERE clauses
  - Columns used in JOIN conditions
  - Columns used in ORDER BY clauses
  - Unique constraints (email, username, etc.)
  - Composite indexes for multi-column queries
- **Data Types**: Use appropriate data types (INT for IDs, VARCHAR for short strings, TEXT for long text, TIMESTAMP for dates, DECIMAL for money, JSONB for semi-structured data)
- **Constraints**: Use NOT NULL, UNIQUE, CHECK constraints to enforce data integrity
- **Timestamps**: Add `created_at` and `updated_at` to all tables (audit trail)
- **Soft Deletes**: Use `deleted_at` for soft deletes (preserve data, enable recovery)
- **Naming Conventions**:
  - Tables: plural, snake_case (e.g., `users`, `blog_posts`)
  - Columns: singular, snake_case (e.g., `user_id`, `created_at`)
  - Foreign keys: `{table}_id` (e.g., `user_id`, `post_id`)
  - Indexes: `idx_{table}_{column}` (e.g., `idx_users_email`)

**Database Performance Optimization:**

**MUST implement:**

- **Indexing Strategy**: Analyze slow queries (pg_stat_statements, slow query log) and add indexes
- **Connection Pooling**: Use connection pooling (PgBouncer for PostgreSQL, connection pool libraries)
- **Query Optimization**:
  - Avoid N+1 queries (use joins or eager loading)
  - Use EXPLAIN ANALYZE to understand query plans
  - Avoid SELECT * (select only needed columns)
  - Use LIMIT for large result sets
  - Avoid OR in WHERE clauses (use UNION or IN)
  - Use prepared statements (prevent SQL injection, improve performance)
- **Caching**: Cache frequently accessed data (Redis, in-memory cache)
- **Read Replicas**: Use read replicas for read-heavy workloads (scale reads horizontally)
- **Partitioning**: Partition large tables (by date, by range, by hash) for performance
- **Archiving**: Archive old data to separate tables or cold storage

**Migration Strategy:**

**MUST implement:**

- **Version Control**: Store all migrations in version control
- **Migration Tool**: Use migration tool (Alembic, Flyway, Prisma Migrate, Django migrations, TypeORM migrations)
- **Forward-Only**: Migrations should be forward-only (rarely roll back)
- **Backward Compatible**: Make migrations backward compatible (add columns, then deploy code, then remove old columns)
- **Zero-Downtime**: Design migrations for zero-downtime deployments:
  - Add new columns with defaults (not remove old columns)
  - Add new tables (not rename existing tables)
  - Deploy code changes after schema changes
- **Testing**: Test migrations on staging environment before production
- **Rollback Plan**: Have rollback plan for every migration

**Data Integrity & Consistency:**

**MUST implement:**

- **Transactions**: Use transactions for multi-step operations (ACID guarantees)
- **Foreign Key Constraints**: Enforce referential integrity at database level
- **Unique Constraints**: Prevent duplicates (email, username, etc.)
- **Check Constraints**: Validate data at database level (e.g., age > 0)
- **Database-Level Defaults**: Use database defaults for timestamps, statuses
- **Row-Level Security**: Use row-level security (PostgreSQL RLS) for multi-tenancy
- **Audit Logging**: Log critical data changes (trigger-based or application-level)

**Database Backup & Recovery:**

**MUST implement:**

- **Automated Backups**: Daily full backups + continuous WAL archiving (PostgreSQL) or binlog (MySQL)
- **Backup Retention**: Retain backups for 30 days minimum (compliance-dependent)
- **Backup Testing**: Test backup restoration monthly (verify backup integrity)
- **Point-in-Time Recovery (PITR)**: Enable PITR for production databases
- **Geographic Redundancy**: Store backups in different region/availability zone
- **Disaster Recovery Plan**: Document recovery procedures and RTO/RPO targets

**Multi-Tenancy Patterns (for SaaS):**

Choose based on isolation requirements:

1. **Shared Database, Shared Schema** (row-level isolation):
   - Pros: Cost-effective, easy to scale, simple schema
   - Cons: Risk of data leakage, limited customization
   - Implementation: Add `tenant_id` to all tables, filter all queries by tenant_id
   - Use: Small tenants, similar requirements, cost-sensitive

2. **Shared Database, Separate Schemas**:
   - Pros: Better isolation, per-tenant customization possible
   - Cons: Schema migration complexity, limited scalability
   - Implementation: One schema per tenant (e.g., `tenant_123.users`)
   - Use: Medium tenants, moderate customization needs

3. **Separate Databases**:
   - Pros: Maximum isolation, per-tenant backups, compliance-friendly
   - Cons: Higher cost, operational complexity
   - Implementation: One database per tenant with connection routing
   - Use: Large tenants, high security/compliance requirements, enterprise customers

**ORM Best Practices:**

**MUST implement:**

- **Raw SQL for Complex Queries**: Use raw SQL for complex queries (ORM can generate inefficient queries)
- **Lazy Loading Control**: Control lazy loading (avoid N+1 queries)
- **Query Result Caching**: Cache ORM query results where appropriate
- **Connection Management**: Properly close connections (use context managers)
- **Migration Generation**: Review auto-generated migrations before applying
- **Type Safety**: Use TypeScript with Prisma, TypeORM, or Pydantic with SQLAlchemy

**Database Selection Guidance:**

- **PostgreSQL**: Best for transactional apps, complex queries, JSON data, geospatial data (recommended default)
- **MySQL**: Good for read-heavy workloads, simple queries, large-scale deployments
- **MongoDB**: Good for flexible schemas, rapid prototyping, document-oriented data (use cautiously for critical data)
- **Redis**: Best for caching, session storage, real-time features, leaderboards
- **Elasticsearch**: Best for full-text search, log analytics (not primary data store)

### Email, SMS & Notifications Infrastructure

**For applications requiring user communication (most production apps):**

**Email Infrastructure:**

**MUST implement:**

- **Email Service Provider**: Use managed email service (avoid self-hosting SMTP):
  - **Transactional Email**: SendGrid, Postmark, Amazon SES, Mailgun, Resend
  - **Marketing Email**: Mailchimp, ConvertKit, SendGrid Marketing, Brevo (Sendinblue)
- **Email Types**:
  - Transactional: Welcome emails, password resets, order confirmations, receipts
  - Notification: Activity alerts, updates, reminders
  - Marketing: Newsletters, promotions, announcements
- **Email Authentication**:
  - MUST configure SPF records (Sender Policy Framework)
  - MUST configure DKIM (DomainKeys Identified Mail)
  - MUST configure DMARC (Domain-based Message Authentication)
  - Use custom domain (not generic provider domain)
- **Email Template Management**:
  - Use templating system (Handlebars, Liquid, React Email, MJML)
  - Version control email templates
  - Support dynamic content (user name, order details, etc.)
  - Provide plain-text alternative for HTML emails
  - Test across email clients (Gmail, Outlook, Apple Mail, mobile)
- **Deliverability Best Practices**:
  - Implement double opt-in for marketing emails
  - Provide easy unsubscribe (one-click, visible link)
  - Monitor bounce rates and spam complaints
  - Maintain email reputation (avoid spam triggers)
  - Implement email verification (validate email addresses on signup)
- **Email Tracking & Analytics**:
  - Track open rates (use tracking pixels)
  - Track click rates (use tracked links)
  - Track bounces (hard bounces, soft bounces)
  - Track unsubscribes and spam complaints
  - Monitor delivery rates and time-to-inbox

**SMS Infrastructure:**

**MUST implement (if using SMS):**

- **SMS Provider**: Twilio, AWS SNS, Vonage (Nexmo), MessageBird
- **SMS Use Cases**:
  - Two-factor authentication (2FA)
  - Order/delivery notifications
  - Appointment reminders
  - Alerts and critical notifications
- **SMS Best Practices**:
  - Keep messages concise (<160 characters for single SMS)
  - Include opt-out instructions (e.g., "Reply STOP to unsubscribe")
  - Respect timezone (send during appropriate hours)
  - Implement rate limiting (avoid SMS spam)
  - Use short codes or branded sender IDs (where available)
  - Comply with regulations (TCPA in US, GDPR in EU)
- **SMS Fallback**: Provide alternative delivery methods (email, push notification) if SMS fails
- **Cost Management**: SMS is expensive; use judiciously and monitor costs

**Push Notifications:**

**MUST implement (for web apps with PWA, mobile apps):**

- **Push Notification Services**:
  - Web Push: Firebase Cloud Messaging (FCM), OneSignal, Pusher Beams
  - Mobile: Firebase Cloud Messaging (FCM), Apple Push Notification Service (APNS), AWS SNS
- **Notification Types**:
  - Transactional: Order updates, messages, alerts
  - Engagement: Reminders, suggestions, updates
  - Marketing: Promotions, announcements (use sparingly)
- **Permission Handling**:
  - Request permission at appropriate time (not immediately on page load)
  - Explain value before requesting ("Get notified when your order ships")
  - Respect user's choice (don't re-prompt aggressively)
- **Notification Best Practices**:
  - Personalize notifications (use user name, relevant data)
  - Use action buttons (e.g., "View Order", "Reply")
  - Include notification icon and badge
  - Group related notifications (avoid notification spam)
  - Respect quiet hours (don't send at night unless critical)
  - Provide notification preferences (users control frequency and types)
- **Delivery Strategy**:
  - Use notification priority (high for urgent, normal for regular)
  - Implement notification expiry (don't deliver stale notifications)
  - Handle offline devices (queue notifications, deliver when online)
  - Track delivery and engagement metrics

**In-App Notifications:**

**MUST implement (for web/mobile apps):**

- **Notification Center**: In-app notification inbox/feed
- **Real-Time Delivery**: Use WebSockets or Server-Sent Events for real-time notifications
- **Notification States**: Unread, read, archived
- **Notification Actions**: Mark as read, dismiss, view details
- **Notification Preferences**: Per-channel controls (email, push, in-app)
- **Notification Batching**: Group similar notifications (e.g., "5 new messages")

**Notification Architecture:**

**Recommended Architecture:**

```
User Action → Event Emitted → Notification Service
                                    ↓
                    [Queue: RabbitMQ/Kafka/Redis]
                                    ↓
            Worker Processes (parallel processing)
                ↓           ↓           ↓
              Email        SMS        Push
            (SendGrid)   (Twilio)     (FCM)
```

**MUST implement:**

- **Event-Driven**: Decouple notification sending from business logic
- **Message Queue**: Use message queue (RabbitMQ, Kafka, Redis Pub/Sub, AWS SQS) for async processing
- **Worker Processes**: Use background workers (Celery, Bull, Sidekiq) to process notifications
- **Retry Logic**: Implement retry with exponential backoff for failed deliveries
- **Dead Letter Queue**: Store failed notifications after max retries (investigate and reprocess)
- **Rate Limiting**: Prevent notification spam (max N notifications per user per hour)
- **Idempotency**: Prevent duplicate notifications (deduplicate based on event ID)

**Notification Preferences & Compliance:**

**MUST implement:**

- **Granular Controls**: Let users control notification types and channels
- **Frequency Capping**: Limit notification frequency per user
- **Quiet Hours**: Respect user timezone and quiet hour preferences
- **Unsubscribe**: One-click unsubscribe from all or specific notification types
- **Compliance**:
  - CAN-SPAM Act (US): Include unsubscribe, physical address, accurate headers
  - GDPR (EU): Obtain consent, provide data export/deletion
  - CASL (Canada): Obtain consent for commercial messages
  - TCPA (US): Obtain consent for SMS, respect do-not-call lists

**Notification Testing:**

- MUST test all notification templates (rendering, links, personalization)
- MUST test across devices and clients (email clients, mobile devices)
- MUST test delivery success and failure scenarios
- MUST test unsubscribe flows
- SHOULD test with real users in staging environment

**Monitoring & Analytics:**

- Track delivery rates (successful, failed, bounced)
- Track engagement rates (opens, clicks, conversions)
- Monitor delivery latency (time from event to delivery)
- Alert on delivery failures or rate drops
- Analyze notification effectiveness (which types drive engagement)

### AI Features & Machine Learning Integration

**When to Integrate AI Features:**

AI features add significant value when they solve real user problems: personalization, automation, intelligent search, content moderation, or assistance. Avoid AI for the sake of AI.

**Common AI Use Cases by Feature Type:**

1. **Conversational AI & Chatbots**:
   - Customer support automation (24/7 availability)
   - Lead qualification and sales assistance
   - Product recommendations and discovery
   - Interactive troubleshooting and FAQs
   - Personalized onboarding assistance
   - Technologies: OpenAI GPT-4, Anthropic Claude, LangChain, LlamaIndex

2. **Recommendation Systems**:
   - Product recommendations (e-commerce)
   - Content recommendations (articles, videos, products)
   - Personalized search results
   - Related items and cross-selling
   - Technologies: Collaborative filtering, content-based filtering, hybrid models, vector databases

3. **Natural Language Processing (NLP)**:
   - Semantic search (understand user intent)
   - Content classification and tagging
   - Sentiment analysis (reviews, feedback, social media)
   - Text summarization (long articles, documents)
   - Translation and multilingual support
   - Named entity recognition (extract names, dates, locations)
   - Technologies: OpenAI embeddings, Hugging Face Transformers, spaCy, NLTK

4. **Computer Vision**:
   - Image recognition and classification
   - Visual search (search by image)
   - Content moderation (NSFW, inappropriate content)
   - Face detection and recognition
   - Object detection (e-commerce, inventory)
   - OCR (extract text from images)
   - Technologies: OpenAI CLIP, TensorFlow, PyTorch, Hugging Face Vision models

5. **Content Generation**:
   - Automated product descriptions
   - Blog post drafting and SEO optimization
   - Social media content creation
   - Email and marketing copy generation
   - Image generation (DALL-E, Stable Diffusion)
   - Technologies: OpenAI GPT-4, Anthropic Claude, DALL-E, Stable Diffusion

6. **Predictive Analytics**:
   - Customer churn prediction
   - Demand forecasting (inventory, pricing)
   - Lead scoring and prioritization
   - Anomaly detection (fraud, security threats)
   - User behavior prediction
   - Technologies: scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch

7. **Speech & Audio**:
   - Speech-to-text (voice commands, transcription)
   - Text-to-speech (accessibility, voice assistants)
   - Audio classification (music genre, sound events)
   - Voice assistants and voice search
   - Technologies: OpenAI Whisper, Google Cloud Speech-to-Text, Azure Speech Services

**Technical Architecture for AI Integration:**

**Backend (Python Recommended for AI/ML):**

- **Framework**: FastAPI (async, fast, automatic OpenAPI docs) or Flask (lightweight, microservices)
- **AI/ML Libraries**:
  - LangChain / LlamaIndex (LLM orchestration, RAG pipelines)
  - OpenAI SDK / Anthropic SDK (LLM APIs)
  - Hugging Face Transformers (open-source models, embeddings)
  - scikit-learn (traditional ML, preprocessing)
  - TensorFlow / PyTorch (deep learning, custom models)
  - spaCy / NLTK (NLP pipelines)
  - Sentence Transformers (semantic embeddings)
- **Vector Databases** (for RAG, semantic search):
  - Pinecone (managed, easy, scalable)
  - Weaviate (open-source, hybrid search)
  - Qdrant (open-source, fast, Rust-based)
  - Chroma (open-source, developer-friendly)
  - pgvector (PostgreSQL extension, no separate DB needed)
- **Caching & Queuing**:
  - Redis (caching, session management, rate limiting)
  - Celery / RQ (async task queues for ML jobs)
- **Monitoring & Observability**:
  - Sentry (error tracking)
  - Prometheus + Grafana (metrics, dashboards)
  - LangSmith / Helicone (LLM observability, cost tracking)

**Frontend Integration:**

- **React/Next.js Components**: Chat widgets, search interfaces, recommendation carousels
- **Real-time Streaming**: WebSockets or Server-Sent Events for LLM streaming responses
- **State Management**: TanStack Query or SWR for AI API calls (caching, retry, optimistic updates)
- **Loading States**: Skeleton screens, typing indicators, progress bars for AI operations

**AI Safety & Best Practices:**

- MUST implement content moderation (OpenAI Moderation API, Perspective API)
- MUST prevent prompt injection attacks (input validation, system prompt protection)
- MUST implement rate limiting (prevent abuse, control costs)
- MUST handle AI failures gracefully (fallback responses, retry logic)
- MUST monitor AI costs (track API spending, set budgets, alerts)
- MUST log AI interactions (audit, debugging, improvement)
- MUST provide user controls (disable AI features, data deletion)
- MUST be transparent (disclose AI usage, cite sources)
- MUST comply with AI regulations (GDPR, CCPA, EU AI Act)

**AI Development Workflow:**

1. **Problem Definition**: Clearly define problem AI will solve and success metrics
2. **Data Collection**: Gather training/evaluation data (if custom models) or knowledge base (if RAG)
3. **Prototyping**: Start with pre-trained models/APIs (OpenAI, Anthropic) before custom models
4. **Evaluation**: Test with real user scenarios, measure accuracy/relevance/safety
5. **Deployment**: Deploy as separate microservice (Python FastAPI backend)
6. **Monitoring**: Track performance, costs, user feedback, safety violations
7. **Iteration**: Continuously improve based on user feedback and analytics

**Cost Optimization for AI:**

- Use cheaper models for simple tasks (GPT-3.5-turbo vs GPT-4)
- Implement caching (Redis for frequent queries)
- Use embeddings + vector search instead of LLM calls when possible
- Batch requests where possible
- Set max token limits to prevent runaway costs
- Monitor and alert on cost spikes
- Consider self-hosted open-source models for high-volume use cases (Llama 3, Mixtral)

## Website Type Adaptations

**This constitution applies to ALL website types. Additional requirements by type:**

### E-Commerce Websites

**Additional Requirements:**

- Product catalog with search, filters, sorting
- Shopping cart with persistent state
- Checkout flow with payment integration (Stripe, PayPal, etc.)
- Order management and tracking
- Inventory management
- Customer accounts and order history
- Product recommendations and cross-selling
- Reviews and ratings system
- Wishlist functionality
- Multi-currency support (if international)
- Tax calculation (Avalara, TaxJar, etc.)
- Shipping calculation and real-time rates
- Abandoned cart recovery
- PCI DSS compliance for payment processing
- Fraud detection and prevention

**AI-Powered Enhancements:**

- AI chatbot for customer support and product assistance
- Personalized product recommendations (collaborative filtering, content-based)
- Visual search (search by uploading product images)
- Dynamic pricing optimization
- Inventory demand forecasting
- Automated product descriptions and SEO optimization
- Smart search with natural language processing
- Sentiment analysis for product reviews
- Fraud detection using machine learning
- Abandoned cart recovery with personalized messaging
- AI-powered size/fit recommendations
- Customer behavior analytics and segmentation

**Recommended Tech Stack**: Next.js + Stripe + Shopify/Commerce.js + Tailwind + Python FastAPI (for AI features)

### SaaS Applications

**Additional Requirements:**

- User authentication and authorization (Auth0, Clerk, Supabase Auth)
- Subscription management (Stripe Billing, Paddle, Chargebee)
- User onboarding flows and tutorials
- Feature gating based on subscription tier
- Usage tracking and metering
- Team/organization management
- Role-based access control (RBAC)
- API key management for integrations
- Billing and invoicing
- Trial management
- Upgrade/downgrade flows
- Cancellation flows with retention strategies
- SOC 2 compliance (if B2B)
- GDPR/CCPA compliance
- Data export functionality
- Two-factor authentication (2FA)

**AI-Powered Enhancements:**

- AI chatbot for customer onboarding and support
- Intelligent feature recommendations based on usage patterns
- Predictive churn detection and retention strategies
- Automated user segmentation and personalization
- Smart notifications and in-app messaging
- AI-powered search and help documentation
- Usage analytics with ML-driven insights
- Anomaly detection for security and fraud prevention
- Natural language query interface for data/reports
- Automated report generation and insights

**Recommended Tech Stack**: Next.js + Clerk Auth + Stripe + PostgreSQL + Prisma + Python FastAPI (for AI/ML)

### Marketing Websites

**Additional Requirements:**

- Landing pages with conversion optimization
- Lead capture forms
- Email marketing integration (Mailchimp, ConvertKit, SendGrid)
- CRM integration (HubSpot, Salesforce)
- A/B testing framework (Optimizely, VWO, Google Optimize)
- Marketing automation
- Exit-intent popups
- Social proof elements (testimonials, case studies, client logos)
- Video embedding and optimization
- Contact form with anti-spam protection
- Live chat integration (Intercom, Drift)
- Blog/content section
- Press kit/media resources
- Partner/affiliate program pages
- Event registration (if applicable)

**AI-Powered Enhancements:**

- AI chatbot for lead qualification and customer support
- Personalized content recommendations based on visitor behavior
- Predictive lead scoring and prioritization
- Automated content generation for blog posts and social media
- A/B testing with ML-driven optimization
- Sentiment analysis for user feedback and reviews
- Smart form auto-completion and validation
- Dynamic content personalization (headlines, CTAs, images)
- Chatbot for appointment scheduling and event registration
- Intelligent search with natural language understanding

**Recommended Tech Stack**: Next.js + Tailwind + Sanity CMS + Vercel Analytics + Python FastAPI (for AI features)

### Blogs & Content Sites

**Additional Requirements:**

- Content Management System (Sanity, Contentful, Strapi, WordPress headless)
- Article/post listing with pagination or infinite scroll
- Search functionality (Algolia, Typesense, Meilisearch)
- Categories and tags taxonomy
- Author profiles and multi-author support
- Comments system (Disqus, Giscus, custom)
- Newsletter subscription (ConvertKit, Mailchimp, Substack)
- RSS feed generation
- Social sharing buttons with Open Graph
- Reading time estimation
- Table of contents for long articles
- Related posts recommendations
- Archive pages (by date, category, tag)
- Syntax highlighting for code blocks (Prism.js, Shiki)
- Image galleries and lightbox
- Dark/light theme toggle

**AI-Powered Enhancements:**

- AI chatbot for content discovery and reader questions
- Personalized article recommendations based on reading history
- Automated content tagging and categorization
- AI-generated article summaries and meta descriptions
- Sentiment analysis for comments and engagement
- Smart search with semantic understanding
- Automated content translation for international audiences
- Plagiarism detection for submitted content
- AI-powered content moderation for comments
- Reading pattern analytics and insights

**Recommended Tech Stack**: Astro/Next.js + Contentful/Sanity + Tailwind + Algolia + Python FastAPI (for AI features)

### Web Applications

**Additional Requirements:**

- Complex state management (Redux, Zustand, MobX)
- Real-time features (WebSockets, Server-Sent Events)
- Offline support and Progressive Web App features
- Background synchronization
- Push notifications
- File upload and management
- Data visualization (D3.js, Chart.js, Recharts)
- Complex forms with multi-step workflows
- Drag and drop functionality
- Keyboard shortcuts
- Command palette (⌘K menu)
- Collaborative features (if applicable)
- Export functionality (PDF, CSV, Excel)
- Print-optimized views
- Bulk operations
- Undo/redo functionality
- Autosave and draft management

**AI-Powered Enhancements:**

- AI chatbot for in-app assistance and feature discovery
- Intelligent auto-complete and suggestions
- Predictive data entry and validation
- Anomaly detection for data quality
- Natural language query interface for complex searches
- AI-powered data visualization recommendations
- Smart notifications based on user behavior patterns
- Automated report generation with insights
- Content recommendations based on usage context
- Voice commands and speech-to-text integration

**Recommended Tech Stack**: React + TypeScript + Redux Toolkit + TanStack Query + Socket.io + Python FastAPI (for AI/ML)

### Community Platforms

**Additional Requirements:**

- User profiles and customization
- User-generated content moderation
- Community guidelines and enforcement
- Reporting system for content/users
- User reputation and karma system
- Upvoting/downvoting or similar engagement
- Comment threads and discussions
- Direct messaging between users
- Notifications system (in-app, email, push)
- Content flagging and review workflow
- Ban and suspension management
- Spam detection and prevention
- DMCA compliance procedures
- Content ownership and licensing
- Feed algorithms (chronological, algorithmic, personalized)

**AI-Powered Enhancements:**

- AI-powered content moderation (hate speech, NSFW, spam detection)
- Personalized feed algorithms using machine learning
- AI chatbot for community guidelines and support
- Sentiment analysis for community health monitoring
- Automated content recommendations based on user interests
- Smart notifications prioritization
- Fake account and bot detection
- Topic extraction and trend detection
- Automated content summarization
- User behavior analytics and insights

**Recommended Tech Stack**: Next.js + Supabase + PostgreSQL + Redis + Tailwind + Python FastAPI (for AI/ML)

### Portfolio Websites

**Additional Requirements:**

- Personal branding and professional identity showcase
- Project showcase with detailed case studies
- About/Bio section with professional background
- Skills and expertise display (visual or listed)
- Resume/CV download functionality
- Contact form with anti-spam protection
- Social media integration and links
- Testimonials and recommendations
- Work experience timeline
- Education and certifications
- Blog or articles section (optional)
- Image galleries for visual work (photography, design, art)
- Video portfolio integration (YouTube, Vimeo embeds)
- Downloadable portfolio PDF
- Dark/light theme toggle for design appeal
- Smooth scrolling and page transitions
- Interactive elements and micro-animations
- Hero section with compelling introduction
- Call-to-action for hiring/collaboration
- Analytics to track visitor engagement
- Mobile-optimized layout (mobile-first)
- Fast load times (<2s for initial load)
- SEO optimization for personal brand discoverability
- Open Graph tags for social sharing

**AI-Powered Enhancements:**

- AI chatbot for visitor questions about experience and services
- AI-generated project summaries and descriptions
- Intelligent content recommendations based on visitor interest
- Automated resume parsing and skills extraction
- AI-powered contact form with intelligent routing

**Recommended Tech Stack**: Astro/Next.js + Tailwind + Framer Motion + Sanity/Contentful (optional CMS)

### Entertainment Websites

**Additional Requirements:**

- Rich media content (video, audio, images, interactive media)
- Video player integration with streaming support (YouTube, Vimeo, custom HLS/DASH)
- Audio player with playlist functionality
- Content categorization and tagging
- User ratings and reviews
- Trending/popular content sections
- Personalized content recommendations
- User accounts with watch history/favorites
- Social features (likes, shares, comments)
- Content search with filters (genre, year, rating, etc.)
- Multiple content formats (episodes, seasons, series, standalone)
- Parental controls and content rating system
- Multi-device support and responsive player
- Offline viewing capabilities (PWA)
- Subscription/membership tiers for premium content
- Ad integration (if ad-supported)
- Live streaming capabilities (if applicable)
- Interactive elements (polls, quizzes, games)
- Social media integration and viral sharing
- Content licensing and DRM (if required)
- Analytics for content performance and engagement
- Content moderation for user-generated content
- DMCA compliance and copyright protection
- Age verification for mature content
- Multi-language support and subtitles/closed captions
- Accessibility features (audio descriptions, screen reader support)

**AI-Powered Enhancements:**

- AI-powered content recommendations (collaborative filtering, content-based)
- Personalized content discovery based on viewing patterns
- AI chatbot for content discovery and customer support
- Automated content tagging and categorization
- AI-generated subtitles and translations
- Content moderation using AI (NSFW detection, hate speech filtering)
- Sentiment analysis for user reviews and comments
- Predictive analytics for content popularity
- AI-driven search with natural language queries

**Recommended Tech Stack**: Next.js + TypeScript + Video.js/Plyr + PostgreSQL + Redis + Python FastAPI (for AI features)

### Social Media Platforms

**Additional Requirements (extends Community Platforms):**

- Rich user profiles with customization and themes
- Social graph (follow/friend relationships)
- News feed with algorithmic or chronological sorting
- Post creation (text, images, videos, links, polls)
- Stories/ephemeral content (24-hour expiry)
- Direct messaging and group chats
- Real-time notifications (in-app, push, email)
- Trending topics and hashtags
- User mentions and tagging
- Content sharing and reposting
- Privacy controls (public, friends-only, private posts)
- Blocking and muting functionality
- Content reporting and moderation workflows
- User verification badges (verified accounts)
- Analytics dashboard for content creators
- Ad platform integration (if monetized)
- Live streaming functionality
- Events and event management
- Groups and communities
- Marketplace features (if applicable)
- Location tagging and check-ins
- Content reactions (likes, emoji reactions)
- Nested comment threads with voting
- Search functionality (users, posts, hashtags)
- Explore/discovery pages
- Content recommendations and personalization
- Account security (2FA, login alerts, session management)
- Data export and portability (GDPR compliance)
- Anti-spam and anti-bot measures
- Rate limiting to prevent abuse
- Content appeals process

**AI-Powered Enhancements:**

- AI-powered content moderation (hate speech, NSFW, spam detection)
- Personalized feed algorithms using ML
- AI chatbot for platform support and user assistance
- Automated content recommendations and discovery
- Sentiment analysis for community health monitoring
- AI-generated content summaries and highlights
- Smart notifications (ML-driven priority)
- Fake account and bot detection
- Content transcription and accessibility features
- Automated translation for global audiences

**Recommended Tech Stack**: Next.js + TypeScript + PostgreSQL + Redis + Socket.io + Python FastAPI (for AI/ML) + Kafka/RabbitMQ (for messaging)

### School Websites & Student Management Systems

**Additional Requirements for Educational Institutions:**

School websites serve multiple stakeholders (students, parents, teachers, administrators) and handle sensitive educational data. They require robust multi-tenant architecture, strict compliance with education privacy laws, and specialized academic features.

**Core Educational Features:**

- Multi-school/multi-tenant architecture with data isolation
- Student Information System (SIS) integration
- Student profiles with academic records
- Parent/guardian portal with controlled access
- Teacher dashboard and classroom management
- Administrative dashboard with reporting
- Enrollment and registration workflows
- Attendance tracking and reporting
- Grade book and academic progress tracking
- Report card generation and distribution
- Class schedules and timetables
- Course catalog and curriculum management
- Assignment management and submission
- Online learning resources and materials
- School calendar with events and holidays
- Announcements and news management
- Parent-teacher communication system
- School directory (staff, students with privacy controls)
- Document management (handbooks, policies, forms)
- Permission slip and consent form workflows
- Emergency contact information management
- Health records and medical information (HIPAA-compliant storage)
- Transportation and bus tracking information
- Cafeteria menu and meal planning
- Extracurricular activities and clubs management
- Sports schedules and athletic programs
- School policies and code of conduct
- Resource library (textbooks, materials)
- Staff directory and contact information
- Board of directors/trustees information
- Admissions information and application process

**Multi-Tenant Architecture Requirements:**

- MUST implement row-level security (RLS) for data isolation between schools
- MUST support separate branding (logo, colors, domain) per school
- MUST isolate student/parent/teacher data per school tenant
- MUST support school-specific configuration and settings
- MUST implement tenant-aware authentication and authorization
- MUST support school-level administrative roles
- MUST provide cross-school reporting for platform administrators only
- MUST implement tenant-specific data backup and restore
- MUST support school-specific customization (themes, features)
- MUST enforce strict tenant isolation at API and database level
- MUST provide per-school usage analytics and billing (if applicable)
- MUST support school onboarding and offboarding workflows
- MUST test data isolation thoroughly (tenant A cannot access tenant B data)

**Role-Based Access Control (RBAC):**

- **Platform Administrator**: Full system access, manages all schools
- **School Administrator**: Manages single school, full access to school data
- **Principal/Vice Principal**: School leadership access, reporting, oversight
- **Teacher**: Classroom management, gradebook, student progress, parent communication
- **Counselor**: Student records, academic advising, college prep
- **Administrative Staff**: Office functions, enrollment, attendance
- **Parent/Guardian**: View own children's information, communicate with teachers
- **Student**: View own information, submit assignments, access resources
- **Guest/Public**: View public information only (no authentication required)

MUST implement granular permissions within each role (e.g., teacher can view grades but not edit attendance).

**Student Data Privacy & Compliance (CRITICAL):**

School websites handle sensitive student data and MUST comply with strict regulations:

**FERPA Compliance (US - Family Educational Rights and Privacy Act):**

- MUST obtain written consent before disclosing personally identifiable information (PII) from education records
- MUST provide parents/eligible students right to inspect and review records
- MUST provide process to request corrections to inaccurate records
- MUST log all access to student education records (audit trail)
- MUST NOT disclose directory information without prior consent (unless school policy allows with opt-out)
- MUST implement role-based access ensuring only authorized personnel access student records
- MUST provide annual notification of FERPA rights to parents/students
- Directory information (if disclosed): name, address, phone, email, photo, grade level, enrollment status, awards - MUST allow opt-out
- MUST implement strict access controls for education records

**COPPA Compliance (US - Children's Online Privacy Protection Act, <13 years):**

- MUST obtain verifiable parental consent before collecting personal information from children under 13
- MUST NOT require more information than necessary for participation
- MUST provide clear privacy policy describing data collection and use
- MUST provide parents ability to review and delete child's personal information
- MUST implement reasonable security measures to protect collected information
- MUST NOT enable public posting of personal information by children
- MUST implement age gate to identify users under 13

**GDPR Compliance (EU - General Data Protection Regulation):**

- MUST obtain explicit consent for data processing (students/parents)
- MUST provide right to access personal data
- MUST provide right to rectification (correct inaccurate data)
- MUST provide right to erasure ("right to be forgotten")
- MUST provide right to data portability (export data in machine-readable format)
- MUST implement data minimization (collect only necessary data)
- MUST implement privacy by design and by default
- MUST maintain records of processing activities
- MUST implement data breach notification (within 72 hours)
- MUST appoint Data Protection Officer (DPO) if required
- MUST conduct Data Protection Impact Assessments (DPIA) for high-risk processing

**General Student Data Protection Best Practices:**

- MUST encrypt all student PII at rest and in transit (TLS 1.3+, AES-256)
- MUST implement multi-factor authentication (MFA) for all staff accounts
- MUST log all access to student records with timestamp, user, and action
- MUST implement automatic session timeout (15 minutes for sensitive data)
- MUST conduct regular security audits and penetration testing
- MUST implement data retention policies (purge data after student leaves)
- MUST provide data breach response plan with notification procedures
- MUST train all staff on data privacy requirements annually
- MUST implement secure file upload with virus scanning
- MUST sanitize all user inputs to prevent injection attacks
- MUST implement rate limiting to prevent brute force attacks
- MUST use secure password policies (minimum 12 characters, complexity requirements)
- MUST provide secure password reset process (not via email)
- MUST implement account lockout after failed login attempts
- MUST disable accounts for inactive users (90 days)
- MUST conduct background checks for staff with access to student data
- MUST sign Business Associate Agreements (BAA) with third-party services handling student data
- MUST provide transparent privacy policy in plain language
- MUST obtain consent for optional features (photos, directory information)
- MUST provide opt-out mechanisms for non-essential communications

**Student Data That MUST Be Protected:**

- Student names, addresses, phone numbers, email addresses
- Student ID numbers, Social Security Numbers
- Date of birth, age, gender
- Parent/guardian names and contact information
- Academic records (grades, transcripts, test scores)
- Attendance records
- Disciplinary records
- Special education records (IEP, 504 plans)
- Health records and medical information
- Behavioral assessments
- Biometric data (fingerprints, photos)
- Free/reduced lunch status (socioeconomic indicators)
- Race, ethnicity, national origin
- Religion
- Student photos and videos
- Any other personally identifiable information (PII)

**Communication Features:**

- Secure messaging between parents and teachers
- School-wide announcements and notifications
- Email notifications for important events
- SMS notifications for urgent alerts
- Push notifications via mobile app (if applicable)
- Newsletter creation and distribution
- Emergency alert system (lockdown, weather, etc.)
- Absence notifications to parents
- Grade notifications when posted
- Assignment reminders and due dates
- Event reminders (parent-teacher conferences, etc.)
- Permission slip reminders
- MUST implement notification preferences (email, SMS, push)
- MUST respect communication preferences and opt-outs
- MUST provide unsubscribe mechanism for non-critical communications

**Academic Management:**

- Grade book with weighted categories
- Standards-based grading support
- Assignment creation, distribution, and collection
- Online assignment submission (file uploads)
- Rubric-based grading
- Late work policies and tracking
- Extra credit tracking
- Grade calculation and GPA computation
- Progress reports and report cards
- Transcript generation
- Honor roll and academic achievement tracking
- Academic probation and intervention tracking
- Course prerequisites and sequencing
- Credit tracking for graduation requirements
- Attendance tracking (daily, period-level)
- Tardy and absence management
- Attendance reporting and analytics
- Behavior tracking and incident reporting
- Detention and discipline management

**Scheduling & Timetabling:**

- Master schedule creation and management
- Student schedule generation
- Class roster management
- Room assignments and capacity management
- Teacher schedule and planning periods
- Substitute teacher management
- Schedule conflict detection and resolution
- Bell schedule management (regular, early dismissal, etc.)

**Reporting & Analytics:**

- Student progress reports
- Attendance reports (daily, weekly, monthly, yearly)
- Grade distribution reports
- Class performance analytics
- Graduation tracking reports
- State reporting requirements (varies by jurisdiction)
- Enrollment reports and demographics
- Discipline reports
- Teacher performance dashboards
- Parent engagement metrics
- School comparison reports (for multi-school platforms)
- Custom report builder for administrators
- Data export in multiple formats (PDF, Excel, CSV)
- Scheduled automated reports

**Integration Requirements:**

- MUST integrate with Student Information Systems (SIS): PowerSchool, Infinite Campus, Skyward, etc.
- SHOULD integrate with Learning Management Systems (LMS): Google Classroom, Canvas, Schoology, Moodle
- SHOULD integrate with Single Sign-On (SSO): Google Workspace, Microsoft 365, Clever
- SHOULD integrate with payment processors for fees, lunch, activities
- SHOULD integrate with library management systems
- SHOULD integrate with transportation management systems
- MUST provide API documentation for integrations
- MUST support standard data exchange formats (SIF, Ed-Fi, OneRoster)

**Accessibility Requirements (Enhanced for Educational Context):**

- MUST meet WCAG 2.1 Level AA at minimum (ADA compliance)
- SHOULD meet WCAG 2.1 Level AAA for educational content
- MUST support screen readers (JAWS, NVDA, VoiceOver)
- MUST provide alternative text for all educational images
- MUST provide closed captions for all video content
- MUST provide transcripts for audio content
- MUST support keyboard-only navigation
- MUST provide skip navigation links
- MUST ensure readable fonts and high contrast
- MUST support text resizing without breaking layout
- MUST provide alternative formats for documents (Word, PDF with accessibility tags)
- MUST test with assistive technologies
- MUST accommodate students with disabilities (Section 504, ADA)
- SHOULD support multiple languages for multilingual families

**Mobile Experience:**

- MUST be fully responsive on mobile devices
- SHOULD provide native mobile app (iOS, Android) or PWA
- MUST support mobile notifications
- MUST optimize for low-bandwidth connections
- MUST support offline access for critical features
- MUST provide mobile-friendly forms and input
- MUST test on iOS and Android devices

**Performance Requirements (Enhanced for Educational Context):**

- MUST support concurrent access during peak times (start of school year, report card day, registration periods)
- MUST handle high traffic during registration windows
- MUST support large file uploads (assignments, transcripts)
- MUST implement caching for frequently accessed data
- MUST optimize database queries for large student populations
- MUST implement CDN for static assets
- MUST support auto-scaling for traffic spikes
- MUST provide offline functionality where appropriate

**Security Requirements (Enhanced for Educational Context):**

- MUST implement HTTPS with HSTS (Strict-Transport-Security)
- MUST implement Content Security Policy (CSP)
- MUST implement multi-factor authentication (MFA) for staff
- MUST implement IP whitelisting for administrative access (optional)
- MUST conduct regular security audits and penetration testing
- MUST implement intrusion detection and prevention
- MUST implement DDoS protection
- MUST encrypt backups
- MUST implement disaster recovery plan
- MUST conduct annual security training for staff
- MUST implement incident response plan
- MUST comply with CJIS security policy if handling law enforcement data

**AI-Powered Enhancements for School Websites:**

- AI chatbot for answering common parent/student questions
- Automated absence notifications with pattern detection
- Predictive analytics for student at-risk identification
- Personalized learning recommendations
- Automated grading assistance (not replacement) for objective assessments
- Natural language processing for parent feedback sentiment analysis
- AI-powered search for school policies and documents
- Intelligent scheduling assistance for parent-teacher conferences
- Automated report card narrative generation assistance
- Plagiarism detection for student submissions
- Content recommendation for teachers (curriculum resources)
- Predictive enrollment forecasting
- Automated language translation for multilingual families
- AI-assisted special education documentation
- Behavioral pattern recognition for intervention opportunities

**Testing Requirements (Enhanced for Educational Context):**

- MUST test data isolation between schools (multi-tenant security)
- MUST test role-based access controls thoroughly
- MUST test student data privacy and compliance features
- MUST test with assistive technologies (screen readers)
- MUST perform security penetration testing
- MUST test high-concurrency scenarios (registration day)
- MUST test data import/export functionality
- MUST test integration points (SIS, LMS, SSO)
- MUST test backup and disaster recovery procedures
- MUST test grade calculation accuracy
- MUST test report generation with large datasets

**Documentation Requirements (Enhanced for Educational Context):**

- MUST provide comprehensive user guides for each role (admin, teacher, parent, student)
- MUST document data privacy policies and compliance measures
- MUST provide API documentation for integrations
- MUST document data retention and deletion policies
- MUST provide training materials for staff
- MUST document emergency procedures and incident response
- MUST maintain changelog for all releases
- MUST document tenant onboarding procedures
- MUST provide FAQ for common questions
- MUST provide video tutorials for key features

**Launch Checklist for School Websites:**

- [ ] Multi-tenant architecture tested and verified
- [ ] FERPA compliance reviewed and implemented
- [ ] COPPA compliance verified (if serving children under 13)
- [ ] GDPR compliance verified (if serving EU residents)
- [ ] Local education privacy laws compliance verified
- [ ] Data encryption at rest and in transit verified
- [ ] Role-based access controls tested
- [ ] Audit logging implemented and tested
- [ ] Privacy policy and terms of service published
- [ ] Consent mechanisms implemented
- [ ] Data breach response plan documented
- [ ] Security audit and penetration testing completed
- [ ] Accessibility audit completed (WCAG 2.1 AA)
- [ ] Load testing completed for peak registration periods
- [ ] Backup and disaster recovery tested
- [ ] Staff training materials prepared
- [ ] Parent/student onboarding guides created
- [ ] Integration testing with SIS/LMS completed
- [ ] Mobile responsiveness verified
- [ ] SSL certificate installed and HSTS configured
- [ ] Monitoring and alerting configured
- [ ] Incident response procedures documented
- [ ] Legal review of data handling practices completed
- [ ] Insurance coverage verified (cyber liability)

**Recommended Tech Stack for School Websites:**

**Option 1: Next.js Full-Stack (Recommended for Most School Platforms)**
- **Frontend**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **Backend**: Next.js API routes or tRPC for type-safe APIs
- **Database**: PostgreSQL with row-level security (RLS) for multi-tenancy
- **ORM**: Prisma or Drizzle ORM with TypeScript
- **Authentication**: NextAuth.js with support for SSO (Google, Microsoft)
- **File Storage**: AWS S3 or Cloudflare R2 with encryption
- **Real-time**: Pusher or Ably for notifications
- **Email**: SendGrid or AWS SES
- **Testing**: Vitest + Testing Library + Playwright
- **Hosting**: Vercel or AWS with auto-scaling
- **Pros**: Excellent developer experience, built-in optimizations, great for full-stack apps
- **Cons**: Vercel vendor lock-in considerations, serverless cold starts

**Option 2: Python Django Full-Stack (Traditional, Battle-Tested)**
- **Backend**: Django 5+ with Python 3.11+
- **Frontend**: React with TypeScript or Django Templates with HTMX
- **Database**: PostgreSQL with django-tenants for multi-tenancy
- **Authentication**: Django-allauth with SSO support
- **File Storage**: django-storages with S3
- **Real-time**: Django Channels with WebSockets
- **Email**: Django email backends (SendGrid, AWS SES)
- **Testing**: pytest + pytest-django + Playwright
- **Hosting**: AWS, Heroku, or DigitalOcean
- **Pros**: Mature ecosystem, excellent admin interface, strong security defaults, proven for educational SIS
- **Cons**: Monolithic, less modern frontend patterns without additional frameworks

**Option 3: Microservices with Next.js + FastAPI (Scalable, AI-Ready)**
- **Frontend**: Next.js 14+ with TypeScript
- **Backend**: Python FastAPI for APIs and AI/ML services
- **Database**: PostgreSQL with row-level security
- **Authentication**: Auth0 or Supabase Auth with SSO
- **File Storage**: AWS S3 with encryption
- **Real-time**: Supabase Realtime or Socket.io
- **Email**: SendGrid or Postmark
- **AI/ML**: FastAPI microservices with scikit-learn, TensorFlow, or OpenAI SDK
- **Testing**: pytest + Vitest + Playwright
- **Hosting**: Vercel (frontend) + AWS ECS/Lambda (backend)
- **Pros**: Excellent for AI features, scalable, modern, type-safe with tRPC or OpenAPI
- **Cons**: More complex deployment, requires managing multiple services

**Database Schema Design Considerations:**

- MUST implement multi-tenant architecture with `school_id` or `tenant_id` on all tables
- MUST implement row-level security (RLS) policies in PostgreSQL
- MUST index foreign keys and commonly queried fields
- MUST implement soft deletes for audit trail (deleted_at timestamp)
- MUST implement created_at and updated_at timestamps on all tables
- MUST implement database-level constraints for data integrity
- MUST normalize data to avoid redundancy
- MUST implement proper foreign key relationships with ON DELETE CASCADE/RESTRICT policies
- MUST implement full-text search indexes for search features
- MUST plan for horizontal scaling (sharding) if serving many schools
- SHOULD implement read replicas for reporting queries
- SHOULD implement connection pooling (PgBouncer, Supabase Pooler)

**Key Database Tables for School Platform:**

- schools (tenants)
- users (multi-role: students, teachers, parents, admins)
- students
- parents/guardians
- teachers
- classes/courses
- enrollments (student-class relationship)
- assignments
- grades
- attendance
- announcements
- messages
- events
- documents
- permissions and roles
- audit_logs

**Rationale**: School websites require specialized features for academic management, strict compliance with education privacy laws (FERPA, COPPA, GDPR), multi-tenant architecture for serving multiple schools, and robust security to protect sensitive student data. The enhanced requirements ensure the platform meets the unique needs of educational institutions while maintaining the highest standards for data privacy, security, and accessibility.

## Load Testing & Performance Validation

### Load Testing Requirements

**All websites MUST undergo load testing before production launch:**

**Types of Load Testing:**

1. **Baseline Testing**: Establish performance baseline under normal load
   - Test with expected average concurrent users
   - Measure response times, throughput, error rates
   - Document baseline metrics for future comparison

2. **Load Testing**: Verify system handles expected peak load
   - Test with expected peak concurrent users (2-3x average)
   - Duration: Minimum 30 minutes at peak load
   - Acceptance: Response time < 3 seconds for 95th percentile
   - Acceptance: Error rate < 1%
   - Acceptance: Server CPU < 80%, Memory < 85%

3. **Stress Testing**: Determine breaking point and failure modes
   - Gradually increase load beyond expected peak
   - Identify maximum capacity before degradation
   - Verify graceful degradation (no crashes, data corruption)
   - Document breaking point and failure behavior
   - Test recovery after stress

4. **Spike Testing**: Verify system handles sudden traffic surges
   - Simulate sudden 5-10x increase in traffic
   - Duration: Hold spike for 5-10 minutes
   - Acceptance: System recovers within 2 minutes after spike
   - Verify auto-scaling triggers (if applicable)

5. **Endurance Testing** (Soak Testing): Verify stability over extended periods
   - Run at 70-80% peak capacity for extended duration (4-8 hours minimum)
   - Monitor for memory leaks, resource exhaustion
   - Verify database connection pool doesn't exhaust
   - Check for gradual performance degradation
   - Acceptance: Performance remains stable throughout test

6. **Scalability Testing**: Verify system scales with increasing load
   - Test with increasing user counts (100, 500, 1000, 5000, etc.)
   - Measure linear vs non-linear scaling characteristics
   - Identify bottlenecks preventing horizontal scaling
   - Verify auto-scaling policies work as expected

**Load Testing Tools:**

- **k6**: Modern load testing tool with JavaScript scripting (Recommended)
- **Apache JMeter**: Industry standard, GUI-based load testing
- **Gatling**: Scala-based, excellent reporting
- **Artillery**: Node.js-based, YAML configuration
- **Locust**: Python-based, distributed load generation
- **ab (Apache Bench)**: Simple CLI tool for basic load testing
- **wrk**: Modern HTTP benchmarking tool
- **Lighthouse CI**: Automated performance testing in CI/CD

**Load Testing Scenarios to Include:**

- Homepage load with and without caching
- User authentication flow (login, session management)
- API endpoints (GET, POST, PUT, DELETE)
- Search functionality with complex queries
- Form submissions
- File uploads (if applicable)
- Database-heavy operations
- Third-party API integrations
- Static asset delivery (images, CSS, JS)
- Checkout flow (for e-commerce)
- Real-time features (WebSocket connections)

**Acceptance Criteria:**

- **Response Time**: p95 < 3 seconds, p99 < 5 seconds
- **Throughput**: Meet expected requests per second (RPS) at peak
- **Error Rate**: < 0.5% under normal load, < 1% under peak load
- **Resource Utilization**: CPU < 80%, Memory < 85%, Disk I/O < 80%
- **Database**: Connection pool not exhausted, query times < 500ms p95
- **CDN Hit Rate**: > 85% for static assets
- **Concurrent Users**: Handle expected peak concurrent users
- **Recovery Time**: System recovers to normal performance within 2 minutes after spike

**Load Testing Schedule:**

- MUST perform load testing before initial production launch
- MUST perform load testing before major releases (major version bump)
- MUST perform load testing after significant infrastructure changes
- SHOULD perform monthly load testing for high-traffic sites
- MUST include load testing results in launch readiness checklist

**Load Testing Documentation:**

- Document expected traffic patterns and peak periods
- Document load testing scenarios and scripts
- Document baseline and acceptance criteria
- Document load testing results with graphs and metrics
- Document identified bottlenecks and optimization recommendations
- Document capacity planning and scaling recommendations

## Design Fidelity & Implementation Quality

### Figma-to-Code Verification

**All UI implementations MUST match approved design specifications:**

**Design Handoff Requirements:**

- Designs MUST be in Figma (or equivalent design tool with inspect capabilities)
- MUST use design tokens for colors, typography, spacing, shadows
- MUST provide component specifications and variants
- MUST provide interaction and animation specifications
- MUST provide responsive breakpoint specifications
- MUST provide accessibility annotations (color contrast, focus states, aria labels)
- MUST provide error state and edge case designs

**Implementation Fidelity Standards:**

**Pixel-Perfect Requirements** (for brand-critical pages and components):

- Layout positioning: ± 2px tolerance
- Spacing (margin/padding): ± 1px tolerance for < 16px, ± 2px for >= 16px
- Font sizes: Exact match (no tolerance)
- Line heights: ± 1px tolerance
- Colors: Exact match (use design tokens)
- Border radius: ± 1px tolerance
- Shadows: Exact match (use design tokens)
- Icons: Exact size and position

**Responsive Fidelity**:

- MUST implement all specified breakpoints
- MUST match layout reflow behavior specified in designs
- MUST implement mobile, tablet, desktop designs (if provided)
- Spacing scales proportionally across breakpoints
- Font sizes follow specified responsive scale

**Interactive State Fidelity**:

- Hover states: Exact match for colors, transforms, timing
- Focus states: Exact match with visible focus indicators
- Active/pressed states: Exact match
- Disabled states: Exact match with appropriate cursor
- Loading states: Match skeleton or spinner designs
- Error states: Match error message and validation UI designs

**Animation & Transition Fidelity**:

- Transition durations: ± 50ms tolerance
- Easing functions: Use specified easing or CSS equivalent
- Animation sequences: Follow specified timing and choreography
- Micro-interactions: Match specified hover, click, scroll effects

**Design Fidelity Verification Process:**

1. **Developer Review**: Developer inspects Figma designs before implementation
   - Extract design tokens
   - Note interactive states and animations
   - Ask questions about unclear specifications

2. **Implementation**: Develop component/page matching designs

3. **Self-Review**: Developer compares implementation to designs
   - Use Figma inspect mode for measurements
   - Test all interactive states
   - Test all breakpoints
   - Screenshot comparison

4. **Designer Review**: Designer reviews implementation
   - Side-by-side comparison with designs
   - Test on real devices for responsive fidelity
   - Verify animations and transitions
   - Approve or request changes

5. **Visual Regression Testing**: Automated screenshot comparison
   - Percy, Chromatic, or equivalent tool
   - Capture screenshots across breakpoints
   - Capture screenshots of interactive states
   - Flag visual differences for review

6. **QA Testing**: Verify across browsers and devices
   - Cross-browser testing (Chrome, Firefox, Safari, Edge)
   - Mobile device testing (iOS, Android)
   - Verify responsive breakpoints
   - Verify interactive states

**Tools for Design Fidelity:**

- **Figma Inspect**: Extract CSS, measurements, assets
- **Chromatic**: Visual regression testing for Storybook components
- **Percy**: Visual regression testing in CI/CD
- **PixelParallel**: Browser extension for design overlay comparison
- **PerfectPixel**: Browser extension for pixel-perfect comparison
- **Responsively**: Test responsive designs across multiple devices simultaneously

**Acceptable Deviations:**

Deviations from designs MUST be documented and approved by designer:

- Technical limitations (browser support, performance considerations)
- Accessibility improvements (e.g., larger touch targets, better contrast)
- SEO improvements (e.g., semantic HTML over design-specified divs)
- Performance optimizations (e.g., simplified animations)

**Design Fidelity in Code Reviews:**

- Pull requests MUST include screenshots showing implementation
- Screenshots SHOULD show: desktop, tablet, mobile views
- Screenshots SHOULD show: default, hover, focus, error states
- Designer MUST approve before merge (for UI changes)
- Visual regression tests MUST pass before merge

## AI Safety & Content Moderation

### AI-Generated Content Safety

**If website uses AI-generated content, MUST implement safety measures:**

**Content Generation Safety:**

- MUST implement content filtering for inappropriate, harmful, or illegal content
- MUST implement bias detection and mitigation
- MUST provide human review for sensitive content categories
- MUST display clear labeling when content is AI-generated
- MUST implement fact-checking for factual claims (where applicable)
- MUST provide source attribution for training data (where applicable)
- MUST implement rate limiting to prevent abuse
- MUST log all AI-generated content for audit purposes

**AI Model Safety:**

- MUST use models with content safety filters (OpenAI Moderation API, Perspective API, etc.)
- MUST implement prompt injection prevention
- MUST sanitize user inputs to AI models
- MUST implement output validation to catch harmful content
- MUST have fallback mechanisms when AI fails
- MUST monitor AI model performance and accuracy
- MUST have procedures for model updates and versioning
- MUST comply with AI model terms of service

**User-Generated Content with AI Assistance:**

- MUST implement spam detection (Akismet, reCAPTCHA, custom)
- MUST implement profanity filtering (if appropriate for audience)
- MUST implement hate speech detection
- MUST implement personal information detection (PII, phone numbers, addresses)
- MUST implement link and malware detection
- MUST provide user reporting mechanisms
- MUST have content moderation workflow (automated + human review)
- MUST have clear community guidelines
- MUST have enforcement procedures (warnings, suspensions, bans)

**AI Chatbots & Conversational AI:**

- MUST implement conversation safety guidelines
- MUST prevent chatbot from providing medical, legal, or financial advice (unless qualified)
- MUST prevent chatbot from impersonating humans
- MUST provide clear disclosure that user is interacting with AI
- MUST implement escalation to human support when needed
- MUST log conversations for quality assurance and safety
- MUST implement timeout mechanisms for long conversations
- MUST provide user controls (report, block, end conversation)

**Bias Detection & Mitigation:**

- MUST test AI outputs for demographic bias (race, gender, age, etc.)
- MUST monitor for algorithmic discrimination
- MUST provide diverse training data where possible
- MUST have procedures for addressing reported bias
- MUST document known limitations and biases
- MUST provide user controls for personalization vs fairness tradeoffs

**AI Safety Tools & Services:**

- **OpenAI Moderation API**: Content safety classification
- **Perspective API (Google)**: Toxicity and profanity detection
- **AWS Comprehend**: Sentiment and entity analysis
- **Azure Content Moderator**: Image and text moderation
- **Akismet**: Spam detection
- **reCAPTCHA v3**: Bot detection
- **CleanSpeak**: Profanity filtering and moderation
- **Sightengine**: Image and video moderation

**AI Transparency Requirements:**

- MUST provide clear AI disclosure to users
- MUST explain AI capabilities and limitations
- MUST provide opt-out mechanisms where appropriate
- MUST respect user privacy (don't use user data for model training without consent)
- MUST comply with AI regulations (EU AI Act, etc., as applicable)

## AI Chatbots for Commercial Websites

**Comprehensive requirements for implementing AI-powered chatbots on commercial websites:**

### Chatbot Types & Use Cases

**When to Implement Chatbots:**

- Customer support automation (24/7 availability, tier 1 support)
- Lead qualification and sales assistance
- Product recommendations and discovery
- FAQ and knowledge base navigation
- Appointment booking and scheduling
- Order tracking and status updates
- Onboarding assistance for new users
- Interactive troubleshooting and diagnostics
- Multi-language customer support
- Personalized shopping assistance (e-commerce)

**Chatbot Architecture Options:**

1. **Rule-Based Chatbots**:
   - Use for: Simple FAQ, menu-driven navigation, deterministic workflows
   - Pros: Predictable, fast, cost-effective, no AI API costs
   - Cons: Limited flexibility, requires extensive rule definition
   - Tools: Botpress, Rasa (rule-based mode), custom decision trees

2. **Retrieval-Based Chatbots**:
   - Use for: Knowledge base search, document Q&A, support documentation
   - Pros: Accurate answers from verified content, explainable, cost-effective
   - Cons: Limited to existing knowledge, no generative responses
   - Tools: Elasticsearch + semantic search, Pinecone, Weaviate, Qdrant
   - Tech: Vector embeddings (OpenAI ada-002, Cohere, Sentence Transformers)

3. **Generative AI Chatbots** (LLM-powered):
   - Use for: Natural conversations, complex queries, personalized assistance
   - Pros: Human-like responses, handles novel queries, contextual understanding
   - Cons: Higher cost, potential hallucinations, requires safety measures
   - Tools: OpenAI GPT-4, Anthropic Claude, LangChain, LlamaIndex
   - Recommended: Hybrid approach (retrieval + generation) for best results

4. **Hybrid Chatbots** (Recommended for Commercial Use):
   - Combines rule-based routing, retrieval-based accuracy, and generative flexibility
   - Use retrieval for factual queries (pricing, policies, documentation)
   - Use generation for complex, conversational, personalized responses
   - Use rules for critical workflows (payments, account changes, escalation)

### Technical Implementation Requirements

**Backend Architecture (Python Recommended):**

**MUST implement:**

- **FastAPI or Flask** for chatbot API endpoints
- **WebSocket support** for real-time streaming responses
- **Database**: PostgreSQL for conversation history, user context, feedback
- **Vector database**: Pinecone, Weaviate, Qdrant, or pgvector for RAG (Retrieval-Augmented Generation)
- **Caching**: Redis for session management, rate limiting, response caching
- **Message queue**: Celery or RQ for async processing (analytics, training data collection)
- **Monitoring**: Sentry for errors, Prometheus for metrics, custom dashboards for chatbot analytics

**Chatbot API Endpoints:**

```python
# FastAPI example
POST   /api/chat/messages           # Send message, get response
GET    /api/chat/conversations      # List user conversations
GET    /api/chat/conversations/:id  # Get conversation history
POST   /api/chat/feedback           # Submit feedback on response
POST   /api/chat/escalate           # Escalate to human support
DELETE /api/chat/conversations/:id  # Delete conversation (GDPR)
WS     /api/chat/stream             # WebSocket for streaming responses
```

**LLM Integration Best Practices:**

- MUST use streaming for responses > 200 tokens (better UX)
- MUST implement request/response logging for audit and improvement
- MUST implement context window management (truncate old messages when approaching limit)
- MUST implement retry logic with exponential backoff for API failures
- MUST implement fallback responses when LLM unavailable
- MUST implement rate limiting per user (prevent abuse)
- MUST implement cost tracking and budgets (monitor API spending)
- MUST sanitize user inputs before sending to LLM
- MUST filter LLM outputs for safety (use moderation APIs)
- MUST implement conversation memory (maintain context across messages)

**Retrieval-Augmented Generation (RAG) Implementation:**

RAG combines retrieval from knowledge base with LLM generation for accurate, grounded responses.

**RAG Pipeline:**

1. **Indexing Phase** (one-time or incremental):
   - Extract content from knowledge sources (docs, FAQs, product info, policies)
   - Chunk content into semantic units (typically 500-1000 tokens)
   - Generate embeddings for each chunk (OpenAI ada-002, Cohere, etc.)
   - Store in vector database with metadata (source, date, category, tags)

2. **Retrieval Phase** (per user query):
   - Generate embedding for user query
   - Perform semantic search in vector database (cosine similarity)
   - Retrieve top K most relevant chunks (K = 3-5 typically)
   - Re-rank results (optional, using Cohere Rerank or cross-encoder)

3. **Generation Phase**:
   - Construct prompt with retrieved context + user query
   - Send to LLM with system prompt: "Answer based on provided context. If answer not in context, say so."
   - Generate response with source citations
   - Return response with source links for transparency

**RAG Example (Python + LangChain):**

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Initialize components
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Pinecone.from_existing_index("knowledge-base", embeddings)
llm = ChatOpenAI(model="gpt-4", temperature=0.7, streaming=True)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What is your return policy?"})
response = result["result"]
sources = result["source_documents"]
```

**Conversation Memory Management:**

- MUST maintain conversation history (last 5-10 messages minimum)
- MUST store conversation state (user intent, extracted entities, conversation stage)
- MUST implement conversation summarization for long conversations (>20 messages)
- MUST implement conversation reset/clear functionality
- MUST associate conversations with user accounts (if authenticated)
- MUST implement conversation expiry (delete after 30-90 days)

### Frontend Integration

**Chatbot UI Components:**

**MUST implement:**

- **Chat widget/bubble**: Persistent button in corner (bottom-right typically)
- **Chat window**: Expandable panel or full-screen overlay
- **Message list**: Scrollable conversation history
- **Input field**: Text input with send button, character limit indicator
- **Typing indicators**: Show when bot is generating response
- **Streaming display**: Display LLM response word-by-word as it generates
- **Message timestamps**: Show when each message was sent
- **Avatar/branding**: Bot avatar, company branding
- **Action buttons**: Quick replies, suggested actions, escalation to human
- **Rich content**: Support for links, images, buttons, carousels, forms
- **Feedback buttons**: Thumbs up/down on each bot response
- **Conversation reset**: Clear conversation button
- **Minimize/maximize**: Collapse chat widget when not in use

**Accessibility Requirements:**

- MUST support keyboard navigation (Tab, Enter, Escape)
- MUST provide ARIA labels for screen readers
- MUST announce new messages to screen readers
- MUST provide focus management (focus input after bot response)
- MUST support high contrast mode
- MUST provide text resize support

**Mobile Optimization:**

- MUST be responsive (adapt to mobile screens)
- MUST provide full-screen mode on mobile
- MUST handle keyboard appearance (iOS/Android)
- MUST support touch gestures (scroll, swipe to dismiss)
- MUST optimize for mobile performance (lazy load history)

**Chatbot UI Libraries:**

- **React**: Chatscope, react-chat-elements, @chatscope/chat-ui-kit-react
- **Vue**: vue-advanced-chat, vue-beautiful-chat
- **Custom**: Build with WebSocket + React/Vue components (recommended for full control)

### Conversation Design & UX

**Conversation Flow Best Practices:**

- MUST greet users with clear value proposition ("Hi! I can help you with orders, returns, and product questions.")
- MUST set expectations ("I'm an AI assistant. For complex issues, I'll connect you with a human.")
- MUST provide suggested prompts/quick replies for common questions
- MUST confirm understanding before taking actions ("You'd like to cancel order #12345, correct?")
- MUST provide clear error messages ("I didn't understand that. Could you rephrase?")
- MUST offer escalation path ("Would you like to speak with a human agent?")
- MUST summarize actions taken ("I've submitted your return request. You'll receive an email confirmation.")
- MUST provide conversation history (users can scroll up to see past messages)

**Tone & Personality:**

- MUST align with brand voice (professional, friendly, casual, formal)
- MUST be consistent across all responses
- MUST be respectful and empathetic
- MUST avoid jargon unless industry-specific context warrants it
- SHOULD use user's name if available (personalization)
- SHOULD acknowledge emotions ("I understand this is frustrating. Let me help.")

**Response Quality Guidelines:**

- MUST be concise (avoid walls of text; break into multiple messages if needed)
- MUST be accurate (verify facts, cite sources when possible)
- MUST be actionable (provide next steps, links, buttons)
- MUST be formatted (use bullets, numbered lists, bold for emphasis)
- SHOULD include relevant links (to FAQs, documentation, product pages)
- SHOULD provide alternatives ("If that doesn't work, you can also...")

### Safety, Privacy & Compliance

**Safety Requirements:**

- MUST implement content moderation (OpenAI Moderation API, Perspective API)
- MUST prevent prompt injection attacks (filter malicious prompts)
- MUST prevent jailbreaking attempts (monitor for system prompt extraction)
- MUST detect and handle abusive users (rate limiting, temporary bans)
- MUST implement profanity filtering (if appropriate for brand)
- MUST prevent chatbot from providing harmful advice (medical, legal, financial unless qualified)
- MUST prevent impersonation (clear disclosure that user is chatting with AI)
- MUST implement NSFW content blocking

**Privacy & Data Protection:**

- MUST comply with GDPR (right to deletion, data portability, consent)
- MUST comply with CCPA (California Consumer Privacy Act)
- MUST provide privacy notice before chat (link to privacy policy)
- MUST obtain consent for data collection (conversation logging, analytics)
- MUST NOT store sensitive information (credit cards, passwords, SSN, health data)
- MUST encrypt conversations at rest and in transit
- MUST implement data retention policy (delete conversations after 90 days)
- MUST provide data export functionality (user can download conversation history)
- MUST provide data deletion functionality (user can delete conversations)
- MUST anonymize analytics data (no PII in analytics)

**Authentication & Authorization:**

- SHOULD authenticate users before accessing account-specific data
- MUST implement session management (timeout after inactivity)
- MUST implement CSRF protection for chatbot API endpoints
- MUST rate limit unauthenticated users aggressively
- MUST verify user identity before performing sensitive actions (order cancellation, password reset)

### Analytics & Monitoring

**Chatbot Metrics to Track:**

- **Engagement metrics**:
  - Total conversations
  - Messages per conversation (depth of engagement)
  - Unique users
  - Returning users
  - Conversation completion rate

- **Performance metrics**:
  - Average response time (target: <2 seconds)
  - Response accuracy (based on user feedback)
  - Escalation rate (% of conversations escalated to human)
  - Resolution rate (% of issues resolved by bot)
  - User satisfaction score (thumbs up/down ratio)

- **Content metrics**:
  - Most common queries (identify gaps in knowledge base)
  - Unanswered questions (queries bot couldn't handle)
  - Top intents (categories of user queries)
  - Fallback rate (% of times bot says "I don't know")

- **Business metrics**:
  - Conversions from chatbot (sales, sign-ups, bookings)
  - Cost per conversation (LLM API costs / total conversations)
  - Support ticket deflection (% of support queries handled by bot)
  - Customer effort score (ease of getting help)

**Monitoring & Alerting:**

- MUST monitor chatbot uptime (alert if down for >5 minutes)
- MUST monitor response times (alert if p95 >5 seconds)
- MUST monitor error rates (alert if >5% of requests fail)
- MUST monitor safety violations (alert on detected abuse, harmful content)
- MUST monitor cost (alert if daily spend exceeds budget)
- MUST create dashboards for real-time metrics (Grafana, DataDog, custom)

**Continuous Improvement:**

- MUST collect user feedback (thumbs up/down on every response)
- MUST log unanswered questions for knowledge base expansion
- MUST review flagged conversations weekly (safety, quality issues)
- MUST analyze conversation transcripts monthly (identify improvement areas)
- MUST A/B test prompt variations (compare response quality)
- MUST retrain/fine-tune models quarterly (if using custom models)
- MUST update knowledge base monthly (add new FAQs, products, policies)

### Escalation to Human Support

**Escalation Triggers (MUST implement):**

- User explicitly requests human ("I want to talk to a person")
- Bot confidence score below threshold (bot unsure of answer)
- Sensitive issues (complaints, refunds, account issues)
- Complex technical problems beyond bot capabilities
- After multiple failed attempts to resolve issue (3-5 attempts)
- High-value customers (VIP tier, enterprise accounts)
- Legal or compliance matters

**Escalation Flow:**

1. Bot detects escalation trigger
2. Bot confirms escalation with user ("I'll connect you with a human agent. One moment.")
3. Bot collects necessary context (name, email, issue summary)
4. Bot creates support ticket or live chat handoff
5. Bot provides estimated wait time
6. Bot offers alternatives while waiting ("While you wait, you can check our FAQ: [link]")
7. Bot seamlessly transfers conversation history to human agent
8. Human agent receives full context (conversation history, user info, intent)

**Handoff Methods:**

- **Live chat transfer**: Direct handoff to live chat agent (Intercom, Zendesk, Freshdesk)
- **Ticket creation**: Create support ticket with conversation transcript
- **Scheduled callback**: Book callback appointment with agent
- **Email escalation**: Send conversation summary to support email

### Chatbot Platforms & Tools

**Managed Chatbot Platforms:**

- **Intercom**: All-in-one customer messaging with AI chatbot
- **Drift**: Conversational marketing and sales chatbot
- **Zendesk Answer Bot**: AI-powered support automation
- **Freshchat**: Messaging platform with chatbot builder
- **Tidio**: E-commerce focused live chat + chatbot
- **ManyChat**: Marketing chatbot for social media and web
- **Ada**: No-code chatbot builder for customer support

**Open-Source Chatbot Frameworks:**

- **Rasa**: Open-source conversational AI (Python)
- **Botpress**: Open-source chatbot builder with visual flow designer
- **Haystack**: Open-source NLP framework for RAG (Python)
- **LangChain**: Framework for LLM-powered applications (Python, TypeScript)
- **LlamaIndex**: Data framework for LLM applications (Python)
- **Chainlit**: Build production-ready conversational AI (Python)

**LLM Providers for Chatbots:**

- **OpenAI GPT-4/GPT-3.5-turbo**: Industry standard, best quality, moderate cost
- **Anthropic Claude 3**: Excellent safety, long context, competitive quality
- **Google Gemini**: Multimodal, competitive pricing, good quality
- **Cohere Command**: Enterprise-focused, good for retrieval
- **Mistral**: Open-source, cost-effective, EU-based
- **Open-source LLMs**: Llama 3, Mixtral (self-hosted, zero API cost, requires GPU)

**Vector Databases for RAG:**

- **Pinecone**: Managed vector database, easy to use, scalable
- **Weaviate**: Open-source, hybrid search, multimodal
- **Qdrant**: Open-source, fast, Rust-based
- **Milvus**: Open-source, highly scalable, battle-tested
- **Chroma**: Open-source, developer-friendly, embedded mode
- **pgvector**: PostgreSQL extension, no separate database needed

### Testing & Quality Assurance

**Chatbot Testing Requirements:**

- **Unit tests**: Test individual components (intent classification, entity extraction, response generation)
- **Integration tests**: Test API endpoints, database operations, LLM integration
- **Conversation tests**: Test complete conversation flows (happy paths, edge cases)
- **Safety tests**: Test with adversarial inputs (prompt injection, jailbreaking, abuse)
- **Regression tests**: Test that changes don't break existing functionality
- **Load tests**: Test with concurrent users (100, 500, 1000 concurrent conversations)
- **A/B tests**: Test different prompt variations, response styles, UI designs

**Test Scenarios to Cover:**

- Common user queries (FAQ, product info, support issues)
- Edge cases (typos, incomplete sentences, ambiguous queries)
- Multi-turn conversations (follow-up questions, context switching)
- Off-topic queries (personal questions, out-of-scope topics)
- Multilingual queries (if supporting multiple languages)
- Abusive inputs (profanity, harassment, prompt injection)
- System failures (LLM timeout, database down, rate limit exceeded)
- Authentication flows (login required for account queries)
- Escalation triggers (request human, complex issue, multiple failures)

**Quality Metrics:**

- Intent classification accuracy: >85%
- Response relevance (user feedback): >80% thumbs up
- Response latency: <2 seconds (p95)
- First contact resolution: >60%
- Escalation rate: <20%
- User satisfaction: >4.0/5.0

### Cost Optimization

**Strategies to Reduce LLM Costs:**

- Use cheaper models for simple queries (GPT-3.5-turbo vs GPT-4)
- Implement caching for common questions (Redis cache for 1 hour)
- Use retrieval-based answers when possible (no LLM call needed)
- Implement conversation summarization (reduce context size)
- Set max token limits (prevent runaway costs)
- Use streaming to allow early termination (stop generation if user closes chat)
- Batch non-urgent requests (analytics, training data processing)
- Monitor and alert on cost spikes (circuit breaker at daily budget)
- Consider self-hosted open-source LLMs for high-volume use cases (Llama 3, Mixtral)

**Cost Monitoring:**

- Track cost per conversation
- Track cost per user
- Track cost per intent category
- Alert when daily/monthly budget exceeded
- Analyze cost drivers (identify expensive queries)

## Internationalization & Localization (i18n/l10n)

**For websites targeting multiple languages/regions:**

### Internationalization (i18n) Requirements

**MUST implement if targeting multiple countries/languages:**

- **Language Support**:
  - Use i18n framework (react-i18next, next-intl, vue-i18n, etc.)
  - Externalize all user-facing strings (no hardcoded text)
  - Support language switching without page reload
  - Persist language preference (localStorage, cookies, user account)
  - Detect browser language for default (Accept-Language header)
  - Provide language selector in UI

- **RTL (Right-to-Left) Support**:
  - Support RTL languages (Arabic, Hebrew, Persian, Urdu)
  - Mirror layouts for RTL (flexbox, grid, positioning)
  - Mirror icons and images where culturally appropriate
  - Test all features in RTL mode
  - Use logical CSS properties (margin-inline-start vs margin-left)

- **Date & Time Formatting**:
  - Use locale-aware date formatting (Intl.DateTimeFormat)
  - Display dates in user's locale format
  - Handle timezones correctly (display in user's timezone)
  - Use ISO 8601 for data storage
  - Consider calendar differences (Gregorian, Islamic, Hebrew, etc.)

- **Number & Currency Formatting**:
  - Use locale-aware number formatting (Intl.NumberFormat)
  - Support multiple currencies with proper symbols and formatting
  - Handle decimal and thousands separators correctly
  - Support currency conversion (if applicable)
  - Display prices in user's currency preference

- **Pluralization**:
  - Handle plural forms correctly for each language
  - Use i18n framework's pluralization features
  - Test with languages having complex plural rules (Arabic, Russian, Polish)

- **Collation & Sorting**:
  - Use locale-aware string comparison (Intl.Collator)
  - Sort lists correctly for each language
  - Consider accent-insensitive sorting where appropriate

- **Input & Validation**:
  - Support locale-specific input formats (dates, numbers, phone numbers)
  - Validate based on locale rules
  - Support locale-specific keyboards and IME (Input Method Editors)

### Localization (l10n) Requirements

**Translation Management:**

- Use translation management system (Crowdin, Lokalise, Phrase, POEditor)
- Maintain translation keys in organized structure
- Provide context for translators (screenshots, descriptions, character limits)
- Implement translation versioning
- Have translation review and QA process
- Update translations before major releases

**Content Localization:**

- Localize not just text but imagery, colors, cultural references
- Adapt content for cultural appropriateness
- Consider local regulations and compliance requirements
- Adapt examples and case studies to local context
- Localize contact information and support resources

**SEO for Multiple Languages:**

- Use hreflang tags for each language version
- Use proper URL structure (/en/, /es/, /fr/ or subdomains)
- Translate metadata (titles, descriptions, keywords)
- Submit localized sitemaps to search engines
- Avoid automatic redirects based on IP (bad for SEO)

**Testing for i18n/l10n:**

- Test with longest translations (German, Finnish typically longest)
- Test with shortest translations (Chinese often shortest)
- Test with RTL languages
- Test with accented characters and special characters
- Test with different character sets (Latin, Cyrillic, Arabic, Chinese, Japanese, Korean, Thai, etc.)
- Test date, number, currency formatting in all supported locales
- Verify proper text rendering (no text overflow, proper line breaking)
- Test with pseudo-localization for i18n bugs

## Real-Time Features & WebSockets

**For websites with real-time functionality:**

### Real-Time Requirements

**When to Use Real-Time Features:**

- Live notifications and alerts
- Collaborative editing (Google Docs-style)
- Live chat and messaging
- Real-time dashboards and metrics
- Live comments and reactions
- Presence indicators (who's online)
- Live updates (social media feeds, sports scores, stock tickers)
- Real-time maps and tracking
- Multiplayer games
- Live auctions and bidding

**Real-Time Technology Options:**

1. **WebSockets** (Persistent bidirectional connection):
   - Use for: Chat, collaborative editing, high-frequency updates
   - Libraries: Socket.io, ws, uWebSockets.js
   - Pros: Full-duplex, low latency, efficient for frequent updates
   - Cons: Requires persistent connection, scaling complexity, firewall/proxy issues

2. **Server-Sent Events (SSE)** (Server-to-client unidirectional):
   - Use for: Live feeds, notifications, server-pushed updates
   - Native browser API (EventSource)
   - Pros: Built-in reconnection, simpler than WebSockets, HTTP/2 multiplexing
   - Cons: One-directional only, limited browser support for request headers

3. **Long Polling** (HTTP-based):
   - Use for: Fallback when WebSockets/SSE unavailable
   - Libraries: Any HTTP client
   - Pros: Works everywhere, simple, no special server requirements
   - Cons: Higher latency, higher server load, inefficient

4. **HTTP/2 Server Push** (Server-initiated responses):
   - Use for: Preloading assets, proactive data pushing
   - Pros: No client code needed, works with HTTP
   - Cons: Limited use cases, being deprecated in favor of 103 Early Hints

**WebSocket Implementation Requirements:**

- MUST implement connection authentication and authorization
- MUST implement heartbeat/ping-pong to detect disconnections
- MUST implement automatic reconnection with exponential backoff
- MUST handle connection state (connecting, connected, disconnected, reconnecting)
- MUST implement message queuing during disconnection
- MUST handle duplicate messages (idempotent message handling)
- MUST implement rate limiting per connection
- MUST implement connection limits per user
- MUST log WebSocket events for debugging
- SHOULD use wss:// (WebSocket Secure) in production
- SHOULD compress messages when appropriate
- SHOULD implement client-side buffering for offline resilience

**Presence & Collaborative Features:**

- Implement presence tracking (who's online, typing indicators)
- Implement cursor/selection syncing (for collaborative editing)
- Implement operational transforms or CRDTs for conflict resolution
- Implement version vectors or logical clocks for causality
- Implement user identification and avatars
- Implement graceful degradation when real-time fails

**Scaling Real-Time:**

- MUST use Redis or similar for pub/sub across server instances
- MUST implement sticky sessions or connection routing
- MUST consider WebSocket gateway (Socket.io with Redis adapter, Pusher, Ably)
- SHOULD implement horizontal scaling for WebSocket servers
- SHOULD monitor active connections and server capacity
- SHOULD implement connection limits and backpressure

**Real-Time Libraries & Services:**

- **Socket.io**: Popular WebSocket library with fallbacks and Redis adapter
- **Pusher**: Managed real-time infrastructure (WebSockets as a service)
- **Ably**: Real-time messaging platform with global infrastructure
- **PubNub**: Real-time data stream network
- **Supabase Realtime**: PostgreSQL changes as real-time streams
- **Firebase Realtime Database**: Managed real-time database
- **Parer**: Open-source WebSocket server with Redis support
- **Centrifugo**: Real-time messaging server with multiple language SDKs

## Third-Party Integrations

**Framework for evaluating and integrating third-party services:**

### Integration Categories

**Authentication & Identity:**
- Auth0, Clerk, Supabase Auth, Firebase Auth, AWS Cognito
- OAuth providers (Google, GitHub, Facebook, LinkedIn, Twitter)
- SAML providers (Okta, OneLogin, Azure AD) for enterprise
- Passwordless authentication (Magic, Stytch)

**Payments & Billing:**
- Stripe (recommended for most use cases)
- PayPal, Square, Braintree
- Paddle (merchant of record, handles taxes and compliance)
- Chargebee, Recurly (subscription management)
- Lemon Squeezy (merchant of record for digital products)

**Email:**
- Transactional: SendGrid, Postmark, Amazon SES, Mailgun
- Marketing: Mailchimp, ConvertKit, SendinBlue, Customer.io
- Email templates: MJML, React Email, Maizzle

**SMS & Communication:**
- Twilio (SMS, Voice, WhatsApp)
- Vonage (Nexmo)
- Plivo
- AWS SNS

**Analytics:**
- Google Analytics 4, Plausible, Fathom, Umami
- Mixpanel, Amplitude (product analytics)
- Segment (customer data platform)
- PostHog (open-source product analytics)

**Error Tracking:**
- Sentry, Rollbar, Bugsnag, LogRocket, TrackJS

**Search:**
- Algolia, Typesense, Meilisearch, Elasticsearch

**CMS (Content Management):**
- Headless: Contentful, Sanity, Strapi, Payload CMS
- Traditional: WordPress (headless mode), Drupal

**Database & Backend:**
- Supabase (PostgreSQL + realtime + auth)
- Firebase (Firestore, Realtime Database)
- PlanetScale (MySQL), CockroachDB (PostgreSQL)
- MongoDB Atlas, FaunaDB

**File Storage:**
- AWS S3, Google Cloud Storage, Azure Blob Storage
- Cloudflare R2, Backblaze B2
- UploadThing, Uploadcare (managed upload services)

**CDN & Edge:**
- Cloudflare, Fastly, AWS CloudFront, Bunny CDN

**Monitoring & Logging:**
- Datadog, New Relic, Grafana Cloud
- LogDNA (IBM), Papertrail, Logtail

**Customer Support:**
- Intercom, Zendesk, Freshdesk, Help Scout
- Crisp, Tawk.to (live chat)

**CRM:**
- HubSpot, Salesforce, Pipedrive, Zoho CRM

**Compliance & Legal:**
- Termly (privacy policy, cookie consent)
- Osano, OneTrust (consent management)
- TrustArc (privacy compliance)

### Integration Best Practices

**Evaluation Criteria:**

- Pricing and cost predictability
- API quality and documentation
- Rate limits and quotas
- Reliability and uptime SLA
- Security and compliance (SOC 2, GDPR, etc.)
- Developer experience
- Community and support
- Vendor lock-in risk
- Data portability
- Geographic availability

**Implementation Requirements:**

- MUST use environment variables for API keys
- MUST implement error handling for integration failures
- MUST implement retry logic with exponential backoff
- MUST implement circuit breaker for repeated failures
- MUST implement timeouts for third-party requests
- MUST log integration requests for debugging
- MUST monitor integration health and response times
- MUST have fallback behavior when integration unavailable
- MUST document integration setup in README
- SHOULD implement webhook verification for incoming webhooks
- SHOULD cache integration responses where appropriate

**Security Requirements:**

- MUST verify webhook signatures (HMAC, JWT, etc.)
- MUST use HTTPS for all integration requests
- MUST implement CORS correctly for client-side integrations
- MUST sanitize data from third-party APIs before use
- MUST not expose third-party API keys in client-side code
- MUST implement principle of least privilege for API keys

**Testing Integrations:**

- MUST mock third-party APIs in unit tests
- SHOULD use API sandboxes for integration testing
- MUST test error scenarios (timeouts, rate limits, invalid responses)
- SHOULD implement integration health checks
- MUST test webhook processing

## Progressive Web App (PWA) Requirements

**For websites that should work offline or be installable:**

### PWA Core Requirements

**Manifest File:**

- MUST provide web app manifest (`manifest.json`)
- MUST include app name, short name, description
- MUST include icons (multiple sizes: 192x192, 512x512 minimum)
- MUST specify start URL and display mode
- MUST define theme color and background color
- SHOULD include screenshots for app stores
- SHOULD define shortcuts for quick actions

**Service Worker:**

- MUST implement service worker for offline functionality
- MUST cache critical assets for offline use
- MUST implement cache-first or network-first strategy (as appropriate)
- MUST handle failed requests gracefully
- MUST implement background sync for critical operations
- SHOULD implement push notifications (if applicable)
- SHOULD implement periodic background sync (if applicable)

**Offline Experience:**

- MUST provide custom offline page (not browser default)
- MUST cache critical routes for offline viewing
- MUST queue user actions when offline (background sync)
- MUST notify users when offline
- MUST provide clear feedback when operations require connection
- SHOULD allow basic functionality offline

**Install Experience:**

- MUST meet PWA installability criteria (HTTPS, manifest, service worker)
- SHOULD implement custom install prompt
- SHOULD guide users through installation
- SHOULD detect if app is already installed
- SHOULD track installation analytics

**App-Like Experience:**

- Display mode: standalone or minimal-ui (hides browser chrome)
- Splash screen with icon and theme color
- Home screen icon
- Proper viewport configuration for mobile
- Smooth navigation (no page reloads where possible)
- App shell architecture (cached shell, dynamic content)

**Push Notifications:**

- MUST request notification permission explicitly (not on page load)
- MUST provide clear value proposition before requesting permission
- MUST respect user's notification preferences
- MUST implement notification action handling
- SHOULD segment notifications by topic/category
- SHOULD respect quiet hours

**PWA Tools & Libraries:**

- **Workbox**: Google's service worker libraries (recommended)
- **PWA Builder**: Generate manifest and service worker
- **Lighthouse**: Audit PWA compliance
- **WebPageTest**: Test offline functionality and performance

**PWA Testing:**

- MUST test service worker registration and updates
- MUST test offline functionality across all critical paths
- MUST test on actual devices (iOS, Android)
- MUST test installation flow
- MUST test push notifications (if implemented)
- MUST pass Lighthouse PWA audit

## Design System for Teams

**For organizations building and maintaining design systems:**

### Design System Architecture

**Component Library:**

- MUST use monorepo structure (Turborepo, Nx, Lerna)
- MUST version components independently or as cohesive releases
- MUST publish to private or public npm registry
- MUST use Storybook for component development and documentation
- MUST implement atomic design methodology (atoms, molecules, organisms, templates)
- MUST provide TypeScript types for all component props
- MUST document all props with JSDoc comments
- MUST provide usage examples for each component
- MUST implement accessibility props (aria-*) for all interactive components

**Design Tokens:**

- MUST use Style Dictionary or Theo for token management
- MUST define tokens in single source of truth (JSON, YAML)
- MUST generate tokens for multiple platforms (web, iOS, Android)
- MUST version tokens separately from components
- MUST document token usage and semantic meaning
- Token categories:
  - Colors (primitives, semantic, role-based)
  - Typography (font families, sizes, weights, line heights)
  - Spacing (margin, padding scales)
  - Shadows (elevation system)
  - Border radius (corner rounding)
  - Breakpoints (responsive)
  - Z-index (layering)
  - Animation (durations, easings)

**Component Development:**

- MUST develop components in isolation (Storybook)
- MUST provide all component variants and states in Storybook
- MUST implement composition patterns (compound components)
- MUST provide unstyled/headless versions for advanced customization
- MUST follow consistent naming conventions (Button, IconButton, LinkButton)
- MUST implement consistent API patterns across similar components
- MUST provide render props or slots for composition
- SHOULD use CSS-in-JS for component-scoped styles (Styled Components, Emotion)
- SHOULD provide theming capabilities (theme provider)

**Documentation:**

- MUST maintain component documentation site (Storybook Docs, Docusaurus)
- MUST document: Props, usage, accessibility, dos and don'ts
- MUST provide code examples (copy-paste ready)
- MUST document component composition patterns
- MUST provide design guidelines (when to use, alternatives)
- MUST document migration guides for breaking changes
- SHOULD provide design assets (Figma components, Sketch symbols)
- SHOULD provide interactive playgrounds

**Testing:**

- MUST unit test all components (props, interactions)
- MUST test accessibility (axe-core, jest-axe)
- MUST implement visual regression testing (Chromatic, Percy)
- MUST test theming (light/dark mode, custom themes)
- SHOULD test responsiveness across breakpoints
- SHOULD test performance (bundle size, render performance)

**Release Process:**

- MUST use semantic versioning (semver)
- MUST generate changelogs automatically (Changesets, semantic-release)
- MUST provide migration guides for breaking changes
- MUST deprecate components/props before removing (deprecation notices)
- MUST maintain LTS versions for enterprise clients
- SHOULD provide codemods for automated migrations

**Adoption & Governance:**

- MUST track component usage across products (usage analytics)
- MUST have design system working group (designers + engineers)
- MUST have contribution guidelines (how to propose new components)
- MUST have review process for new components (design + code review)
- MUST have deprecation policy (when to remove components)
- SHOULD provide design system office hours
- SHOULD create design system champions in each product team
- SHOULD incentivize adoption (remove duplicate components, consolidate)

**Design System Tools:**

- **Storybook**: Component development and documentation
- **Chromatic**: Visual regression testing
- **Style Dictionary**: Design token management
- **Changesets**: Version management and changelogs
- **Turborepo/Nx**: Monorepo management
- **Figma**: Design tool integration (Figma tokens, code generation)
- **Zeroheight**: Design system documentation
- **Supernova**: Design system platform (Figma to code)

## Public Launch & Domain Setup

### Domain Registration & DNS Configuration

**Domain Setup:**

- MUST register a professional domain name
- MUST configure DNS records at domain registrar or DNS provider (Cloudflare, Route53)
- MUST set up A records or CNAME records pointing to hosting provider
- MUST configure www subdomain redirect
- MUST set appropriate TTL values (3600s for production, lower for testing)
- MUST verify DNS propagation before launch (use dig, nslookup, or online tools)

**SSL/TLS Certificate:**

- MUST obtain SSL/TLS certificate (Let's Encrypt via hosting provider, or custom)
- MUST configure automatic certificate renewal
- MUST enforce HTTPS redirect (HTTP → HTTPS)
- MUST implement HSTS header (Strict-Transport-Security: max-age=31536000)
- MUST verify SSL configuration with SSL Labs test (grade A minimum)

**Email Configuration:**

- SHOULD set up professional email (hello@, contact@, support@)
- SHOULD configure SPF, DKIM, and DMARC records for email security
- SHOULD set up email forwarding if not using custom email service

### Hosting Platform Deployment

**Platform Selection:**

- Vercel: Best for Next.js, automatic deployments, global CDN
- Netlify: Great for static sites, form handling, serverless functions
- Cloudflare Pages: Fast, free tier generous, excellent CDN
- GitHub Pages: Free for static sites, good for simple projects
- AWS S3 + CloudFront: Full control, cost-effective for high traffic
- Render: Simple full-stack hosting with databases
- Fly.io: Global edge deployment, Docker support
- Railway: Simple deployment with databases and services

**Deployment Configuration:**

- MUST connect git repository to hosting platform
- MUST configure build command and output directory
- MUST set environment variables in hosting platform dashboard
- MUST enable automatic deployments on push to main branch
- MUST configure preview deployments for pull requests
- MUST set up custom domain in hosting platform
- MUST verify domain ownership (DNS verification or file upload)

**CDN & Caching:**

- MUST enable CDN for static assets
- MUST configure cache headers for different asset types:
  - HTML: Cache-Control: public, max-age=0, must-revalidate
  - CSS/JS: Cache-Control: public, max-age=31536000, immutable
  - Images: Cache-Control: public, max-age=604800 (1 week)
- MUST implement cache invalidation strategy for content updates
- MUST configure compression (gzip/brotli) at CDN level

### Pre-Launch Checklist

**Before Making Site Public:**

- [ ] All tests passing (unit, integration, e2e, accessibility)
- [ ] Load testing completed and results acceptable
- [ ] Design fidelity verified (Figma-to-code comparison)
- [ ] Lighthouse score ≥ 90 on all pages
- [ ] Accessibility audit passed (WCAG 2.1 AA compliance)
- [ ] Security headers configured
- [ ] SSL certificate installed and configured
- [ ] Custom domain configured and verified
- [ ] DNS records propagated
- [ ] Analytics and error tracking configured
- [ ] Uptime monitoring configured
- [ ] XML sitemap generated and submitted to search engines
- [ ] robots.txt configured appropriately
- [ ] Favicon and social sharing images present
- [ ] Contact form tested and working (if applicable)
- [ ] Content reviewed and proofread
- [ ] Cross-browser testing completed
- [ ] Mobile responsiveness tested on real devices
- [ ] Performance tested on slow 3G connection
- [ ] Backup and disaster recovery procedures documented
- [ ] Monitoring dashboards configured
- [ ] AI safety checks implemented (if applicable)
- [ ] Third-party integrations tested
- [ ] PWA install flow tested (if PWA)

**Search Engine Submission:**

- MUST submit sitemap to Google Search Console
- MUST submit sitemap to Bing Webmaster Tools
- SHOULD verify ownership of social media profiles
- SHOULD create Google My Business listing (if applicable)

### Launch Announcement

**Communication Plan:**

- Update all social media profiles with website link
- Share on relevant platforms and communities
- Email professional network with launch announcement
- Update resume/CV with website link
- Create press kit (if applicable)

## Production Operations & Reliability

### Service Level Objectives (SLOs)

**Availability:**

- Target: 99.9% uptime (allows ~43 minutes downtime per month)
- Measurement: HTTP 200 responses to health check endpoint over rolling 30-day window
- Alerting: Page on-call if availability drops below 99.8% over 24 hours

**Performance:**

- Target: 95th percentile page load time < 3 seconds
- Target: 95th percentile API response time < 500ms (if applicable)
- Measurement: Real User Monitoring (RUM) data from production
- Alerting: Notify team if p95 degrades by >20% from baseline

**Error Rate:**

- Target: < 0.1% error rate for all requests
- Measurement: 5xx errors / total requests over rolling 1-hour window
- Alerting: Page on-call if error rate > 1% for 5 minutes

### Monitoring & Alerting

**Health Checks:**

- MUST implement /health endpoint returning 200 OK when service is healthy
- MUST implement /ready endpoint for deployment readiness checks
- Health checks MUST verify critical dependencies
- MUST configure uptime monitoring

**Dashboards:**

- MUST create dashboard showing: uptime, error rate, response times, Core Web Vitals
- MUST create dashboard showing: page views, user sessions, conversion rate
- MUST create dashboard showing: deployment frequency, lead time, MTTR

**Alert Routing:**

- Critical alerts (downtime, error rate spike): Page on-call immediately
- Warning alerts (performance degradation): Notify team Slack channel
- Informational alerts (deployment success): Post to team channel

### Incident Response

**Severity Classification:**

- **SEV-1 (Critical)**: Site completely down or major functionality broken
  - Response time: 15 minutes
  - Escalation: Immediate page to on-call, all hands
- **SEV-2 (High)**: Significant degradation, impacts some users
  - Response time: 1 hour
  - Escalation: Notify on-call, page if no response
- **SEV-3 (Medium)**: Minor issues, workaround available
  - Response time: 4 hours
  - Escalation: Create ticket, address in normal workflow
- **SEV-4 (Low)**: Cosmetic issues, no user impact
  - Response time: Next business day
  - Escalation: Backlog item

**Incident Response Procedure:**

1. **Detect**: Monitoring alerts trigger or user report received
2. **Acknowledge**: On-call acknowledges alert within 15 minutes
3. **Assess**: Determine severity, impact, and root cause
4. **Mitigate**: Implement immediate fix or rollback
5. **Communicate**: Update status page, notify affected users if applicable
6. **Resolve**: Verify fix resolves issue and monitors are green
7. **Post-Mortem**: Write blameless post-mortem within 48 hours (for SEV-1/SEV-2)

**Rollback Procedure:**

- MUST be able to rollback deployment within 5 minutes
- MUST verify rollback restores service to healthy state
- MUST preserve logs and state for post-incident analysis
- Rollback triggers: Error rate >5%, availability <99%, critical bug detected

## Security Incident Response

### Vulnerability Management

**Vulnerability Disclosure Policy:**

- MUST provide security contact email (security@yourdomain.com)
- MUST acknowledge vulnerability reports within 24 hours
- MUST provide status updates every 72 hours until resolved
- MUST credit security researchers who report vulnerabilities (if desired)

**Vulnerability Severity:**

- **Critical**: Remote code execution, authentication bypass, data breach
  - Response: Patch within 24 hours
- **High**: Privilege escalation, injection vulnerabilities, XSS
  - Response: Patch within 1 week
- **Medium**: Information disclosure, CSRF
  - Response: Patch within 1 month
- **Low**: Low-impact issues, security misconfigurations
  - Response: Patch in next release

**Dependency Scanning:**

- MUST run automated dependency scanning in CI (Dependabot, Snyk, etc.)
- MUST review and update dependencies monthly
- MUST patch critical vulnerabilities within 24 hours
- MUST patch high vulnerabilities within 1 week
- MUST test patches in staging before production

### Security Incident Response Procedure

**Detection:**

- Automated vulnerability scanning alerts
- Security researcher disclosure
- User report of suspicious activity
- Monitoring alerts (unusual traffic, error patterns)

**Response Steps:**

1. **Contain**: Isolate affected systems, disable compromised accounts
2. **Assess**: Determine scope of breach, data accessed, attacker methods
3. **Eradicate**: Remove malicious code, close vulnerability, patch systems
4. **Recover**: Restore systems from clean backups, verify integrity
5. **Notify**: Inform affected users if PII compromised (GDPR/CCPA requirement)
6. **Learn**: Conduct post-incident review, update security controls

**Data Breach Notification:**

- MUST notify affected users within 72 hours of discovery (GDPR requirement)
- MUST notify relevant authorities (data protection authority)
- MUST provide clear information: what data, what happened, what steps taken
- MUST offer remediation (password reset, credit monitoring if applicable)

## Disaster Recovery & Backups

### Backup Strategy

**Backup Targets:**

- Repository code: Git (already backed up on GitHub/GitLab)
- Configuration files: Stored in repository or secrets manager
- Content data: Structured content files in repository or CMS
- Database: Automated daily backups (if applicable)
- User uploads: S3 or equivalent with versioning enabled
- Analytics data: Exported monthly to secure storage

**Backup Frequency:**

- Code/content: Continuous (git commits)
- Database: Daily automated snapshots, retained 30 days
- File uploads: Continuous with versioning
- Configuration: On change (versioned in IaC)
- Analytics exports: Monthly

**Backup Retention:**

- Git history: Indefinite
- Database snapshots: 30 days
- File upload versions: 90 days
- Configuration snapshots: 90 days
- Analytics exports: 13 months

**Backup Verification:**

- MUST test disaster recovery procedure quarterly
- MUST verify backup integrity monthly
- MUST document recovery steps in runbook

### Recovery Objectives

**RTO (Recovery Time Objective): 1 hour**

- Maximum acceptable time to restore service after disaster

**RPO (Recovery Point Objective): 24 hours**

- Maximum acceptable data loss

**Recovery Scenarios:**

- **Hosting provider outage**: Redeploy to backup hosting provider
  - Time estimate: 30 minutes
  - Prerequisites: Backup hosting account configured, DNS records documented
- **Database corruption**: Restore from last good snapshot
  - Time estimate: 15 minutes
  - Prerequisites: Regular snapshots, tested restore procedure
- **Accidental deployment of broken code**: Rollback to last known good version
  - Time estimate: 5 minutes
  - Prerequisites: Versioned deployments, rollback automation
- **Domain hijacking**: Restore DNS records, transfer domain to backup registrar
  - Time estimate: 4 hours
  - Prerequisites: Domain transfer code stored securely, backup registrar account

### Geographic Redundancy

**CDN Distribution:**

- MUST use CDN with global edge locations
- MUST serve static assets from multiple geographic regions
- MUST configure automatic failover if primary region unavailable

**DNS Redundancy:**

- MUST use DNS provider with multiple nameservers
- SHOULD configure secondary DNS provider for critical domains

## Launch Readiness Checklist

**This checklist MUST be completed before production launch:**

### Security

- [ ] HTTPS enabled with valid SSL certificate (grade A on SSL Labs)
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Rate limiting configured (forms, APIs)
- [ ] Input validation implemented on all user inputs
- [ ] Dependency vulnerability scan passed (zero critical/high vulnerabilities)
- [ ] Secret scanning enabled on repository
- [ ] Environment variables properly secured
- [ ] Error messages do not expose sensitive information
- [ ] Security incident response procedure documented
- [ ] Vulnerability disclosure policy published
- [ ] AI safety measures implemented (if using AI)

### Performance

- [ ] Lighthouse score ≥ 90 on all critical pages (mobile and desktop)
- [ ] Core Web Vitals meet "Good" thresholds
- [ ] Images optimized and served in modern formats
- [ ] JavaScript bundle size meets budget (< 150KB gzipped)
- [ ] CSS bundle size meets budget (< 50KB gzipped)
- [ ] Critical CSS inlined, non-critical CSS deferred
- [ ] Fonts optimized
- [ ] Third-party scripts lazy-loaded
- [ ] Page load time < 3 seconds on 3G tested and verified
- [ ] Load testing completed (baseline, load, stress, spike tests)
- [ ] Load test results meet acceptance criteria

### Design & UX

- [ ] Design fidelity verified (Figma-to-code comparison)
- [ ] Visual regression tests passed
- [ ] Designer approved implementation
- [ ] Responsive design tested across breakpoints
- [ ] Interactive states implemented (hover, focus, active, disabled)
- [ ] Animations and transitions match specifications
- [ ] Error states and edge cases designed and implemented
- [ ] Loading states implemented (skeleton screens or spinners)
- [ ] Empty states implemented

### Accessibility

- [ ] WCAG 2.1 Level AA compliance verified
- [ ] Automated accessibility tests passed (axe-core)
- [ ] Manual keyboard navigation tested
- [ ] Screen reader tested (NVDA, VoiceOver)
- [ ] Color contrast ratios meet WCAG requirements (4.5:1)
- [ ] Touch targets ≥ 44px x 44px
- [ ] Form labels and ARIA attributes present
- [ ] Skip-to-content link implemented
- [ ] Focus indicators visible

### SEO

- [ ] Meta tags present on all pages (title, description)
- [ ] Open Graph tags configured for social sharing
- [ ] Twitter Card tags configured
- [ ] Structured data (JSON-LD) implemented (appropriate schemas for website type)
- [ ] XML sitemap generated and accessible
- [ ] robots.txt configured and accessible
- [ ] Canonical URLs configured
- [ ] Favicon present (multiple sizes)
- [ ] 404 page customized with helpful navigation
- [ ] SEO-friendly URLs

### Content

- [ ] All content reviewed and proofread
- [ ] All images have descriptive alt text
- [ ] All internal links tested and working
- [ ] All external links tested
- [ ] Contact form tested and delivers messages (if applicable)
- [ ] Social media links present and correct
- [ ] Legal pages present (privacy policy, terms, cookie policy as needed)

### Testing

- [ ] All unit tests passing (≥90% coverage for critical paths)
- [ ] All integration tests passing
- [ ] All e2e tests passing (critical user journeys)
- [ ] Cross-browser testing completed (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsiveness tested on real devices (iOS, Android)
- [ ] Visual regression tests passed
- [ ] Accessibility tests passed
- [ ] Performance tests passed

### Monitoring & Analytics

- [ ] Uptime monitoring configured
- [ ] Error tracking configured (Sentry, Rollbar, etc.)
- [ ] Analytics configured (privacy-respecting)
- [ ] Cookie consent banner implemented (if needed)
- [ ] Monitoring dashboards created
- [ ] Alerting configured (downtime, error spikes, performance degradation)
- [ ] Health check endpoints implemented and tested

### Deployment

- [ ] Production environment configured
- [ ] Staging environment configured (mirrors production)
- [ ] CI/CD pipeline configured
- [ ] Automatic deployments on push to main branch
- [ ] Preview deployments on pull requests
- [ ] Environment variables configured in hosting platform
- [ ] Custom domain configured and verified
- [ ] DNS records configured and propagated
- [ ] CDN configured for static assets
- [ ] Cache headers configured appropriately
- [ ] Rollback procedure tested
- [ ] Disaster recovery procedure documented

### Integrations

- [ ] All third-party integrations tested
- [ ] API keys secured in environment variables
- [ ] Webhook verification implemented
- [ ] Integration error handling implemented
- [ ] Integration monitoring configured

### i18n/l10n (if applicable)

- [ ] All languages tested
- [ ] RTL layout tested (if supporting RTL languages)
- [ ] Date/number/currency formatting verified for all locales
- [ ] Translations reviewed by native speakers
- [ ] hreflang tags implemented

### PWA (if applicable)

- [ ] Manifest file present and configured
- [ ] Service worker implemented and tested
- [ ] Offline functionality tested
- [ ] Install prompt tested
- [ ] Icons present (multiple sizes)
- [ ] Lighthouse PWA audit passed

### Legal & Compliance

- [ ] Privacy policy published (if collecting user data)
- [ ] Terms of service published (if applicable)
- [ ] Cookie policy published (if using cookies)
- [ ] GDPR compliance verified (if serving EU users)
- [ ] CCPA compliance verified (if serving California users)
- [ ] Industry-specific compliance verified (HIPAA, PCI DSS, SOC 2, etc.)
- [ ] Copyright notice present
- [ ] License information for open-source dependencies

### Operations

- [ ] Incident response procedure documented
- [ ] On-call rotation configured (if team)
- [ ] Backup strategy documented and tested
- [ ] Recovery procedures documented
- [ ] Maintenance window policy defined
- [ ] Status page configured (if applicable)
- [ ] Launch announcement prepared

## Maintenance & Update Policy

### Dependency Management

**Update Schedule:**

- **Security patches (Critical/High)**: Within 24 hours of disclosure
- **Security patches (Medium/Low)**: Within 1 week
- **Minor updates**: Monthly (first Monday of month)
- **Major updates**: Quarterly (requires testing and migration plan)

**Update Procedure:**

1. Review changelog and breaking changes
2. Update in staging environment
3. Run full test suite
4. Perform manual testing of critical paths
5. Deploy to production during maintenance window
6. Monitor for 24 hours for issues

**Dependency Review:**

- MUST review all dependencies quarterly for:
  - Security vulnerabilities (CVSS score ≥ 7.0)
  - License compliance (ensure compatible licenses)
  - Maintenance status (avoid abandoned packages)
  - Bundle size impact (consider lighter alternatives)

### Technical Debt Management

**Technical Debt Tracking:**

- MUST tag technical debt items in issue tracker
- MUST categorize as: Code Quality, Performance, Security, Documentation
- MUST prioritize based on impact and effort
- MUST allocate 20% of sprint capacity to technical debt reduction

**Refactoring Policy:**

- MUST write tests before refactoring
- MUST refactor incrementally (not big bang rewrites)
- MUST verify tests pass after refactoring
- MUST update documentation when refactoring public APIs

### Performance Monitoring

**Monthly Performance Review:**

- Review Core Web Vitals trends from RUM data
- Identify pages with degraded performance
- Analyze bundle size growth
- Review third-party script impact
- Create tickets for performance improvements

**Performance Regression Alerts:**

- Alert if Lighthouse score drops below 85
- Alert if bundle size increases by >10KB
- Alert if Core Web Vitals degrade by >20% from baseline

### Content Maintenance

**Content Review Schedule:**

- Content audit: Quarterly (remove outdated, add new)
- Link checking: Monthly (fix broken links)
- Contact information: Monthly verification
- Legal pages (privacy policy, terms): Quarterly review

**Content Deprecation:**

- Mark outdated content as "Archived" rather than deleting
- Implement redirects for removed pages (301 permanent redirects)
- Update internal links when content is moved
- Preserve historical content for reference

## Quality Standards

### Code Quality Gates

**All code MUST pass these quality gates before merge:**

- All tests pass (unit, integration, e2e)
- Linting passes with zero errors
- Type checking passes with no errors (TypeScript strict mode)
- Code coverage meets minimum threshold (80% for critical paths)
- No high-severity security vulnerabilities in dependencies
- Accessibility audit passes (via axe-core)
- Performance budget met (Lighthouse score ≥ 90)
- SEO audit passes (meta tags, structured data present)
- Visual regression tests pass (no unintended UI changes)
- Design fidelity verified (for UI changes)
- Load testing passed (for performance-critical changes)
- Peer review approved by at least one reviewer

### Testing Strategy

**Testing MUST cover multiple levels:**

- **Unit Tests**: Test individual functions/components in isolation
- **Integration Tests**: Test component interactions and data flow
- **End-to-End Tests**: Test critical user journeys
- **Visual Regression Tests**: Prevent unintended UI changes
- **Accessibility Tests**: Automated a11y checks in test suite
- **Performance Tests**: Lighthouse CI in pull requests
- **Load Tests**: Verify system handles expected traffic

### Browser & Device Support

**MUST support:**

- Modern browsers: Last 2 versions of Chrome, Firefox, Safari, Edge
- Mobile devices: iOS Safari 14+, Chrome Android
- Screen readers: NVDA, JAWS, VoiceOver
- Keyboard-only navigation
- Touch and mouse interactions
- Tablets: iPad, Android tablets

## Development Workflow

### Git Workflow

**MUST follow this git workflow:**

- Work on feature branches: `feature/brief-description`
- Commit messages MUST follow Conventional Commits format
- Commits MUST be atomic and focused
- MUST create pull requests for all changes
- Pull requests MUST pass all CI checks before merge
- MUST use semantic versioning for releases
- MUST tag releases in git

### Code Review Requirements

**All pull requests MUST:**

- Include description of changes and rationale
- Reference related issues or specs
- Include tests for new functionality
- Update documentation if APIs changed
- Include screenshots for UI changes
- Pass all automated checks
- Receive approval from at least one reviewer
- Have designer approval for UI changes
- Have no unresolved comments before merge

### Continuous Integration & Deployment

**CI pipeline MUST:**

- Run all tests on every commit
- Check code style and linting
- Run TypeScript type checking
- Run security scans on dependencies
- Generate code coverage reports
- Run accessibility audits
- Run Lighthouse performance audit
- Validate content schema (if applicable)
- Build and deploy preview for pull requests
- Block merge if any checks fail

**Deployment & Release Management:**

**Deployment Environments:**

- **Development**: Local development environment
- **Staging**: Mirrors production, for final testing
- **Production**: Live site serving public traffic

**Deployment Strategy:**

- MUST use automated deployments (CI/CD)
- MUST deploy to staging first, then production
- MUST run smoke tests after staging deployment
- MUST deploy during maintenance window (if disruptive)
- MUST communicate deployments to team

**Canary Deployments (Recommended for Major Changes):**

- Deploy to 5% of traffic initially
- Monitor error rates and performance for 1 hour
- If metrics are healthy, increase to 50% for 1 hour
- If metrics remain healthy, deploy to 100%
- If metrics degrade at any point, automatic rollback

**Feature Flags:**

- MUST use feature flags for large features or risky changes
- Feature flags allow enabling features for specific users or environments
- Feature flags enable safe rollout and instant rollback without redeployment

**Rollback Procedures:**

- MUST be able to rollback within 5 minutes
- Rollback triggers: Error rate >5%, availability <99%, critical bug
- Rollback process:
  1. Identify last known good deployment version
  2. Trigger rollback via hosting platform or revert git commit
  3. Verify rollback successful (health checks green)
  4. Monitor for 30 minutes to ensure stability
  5. Investigate root cause of issue
  6. Create hotfix if necessary

**Release Management:**

- MUST follow semantic versioning (MAJOR.MINOR.PATCH)
- MUST create git tags for releases
- MUST generate release notes for each version
- MUST announce releases in changelog
- Major releases: Include breaking changes, migrations
- Minor releases: Include new features, enhancements
- Patch releases: Include bug fixes, security patches

**Deployment Infrastructure:**

- MUST use Infrastructure as Code where applicable
- MUST support zero-downtime deployments
- MUST provide rollback capability
- MUST maintain environment parity (dev/staging/prod)
- MUST use CDN for static assets
- MUST implement cache invalidation strategy
- MUST monitor deployment health and rollback on errors
- MUST tag releases in git with semantic versioning

**Environment Configuration:**

- MUST use environment variables for configuration
- MUST NOT commit secrets to repository
- MUST document all required environment variables
- MUST provide example .env file
- MUST validate environment configuration on startup

## Governance

### Amendment Process

**Constitution changes require:**

1. Documented proposal with rationale
2. Impact analysis on existing features
3. Update to affected templates and documentation
4. Team review and approval
5. Version bump following semantic versioning
6. Migration plan if breaking changes introduced

### Complexity Justification

**Any deviation from principles MUST be justified:**

- Document why simpler approach is insufficient
- Explain specific problem being solved
- Include plan to return to compliance if temporary
- Require additional review and approval
- Track as technical debt if not resolved

### Compliance Verification

**Constitution compliance is enforced through:**

- Automated checks in CI/CD pipeline
- Code review checklist referencing principles
- Regular architecture review sessions
- Documentation audits for completeness
- Periodic security and accessibility audits

### Living Document

**This constitution is a living document:**

- Review quarterly or when significant changes planned
- Update based on lessons learned and project evolution
- Maintain version history in git
- Communicate changes to all team members
- Update dependent templates when amended

**Version**: 1.6.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-12
