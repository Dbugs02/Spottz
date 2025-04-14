import psycopg2
import datetime as dt
from dotenv import load_dotenv
import os



def conexion():
    load_dotenv(dotenv_path="credenciais.env")
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
        print(f"Error in connexion {e}")
        return None,None
       


def entry_car(car_plate,cursor,conn):
    entry_datetime=dt.datetime.now()
    
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS active_parking (
        "CAR_PLATE" VARCHAR(20) PRIMARY KEY,
        "ENTRY_DATETIME" TIMESTAMP,
        "EXIT_DATETIME" TIMESTAMP,
        "TOTAL_VALUE" NUMERIC (10,2));""")

        cursor.execute("INSERT INTO active_parking(CAR_PLATE,ENTRY_DATETIME) VALUES (%s,%s);",(car_plate,entry_datetime))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error in entry_car:{e}")
        return False

#Função responsavel por calcular valor total, adicionar no historico e retornar verdadeiro pra abrir a cancela 
def exit_car(car_plate,cursor,conn):
    exit_datetime=dt.datetime.now()
    cursor.execute("SELECT ENTRY_DATETIME FROM active_parking WHERE CAR_PLATE=%s;",(car_plate))
    entry_datetime=cursor.fetchone()[0]
    gap_time=exit_datetime-entry_datetime
    hour=gap_time.total_seconds()/3600
    hour_value=2
    total_value=hour*hour_value

    try:
        cursor.execute("UPDATE active_parking SET EXIT_DATETIME=%s, TOTAL_VALUE=%s WHERE CAR_PLATE=%s;", (exit_datetime, total_value, car_plate))
        conn.commit()
        cursor.close()
        conn.close()
        return True,total_value
    except Exception as e:
        print(f"Error in exit_car:{e}")
        return False,None


