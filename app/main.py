import time
import mysql.connector

from fastapi import FastAPI
from app.routes import posts, users

app = FastAPI()

while True:
    try:
        print("INFO:\tConnecting to database...")
        connection = mysql.connector.connect(user="root",
                                             password="9Xma$kb2LY",
                                             host="localhost",
                                             database="fastapi"
                                             )
        cursor = connection.cursor(dictionary=True)
        print("INFO:\tDatabase connection successfu!")
        break
    except Exception as error:
        print(f"ERROR:\t{error}")
        time.sleep(3)


app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
