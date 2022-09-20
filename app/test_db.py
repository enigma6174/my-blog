import mysql.connector

TABLE_NAME = "fastapi_users"

try:
    connection = mysql.connector.connect(user="root",
                                         password="9Xma$kb2LY",
                                         host="127.0.0.1",
                                         database="fastapi"
                                         )
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM {TABLE_NAME};"
    cursor.execute(query)

    for row in cursor:
        print(row)
except Exception as e:
    print(f"[ERR] {e}")
