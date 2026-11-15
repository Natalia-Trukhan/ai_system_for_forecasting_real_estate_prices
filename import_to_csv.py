import sqlite3
from tkinter import messagebox

import pandas as pd

from save_to_sqlite import DB_NAME


def import_to_csv():
    try:
        conn = sqlite3.connect(DB_NAME)
        df_history = pd.read_sql_query("SELECT * FROM history", conn)

        conn.close()

        if df_history.empty:
            messagebox.showwarning("Увага", "Історія прогнозів порожня! Спочатку зробіть хоча б один прогноз.")
            return

        filename = "predictions_history.csv"
        df_history.to_csv(filename, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Успіх", f"Історію прогнозів успішно експортовано у файл:\n{filename}")
    except Exception as e:
        messagebox.showerror("Помилка експорту", f"Не вдалося зберегти CSV:\n{e}")
