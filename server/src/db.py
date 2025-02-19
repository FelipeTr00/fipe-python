import os
import sqlite3
from server.config import config

# Config
DB_URI = config.get("DB_URI", "../database/db.sqlite")
DEBUG = config.get("DEBUG", "false")

# Conn
def connect():
    
    try:
        conn = sqlite3.connect(DB_URI)
        return conn
    except Exception as e:
        if DEBUG:
            print(f"[{__name__}] Erro ao conectar ao banco: {e}")
        return None

# INSERT INTO
def add(table_name, data):
    
    if not table_name or not data:
        return False

    if not isinstance(data, list):
        data = [data]

    conn = connect()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("BEGIN TRANSACTION")
        for row in data:
            columns = list(row.keys())
            placeholders = ", ".join(["?"] * len(columns))
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            values = [row[col] for col in columns]
            try:
                cursor.execute(sql, values)
            except Exception as e:
                if DEBUG:
                    print(f"[{__name__}] Erro ao salvar dados: {e}")
        conn.commit()
    except Exception as e:
        if DEBUG:
            print(f"[{__name__}] Erro ao inserir dados: {e}")
        return False
    finally:
        conn.close()

    return True

# DROP
def drop(table_name):

    if not table_name:
        return False

    conn = connect()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()
    except Exception as e:
        if DEBUG:
            print(f"[{__name__}] Erro ao dropar a tabela: {e}")
        return False
    finally:
        conn.close()

    return True

# SELECT
def find(table_name, query=None):

    if not table_name:
        return None

    conn = connect()
    if not conn:
        return None

    rows = None
    try:
        cursor = conn.cursor()
        sql = f"SELECT * FROM {table_name}"
        values = []
        if query and len(query) > 0:
            conditions = []
            for key, val in query.items():
                conditions.append(f"{key} = ?")
                values.append(val)
            sql += " WHERE " + " AND ".join(conditions)

        cursor.execute(sql, values)
        rows = cursor.fetchall()
    except Exception as e:
        if DEBUG:
            print(f"[{__name__}] Erro ao selecionar dados: {e}")
    finally:
        conn.close()

    return rows
