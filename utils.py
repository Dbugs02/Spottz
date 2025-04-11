import psycopg2
import datetime as dt
from dotenv import load_dotenv
import os


 
def conexion():
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    try:
        conn=psycopg2.connect(user=DB_USER,host=DB_HOST,port=DB_PORT,database=DB_NAME,password=DB_PASSWORD)
        cursor=conn.cursor()
        print("Connection successful, cursor created!")
        return conn, cursor
    except Exception as e:
        print(f"Error{e}")
        return None,None
       


def entry_car(car_plate,cursor,conn):
    entry_date=dt.now().time()
    entry_time=dt.now().date()
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS active_parking (CAR_PLATE VARCHAR(20) PRIMARY KEY,ENTRY_DATE DATE,ENTRY_TIME TIME);""")
        cursor.execute("INSERT INTO active_parking(CAR_PLATE,ENTRY_DATE,ENTRY_TIME) VALUES (%s,%s,%s);",(car_plate,entry_date,entry_time))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error:{e}")
        return False


    
