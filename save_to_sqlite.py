from datetime import datetime
import sqlite3

DB_NAME = "predictions.sqlite"


def init_sqlite():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_name TEXT,
                med_inc REAL,
                house_age REAL,
                ave_rooms REAL,
                ave_bedrms REAL,
                population REAL,
                ave_occup REAL,
                latitude REAL,
                longitude REAL,
                predicted_price REAL
            )
        """)
    conn.commit()
    conn.close()


def save_to_sqlite(model_name, input_vals, price):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO history (
        timestamp, model_name, med_inc, house_age, ave_rooms, ave_bedrms, population, ave_occup, latitude, longitude, predicted_price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (current_time, model_name, *input_vals, price)
                       )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"Помилка: {e}")
