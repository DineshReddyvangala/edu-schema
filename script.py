# script.py

import mysql.connector
from mysql.connector import Error
import json

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='EduSchema',  # Replace with your database name
            user='root',  # Replace with your username
            password='Dinesh123'  # Replace with your password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection:
        connection.close()

def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        print(f"Error executing query: {e}")
        return False

def fetch_data(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records
    except Error as e:
        print(f"Error fetching data: {e}")
        return None

def log_deletion(entity_type, entity_id):
    connection = create_connection()
    if connection:
        query = "INSERT INTO deleted_entities (entity_type, entity_id, deleted_at) VALUES (%s, %s, NOW())"
        execute_query(connection, query, (entity_type, entity_id))
        close_connection(connection)
