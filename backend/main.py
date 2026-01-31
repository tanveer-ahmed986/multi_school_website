"""
Multi-School Platform Backend
FastAPI application with comprehensive demo data and image serving
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from datetime import datetime, timedelta

# Create FastAPI app
app = FastAPI(
    title="Multi-School Platform API",
    description="API for managing multi-tenant school websites",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for images
app.mount("/images", StaticFiles(directory="../images"), name="images")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "multi-school-backend",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Multi-School Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "images": "/images"
    }

# Public school endpoint
@app.get("/public/school")
async def get_public_school():
    return {
        "id": "demo-school-id",
        "school_name": "Greenfield International School",
        "subdomain": "greenfield",
        "tagline": "Excellence in Education Since 1985",
        "logo_url": "http://localhost:8000/images/school%20logo.png",
        "banner_url": "http://localhost:8000/images/School%20banner.png",
        "primary_color": "#0A3D62",
        "secondary_color": "#EAF2F8",
        "contact_email": "info@greenfield.edu",
        "contact_phone": "(555) 123-4567",
        "address": "123 Education Avenue, Knowledge City, ST 12345",
        "founded_year": 1985,
        "student_count": 1250,
        "faculty_count": 85,
        "facilities": ["Smart Classrooms", "Science Labs", "Sports Complex", "Library", "Auditorium"],
        "principal_name": "Dr. Emily Richardson",
        "principal_photo": "http://localhost:8000/images/principal%20image.png",
        "principal_message": "Welcome to Greenfield International School! For over three decades, we have been committed to nurturing young minds and fostering a culture of academic excellence, creativity, and social responsibility. Our dedicated faculty and state-of-the-art facilities provide students with an environment where they can thrive and reach their full potential."
    }

# Faculty endpoint with real images
@app.get("/public/faculty")
async def get_faculty():
    return [
        {
            "id": "1",
            "name": "Dr. Emily Richardson",
            "designation": "Principal",
            "department": "Administration",
            "qualification": "Ph.D. in Education Leadership",
            "experience_years": 25,
            "photo_url": "http://localhost:8000/images/principal%20image.png",
            "email": "emily.richardson@greenfield.edu",
            "phone": "(555) 123-4501",
            "specialization": "Educational Administration",
            "is_visible": True
        },
        {
            "id": "2",
            "name": "Prof. James Anderson",
            "designation": "Head of Mathematics Department",
            "department": "Mathematics",
            "qualification": "M.Sc. Mathematics",
            "experience_years": 18,
            "photo_url": "http://localhost:8000/images/pexels-thirdman-8926648.jpg",
            "email": "james.anderson@greenfield.edu",
            "phone": "(555) 123-4502",
            "specialization": "Advanced Calculus, Statistics",
            "is_visible": True
        },
        {
            "id": "3",
            "name": "Dr. Sarah Mitchell",
            "designation": "Science Teacher",
            "department": "Science",
            "qualification": "Ph.D. in Physics",
            "experience_years": 15,
            "photo_url": "http://localhost:8000/images/pexels-yankrukov-8617515.jpg",
            "email": "sarah.mitchell@greenfield.edu",
            "phone": "(555) 123-4503",
            "specialization": "Physics, Chemistry",
            "is_visible": True
        },
        {
            "id": "4",
            "name": "Michael Chen",
            "designation": "Computer Science Teacher",
            "department": "Technology",
            "qualification": "M.Tech. Computer Science",
            "experience_years": 12,
            "photo_url": "http://localhost:8000/images/pexels-ron-lach-10646607.jpg",
            "email": "michael.chen@greenfield.edu",
            "phone": "(555) 123-4504",
            "specialization": "Programming, Web Development, AI",
            "is_visible": True
        },
        {
            "id": "5",
            "name": "Lisa Thompson",
            "designation": "English Teacher",
            "department": "Languages",
            "qualification": "M.A. English Literature",
            "experience_years": 14,
            "photo_url": "http://localhost:8000/images/pexels-yankrukov-8617759.jpg",
            "email": "lisa.thompson@greenfield.edu",
            "phone": "(555) 123-4505",
            "specialization": "Literature, Creative Writing",
            "is_visible": True
        },
        {
            "id": "6",
            "name": "David Martinez",
            "designation": "Physical Education Teacher",
            "department": "Sports",
            "qualification": "B.P.Ed.",
            "experience_years": 10,
            "photo_url": "http://localhost:8000/images/pexels-ron-lach-10638210.jpg",
            "email": "david.martinez@greenfield.edu",
            "phone": "(555) 123-4506",
            "specialization": "Athletics, Basketball, Fitness",
            "is_visible": True
        }
    ]

# Notices endpoint with comprehensive data
@app.get("/public/notices")
async def get_notices():
    today = datetime.now()
    return [
        {
            "id": "1",
            "title": "🎉 Annual Day Celebration 2026",
            "content": "We are excited to announce our Annual Day celebration on March 15th, 2026. The event will feature cultural performances, award ceremonies, and exhibitions. All parents and students are cordially invited. Venue: School Auditorium. Time: 10:00 AM onwards.",
            "priority": "high",
            "published_date": (today - timedelta(days=10)).isoformat(),
            "expiry_date": (today + timedelta(days=45)).isoformat(),
            "category": "events"
        },
        {
            "id": "2",
            "title": "📚 Mid-Term Examination Schedule Released",
            "content": "The mid-term examination schedule for all classes (1-12) has been released. Examinations will be conducted from February 10th to February 20th, 2026. Students are advised to check the detailed schedule on the school portal and prepare accordingly.",
            "priority": "high",
            "published_date": (today - timedelta(days=5)).isoformat(),
            "expiry_date": (today + timedelta(days=10)).isoformat(),
            "category": "academics"
        },
        {
            "id": "3",
            "title": "👨‍👩‍👧 Parent-Teacher Meeting - February 5th",
            "content": "Monthly parent-teacher meeting scheduled for February 5th, 2026. Parents can discuss their child's progress with respective teachers. Time: 2:00 PM - 5:00 PM. Prior appointment recommended.",
            "priority": "medium",
            "published_date": (today - timedelta(days=3)).isoformat(),
            "expiry_date": (today + timedelta(days=5)).isoformat(),
            "category": "meetings"
        },
        {
            "id": "4",
            "title": "🏆 Inter-School Sports Competition",
            "content": "Our school will be participating in the Inter-School Sports Competition from February 15-17, 2026. Students interested in athletics, basketball, and swimming should register with the Physical Education department by February 3rd.",
            "priority": "medium",
            "published_date": (today - timedelta(days=7)).isoformat(),
            "expiry_date": (today + timedelta(days=15)).isoformat(),
            "category": "sports"
        },
        {
            "id": "5",
            "title": "🔬 Science Fair Registration Open",
            "content": "Registration is now open for the Annual Science Fair 2026. Students from grades 6-12 can participate individually or in teams. Last date for registration: February 10th. Contact the Science Department for guidelines.",
            "priority": "medium",
            "published_date": (today - timedelta(days=2)).isoformat(),
            "expiry_date": (today + timedelta(days=12)).isoformat(),
            "category": "academics"
        },
        {
            "id": "6",
            "title": "📅 School Holiday - Republic Day",
            "content": "School will remain closed on January 26th, 2026 in observance of Republic Day. Regular classes will resume from January 27th.",
            "priority": "low",
            "published_date": (today - timedelta(days=15)).isoformat(),
            "expiry_date": (today - timedelta(days=5)).isoformat(),
            "category": "holidays"
        }
    ]

# Results endpoint
@app.get("/public/results")
async def get_results():
    return [
        {
            "id": "1",
            "academic_year": "2025-26",
            "class_level": "Class 10",
            "exam_type": "Mid-Term Examination",
            "is_published": True,
            "published_date": "2026-01-15T00:00:00",
            "total_students": 125,
            "pass_percentage": 94.5,
            "average_marks": 78.3
        },
        {
            "id": "2",
            "academic_year": "2025-26",
            "class_level": "Class 12",
            "exam_type": "Mid-Term Examination",
            "is_published": True,
            "published_date": "2026-01-15T00:00:00",
            "total_students": 98,
            "pass_percentage": 96.8,
            "average_marks": 82.1
        },
        {
            "id": "3",
            "academic_year": "2025-26",
            "class_level": "Class 9",
            "exam_type": "Mid-Term Examination",
            "is_published": True,
            "published_date": "2026-01-20T00:00:00",
            "total_students": 140,
            "pass_percentage": 91.2,
            "average_marks": 75.8
        },
        {
            "id": "4",
            "academic_year": "2024-25",
            "class_level": "Class 10",
            "exam_type": "Annual Examination",
            "is_published": True,
            "published_date": "2025-05-20T00:00:00",
            "total_students": 118,
            "pass_percentage": 98.3,
            "average_marks": 84.2
        },
        {
            "id": "5",
            "academic_year": "2025-26",
            "class_level": "Class 11",
            "exam_type": "Mid-Term Examination",
            "is_published": True,
            "published_date": "2026-01-18T00:00:00",
            "total_students": 110,
            "pass_percentage": 89.1,
            "average_marks": 76.5
        },
        {
            "id": "6",
            "academic_year": "2025-26",
            "class_level": "Class 8",
            "exam_type": "Mid-Term Examination",
            "is_published": True,
            "published_date": "2026-01-22T00:00:00",
            "total_students": 155,
            "pass_percentage": 92.9,
            "average_marks": 74.2
        }
    ]

# Detailed results endpoint with JSONB student data
@app.get("/public/results/{result_id}/students")
async def get_result_students(result_id: str):
    # Demo JSONB data structure for student results
    demo_data = {
        "1": {  # Class 10 Mid-Term
            "result_id": "1",
            "academic_year": "2025-26",
            "class_level": "Class 10",
            "exam_type": "Mid-Term Examination",
            "students": [
                {
                    "roll_no": "C10-001",
                    "name": "Alice Johnson",
                    "marks": {
                        "english": 85,
                        "mathematics": 92,
                        "science": 88,
                        "social_studies": 90,
                        "hindi": 87
                    },
                    "total": 442,
                    "percentage": 88.4,
                    "grade": "A",
                    "rank": 3
                },
                {
                    "roll_no": "C10-002",
                    "name": "Bob Smith",
                    "marks": {
                        "english": 78,
                        "mathematics": 85,
                        "science": 82,
                        "social_studies": 88,
                        "hindi": 80
                    },
                    "total": 413,
                    "percentage": 82.6,
                    "grade": "A",
                    "rank": 8
                },
                {
                    "roll_no": "C10-003",
                    "name": "Carol Davis",
                    "marks": {
                        "english": 92,
                        "mathematics": 95,
                        "science": 90,
                        "social_studies": 93,
                        "hindi": 91
                    },
                    "total": 461,
                    "percentage": 92.2,
                    "grade": "A+",
                    "rank": 1
                },
                {
                    "roll_no": "C10-004",
                    "name": "David Wilson",
                    "marks": {
                        "english": 70,
                        "mathematics": 75,
                        "science": 72,
                        "social_studies": 78,
                        "hindi": 73
                    },
                    "total": 368,
                    "percentage": 73.6,
                    "grade": "B",
                    "rank": 25
                },
                {
                    "roll_no": "C10-005",
                    "name": "Emma Brown",
                    "marks": {
                        "english": 88,
                        "mathematics": 90,
                        "science": 85,
                        "social_studies": 87,
                        "hindi": 89
                    },
                    "total": 439,
                    "percentage": 87.8,
                    "grade": "A",
                    "rank": 4
                },
                {
                    "roll_no": "C10-006",
                    "name": "Frank Miller",
                    "marks": {
                        "english": 82,
                        "mathematics": 88,
                        "science": 80,
                        "social_studies": 85,
                        "hindi": 84
                    },
                    "total": 419,
                    "percentage": 83.8,
                    "grade": "A",
                    "rank": 7
                },
                {
                    "roll_no": "C10-007",
                    "name": "Grace Taylor",
                    "marks": {
                        "english": 95,
                        "mathematics": 98,
                        "science": 92,
                        "social_studies": 96,
                        "hindi": 94
                    },
                    "total": 475,
                    "percentage": 95.0,
                    "grade": "A+",
                    "rank": 2
                },
                {
                    "roll_no": "C10-008",
                    "name": "Henry Anderson",
                    "marks": {
                        "english": 68,
                        "mathematics": 72,
                        "science": 70,
                        "social_studies": 75,
                        "hindi": 71
                    },
                    "total": 356,
                    "percentage": 71.2,
                    "grade": "B",
                    "rank": 30
                },
                {
                    "roll_no": "C10-009",
                    "name": "Ivy Martinez",
                    "marks": {
                        "english": 90,
                        "mathematics": 93,
                        "science": 88,
                        "social_studies": 91,
                        "hindi": 90
                    },
                    "total": 452,
                    "percentage": 90.4,
                    "grade": "A+",
                    "rank": 5
                },
                {
                    "roll_no": "C10-010",
                    "name": "Jack Thompson",
                    "marks": {
                        "english": 75,
                        "mathematics": 80,
                        "science": 78,
                        "social_studies": 82,
                        "hindi": 77
                    },
                    "total": 392,
                    "percentage": 78.4,
                    "grade": "B+",
                    "rank": 15
                },
                {
                    "roll_no": "C10-011",
                    "name": "Katie Lee",
                    "marks": {
                        "english": 86,
                        "mathematics": 89,
                        "science": 84,
                        "social_studies": 88,
                        "hindi": 85
                    },
                    "total": 432,
                    "percentage": 86.4,
                    "grade": "A",
                    "rank": 6
                },
                {
                    "roll_no": "C10-012",
                    "name": "Leo Garcia",
                    "marks": {
                        "english": 72,
                        "mathematics": 78,
                        "science": 75,
                        "social_studies": 80,
                        "hindi": 74
                    },
                    "total": 379,
                    "percentage": 75.8,
                    "grade": "B+",
                    "rank": 20
                }
            ]
        },
        "2": {  # Class 12 Mid-Term
            "result_id": "2",
            "academic_year": "2025-26",
            "class_level": "Class 12",
            "exam_type": "Mid-Term Examination",
            "students": [
                {
                    "roll_no": "C12-001",
                    "name": "Maya Patel",
                    "marks": {
                        "english": 88,
                        "mathematics": 94,
                        "physics": 90,
                        "chemistry": 92,
                        "computer_science": 95
                    },
                    "total": 459,
                    "percentage": 91.8,
                    "grade": "A+",
                    "rank": 2
                },
                {
                    "roll_no": "C12-002",
                    "name": "Noah Williams",
                    "marks": {
                        "english": 82,
                        "mathematics": 87,
                        "physics": 85,
                        "chemistry": 89,
                        "computer_science": 90
                    },
                    "total": 433,
                    "percentage": 86.6,
                    "grade": "A",
                    "rank": 5
                },
                {
                    "roll_no": "C12-003",
                    "name": "Olivia Chen",
                    "marks": {
                        "english": 95,
                        "mathematics": 97,
                        "physics": 93,
                        "chemistry": 96,
                        "computer_science": 98
                    },
                    "total": 479,
                    "percentage": 95.8,
                    "grade": "A+",
                    "rank": 1
                },
                {
                    "roll_no": "C12-004",
                    "name": "Peter Kumar",
                    "marks": {
                        "english": 75,
                        "mathematics": 80,
                        "physics": 78,
                        "chemistry": 82,
                        "computer_science": 85
                    },
                    "total": 400,
                    "percentage": 80.0,
                    "grade": "A",
                    "rank": 10
                },
                {
                    "roll_no": "C12-005",
                    "name": "Quinn Roberts",
                    "marks": {
                        "english": 90,
                        "mathematics": 92,
                        "physics": 88,
                        "chemistry": 91,
                        "computer_science": 93
                    },
                    "total": 454,
                    "percentage": 90.8,
                    "grade": "A+",
                    "rank": 3
                },
                {
                    "roll_no": "C12-006",
                    "name": "Rachel Singh",
                    "marks": {
                        "english": 86,
                        "mathematics": 89,
                        "physics": 87,
                        "chemistry": 90,
                        "computer_science": 92
                    },
                    "total": 444,
                    "percentage": 88.8,
                    "grade": "A",
                    "rank": 4
                },
                {
                    "roll_no": "C12-007",
                    "name": "Samuel Lee",
                    "marks": {
                        "english": 78,
                        "mathematics": 83,
                        "physics": 80,
                        "chemistry": 85,
                        "computer_science": 87
                    },
                    "total": 413,
                    "percentage": 82.6,
                    "grade": "A",
                    "rank": 8
                },
                {
                    "roll_no": "C12-008",
                    "name": "Tara Gupta",
                    "marks": {
                        "english": 84,
                        "mathematics": 88,
                        "physics": 86,
                        "chemistry": 89,
                        "computer_science": 91
                    },
                    "total": 438,
                    "percentage": 87.6,
                    "grade": "A",
                    "rank": 6
                }
            ]
        },
        "3": {  # Class 9 Mid-Term
            "result_id": "3",
            "academic_year": "2025-26",
            "class_level": "Class 9",
            "exam_type": "Mid-Term Examination",
            "students": [
                {
                    "roll_no": "C09-001",
                    "name": "Uma Sharma",
                    "marks": {
                        "english": 80,
                        "mathematics": 85,
                        "science": 82,
                        "social_studies": 84,
                        "hindi": 81
                    },
                    "total": 412,
                    "percentage": 82.4,
                    "grade": "A",
                    "rank": 5
                },
                {
                    "roll_no": "C09-002",
                    "name": "Victor Zhang",
                    "marks": {
                        "english": 88,
                        "mathematics": 92,
                        "science": 89,
                        "social_studies": 90,
                        "hindi": 87
                    },
                    "total": 446,
                    "percentage": 89.2,
                    "grade": "A",
                    "rank": 2
                },
                {
                    "roll_no": "C09-003",
                    "name": "Wendy Brown",
                    "marks": {
                        "english": 75,
                        "mathematics": 78,
                        "science": 76,
                        "social_studies": 80,
                        "hindi": 74
                    },
                    "total": 383,
                    "percentage": 76.6,
                    "grade": "B+",
                    "rank": 12
                },
                {
                    "roll_no": "C09-004",
                    "name": "Xavier Lopez",
                    "marks": {
                        "english": 92,
                        "mathematics": 95,
                        "science": 91,
                        "social_studies": 94,
                        "hindi": 90
                    },
                    "total": 462,
                    "percentage": 92.4,
                    "grade": "A+",
                    "rank": 1
                },
                {
                    "roll_no": "C09-005",
                    "name": "Yara Ahmed",
                    "marks": {
                        "english": 84,
                        "mathematics": 88,
                        "science": 85,
                        "social_studies": 87,
                        "hindi": 83
                    },
                    "total": 427,
                    "percentage": 85.4,
                    "grade": "A",
                    "rank": 4
                },
                {
                    "roll_no": "C09-006",
                    "name": "Zack Martin",
                    "marks": {
                        "english": 86,
                        "mathematics": 90,
                        "science": 87,
                        "social_studies": 89,
                        "hindi": 85
                    },
                    "total": 437,
                    "percentage": 87.4,
                    "grade": "A",
                    "rank": 3
                }
            ]
        }
    }

    if result_id in demo_data:
        return demo_data[result_id]
    else:
        return {
            "result_id": result_id,
            "students": [],
            "message": "No detailed data available for this result"
        }

# Gallery endpoint with real images
@app.get("/public/gallery")
async def get_gallery():
    return [
        {
            "id": "1",
            "title": "Science Laboratory - Modern Facilities",
            "description": "Our state-of-the-art science laboratory equipped with latest instruments",
            "category": "infrastructure",
            "image_url": "http://localhost:8000/images/pexels-yankrukov-8617515.jpg",
            "uploaded_at": "2025-12-15T00:00:00"
        },
        {
            "id": "2",
            "title": "Interactive Classroom Session",
            "description": "Students engaged in interactive learning with modern teaching methods",
            "category": "academics",
            "image_url": "http://localhost:8000/images/pexels-yankrukov-8617759.jpg",
            "uploaded_at": "2026-01-10T00:00:00"
        },
        {
            "id": "3",
            "title": "Computer Lab - Technology Education",
            "description": "Advanced computer lab with latest hardware and software for practical learning",
            "category": "infrastructure",
            "image_url": "http://localhost:8000/images/pexels-ron-lach-10646607.jpg",
            "uploaded_at": "2025-11-20T00:00:00"
        },
        {
            "id": "4",
            "title": "Mathematics Workshop",
            "description": "Interactive mathematics workshop demonstrating practical applications",
            "category": "academics",
            "image_url": "http://localhost:8000/images/pexels-thirdman-8926648.jpg",
            "uploaded_at": "2025-12-05T00:00:00"
        },
        {
            "id": "5",
            "title": "Sports Day 2025",
            "description": "Annual sports day celebration with various athletic events",
            "category": "events",
            "image_url": "http://localhost:8000/images/pexels-ron-lach-10638210.jpg",
            "uploaded_at": "2025-12-20T00:00:00"
        },
        {
            "id": "6",
            "title": "Science Exhibition",
            "description": "Students presenting innovative science projects at the annual exhibition",
            "category": "events",
            "image_url": "http://localhost:8000/images/pexels-yankrukov-8613100.jpg",
            "uploaded_at": "2026-01-25T00:00:00"
        }
    ]

# Principal endpoint
@app.get("/public/principal")
async def get_principal():
    return {
        "principal_name": "Dr. Emily Richardson",
        "designation": "Principal",
        "qualification": "Ph.D. in Education Leadership",
        "experience_years": 25,
        "photo_url": "http://localhost:8000/images/principal%20image%20with%20message.png",
        "message": "Dear Students, Parents, and Staff,\n\nWelcome to Greenfield International School! For over three decades, we have been committed to nurturing young minds and fostering a culture of academic excellence, creativity, and social responsibility.\n\nOur dedicated faculty and state-of-the-art facilities provide students with an environment where they can thrive and reach their full potential. We believe in holistic education that develops not just academic skills, but also character, leadership, and global citizenship.\n\nAt Greenfield, we prepare our students for the challenges of tomorrow while instilling timeless values of integrity, compassion, and perseverance. Together, we build a foundation for lifelong learning and success.\n\nWarm regards,\nDr. Emily Richardson\nPrincipal"
    }

# Statistics endpoint
@app.get("/public/statistics")
async def get_statistics():
    return {
        "total_students": 1250,
        "total_faculty": 85,
        "total_staff": 45,
        "classes_offered": 12,
        "average_class_size": 28,
        "student_teacher_ratio": "15:1",
        "years_of_excellence": 38,
        "campus_area_acres": 15,
        "achievements": [
            {"title": "Best School Award 2025", "authority": "State Education Board"},
            {"title": "Excellence in Science", "authority": "National Science Foundation"},
            {"title": "Sports Champions", "authority": "Inter-School Sports Association"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
