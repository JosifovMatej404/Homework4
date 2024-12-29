from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey

from Models.models_base import Base

class Company(Base):

    __tablename__ = 'Companies'

    code = Column(String, primary_key=True)
    last_update = Column(String, default="NULL")

    company_data = relationship("CompanyData", back_populates="company", uselist=False)
    def __init__(self,code,last_update):
        self.code = code
        self.last_update = last_update

    def __repr__(self):
        return f"Company {self.code}"