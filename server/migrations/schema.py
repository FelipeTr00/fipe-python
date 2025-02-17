import sqlite3

def run_schema():
    # .SQL Path
    schema_file = "server/migrations/schema.sql"

    # DB Path
    db_file = "server/database/db.sqlite"

    # Schema.sql
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Conn
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        # Migration
        cursor.executescript(sql_script)
        # Commit
        conn.commit()
    print("Sucessfuly!")

if __name__ == "__main__":
    run_schema()
    