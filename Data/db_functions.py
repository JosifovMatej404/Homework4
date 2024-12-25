# Data/CompanyData_methods.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data.instantiate_db import  get_connection
from Models.CompanyData import CompanyData
from Models.Company import Company
from datetime import datetime
from sqlalchemy import text

import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Method to insert CompanyData into the database
def insert_company_data(code: str, date: str, last_trade_price: float,
                        max_price: float, min_price: float, avg_price: float,
                        percent_change: float,volume:float,turnover_best_denars:float,
                        total_turnover_denars:float):
    """
        Inserts a record from the company data in the database.

        Takes all the arguments from the CompanyData object and creates the object
    """

    session = SessionLocal()
    new_company_data = CompanyData(
        code=code,
        date=date,
        last_trade_price=last_trade_price,
        max_price=max_price,
        min_price=min_price,
        avg_price=avg_price,
        percent_change=percent_change,
        volume = volume,
        turnover_best_denars = turnover_best_denars,
        total_turnover_denars = total_turnover_denars
    )

    try:
        session.add(new_company_data)
        session.commit()
        print(f"Added the company record with code {code} successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return None
    finally:
        session.close()


def insert_company_data_object(company_record :CompanyData):
    """
        Inserts a record from the company data in the database.

        Takes an object from the class CompanyData
    """

    session = SessionLocal()

    try:
        session.add(company_record)
        session.commit()
        print(f"Added the company record with code {company_record.code} successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return None
    finally:
        session.close()

def add_company(code, last_update):
    """
        Takes 2 arguments as strings to create the Company object
        Inserts a company into the database.
    """
    session = SessionLocal()
    try:
        new_company = Company(code= code, last_update=last_update)

        session.add(new_company)
        session.commit()

        print(f"Company with code: {code} added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()



def add_company_object(company : Company):
    """
        Takes Company object as argument
        Inserts a company into the database.
    """
    session = SessionLocal()
    try:

        session.add(company)
        session.commit()

        print(f"Company with code: {company.code} added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def get_company_data_by_code(code: str):
    """
        Takes a string as an argument and retrives all the company records with the company code
        Retrieve all companies from the database with the specified code.
        """
    session = SessionLocal()
    try:
        companies = session.query(Company).filter(Company.code == code).all()
        return companies
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()





