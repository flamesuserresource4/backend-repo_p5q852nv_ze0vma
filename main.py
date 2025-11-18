import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Department, Course, News, Inquiry

app = FastAPI(title="University API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "University API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# ---------- Public content endpoints ----------

@app.get("/api/departments", response_model=List[Department])
def list_departments(limit: int = 50):
    docs = get_documents("department", {}, limit)
    # Convert ObjectId to string-safe dicts
    return [
        Department(**{k: (str(v) if k == "_id" else v) for k, v in doc.items() if k != "_id"})
        for doc in docs
    ]

@app.get("/api/courses", response_model=List[Course])
def list_courses(limit: int = 100, department: Optional[str] = None):
    filt = {"department_id": department} if department else {}
    docs = get_documents("course", filt, limit)
    return [
        Course(**{k: (str(v) if k == "_id" else v) for k, v in doc.items() if k != "_id"})
        for doc in docs
    ]

@app.get("/api/news", response_model=List[News])
def list_news(limit: int = 10):
    docs = get_documents("news", {}, limit)
    return [
        News(**{k: (str(v) if k == "_id" else v) for k, v in doc.items() if k != "_id"})
        for doc in docs
    ]

class InquiryIn(BaseModel):
    name: str
    email: str
    message: str
    topic: Optional[str] = None

@app.post("/api/inquiries")
def create_inquiry(payload: InquiryIn):
    try:
        _id = create_document("inquiry", payload.model_dump())
        return {"status": "ok", "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seed minimal demo content if collections are empty (for preview UX)
@app.get("/api/seed")
def seed_data():
    inserted = {"departments": 0, "courses": 0, "news": 0}
    if db is None:
        return {"status": "no-db"}
    if db["department"].count_documents({}) == 0:
        deps = [
            {"name": "Computer Science", "description": "CS, AI and Systems", "chair": "Dr. Ada"},
            {"name": "Business", "description": "Management and Finance", "chair": "Dr. Drucker"},
            {"name": "Design", "description": "UX, Visual and Product", "chair": "Prof. Rams"},
        ]
        for d in deps:
            create_document("department", d)
            inserted["departments"] += 1
    if db["course"].count_documents({}) == 0:
        courses = [
            {"code": "CS101", "title": "Intro to CS", "description": "Fundamentals of computing", "department_id": "Computer Science", "credits": 3, "level": "Undergraduate"},
            {"code": "BUS201", "title": "Marketing", "description": "Principles of marketing", "department_id": "Business", "credits": 3, "level": "Undergraduate"},
        ]
        for c in courses:
            create_document("course", c)
            inserted["courses"] += 1
    if db["news"].count_documents({}) == 0:
        items = [
            {"title": "Welcome to Our University", "summary": "Orientation starts next week.", "content": "Join us for a week of events.", "image_url": None},
            {"title": "New AI Lab Opened", "summary": "Cutting-edge research facilities.", "content": "The CS dept opens new lab.", "image_url": None},
        ]
        for n in items:
            create_document("news", n)
            inserted["news"] += 1
    return {"status": "seeded", "inserted": inserted}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
