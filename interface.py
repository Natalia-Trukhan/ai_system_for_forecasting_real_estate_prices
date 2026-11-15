import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd

from import_to_csv import import_to_csv
from make_plots import make_plots
from save_to_sqlite import save_to_sqlite, init_sqlite
from model_train import x, model_1, model_2

init_sqlite()
print("\nЗапускаємо графічний інтерфейс...")

root = tk.Tk()
root.title("Прогноз цін на нерухомість (Каліфорнія)")
root.geometry("460x660")
root.configure(background="#f0f0f0")

style_but = ttk.Style()

style_but.configure(
    'TCombobox',
    font=('Carlito', 11),
    fieldbackground="white",
    background="white",
)

style_but.map(
    'TCombobox',
    fielbackground=[('readonly', '#e3e2e1')],
)

tittle_label = tk.Label(root, text="Калькулятор цін на нерухомість", font=('Carlito', 14, 'bold'), bg="#f0f0f0",
                        fg="black")
tittle_label.pack(pady=10)

frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(pady=5)

default_value = x.mean().to_dict()

entries = {}

for i, (name_field, value) in enumerate(default_value.items()):
    lbl = tk.Label(frame_inputs, text=name_field, font=('Carlito', 10, 'bold'), bg="#f0f0f0", fg="black")
    lbl.grid(row=i, column=0, padx=10, pady=5)

    ent = tk.Entry(frame_inputs, font=('Arial', 10), width=15)
    ent.insert(0, f'{value:.2f}')
    ent.grid(row=i, column=1, padx=10, pady=5)
    entries[name_field] = ent

model_label = tk.Label(root, text='Оберіть модель:', font=('Carlito', 14, 'bold'), bg="#f0f0f0", fg="black")
model_label.pack(pady=5)

model_choice = ttk.Combobox(root, values=["Лінійна регресія (Linear Regression)", "Дерево рішень (Decision Tree)"],
                            width=50, state='readonly')
model_choice.current(0)
model_choice.pack(pady=10)


def make_predict():
    try:
        input_data = []
        for feature in default_value.keys():
            val = float(entries[feature].get())
            input_data.append(val)

        x_new = pd.DataFrame([input_data], columns=default_value.keys())

        selected_model = model_choice.get()
        if "Лінійна" in selected_model:
            prediction = model_1.predict(x_new)[0]
        else:
            prediction = model_2.predict(x_new)[0]

        real_price = prediction * 100000
        save_to_sqlite(selected_model, input_data, real_price)

        result_label.config(text=f"Прогнозована вартість:\n${real_price:,.2f}", fg="green")
    except ValueError:
        messagebox.showerror("Помилка", "Будь ласка, введіть числові значення у всі поля!")


# Кнопки дій
predict_btn = tk.Button(root, text="1. Отримати прогноз (і зберегти в БД)",
                        font=("Carlito", 11, "bold"), bg="#436942", fg="#e3e2e1", width=35, pady=6,
                        command=make_predict)
predict_btn.pack(pady=(40, 8))

plot_btn = tk.Button(root, text="2. Побудувати графіки оцінки моделі",
                     font=("Carlito", 11, "bold"), bg="#415a6e", fg="#e3e2e1", width=35, pady=6,
                     command=lambda: make_plots(model_choice))
plot_btn.pack(pady=8)

export_btn = tk.Button(root, text="3. Експортувати історію в CSV",
                       font=("Carlito", 11, "bold"), bg="#6b4d85", fg="#e3e2e1", width=35, pady=6,
                       command=import_to_csv)
export_btn.pack(pady=8)

# Мітка для виведення результату
result_label = tk.Label(root, text="Прогноз з'явиться тут", font=("Carlito", 12, "bold"), bg="#f0f0f0", fg="#333")
result_label.pack(pady=15)

root.mainloop()
