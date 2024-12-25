from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,DECIMAL

from Models.models_base import Base
class CompanyData(Base):
    __tablename__ = 'AllCompaniesData'
    # Define columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, ForeignKey("Companies.code"))
    date = Column(String)
    last_trade_price = Column(DECIMAL)
    max_price = Column(DECIMAL)
    min_price = Column(DECIMAL)
    avg_price = Column(DECIMAL)
    percent_change = Column(DECIMAL)
    volume = Column(DECIMAL)
    turnover_best_denars = Column(DECIMAL)
    total_turnover_denars = Column(DECIMAL)

    # Define the relationship back to Company
    company = relationship("Company", back_populates="company_data")
    def __init__(self,code,date,last_trade_price,max_price,min_price,avg_price,percent_change,volume,turnover_best_denars,total_turnover_denars):
        self.code = code
        self.date = date
        self.last_trade_price = last_trade_price
        self.max_price= max_price
        self.min_price = min_price
        self.avg_price = avg_price
        self.percent_change = percent_change
        self.volume = volume
        self.turnover_best_denars = turnover_best_denars
        self.total_turnover_denars = total_turnover_denars