from sqlalchemy import create_engine

def connect_db():
    connection_string = "postgresql://postgres:Sathya@12@localhost:5432/GreenDeals"
    return create_engine(connection_string)
