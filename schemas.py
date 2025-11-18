"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (leave for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# University app schemas

class Department(BaseModel):
    name: str = Field(..., description="Department name")
    description: Optional[str] = Field(None, description="Short description of the department")
    chair: Optional[str] = Field(None, description="Department chair")

class Course(BaseModel):
    code: str = Field(..., description="Course code, e.g., CS101")
    title: str = Field(..., description="Course title")
    description: Optional[str] = Field(None, description="Course description")
    department_id: Optional[str] = Field(None, description="Related department id as string")
    credits: int = Field(3, ge=0, le=10, description="Credit hours")
    level: str = Field("Undergraduate", description="Undergraduate or Graduate")

class News(BaseModel):
    title: str = Field(..., description="News headline")
    summary: Optional[str] = Field(None, description="Short summary")
    content: Optional[str] = Field(None, description="Full content")
    image_url: Optional[str] = Field(None, description="Optional image URL")

class Inquiry(BaseModel):
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., description="Message body")
    topic: Optional[str] = Field(None, description="Topic selection like Admissions, Programs, Support")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
