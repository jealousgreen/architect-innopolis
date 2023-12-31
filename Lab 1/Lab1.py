# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xEn_wrERp4zsbRLG0w6R1mhtGARkUDiW

Лабораторная работа по теме “Фреймворки Python для ML(CatBoost,scikitlearn)”
"""

pip install catboost

"""1.Создайте датасет из не менее чем 2000 записей,содержащий данные о среднем балле студентов(от 0 до 99) по 6 предметам и оценка итоговой лабораторной работы(удовлетворительно,хорошо,отлично).Названия предметов,средний балл,время решения итоговой лабораторной работы задается произвольно на ваше усмотрение."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Создаем датафрейм с рандомными оценками
subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Computer Science']
grades = np.random.randint(0, 100, size=(2000, 6))
lab_grade = np.random.choice(['C', 'B', 'A'], size=2000)

# Оценка по лабораторной работе
data = pd.DataFrame(grades, columns=subjects)
data.insert(6,'Grade', lab_grade)

print(data)

# Оценки по лабараторным в кат. данные
le = LabelEncoder()
le.fit(data.Grade)
data.Grade = le.transform(data.Grade)
data.head()

"""2. Разбейте датасет на тестовую и обучающую выборку.
3. Выберите лучшие 3 признака для обучения.
"""

# Топ 3 по grade
corr = data.corr()
corr.style.background_gradient(cmap='PuBu', low=0, high=0, axis=0, subset=None)

# Деление датасета на тестовую и обучающую выборки
from sklearn.model_selection import train_test_split
x_train1, x_test1, y_train1, y_test1 = train_test_split(data[['Mathematics', 'Chemistry', 'Computer Science']], data.Grade, test_size=0.2)

"""4. Проведите обучение модели,результатом должна быть сохраненная модель"""

from catboost import CatBoostClassifier

model = CatBoostClassifier(iterations=500, depth=4, learning_rate=0.1)
model.fit(x_train1, y_train1, silent=True)

"""5. Проведите тестирование модели,результатом должно быть число-точность модели на тестовой выборке."""

accuracy = model.score(x_test1, y_test1)
print(f'точность: {accuracy*100}%')

"""6. Реализуйте функцию,которая на вход принимает оценку студента по 6 предметам и возвращает прогноз оценки."""

def get_predict_grade(math, phis, chem, bio, hist, comsc):
  subjects_test = ['Mathematics', 'Chemistry', 'Computer Science']
  grades_test = np.array([[math, chem, comsc]])


# добавление столбца с оценкой по лабораторной работе
  data_test = pd.DataFrame(grades_test, columns=subjects_test)

  pr = model.predict(data_test)
  grade =''
  match pr:
    case 2:
      grade='C'
    case 1:
      grade ='B'
    case 0:
      grade='A'

  return grade

# Результат работы функции
print(get_predict_grade(70,90,56,12,65,100))