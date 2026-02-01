# 🚀 Deployment Guide - ABC Higher Secondary School Website

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Step 1: Configure School Data](#step-1-configure-school-data)
- [Step 2: Update Data Files](#step-2-update-data-files)
- [Step 3: Configure Environment](#step-3-configure-environment)
- [Step 4: Deploy to Vercel](#step-4-deploy-to-vercel)
- [Step 5: Custom Domain Setup](#step-5-custom-domain-setup)
- [Updating School Data](#updating-school-data)
- [Alternative Deployment Options](#alternative-deployment-options)

---

## Overview

This guide will help you deploy the ABC Higher Secondary School website **without PostgreSQL database** using static JSON configuration files. All school data will be stored in configuration files that can be updated without changing code.

### Architecture
- **Frontend**: Next.js (Static/Server-Side Rendered)
- **Data Storage**: JSON configuration files
- **Hosting**: Vercel (recommended) or Netlify
- **No Backend Required**: Pure frontend deployment

---

## Prerequisites

Before starting, ensure you have:

- ✅ Node.js 18.x or higher installed
- ✅ Git installed
- ✅ A Vercel account (free tier is sufficient) - [Sign up here](https://vercel.com)
- ✅ School logo image
- ✅ School photos and faculty images
- ✅ Principal's photo
- ✅ School information (name, address, contact details)

---

## Step 1: Configure School Data

### 1.1 Create Data Directory Structure

Create a new directory for school data:

```bash
cd frontend
mkdir -p public/data
mkdir -p public/images/faculty
mkdir -p public/images/gallery
```

### 1.2 Add School Images

Place your school images in the following folders:

```
frontend/public/images/
├── logo.png                    # School logo (recommended: 200x200px)
├── hero-banner.jpg             # Homepage banner (recommended: 1920x600px)
├── principal.jpg               # Principal's photo (recommended: 400x400px)
├── faculty/
│   ├── teacher1.jpg           # Faculty photos (recommended: 300x300px)
│   ├── teacher2.jpg
│   └── ...
└── gallery/
    ├── event1.jpg             # School activities (recommended: 800x600px)
    ├── event2.jpg
    └── ...
```

---

## Step 2: Update Data Files

### 2.1 Create School Configuration File

Create `frontend/public/data/school-config.json`:

```json
{
  "school_name": "ABC Higher Secondary School",
  "tagline": "Excellence in Education Since 1990",
  "logo_url": "/images/logo.png",
  "banner_url": "/images/hero-banner.jpg",
  "primary_color": "#1E40AF",
  "secondary_color": "#3B82F6",
  "address": "123 Education Street, Knowledge City, State 12345",
  "phone": "+1 (555) 123-4567",
  "email": "info@abchighersecondary.edu",
  "established_year": 1990,
  "total_students": 850,
  "total_teachers": 45,
  "facilities": [
    "Science Labs",
    "Computer Labs",
    "Library",
    "Sports Complex",
    "Auditorium",
    "Cafeteria"
  ],
  "social_media": {
    "facebook": "https://facebook.com/abchighersecondary",
    "twitter": "https://twitter.com/abchighersec",
    "instagram": "https://instagram.com/abchighersecondary"
  }
}
```

### 2.2 Create Principal Profile

Create `frontend/public/data/principal.json`:

```json
{
  "principal_name": "Dr. John Smith",
  "designation": "Principal",
  "qualification": "Ph.D. in Educational Administration",
  "experience_years": 20,
  "photo_url": "/images/principal.jpg",
  "email": "principal@abchighersecondary.edu",
  "phone": "+1 (555) 123-4568",
  "message": "Dear Students, Parents, and Staff,\n\nWelcome to ABC Higher Secondary School! It is my great honor to serve as the Principal of this prestigious institution.\n\nFor over three decades, ABC Higher Secondary School has been committed to providing quality education and nurturing young minds. Our dedicated faculty members work tirelessly to create an environment where students can excel academically, develop their talents, and grow into responsible citizens.\n\nWe believe in holistic education that balances academics with extracurricular activities, character building, and life skills development. Our state-of-the-art facilities and innovative teaching methods ensure that every student receives the best possible education.\n\nI invite you to explore our website and learn more about our programs, achievements, and vibrant school community. Together, we can build a brighter future for our students.\n\nWarm regards,\nDr. John Smith\nPrincipal, ABC Higher Secondary School"
}
```

### 2.3 Create Faculty Data

Create `frontend/public/data/faculty.json`:

```json
[
  {
    "id": "1",
    "name": "Mrs. Sarah Johnson",
    "designation": "Mathematics Teacher",
    "qualification": "M.Sc. Mathematics",
    "photo_url": "/images/faculty/teacher1.jpg",
    "email": "sarah.johnson@abchighersecondary.edu",
    "subjects": ["Mathematics", "Statistics"],
    "experience_years": 12,
    "is_visible": true
  },
  {
    "id": "2",
    "name": "Mr. Robert Williams",
    "designation": "Science Teacher",
    "qualification": "M.Sc. Physics",
    "photo_url": "/images/faculty/teacher2.jpg",
    "email": "robert.williams@abchighersecondary.edu",
    "subjects": ["Physics", "Chemistry"],
    "experience_years": 10,
    "is_visible": true
  },
  {
    "id": "3",
    "name": "Ms. Emily Davis",
    "designation": "English Teacher",
    "qualification": "M.A. English Literature",
    "photo_url": "/images/faculty/teacher3.jpg",
    "email": "emily.davis@abchighersecondary.edu",
    "subjects": ["English", "Literature"],
    "experience_years": 8,
    "is_visible": true
  }
]
```

### 2.4 Create Notices Data

Create `frontend/public/data/notices.json`:

```json
[
  {
    "id": "1",
    "title": "Annual Sports Day 2024",
    "content": "Our Annual Sports Day will be held on March 15, 2024. All students are required to participate. Parents are welcome to attend.",
    "priority": "high",
    "published_date": "2024-02-01",
    "is_active": true
  },
  {
    "id": "2",
    "title": "Parent-Teacher Meeting",
    "content": "Parent-Teacher meeting scheduled for February 20, 2024. Please check the school notice board for timing details.",
    "priority": "medium",
    "published_date": "2024-02-05",
    "is_active": true
  },
  {
    "id": "3",
    "title": "Summer Vacation Announcement",
    "content": "Summer vacation will commence from May 1, 2024. School will reopen on June 15, 2024.",
    "priority": "low",
    "published_date": "2024-02-10",
    "is_active": true
  }
]
```

### 2.5 Create Gallery Data

Create `frontend/public/data/gallery.json`:

```json
[
  {
    "id": "1",
    "title": "Annual Day Celebration 2023",
    "description": "Students performing cultural dances and skits during our Annual Day celebration",
    "image_url": "/images/gallery/event1.jpg",
    "category": "Events",
    "upload_date": "2024-01-15"
  },
  {
    "id": "2",
    "title": "Science Exhibition",
    "description": "Students showcasing their innovative science projects",
    "image_url": "/images/gallery/event2.jpg",
    "category": "Academics",
    "upload_date": "2024-01-20"
  },
  {
    "id": "3",
    "title": "Sports Championship Trophy",
    "description": "Our school team winning the inter-school sports championship",
    "image_url": "/images/gallery/event3.jpg",
    "category": "Sports",
    "upload_date": "2024-01-25"
  }
]
```

### 2.6 Create Results Data

Create `frontend/public/data/results.json`:

```json
[
  {
    "id": "1",
    "academic_year": "2023-2024",
    "class_level": "Class 10",
    "exam_type": "Annual Examination",
    "total_students": 120,
    "pass_percentage": 98.5,
    "average_marks": 87.3,
    "students": [
      {
        "roll_no": "1001",
        "name": "Alice Anderson",
        "marks": {
          "English": 95,
          "Mathematics": 98,
          "Science": 96,
          "Social Studies": 92,
          "Hindi": 90
        },
        "total": 471,
        "percentage": 94.2,
        "grade": "A+",
        "rank": 1
      },
      {
        "roll_no": "1002",
        "name": "Bob Brown",
        "marks": {
          "English": 92,
          "Mathematics": 95,
          "Science": 94,
          "Social Studies": 90,
          "Hindi": 88
        },
        "total": 459,
        "percentage": 91.8,
        "grade": "A+",
        "rank": 2
      },
      {
        "roll_no": "1003",
        "name": "Carol Chen",
        "marks": {
          "English": 90,
          "Mathematics": 93,
          "Science": 92,
          "Social Studies": 89,
          "Hindi": 86
        },
        "total": 450,
        "percentage": 90.0,
        "grade": "A+",
        "rank": 3
      }
    ]
  },
  {
    "id": "2",
    "academic_year": "2023-2024",
    "class_level": "Class 12",
    "exam_type": "Final Examination",
    "total_students": 100,
    "pass_percentage": 99.0,
    "average_marks": 85.7,
    "students": [
      {
        "roll_no": "2001",
        "name": "David Davis",
        "marks": {
          "English": 94,
          "Physics": 97,
          "Chemistry": 95,
          "Mathematics": 98,
          "Computer Science": 96
        },
        "total": 480,
        "percentage": 96.0,
        "grade": "A+",
        "rank": 1
      },
      {
        "roll_no": "2002",
        "name": "Emma Evans",
        "marks": {
          "English": 92,
          "Physics": 94,
          "Chemistry": 93,
          "Mathematics": 96,
          "Computer Science": 94
        },
        "total": 469,
        "percentage": 93.8,
        "grade": "A+",
        "rank": 2
      },
      {
        "roll_no": "2003",
        "name": "Frank Foster",
        "marks": {
          "English": 90,
          "Physics": 92,
          "Chemistry": 91,
          "Mathematics": 94,
          "Computer Science": 92
        },
        "total": 459,
        "percentage": 91.8,
        "grade": "A+",
        "rank": 3
      }
    ]
  }
]
```

---

## Step 3: Configure Environment

### 3.1 Create Static Data Service

Create `frontend/src/services/staticDataService.ts`:

```typescript
/**
 * Static data service for file-based school data
 * Replaces database calls with JSON file reads
 */

export class StaticDataService {
  private baseUrl = '/data';

  async getSchoolConfig() {
    const response = await fetch(`${this.baseUrl}/school-config.json`);
    return response.json();
  }

  async getPrincipal() {
    const response = await fetch(`${this.baseUrl}/principal.json`);
    return response.json();
  }

  async getFaculty() {
    const response = await fetch(`${this.baseUrl}/faculty.json`);
    const data = await response.json();
    return data.filter((faculty: any) => faculty.is_visible);
  }

  async getNotices() {
    const response = await fetch(`${this.baseUrl}/notices.json`);
    const data = await response.json();
    return data
      .filter((notice: any) => notice.is_active)
      .sort((a: any, b: any) => {
        const priorityOrder = { high: 1, medium: 2, low: 3 };
        return priorityOrder[a.priority as keyof typeof priorityOrder] -
               priorityOrder[b.priority as keyof typeof priorityOrder];
      });
  }

  async getGallery(category?: string) {
    const response = await fetch(`${this.baseUrl}/gallery.json`);
    const data = await response.json();
    if (category) {
      return data.filter((image: any) => image.category === category);
    }
    return data;
  }

  async getResults() {
    const response = await fetch(`${this.baseUrl}/results.json`);
    return response.json();
  }

  async getResultById(id: string) {
    const response = await fetch(`${this.baseUrl}/results.json`);
    const data = await response.json();
    return data.find((result: any) => result.id === id);
  }
}

export const staticDataService = new StaticDataService();
```

### 3.2 Update Components to Use Static Data

Update your components to use `staticDataService` instead of `publicService`:

**Example for PrincipalMessage.tsx:**
```typescript
import { staticDataService } from '../../services/staticDataService';

// Replace this line:
// const data = await publicService.getPrincipal();

// With this:
const data = await staticDataService.getPrincipal();
```

### 3.3 Create Environment File

Create `frontend/.env.local`:

```env
# School Configuration
NEXT_PUBLIC_SCHOOL_NAME="ABC Higher Secondary School"
NEXT_PUBLIC_API_URL=""
NEXT_PUBLIC_USE_STATIC_DATA=true
```

---

## Step 4: Deploy to Vercel

### 4.1 Prepare for Deployment

1. **Initialize Git Repository** (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - ABC Higher Secondary School website"
```

2. **Create GitHub Repository**:
   - Go to [GitHub](https://github.com) and create a new repository
   - Name it: `abc-higher-secondary-school`
   - Make it private if you don't want it publicly visible

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/abc-higher-secondary-school.git
git branch -M main
git push -u origin main
```

### 4.2 Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard

1. **Sign in to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Project**:
   - Click "Add New" → "Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

4. **Environment Variables**:
   Add these in the Vercel dashboard:
   ```
   NEXT_PUBLIC_SCHOOL_NAME=ABC Higher Secondary School
   NEXT_PUBLIC_USE_STATIC_DATA=true
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for deployment to complete
   - You'll get a URL like: `https://abc-higher-secondary-school.vercel.app`

#### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
```bash
npm install -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
cd frontend
vercel
```

4. **Follow the prompts**:
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name: `abc-higher-secondary-school`
   - In which directory is your code? `./`
   - Auto-detected settings? `Y`

5. **Deploy to Production**:
```bash
vercel --prod
```

---

## Step 5: Custom Domain Setup

### 5.1 Purchase a Domain

Recommended domain registrars:
- [Namecheap](https://www.namecheap.com) - Budget-friendly
- [GoDaddy](https://www.godaddy.com) - Popular choice
- [Google Domains](https://domains.google) - Simple interface

Suggested domain: `abchighersecondary.edu` or `abchighersecondary.com`

### 5.2 Configure Domain in Vercel

1. **Go to Vercel Dashboard**:
   - Select your project
   - Click "Settings" → "Domains"

2. **Add Domain**:
   - Enter your domain: `www.abchighersecondary.com`
   - Click "Add"

3. **Configure DNS**:
   Vercel will show you DNS records to add. In your domain registrar:

   **Type A Record:**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   TTL: 3600
   ```

   **Type CNAME Record:**
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 3600
   ```

4. **Wait for DNS Propagation**:
   - Usually takes 1-24 hours
   - Vercel will automatically issue SSL certificate

---

## Updating School Data

### How to Update Data Without Changing Code

#### Quick Update Process:

1. **Update Data Files**:
   - Navigate to `frontend/public/data/`
   - Edit the relevant JSON file (e.g., `notices.json`)
   - Save the file

2. **Update Images** (if needed):
   - Add/replace images in `frontend/public/images/`

3. **Commit and Push**:
```bash
git add .
git commit -m "Update school notices"
git push
```

4. **Auto-Deploy**:
   - Vercel automatically detects changes
   - Website updates in 1-2 minutes

### Common Updates:

#### Update Notices
Edit `frontend/public/data/notices.json`:
```json
{
  "id": "4",
  "title": "New Notice Title",
  "content": "Notice content here...",
  "priority": "high",
  "published_date": "2024-02-15",
  "is_active": true
}
```

#### Add Faculty Member
Edit `frontend/public/data/faculty.json`:
1. Add teacher photo to `frontend/public/images/faculty/`
2. Add entry to JSON:
```json
{
  "id": "4",
  "name": "New Teacher Name",
  "designation": "Subject Teacher",
  "qualification": "M.Sc. Subject",
  "photo_url": "/images/faculty/teacher4.jpg",
  "email": "teacher@abchighersecondary.edu",
  "subjects": ["Subject Name"],
  "experience_years": 5,
  "is_visible": true
}
```

#### Update Exam Results
Edit `frontend/public/data/results.json` - Add new result entry or update existing ones.

#### Update Principal Message
Edit `frontend/public/data/principal.json` - Change the `message` field.

---

## Alternative Deployment Options

### Option 1: Netlify

1. **Sign up**: [netlify.com](https://netlify.com)
2. **New Site from Git**: Connect GitHub repository
3. **Build Settings**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/.next`
4. **Deploy**: Click deploy

### Option 2: GitHub Pages (Static Export)

1. **Update `next.config.js`**:
```javascript
module.exports = {
  output: 'export',
  images: { unoptimized: true }
}
```

2. **Build**:
```bash
npm run build
```

3. **Deploy to GitHub Pages**:
```bash
npm install -g gh-pages
gh-pages -d out
```

### Option 3: Traditional Web Hosting (cPanel)

1. **Build Static Site**:
```bash
cd frontend
npm run build
npm run export
```

2. **Upload**:
   - Use FTP/FileZilla
   - Upload contents of `out/` folder
   - Point domain to this directory

---

## Troubleshooting

### Issue: Images Not Loading
**Solution**: Ensure all image paths start with `/images/` and files exist in `frontend/public/images/`

### Issue: Data Not Updating
**Solution**:
1. Clear browser cache (Ctrl+Shift+R)
2. Check JSON files are valid (use [JSONLint](https://jsonlint.com))
3. Verify Vercel deployment completed

### Issue: Build Fails
**Solution**:
1. Check Node.js version: `node --version` (should be 18.x+)
2. Delete `node_modules` and reinstall:
```bash
rm -rf node_modules
npm install
```

### Issue: Custom Domain Not Working
**Solution**:
1. Check DNS propagation: [whatsmydns.net](https://whatsmydns.net)
2. Verify DNS records in domain registrar
3. Wait up to 24 hours for propagation

---

## File Structure Summary

```
frontend/
├── public/
│   ├── data/                      # All school data (UPDATE HERE)
│   │   ├── school-config.json     # School information
│   │   ├── principal.json         # Principal profile
│   │   ├── faculty.json           # Teachers data
│   │   ├── notices.json           # Notices/announcements
│   │   ├── gallery.json           # Gallery images metadata
│   │   └── results.json           # Exam results
│   └── images/                    # All images (UPDATE HERE)
│       ├── logo.png
│       ├── hero-banner.jpg
│       ├── principal.jpg
│       ├── faculty/
│       │   └── teacher*.jpg
│       └── gallery/
│           └── event*.jpg
├── src/
│   ├── components/
│   ├── services/
│   │   └── staticDataService.ts  # Data fetching service
│   └── app/
└── .env.local                    # Environment variables
```

---

## Support & Maintenance

### Regular Updates Checklist

- [ ] Update notices monthly
- [ ] Add new gallery images after events
- [ ] Update exam results after each term
- [ ] Review and update faculty information annually
- [ ] Update school achievements and facilities

### Performance Optimization

1. **Optimize Images**:
   - Use [TinyPNG](https://tinypng.com) to compress images
   - Recommended formats: JPG for photos, PNG for logos

2. **Monitor Performance**:
   - Use [PageSpeed Insights](https://pagespeed.web.dev)
   - Aim for 90+ score

3. **Regular Backups**:
   - GitHub automatically backs up your code
   - Keep local backup of `public/data/` and `public/images/`

---

## Cost Estimate

| Service | Plan | Cost |
|---------|------|------|
| Vercel Hosting | Free Tier | $0/month |
| Domain Name | Annual | $10-15/year |
| **Total** | | **~$1/month** |

---

## Security Best Practices

1. ✅ Never commit sensitive data (passwords, API keys)
2. ✅ Use environment variables for configuration
3. ✅ Keep dependencies updated: `npm update`
4. ✅ Enable HTTPS (automatic with Vercel)
5. ✅ Regular backups of data files

---

## Next Steps

After deployment:

1. ✅ Test all pages on the live website
2. ✅ Share the URL with stakeholders
3. ✅ Set up Google Analytics (optional)
4. ✅ Submit to Google Search Console for SEO
5. ✅ Create social media profiles and link them

---

## Questions?

If you encounter any issues:
1. Check the troubleshooting section
2. Review Vercel deployment logs
3. Ensure all JSON files are valid
4. Verify image paths are correct

**Congratulations! Your ABC Higher Secondary School website is now live! 🎉**
