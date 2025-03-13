import psycopg2

def setup_database():
    """Initialize the PostgreSQL database with all required tables."""
    conn = psycopg2.connect(
        dbname="omega_db",
        user="omega_user",
        password="omega_pass",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    with open("omega_ai/db_manager/init_db.sql", "r") as sql_file:
        sql_script = sql_file.read()
        cursor.execute(sql_script)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL Database Fully Initialized!")

if __name__ == "__main__":
    setup_database()
