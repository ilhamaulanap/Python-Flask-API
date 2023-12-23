import os
from datetime import datetime, timezone
import psycopg2
from flask import Flask, request
from dotenv import load_dotenv

from sql.query import *



load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

@app.post("/api/room")
def create_room():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID,(name,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {name} created"}, 201

@app.post("/api/temperature")
def add_temp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room"]
    try:
        date = datetime.strptime(data["date"], '%Y-%m-%d %H:%M:%S')
    except KeyError:
        date = datetime.now(timezone.utc)
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TEMPS_TABLE)
            cursor.execute(INSERT_TEMP, (room_id, temperature, date))
    return {"message":"Temperaturee added."}, 201

@app.get("/api/average")
def get_global_avg():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()[0]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()[0]
    return {"average": round(average,2), "days":days}