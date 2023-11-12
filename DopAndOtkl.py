import psycopg2
import tkinter as tk
from tkinter import Entry, Button, Label, StringVar, OptionMenu


# Функция для обработки нажатия кнопки "Вычислить"
def calculate():
    size_input = int(entry_size.get())
    letter = letter_var.get().lower()
    digit = digit_var.get()
    system_input = system_var.get()
    system = case_system(system_input)
    diameter_size = case_size(size_input)

    # Проверка существования комбинации литеры и квалитета в базе данных
    if not combination_exists(letter + digit, system):
        result_var.set("Значение не найдено. Пожалуйста, проверьте введенные данные.")
        print(letter+digit, system)
        return

    sql_query = f"SELECT {letter}{digit}_max, {letter}{digit}_min FROM temp_{system} WHERE diameter_range = '{diameter_size}'"

    conn = psycopg2.connect(
        host="localhost",
        database="DataDopAndOtkl",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()
    cur.execute(sql_query)
    row = cur.fetchone()

    min = row[0]
    max = row[1]
    avg = (min + max) / 2
    result_var.set(f"Максимальное: {min}, Минимальное: {max}, Среднее: {avg}")

    conn.commit()
    cur.close()
    conn.close()


def combination_exists(combination, system):
    conn = psycopg2.connect(
        host="localhost",
        database="DataDopAndOtkl",
        user="postgres",
        password="postgres"
    )

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

    # Если count больше нуля, комбинация существует
    return count > 0


# Функция для проверки существования таблицы
def table_exists(cur, table_name):
    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    return cur.fetchone()[0]


# Функция для проверки существования столбца в таблице
def column_exists(cur, table_name, column_name):
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name = %s", (table_name, column_name))
    return cur.fetchone() is not None


def case_system(value):
    if value == "система отверстия":
        return "otv"
    elif value == "система вала":
        return "val"
    else:
        return None


# Функция для определения диапазона размера
def case_size(value):
    if value >= 3:
        return "До 3 включ."
    elif 3 < value < 6:
        return "Св. 3 до 6"
    elif 6 <= value < 10:
        return "Св. 6 до 10"
    elif 10 <= value < 14:
        return "Св. 10 до 14"
    elif 18 <= value < 24:
        return "Св. 18 до 24"
    elif 24 <= value < 30:
        return "Св. 24 до 30"
    elif 30 <= value < 40:
        return "Св. 30 до 40"
    elif 30 <= value < 50:
        return "Св. 30 до 50"
    elif 40 <= value < 50:
        return "Св. 40 до 50"
    elif 50 <= value < 65:
        return "Св. 50 до 65"
    elif 50 <= value < 80:
        return "Св. 50 до 80"
    elif 65 <= value < 80:
        return "Св. 65 до 80"
    elif 80 <= value < 100:
        return "Св. 80 до 100"
    elif 80 <= value < 120:
        return "Св. 80 до 120"
    elif 100 <= value < 120:
        return "Св. 100 до 120"
    elif 120 <= value < 140:
        return "Св. 120 до 140"
    elif 120 <= value < 180:
        return "Св. 120 до 180"
    elif 140 <= value < 160:
        return "Св. 140 до 180"
    elif 160 <= value < 180:
        return "Св. 160 до 180"
    elif 180 <= value < 200:
        return "Св. 180 до 200"
    elif 180 <= value < 250:
        return "Св. 180 до 250"
    elif 200 <= value < 225:
        return "Св. 200 до 225"
    elif 225 <= value < 250:
        return "Св. 225 до 250"
    elif 250 <= value < 280:
        return "Св. 250 до 280"
    elif 250 <= value < 315:
        return "Св. 250 до 315"
    elif 280 <= value < 315:
        return "Св. 280 до 315"
    elif 315 <= value < 355:
        return "Св. 315 до 355"
    elif 315 <= value < 400:
        return "Св. 315 до 400"
    elif 355 <= value < 400:
        return "Св. 355 до 400"
    elif 400 <= value < 450:
        return "Св. 400 до 450"
    elif 450 <= value < 500:
        return "Св. 450 до 500"
    elif 500 <= value < 560:
        return "Св. 500 до 560"
    elif 500 <= value < 630:
        return "Св. 500 до 630"
    elif 560 <= value < 630:
        return "Св. 560 до 630"
    elif 630 <= value < 710:
        return "Св. 630 до 710"
    elif 630 <= value < 800:
        return "Св. 630 до 800"
    elif 710 <= value < 800:
        return "Св. 710 до 800"
    elif 800 <= value < 900:
        return "Св. 800 до 900"
    elif 800 <= value < 1000:
        return "Св. 800 до 1000"
    elif 900 <= value < 1000:
        return "Св. 900 до 1000"
    elif 1000 <= value < 1120:
        return "Св. 1000 до 1120"
    elif 1000 <= value < 1250:
        return "Св. 1000 до 1250"
    elif 1120 <= value < 1250:
        return "Св. 1120 до 1250"
    elif 1250 <= value < 1400:
        return "Св. 1250 до 1400"
    elif 1250 <= value < 1600:
        return "Св. 1250 до 1600"
    elif 1400 <= value < 1600:
        return "Св. 1400 до 1600"
    elif 1600 <= value < 1800:
        return "Св. 1600 до 1800"
    elif 1600 <= value < 2000:
        return "Св. 1600 до 2000"
    elif 1800 <= value < 2000:
        return "Св. 1800 до 2000"
    elif 2000 <= value < 2240:
        return "Св. 2000 до 2240"
    elif 2000 <= value < 2500:
        return "Св. 2000 до 2500"
    elif 2240 <= value < 2500:
        return "Св. 2240 до 2500"
    elif 2500 <= value < 2800:
        return "Св. 2500 до 2800"
    elif 2500 <= value < 3150:
        return "Св. 2500 до 3150"
    elif 2800 <= value < 3150:
        return "Св. 2800 до 3150"
    else:
        return "Null"


# Создание графического интерфейса
root = tk.Tk()
root.title("Допуски и посадки")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="Введите размер в мм:").grid(row=0, column=0)
entry_size = Entry(frame)
entry_size.grid(row=0, column=1)

Label(frame, text="Выберите литеру основного отклонения:").grid(row=1, column=0)
letter_options = ["A", "B", "C", "CD", "D", "E", "EF", "F", "FG", "G", "H", "JS", "J", "K", "M", "N", "P", "R", "S", "T", "U", "V", "X", "Y", "Z", "ZA", "ZB", "ZC"]
letter_var = StringVar()
letter_var.set(letter_options[0])  # Значение по умолчанию
letter_menu = OptionMenu(frame, letter_var, *letter_options)
letter_menu.grid(row=1, column=1)

Label(frame, text="Выберите квалитет:").grid(row=2, column=0)
digit_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
digit_var = StringVar()
digit_var.set(digit_options[0])  # Значение по умолчанию
digit_menu = OptionMenu(frame, digit_var, *digit_options)
digit_menu.grid(row=2, column=1)

Label(frame, text="Выберите систему:").grid(row=3, column=0)
system_options = ["система отверстия", "система вала"]
system_var = StringVar()
system_var.set(system_options[0])  # Значение по умолчанию
system_menu = OptionMenu(frame, system_var, *system_options)
system_menu.grid(row=3, column=1)

Button(frame, text="Вычислить", command=calculate).grid(row=4, columnspan=2)

result_var = StringVar()
Label(frame, textvariable=result_var).grid(row=5, columnspan=2)

root.mainloop()
