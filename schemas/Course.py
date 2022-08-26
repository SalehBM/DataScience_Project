from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel

class Course(BaseModel):
    id: Optional[int]
    name: str
    description: str
    requirements: str
    start_date: date
    end_date: date = date.today() + timedelta(days = 3) # By default
    num_trainees: int = 25
    diffculty: str = "Beginner"
    created_by_id: int
    status: bool = True

    class Config:
        orm_mode= True

class CourseCreate(BaseModel):
    name: str
    description: str
    requirements: str
    start_date: date
    num_trainees: int = 25
    diffculty: str = "Beginner"
    end_date: date = date.today() + timedelta(days = 3) # By default
    status: bool = True
    
    class Config:
        orm_mode= True
