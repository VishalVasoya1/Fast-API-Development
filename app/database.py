'''
    Create a connection of orm to database.
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import psycopg2 
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}" % quote_plus(f"{settings.database_password}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgre:{}@localhost/fastapi".format("Vishal12345@@")
# conn = psycopg2.connect(host='localhost',database='fast-api',user='postgres',password='Vishal12345@@', cursor_factory= RealDictCursor)
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

# dependency
# session object that is reponsible for talking with the object. create a this function where we actually get connection or session to a database. every time we get a request we can get a session then after the request is done then close it connection.
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fast-api',user='postgres',password='Vishal12345@@', cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print('Database Connection was succesful!')
#         break
#     except Exception as e:
#         print(e)
