import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

print("Завантажуємо набір даних...")
housing = fetch_california_housing(as_frame=True)
df = housing.frame

print("Перевіряємо та обробляємо пропущені значення...")
df = df.fillna(df.mean())

x = df.drop(columns=['MedHouseVal'])
y = df['MedHouseVal']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("\nНавчаємо модель 1 (Лінійна регресія)...")
model_1 = LinearRegression()
model_1.fit(x_train, y_train)

print("Навчаємо модель 2 (Дерево рішень)...")
model_2 = DecisionTreeRegressor(random_state=42)
model_2.fit(x_train, y_train)

print("\nМоделі успішно навчені і готові до роботи!")
