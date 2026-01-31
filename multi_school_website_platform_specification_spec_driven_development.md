# Multi‑School Website Platform – Technical & Functional Specification

> **Purpose**: This specification defines a **multi‑school, reusable, secure website platform** designed for **spec‑driven development**. The same codebase must support **multiple schools** by configuration and data separation only. No code changes should be required when onboarding a new school.

This spec is suitable for implementation using **Claude Code + Cursor**.

---

## 1. Core Design Principles

1. **Single Codebase, Multiple Schools**
2. **Strict Data Isolation per School**
3. **Configuration‑Driven Behavior**
4. **Folder & Database Separation**
5. **High Security by Default**
6. **Admin‑Friendly Updates (Non‑Technical)**
7. **Scalable & Maintainable Architecture**

---

## 2. Multi‑Tenant Architecture Model

### 2.1 Tenant Definition
- Each school is a **tenant**
- Tenant is identified by:
  - Subdomain / domain
  - OR unique school_id

Example:
```
schoolA.domain.com  → school_id = A001
schoolB.domain.com  → school_id = B002
```

---

## 3. High‑Level System Architecture

```
/client (frontend)
/core (shared logic)
/modules (feature modules)
/data
  └── schools
        ├── A001
        │    ├── config
        │    ├── faculty
        │    ├── students
        │    ├── results
        │    ├── gallery
        │    ├── notices
        │    └── management
        └── B002
/admin-panel
/security
```

---

## 4. School Configuration (Single Source of Truth)

Each school **must** have a configuration file.

### 4.1 school.config.json

```
/data/schools/A001/config/school.config.json
```

Example:
```json
{
  "school_id": "A001",
  "school_name": "ABC Public School",
  "logo": "logo.png",
  "theme": {
    "primary_color": "#0A3D62",
    "secondary_color": "#f1f1f1"
  },
  "principal": {
    "name": "Dr. XYZ",
    "photo": "principal.jpg",
    "message": "..."
  },
  "contact": {
    "email": "info@abcschool.com",
    "phone": "+91‑XXXXXXXX"
  }
}
```

📌 **Rule**: UI, branding, and content must be rendered strictly from this config.

---

## 5. Frontend Requirements (All Schools)

### 5.1 Home Page

Components (Config & Data Driven):
- Hero image slider (students, management, activities)
- School introduction
- Principal message preview
- Quick links
- Latest notices
- Highlighted results

No hardcoded school data allowed.

---

## 6. Modules (Reusable Across All Schools)

### 6.1 Principal Module

Data Source:
```
/data/schools/{school_id}/management/principal.json
```

Fields:
- Name
- Photo
- Message
- Last updated

---

### 6.2 Faculty Module

Data Structure:
```
/data/schools/{school_id}/faculty/faculty.json
```

Each faculty record:
- Full Name
- Designation
- Qualification
- Experience
- Subject
- Photo

📌 Adding a teacher must not affect other schools.

---

### 6.3 Students & Results Module

Folder Structure:
```
/data/schools/{school_id}/results/
   ├── 2024‑25/
   │     ├── class_10.json
   │     └── class_12.json
   └── 2025‑26/
```

Rules:
- Results are **year‑wise & class‑wise**
- Only admins of the same school can upload

---

### 6.4 Gallery & Activities Module

```
/data/schools/{school_id}/gallery/
   ├── sports
   ├── cultural
   └── academics
```

Features:
- Category filtering
- Image optimization
- Lazy loading

---

### 6.5 Notices & Announcements

```
/data/schools/{school_id}/notices/notices.json
```

Fields:
- Title
- Description
- Priority
- Expiry date

---

## 7. Admin Panel (Multi‑School Aware)

### 7.1 Roles

- **Super Admin**
  - Manage schools
  - Create school tenants

- **School Admin**
  - Manage only assigned school

- **Staff**
  - Limited content updates

---

### 7.2 Admin Capabilities

School Admin can:
- Upload results
- Add/edit faculty
- Update gallery
- Edit principal message
- Publish notices

📌 All actions scoped to `school_id`.

---

## 8. Security Specifications (Mandatory)

### 8.1 Authentication & Authorization
- Role‑based access control (RBAC)
- JWT / session‑based auth
- School‑scoped permissions

---

### 8.2 Data Isolation

Rules:
- No shared upload directories
- school_id mandatory in all queries
- Backend validation (not UI‑only)

---

### 8.3 Application Security

- HTTPS enforced
- Input sanitization
- CSRF protection
- Rate limiting
- CAPTCHA on public forms

---

### 8.4 File Security

- Admin folders not publicly accessible
- Results read‑only after publish
- No directory listing

---

## 9. Technology Stack (Implementation‑Friendly)

Recommended:
- Frontend: React / Next.js
- Backend: Node.js (NestJS) or Django
- Database: PostgreSQL
- Storage: Structured filesystem or S3‑like

Spec allows alternate stacks if principles remain intact.

---

## 10. Performance & Scalability

- Per‑school caching
- Image CDN
- Lazy loading
- Horizontal scalability

---

## 11. Onboarding a New School (No Code Changes)

Steps:
1. Generate new school_id
2. Create school folder
3. Add config file
4. Assign admin
5. Upload data

⏱️ Expected time: **< 2 hours**

---

## 12. Non‑Functional Requirements

- Mobile‑first responsive UI
- SEO‑ready
- Accessibility (WCAG)
- Daily backups
- Audit logs

---

## 13. Acceptance Criteria (Spec‑Driven)

- Same build runs for multiple schools
- No hardcoded school content
- Complete data isolation
- Security tests pass
- Admin cannot cross school boundary

---

## 14. Future‑Ready Extensions

- Parent / Student portal
- ERP integration
- Mobile app
- Analytics per school

---

## 15. Summary

This specification defines a **secure, scalable, multi‑school website platform** suitable for **long‑term reuse**, **low onboarding cost**, and **spec‑driven development workflows** using modern AI coding tools.

