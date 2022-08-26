from db.admin_database import Base
from sqlalchemy import Boolean, Text, Integer, Column, Date, Float

class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key = True, unique = True, nullable = False)
    course_id = Column(Integer, nullable = False)
    name = Column(Text, nullable = False)
    email = Column(Text, nullable = False)
    age = Column(Integer)
    phone = Column(Text)
    speciality = Column(Integer)
    occupation = Column(Integer)
    linkedin = Column(Text)
    github = Column(Text)
    score = Column(Float)
    Approved = Column(Boolean)
    date = Column(Date)