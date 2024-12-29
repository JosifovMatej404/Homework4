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

engine = create_engine(DATABASE_URL)
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
        company_data = session.query(CompanyData).filter(CompanyData.code == code).all()
        #ompany_data.sort(key=lambda x: datetime.strptime(x.date.replace(".","-") or datetime.min, '%d-%m-%Y'))
        return company_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()

def get_last_update_for_all_companies():
    """
        Retrieves the last update for each Company in the database as a list of tuples.
        Each tuple contains (code, last_update).
    """
    session = SessionLocal()
    try:
        companies = session.query(Company.code, Company.last_update).all()
        return companies
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()


def get_companies_by_code(code: str):
    """
        Retrieves all Company objects with the specified code.
        Returns a list of Company objects.
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

def update_last_update_by_code(code: str, new_last_update: str):
    """
        Updates the last_update field for a Company record with the specified code.

        Args:
            code (str): The company code to identify the record.
            new_last_update (datetime): The new value for the last_update field.
    """
    session = SessionLocal()
    try:
        company = session.query(Company).filter(Company.code == code).first()
        if not company:
            print(f"No company found with code: {code}")
            return False

        company.last_update = new_last_update
        session.commit()
        print(f"Updated last_update for company with code {code}.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_companies_by_code(code: str):
    """
        Deletes all Company objects with the specified code from the database.

        Args:
            code (str): The company code to identify the records to be deleted.

        Returns:
            bool: True if deletion is successful, False otherwise.
    """
    session = SessionLocal()
    try:
        # Find and delete all companies with the specified code
        deleted_count = session.query(CompanyData).filter(Company.code == code).delete()
        session.commit()

        if deleted_count > 0:
            print(f"Successfully deleted {deleted_count} record(s) with code: {code}.")
            return True
        else:
            print(f"No records found with code: {code}.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def delete_data_for_unfinished_companies():
    """
    Deletes all records in the CompanyData table for companies
    that have not finished loading (e.g., last_update is NULL).

    Returns:
        bool: True if deletion is successful, False otherwise.
    """
    session = SessionLocal()
    try:
        # Identify companies that haven't finished loading
        unfinished_companies = session.query(Company).filter(Company.last_update == 'None').all()

        if not unfinished_companies:
            print("No unfinished companies found.")
            return False

        # Delete all CompanyData for these companies
        codes_to_delete = [company.code for company in unfinished_companies]
        deleted_count = session.query(CompanyData).filter(CompanyData.code.in_(codes_to_delete)).delete(synchronize_session=False)
        session.commit()

        print(f"Successfully deleted {deleted_count} records for unfinished companies.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return False
    finally:
        session.close()

