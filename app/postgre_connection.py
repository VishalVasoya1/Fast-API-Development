import psycopg2 
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fast-api',user='postgres',password='Vishal12345@@', cursor_factory= RealDictCursor)

        cursor = conn.cursor()
        print('Database Connection was succesful!')
        break
    except Exception as e:
        print(e)
        time.sleep(2)
