import sqlite3


def create_db(db_name: str):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_db("test_db.db")
