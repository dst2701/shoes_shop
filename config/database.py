"""
Cấu hình kết nối database
"""
import mysql.connector
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="tungds270105",
        database="shopgiaydep09102025"
    )
