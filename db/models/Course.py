from db.admin_database import Base
from sqlalchemy import String, Integer, Column, Text, Date, Boolean

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key = True, unique = True, nullable = False)
    name = Column(String(55), nullable = False)
    description = Column(Text)
    requirements = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    num_trainees = Column(Integer)
    diffculty = Column(String(15))
    created_by_id = Column(Integer, nullable = False)
    status = Column(Boolean)