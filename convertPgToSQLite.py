from sqlalchemy import create_engine
import pandas as pd

# Подключение к базе данных PostgreSQL
postgres_url = "postgresql://postgres:postgres@localhost/DataDopAndOtkl"
engine_postgres = create_engine(postgres_url)

# Подключение к базе данных SQLite
sqlite_url = "sqlite:///output2.db"
engine_sqlite = create_engine(sqlite_url)

# Имя таблицы для конвертации
table_name = "temp_otv"

# Запрос на выборку данных из PostgreSQL
query = f"SELECT * FROM {table_name}"

# Чтение данных из PostgreSQL
data = pd.read_sql(query, con=engine_postgres)

# Запись данных в SQLite
data.to_sql(table_name, con=engine_sqlite, if_exists="replace", index=False)