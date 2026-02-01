# 🏫 Multi-School Setup Guide
## How to Deploy This Website for Different Schools

This guide explains how to quickly set up this website for **multiple different schools** (e.g., ABC School, CDF School, XYZ School, etc.).

---

## 📋 Table of Contents
- [Overview](#overview)
- [One-Time Setup (Template)](#one-time-setup-template)
- [For Each New School](#for-each-new-school)
- [Quick Setup Checklist](#quick-setup-checklist)
- [Automation Script](#automation-script)
- [Pricing Model](#pricing-model)
- [Maintenance & Support](#maintenance--support)

---

## Overview

### Business Model Options

**Option 1: Separate Deployment Per School** (Recommended)
- Each school gets their own Vercel project
- Independent domains (e.g., cdfschool.com, abcschool.com)
- Completely isolated data
- **Cost**: ~$1/month per school (domain only, hosting free)

**Option 2: Multi-Tenant (Advanced)**
- One deployment, multiple schools
- Requires database setup
- **Cost**: $20-50/month (hosting + database)
- Not covered in this guide

This guide focuses on **Option 1** - easiest and most cost-effective.

---

## One-Time Setup (Template)

### Create a Clean Template Repository

1. **Create Template Repository on GitHub**:
```bash
# Clone your current repo
git clone https://github.com/YOUR_USERNAME/multi-school-website.git school-website-template

cd school-website-template

# Remove school-specific data
rm -rf frontend/public/data/*.json
rm -rf frontend/public/images/*

# Keep only the template structure
git add .
git commit -m "Create clean template for new schools"
git push origin main
```

2. **Mark as Template on GitHub**:
   - Go to repository Settings
   - Check "Template repository"
   - Now you can create new repos from this template!

---

## For Each New School

### 🎯 Example: Setting Up for CDF School

#### Step 1: Create New Repository (2 minutes)

**Option A: From GitHub Template**
1. Go to your template repository
2. Click "Use this template" → "Create a new repository"
3. Name it: `cdf-school-website`
4. Make it private if needed
5. Click "Create repository"

**Option B: Manual Clone**
```bash
# Clone template
git clone https://github.com/YOUR_USERNAME/school-website-template.git cdf-school-website

cd cdf-school-website

# Remove old git history
rm -rf .git
git init

# Create new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/cdf-school-website.git
git add .
git commit -m "Initial setup for CDF School"
git push -u origin main
```

#### Step 2: Gather School Information (10-15 minutes)

**Checklist of Information to Collect from School:**

**A. Basic Information**
- [ ] School full name: "CDF Higher Secondary School"
- [ ] Tagline/Motto: "Building Future Leaders"
- [ ] Established year: 1995
- [ ] Address: Complete postal address
- [ ] Phone: Primary contact number
- [ ] Email: info@cdfschool.edu
- [ ] Total students: Approximate count
- [ ] Total teachers: Approximate count

**B. Branding**
- [ ] School logo (PNG, 200x200px)
- [ ] Brand colors (Primary & Secondary hex codes)
- [ ] Hero banner image (1920x600px)

**C. Principal Information**
- [ ] Name: Dr. Sarah Thompson
- [ ] Designation: Principal
- [ ] Qualification: Ph.D. Education
- [ ] Experience: 15 years
- [ ] Photo (400x400px)
- [ ] Email: principal@cdfschool.edu
- [ ] Phone: Direct number
- [ ] Welcome message (2-3 paragraphs)

**D. Faculty (At least 5 teachers)**
For each teacher:
- [ ] Name
- [ ] Designation/Subject
- [ ] Qualification
- [ ] Photo (300x300px)
- [ ] Email
- [ ] Subjects taught
- [ ] Years of experience

**E. Content**
- [ ] Current notices (3-5)
- [ ] Gallery photos (5-10 with descriptions)
- [ ] Recent exam results (optional for launch)
- [ ] List of facilities

**F. Social Media**
- [ ] Facebook URL (if any)
- [ ] Twitter/X URL (if any)
- [ ] Instagram URL (if any)

#### Step 3: Update Configuration Files (20 minutes)

**Navigate to data folder:**
```bash
cd frontend/public/data
```

**A. Update `school-config.json`:**
```json
{
  "school_name": "CDF Higher Secondary School",
  "tagline": "Building Future Leaders Since 1995",
  "logo_url": "/images/logo.png",
  "banner_url": "/images/hero-banner.jpg",
  "primary_color": "#8B0000",
  "secondary_color": "#DC143C",
  "address": "456 Learning Avenue, Education District, State 67890",
  "phone": "+1 (555) 987-6543",
  "email": "info@cdfschool.edu",
  "established_year": 1995,
  "total_students": 950,
  "total_teachers": 52,
  "facilities": [
    "Modern Science Laboratories",
    "Digital Learning Center",
    "Sports Stadium",
    "Music & Arts Wing",
    "Robotics Lab",
    "Library with 15,000+ books"
  ],
  "social_media": {
    "facebook": "https://facebook.com/cdfschool",
    "twitter": "https://twitter.com/cdfschool",
    "instagram": "https://instagram.com/cdfschool"
  }
}
```

**B. Update `principal.json`:**
```json
{
  "principal_name": "Dr. Sarah Thompson",
  "designation": "Principal",
  "qualification": "Ph.D. in Educational Leadership, M.Ed.",
  "experience_years": 15,
  "photo_url": "/images/principal.jpg",
  "email": "principal@cdfschool.edu",
  "phone": "+1 (555) 987-6544",
  "message": "Dear Students, Parents, and Well-wishers,\n\nWelcome to CDF Higher Secondary School! [Custom message from principal...]"
}
```

**C. Update `faculty.json`:**
```json
[
  {
    "id": "1",
    "name": "Mr. James Wilson",
    "designation": "Mathematics Department Head",
    "qualification": "M.Sc. Mathematics, B.Ed.",
    "photo_url": "/images/faculty/teacher1.jpg",
    "email": "james.wilson@cdfschool.edu",
    "subjects": ["Mathematics", "Advanced Calculus"],
    "experience_years": 10,
    "is_visible": true
  }
  // ... add more teachers
]
```

**D. Update `notices.json`, `gallery.json`, `results.json`** with school-specific data.

#### Step 4: Add School Images (15 minutes)

```bash
cd frontend/public/images
```

**Required Images:**
```
images/
├── logo.png                    # CDF School logo
├── hero-banner.jpg             # School building/campus
├── principal.jpg               # Principal's photo
├── faculty/
│   ├── teacher1.jpg           # Faculty photos
│   ├── teacher2.jpg
│   └── ...
└── gallery/
    ├── event1.jpg             # School events
    ├── event2.jpg
    └── ...
```

**Tips:**
- Use [TinyPNG](https://tinypng.com) to compress images
- Maintain consistent naming convention
- Keep images under 2MB each

#### Step 5: Test Locally (5 minutes)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 and verify:
- [ ] School name displays correctly
- [ ] Logo appears
- [ ] Colors match branding
- [ ] Principal message shows
- [ ] Faculty page loads with teachers
- [ ] Notices display
- [ ] Gallery works
- [ ] Contact information is correct

#### Step 6: Deploy to Vercel (5 minutes)

**A. Deploy:**
```bash
# Make sure you're in frontend directory
cd frontend

# Deploy
vercel --prod
```

**B. Configure Environment:**
When prompted:
- Project name: `cdf-school-website`
- Root directory: `./`
- Build settings: Accept defaults

**C. Set Environment Variables** in Vercel Dashboard:
```
NEXT_PUBLIC_SCHOOL_NAME=CDF Higher Secondary School
NEXT_PUBLIC_USE_STATIC_DATA=true
```

**D. You'll get a URL:** `https://cdf-school-website.vercel.app`

#### Step 7: Custom Domain Setup (10 minutes)

1. **Purchase Domain:**
   - Buy `cdfschool.com` or `cdfschool.edu`
   - Cost: ~$10-15/year

2. **Add to Vercel:**
   - Vercel Dashboard → Your Project → Settings → Domains
   - Add `www.cdfschool.com` and `cdfschool.com`

3. **Configure DNS:**
   In your domain registrar (Namecheap/GoDaddy):

   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   TTL: 3600

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 3600
   ```

4. **Wait for DNS propagation** (1-24 hours)
5. **SSL certificate** automatically issued by Vercel

#### Step 8: Final Handoff (5 minutes)

**Deliver to Client:**
- [ ] Live website URL
- [ ] Admin access to Vercel (add their email)
- [ ] GitHub repository access (optional)
- [ ] Data update guide (`frontend/public/data/README.md`)
- [ ] Support contact information

---

## Quick Setup Checklist

Use this for each new school:

### Pre-Deployment Checklist
- [ ] Create new repository from template
- [ ] Collect all school information
- [ ] Update `school-config.json`
- [ ] Update `principal.json`
- [ ] Update `faculty.json` (minimum 5 teachers)
- [ ] Update `notices.json` (minimum 3 notices)
- [ ] Update `gallery.json` (minimum 5 photos)
- [ ] Add school logo
- [ ] Add hero banner
- [ ] Add principal photo
- [ ] Add faculty photos (all teachers)
- [ ] Add gallery photos
- [ ] Test locally
- [ ] Validate all JSON files

### Deployment Checklist
- [ ] Push to GitHub
- [ ] Deploy to Vercel
- [ ] Set environment variables
- [ ] Test live URL
- [ ] Purchase domain
- [ ] Configure DNS
- [ ] Wait for SSL certificate
- [ ] Final testing on custom domain

### Handoff Checklist
- [ ] Provide live URL
- [ ] Grant Vercel access
- [ ] Share data update guide
- [ ] Provide support contact
- [ ] Schedule training session (optional)
- [ ] Invoice/payment

---

## Automation Script

### Create Setup Script for Faster Deployment

Create `setup-new-school.sh`:

```bash
#!/bin/bash

# Usage: ./setup-new-school.sh "CDF School" cdf-school

SCHOOL_NAME=$1
SCHOOL_SLUG=$2

echo "Setting up website for $SCHOOL_NAME..."

# Clone template
git clone https://github.com/YOUR_USERNAME/school-website-template.git ${SCHOOL_SLUG}-website
cd ${SCHOOL_SLUG}-website

# Remove template git history
rm -rf .git
git init

# Create placeholder for school data
echo "Please update the following files:"
echo "1. frontend/public/data/school-config.json"
echo "2. frontend/public/data/principal.json"
echo "3. frontend/public/data/faculty.json"
echo "4. frontend/public/data/notices.json"
echo "5. frontend/public/data/gallery.json"
echo ""
echo "Add images to:"
echo "- frontend/public/images/"
echo ""
echo "Then run:"
echo "git add ."
echo "git commit -m 'Initial setup for $SCHOOL_NAME'"
echo "git remote add origin https://github.com/YOUR_USERNAME/${SCHOOL_SLUG}-website.git"
echo "git push -u origin main"
echo ""
echo "Deploy with: cd frontend && vercel --prod"
```

**Make executable:**
```bash
chmod +x setup-new-school.sh
```

**Use it:**
```bash
./setup-new-school.sh "CDF Higher Secondary School" cdf-school
```

---

## Pricing Model

### Suggested Pricing Structure

**One-Time Setup Fee:**
- Website setup & deployment: **$500 - $1,500**
- Custom domain setup: **Included**
- Initial content upload: **Included**
- Training session: **Included**

**Annual Costs (Paid by School):**
- Domain renewal: **$10-15/year**
- Hosting (Vercel): **FREE** (or $20/month for Pro features)

**Optional Add-Ons:**
- Content updates: **$50/hour**
- Monthly maintenance: **$50-100/month**
- Custom features: **$200-500 per feature**
- Priority support: **$25/month**

**Package Pricing:**
- **Basic**: $500 (setup only)
- **Standard**: $800 (setup + 3 months support)
- **Premium**: $1,200 (setup + 6 months support + custom features)

---

## Time Estimates Per School

| Task | Time Required | Who |
|------|---------------|-----|
| Gather information | 30 min | Client |
| Repository setup | 5 min | You |
| Update data files | 20 min | You |
| Optimize images | 15 min | You |
| Local testing | 10 min | You |
| Deploy to Vercel | 5 min | You |
| Domain setup | 15 min | You |
| Documentation | 10 min | You |
| Client training | 30 min | Both |
| **Total** | **~2.5 hours** | |

**After first 2-3 schools, you can reduce this to 1.5 hours per school.**

---

## Maintenance & Support

### Monthly Maintenance Package

Offer clients a monthly package:

**What's Included:**
- Content updates (up to 5 per month)
- Image uploads (up to 10 per month)
- Notice board updates (unlimited)
- Exam results upload (as needed)
- Technical support via email
- Monthly backup

**How Clients Update Content:**
1. Email you the updates
2. You update the JSON files
3. Push to GitHub
4. Auto-deployment (1-2 minutes)

**Or teach them to do it:**
- Provide video tutorial
- Share JSON editing guide
- They update, you review and deploy

---

## Scaling to Multiple Schools

### Portfolio of 10 Schools

**Setup:**
- Create 10 separate repositories
- 10 Vercel projects
- 10 different domains

**Monthly Revenue Potential:**
| Service | Per School | 10 Schools |
|---------|-----------|------------|
| Setup fee (one-time) | $800 | $8,000 |
| Monthly maintenance | $75 | $750/month |
| Domain costs | $1 | $10/month |
| Hosting | $0 | $0 |

**Annual Revenue from 10 Schools:**
- Setup fees: $8,000 (one-time)
- Maintenance: $750 × 12 = $9,000/year
- **Total Year 1**: $17,000
- **Recurring**: $9,000/year

### Tools for Managing Multiple Schools

**Recommended Tools:**
1. **GitHub** - Repository management
2. **Vercel** - Deployment & hosting
3. **Notion/Airtable** - Client database
4. **Calendly** - Schedule meetings
5. **Stripe** - Payment processing

---

## Template Repository Structure

Keep a clean template with:

```
school-website-template/
├── frontend/
│   ├── public/
│   │   ├── data/
│   │   │   ├── school-config.template.json
│   │   │   ├── principal.template.json
│   │   │   ├── faculty.template.json
│   │   │   ├── notices.template.json
│   │   │   ├── gallery.template.json
│   │   │   └── results.template.json
│   │   └── images/
│   │       └── placeholder/
│   └── ...
├── DEPLOYMENT_GUIDE.md
├── CLIENT_HANDOFF.md
├── DATA_UPDATE_GUIDE.md
└── setup-new-school.sh
```

---

## Client Handoff Package

Create a "CLIENT_HANDOFF.md" for each school:

```markdown
# CDF Higher Secondary School - Website Handoff

## Your Website
- **Live URL**: https://www.cdfschool.com
- **Admin Panel**: https://vercel.com/cdf-school-website

## Login Credentials
- **Vercel**: Check your email for invitation
- **GitHub**: (Optional) Check your email for invitation

## How to Update Content
See the attached "Data Update Guide" PDF

## Support Contact
- **Email**: support@yourcompany.com
- **Phone**: +1 (555) 123-4567
- **Hours**: Mon-Fri, 9 AM - 6 PM

## Monthly Maintenance
- Included: Up to 5 content updates per month
- Send updates to: updates@yourcompany.com

## Domain Renewal
- **Next renewal**: March 1, 2025
- **Cost**: $12/year
- We'll email you 30 days before renewal
```

---

## FAQs

**Q: Can I use the same codebase for all schools?**
A: No, create separate repositories for each school. This keeps data isolated and allows independent updates.

**Q: What if a school wants custom features?**
A: Create a feature branch, develop the feature, merge, and redeploy. Charge accordingly.

**Q: How do I handle data updates?**
A: Either update yourself (maintenance package) or teach clients to update JSON files themselves.

**Q: Can schools share the same Vercel account?**
A: Yes, you can have multiple projects under one Vercel account.

**Q: What about backups?**
A: GitHub automatically backs up all code and data. Download monthly backups for extra safety.

---

## Summary

**Same Steps for Every School: YES! ✅**

1. Clone template
2. Update data files
3. Add images
4. Deploy to Vercel
5. Configure domain

**Time per school:** 1.5-2.5 hours
**Cost per school:** ~$1/month (domain only)
**Revenue potential:** $500-1,500 setup + $50-100/month maintenance

---

**You now have a scalable, repeatable process for deploying this website to unlimited schools! 🚀**
