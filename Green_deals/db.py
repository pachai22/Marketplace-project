from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def connect_db():
    connection_string = "postgresql://postgres:Sathya@12@localhost:5432/GreenDeals"
    db= create_engine(connection_string)
    Session = sessionmaker(bind=db)
    session = Session()
    return session
print("Database connected successfully")
