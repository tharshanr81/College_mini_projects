import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # or your real password
        database="tharshan"
    )
    print(" Database connected")
    conn.close()
except mysql.connector.Error as e:
    print(" MySQL error:", e)
