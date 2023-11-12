import os
import sqlite3
import tkinter as tk
from tkinter import Entry, Label, StringVar, OptionMenu, font


# Функция для обработки нажатия кнопки "Вычислить"
def calculate(*args):
    size_input = int(entry_size.get())
    letter = letter_var.get().lower()
    digit = digit_var.get()
    system_input = system_var.get()
    system = case_system(system_input)
    diameter_size = case_size(size_input, letter)

    # Проверка существования комбинации литеры и квалитета в базе данных
    if not combination_exists(letter + digit, system):
        result_var.set("Значение не найдено. Пожалуйста, проверьте введенные данные.")
        return

    sql_query = f"SELECT {letter}{digit}_max, {letter}{digit}_min FROM temp_{system} WHERE diameter_range = '{diameter_size}'"

    conn = sqlite3.connect(db_path)  # Используем путь к базе данных из ресурсов
    cur = conn.cursor()
    cur.execute(sql_query)
    row = cur.fetchone()

    if row is not None:
        min_value = row[0]
        max_value = row[1]
        avg = (min_value + max_value) / 2
        result_var.set(f"Максимальное: {min_value}, Минимальное: {max_value}, Среднее: {avg}")
    else:
        result_var.set("Значение не найдено. Пожалуйста, проверьте введенные данные.")

    conn.commit()
    cur.close()
    conn.close()


def update_letters(letter_menu, *args):
    selected_system = system_var.get()
    if selected_system == "система отверстия":
        letter_options = ["H", "Js", "K", "F"]
    elif selected_system == "система вала":
        letter_options = ["g", "h", "js", "k", "n", "r", "f", "s", "u", "d", "b"]
    letter_var.set(letter_options[0])
    letter_menu['menu'].delete(0, 'end')
    for option in letter_options:
        letter_menu['menu'].add_command(label=option, command=tk._setit(letter_var, option))


def combination_exists(combination, system):
    db_path = os.path.abspath("output2.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Проверяем существование комбинации перед выполнением запроса
    table_name = f"temp_{system}"
    if table_exists(cur, table_name) and column_exists(cur, table_name, f'{combination}_max') and column_exists(cur, table_name, f'{combination}_min'):
        sql_query = f"SELECT COUNT(*) FROM {table_name} WHERE {combination}_max IS NOT NULL AND {combination}_min IS NOT NULL"
        cur.execute(sql_query)
        count = cur.fetchone()[0]
    else:
        count = 0

    cur.close()
    conn.close()

    return count > 0


# Функция для проверки существования таблицы
def table_exists(cur, table_name):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None


# Функция для проверки существования столбца в таблице
def column_exists(cur, table_name, column_name):
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cur.fetchall()]
    return column_name in columns


def case_system(value):
    if value == "система отверстия":
        return "otv"
    elif value == "система вала":
        return "val"
    else:
        return None


# Функция для определения диапазона размера
def case_size(value, letter):
    if value <= 1:
        return "до 1 мм"
    elif 1 <= value <= 3:
        return "от 1 до 3 вкл"
    elif 3 <= value < 6:
        return "св 3 - 6"
    elif 6 <= value < 10:
        return "6 - 10"
    elif 10 <= value < 18:
        return "10 - 18"
    elif 18 <= value < 24:
        return "18 - 24"
    elif 24 <= value < 30:
        return "24 - 30"
    elif 30 <= value < 40:
        return "30 - 40"
    elif 40 <= value < 50:
        return "40 - 50"
    elif 50 <= value < 65:
        return "50 - 65"
    elif 65 <= value < 80:
        return "65 - 80"
    elif 80 <= value < 100:
        return "80 - 100"
    elif 100 <= value < 120:
        return "100 - 120"
    elif 120 <= value < 140:
        return "120 - 140"
    elif 140 <= value < 160:
        return "140 - 160"
    elif 160 <= value < 180:
        return "160 - 180"
    elif 180 <= value < 200:
        return "180 - 200"
    elif 200 <= value < 225:
        return "200 - 225"
    elif 225 <= value < 250:
        return "225 - 250"
    elif 250 <= value < 280:
        return "250 - 280"
    elif 280 <= value < 315:
        return "280 - 315"
    elif 315 <= value < 355:
        return "315 - 355"
    elif 355 <= value < 400:
        return "355 - 400"
    elif 400 <= value < 450:
        return "400 - 450"
    elif 450 <= value < 500:
        return "450 - 500"
    elif 500 <= value < 630:
        return "500 - 630"
    elif 630 <= value < 800:
        return "630 - 800"
    elif 800 <= value < 1000:
        return "800 - 1000"
    elif 1000 <= value < 1250:
        return "1000 - 1250"
    elif 1250 <= value < 1600:
        return "1250 - 1600"
    elif 1600 <= value < 2000:
        return "1600 - 2000"
    elif 2000 <= value < 2500:
        return "2000 - 2500"
    elif 2500 <= value < 3150:
        return "2500 - 3150"
    elif 3150 <= value < 4000:
        return "3150 - 4000"
    elif 4000 <= value < 5000:
        return "4000 - 5000"
    else:
        return "Null"


# Создание графического интерфейса
root = tk.Tk()
root.title("Допуски и посадки")

default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=default_font.cget("size") * 2)

db_path = os.path.abspath("output2.db")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="Введите размер в мм:", font=default_font).grid(row=0, column=0)
entry_size_var = StringVar()
entry_size = Entry(frame, textvariable=entry_size_var, font=default_font)
entry_size.grid(row=0, column=1)

Label(frame, text="Выберите литеру основного отклонения:", font=default_font).grid(row=1, column=0)
letter_options = ["H", "Js", "K", "F", "Js"]
letter_var = StringVar()
letter_var.set(letter_options[0])

# Установка шрифта для элементов OptionMenu
option_menu_font = font.Font(size=default_font.cget("size"))
option_menu = OptionMenu(frame, letter_var, *letter_options)
menu = option_menu.nametowidget(option_menu.menuname)
menu.configure(font=option_menu_font)

option_menu.grid(row=1, column=1)

Label(frame, text="Выберите квалитет:", font=default_font).grid(row=2, column=0)
digit_options = ["6", "7", "8", "9", "11", "12", "13", "14", "15", "16"]
digit_var = StringVar()
digit_var.set(digit_options[0])
digit_menu = OptionMenu(frame, digit_var, *digit_options)
menu = digit_menu.nametowidget(digit_menu.menuname)
menu.configure(font=option_menu_font)
digit_menu.grid(row=2, column=1)

Label(frame, text="Выберите систему:", font=default_font).grid(row=3, column=0)
system_options = ["система отверстия", "система вала"]
system_var = StringVar()
system_var.set(system_options[0])
system_var.trace_add("write", update_letters)
system_menu = OptionMenu(frame, system_var, *system_options)
menu = system_menu.nametowidget(system_menu.menuname)
menu.configure(font=option_menu_font)
system_menu.grid(row=3, column=1)

entry_size_var.trace_add("write", calculate)

result_var = StringVar()
Label(frame, textvariable=result_var, font=default_font).grid(row=5, columnspan=4)

root.mainloop()
