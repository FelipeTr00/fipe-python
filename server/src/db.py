import os
import sqlite3
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Config
DB_URI = os.getenv("DB_URI", "components/database.sqlite")
DEBUG = (os.getenv("DEBUG", "false") == "true")

def connect():
    """
    Função de conexão ao banco de dados SQLite.
    Retorna o objeto de conexão ou None em caso de erro.
    """
    try:
        conn = sqlite3.connect(DB_URI)
        return conn
    except Exception as e:
        if DEBUG:
            print(f"[{__name__}] Erro ao conectar ao banco: {e}")
        return None

def add(table_name, data):
    """
    Insere dados em 'table_name'. 'data' pode ser um dicionário ou uma lista de dicionários.
    Retorna True em caso de sucesso, False em caso de falha.
    """
    if not table_name or not data:
        return False

    # Data to List
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

def drop(table_name):
    """
    Exclui (DROP) a tabela informada.
    Retorna True em caso de sucesso, False em caso de falha.
    """
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

def find(table_name, query=None):
    """
    Busca registros em 'table_name'.
    'query' é um dicionário cujas chaves são colunas e valores são condições de igualdade.
    Retorna uma lista de tuplas (cada tupla é uma linha) ou None em caso de erro.
    """
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
