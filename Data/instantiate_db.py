import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Define the Base for ORM models
from Models.models_base import Base


# Define the database file path

DB_PATH = 'database.db'
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)  # Set echo=False in production

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def get_connection():
    """
    Provides a database session connection.
    Use this function to interact with the database.

    Example usage:
        with get_connection() as session:
            # Perform database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    with engine.connect() as connection:
        # Step 1: Create a new table with the foreign key
        connection.execute(
            text("""
            CREATE TABLE Companies (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
             last_update TEXT DEFAULT 'NULL'
        );  
            """)
        )

        # Step 2: Copy data from the old table to the new table
        connection.execute(
            text("""CREATE TABLE company_data (
    code TEXT PRIMARY KEY,
    date TEXT,
    last_trade_price DECIMAL,
    max_price DECIMAL,
    min_price DECIMAL,
    avg_price DECIMAL,
    percent_change DECIMAL,
    volume DECIMAL,
    turnover_best_denars DECIMAL,
    total_turnover_denars DECIMAL 
    
    );
    """
    ))


        connection.execute(text("""ALTER TABLE Companies
            ADD CONSTRAINT Company.code FOREIGN KEY (code) REFERENCES AllDataCompanies.code(code));"""))


        # Step 4: Rename the new table




if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # inspector = inspect(engine)
    # tables = inspector.get_table_names()
    # print(f"Database URL: {DATABASE_URL}")