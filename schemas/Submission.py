from datetime import date
from typing import Optional
from pydantic import BaseModel

class SubmissionBase(BaseModel):
    id: Optional[int]
    course_id: int
    name: str
    email: str
    age: int
    phone: str
    speciality: int
    occupation: int
    linkedin: str
    github: str
    score: float
    Approved: bool = False
    date: date

    class Config:
        orm_mode= True

class SubmissionCreate(BaseModel):
    course_id: int
    name: str
    email: str
    age: int
    phone: str
    speciality: int
    occupation: int
    linkedin: str
    github: str
    score: float
    Approved: bool = False

class SubmissionRow(BaseModel):
    id: int
    course_name: str
    name: str
    email: str
    phone: str
    linkedin: str
    github: str
    score: float
    Approved: str = "No"
    date: date