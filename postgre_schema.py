import psycopg2

conn = psycopg2.connect(database = "postgres", 
                        user = "user", 
                        host= 'localhost',
                        password = "password",
                        port = 5432)

cursor = conn.cursor()

cursor.execute("SELECT pg_is_in_recovery();")
print(f"Response: {cursor.fetchall()}")

tables = {}

tables['user_data'] = """
CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE spend_class_enum AS ENUM ('A', 'B', 'C', 'D', 'E');

CREATE TABLE user_data (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(100),
    language VARCHAR(50),
    gender gender_enum,
    age SMALLINT,
    spend_class spend_class_enum,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    notifications BOOLEAN DEFAULT FALSE,
    features JSONB
);
"""

cursor.execute(tables['user_data'])



cursor.close()
conn.close()
