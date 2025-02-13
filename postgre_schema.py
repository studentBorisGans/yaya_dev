import psycopg2

conn = psycopg2.connect(database = "postgres", 
                        user = "user", 
                        host= 'localhost',
                        password = "password",
                        port = 5432)

cursor = conn.cursor()

# cursor.execute("SELECT pg_is_in_recovery();")
# print(f"Response: {cursor.fetchall()}")

tables = {}

tables['user_data'] = """
CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE spend_class_enum AS ENUM ('A', 'B', 'C', 'D', 'E', 'NA');

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

tables['venues'] = """
CREATE TABLE IF NOT EXISTS venues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    capacity INTEGER,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip VARCHAR(20),
    country VARCHAR(100),
    table_count SMALLINT,
    features JSONB
);
"""

tables['organizer'] = """
CREATE TABLE IF NOT EXISTS organizer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    country VARCHAR(100),
    website VARCHAR(255),
    notifications BOOLEAN DEFAULT FALSE,
    features JSONB
);
"""

tables['dj'] = """
CREATE TABLE IF NOT EXISTS dj (
    id SERIAL PRIMARY KEY,
    alias VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bio TEXT,
    location VARCHAR(100),
    interested_count INT DEFAULT 0,
    notifications BOOLEAN DEFAULT FALSE,
    features JSONB
);
"""


tables['event_data'] = """
CREATE TABLE IF NOT EXISTS event_data (
    id SERIAL PRIMARY KEY,
    organizer_id INT NOT NULL,
    venue_id INT NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    date TIMESTAMPTZ NOT NULL,
    budget FLOAT,
    pre_event_poster VARCHAR(2083) NULL,
    pre_bio TEXT NULL,
    features JSONB,
    FOREIGN KEY (organizer_id) REFERENCES organizer(id) ON DELETE RESTRICT,
    FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE RESTRICT
);
ALTER TABLE organizer ADD COLUMN deleted BOOLEAN DEFAULT FALSE;
ALTER TABLE dj ADD COLUMN deleted BOOLEAN DEFAULT FALSE;
ALTER TABLE user_data ADD COLUMN deleted BOOLEAN DEFAULT FALSE;
ALTER TABLE venues ADD COLUMN deleted BOOLEAN DEFAULT FALSE;
"""




tables['dj_socials'] = """
CREATE TABLE IF NOT EXISTS dj_socials (
    dj_id INT NOT NULL,
    website VARCHAR(2083) NULL,
    soundcloud VARCHAR(2083) NULL,
    spotify VARCHAR(2083) NULL,
    facebook VARCHAR(2083) NULL,
    instagram VARCHAR(2083) NULL,
    snapchat VARCHAR(2083) NULL,
    x VARCHAR(2083) NULL,
    FOREIGN KEY (dj_id) REFERENCES dj(id) ON DELETE RESTRICT
);
"""



tables['published_events'] = """
CREATE TABLE IF NOT EXISTS published_events (
    event_id INT NOT NULL,
    dj_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    sold_out BOOLEAN DEFAULT FALSE,
    event_poster VARCHAR(2083) NOT NULL,
    bio TEXT NOT NULL,
    published_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES event_data(id) ON DELETE RESTRICT,
    FOREIGN KEY (dj_id) REFERENCES dj(id) ON DELETE RESTRICT
);
ALTER TABLE user_data RENAME COLUMN timestamp TO registered_at;
ALTER TABLE event_data ADD COLUMN created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE venues ADD COLUMN created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE organizer ADD COLUMN created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE dj ADD COLUMN created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
"""



tables['friendships'] = """
CREATE TABLE IF NOT EXISTS friendships (
    id SERIAL PRIMARY KEY,
    user_a_id INT NOT NULL,
    user_b_id INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_a_id, user_b_id),
    FOREIGN KEY (user_a_id) REFERENCES user_data(id) ON DELETE RESTRICT,
    FOREIGN KEY (user_b_id) REFERENCES user_data(id) ON DELETE RESTRICT
);
"""

tables['music_service'] = """
CREATE TABLE IF NOT EXISTS music_service (
    user_id INT NOT NULL,
    apple BOOLEAN DEFAULT FALSE,
    spotify BOOLEAN DEFAULT FALSE,
    sc BOOLEAN DEFAULT FALSE,
    access_token VARCHAR(255),
    refresh_token VARCHAR(255),
    expiration TIMESTAMPTZ,
    FOREIGN KEY (user_id) REFERENCES user_data(id) ON DELETE CASCADE
);
"""

tables['purchase'] = """
CREATE TABLE IF NOT EXISTS purchase (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    num_tickets INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    table_booking BOOLEAN DEFAULT FALSE,
    purchased_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    extra_info JSONB,
    FOREIGN KEY (user_id) REFERENCES user_data(id) ON DELETE RESTRICT,
    FOREIGN KEY (event_id) REFERENCES event_data(id) ON DELETE RESTRICT
);
"""

tables['shared_ticket'] = """
CREATE TABLE IF NOT EXISTS shared_ticket (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255),
    resolved BOOLEAN DEFAULT FALSE,
    shared_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    extra_info JSONB
);
"""

tables['shared_ticket_details'] = """
CREATE TABLE IF NOT EXISTS shared_ticket_details (
    purchase_id INT NOT NULL,
    share_id INT NOT NULL,
    PRIMARY KEY (purchase_id, share_id),
    FOREIGN KEY (purchase_id) REFERENCES purchase(id) ON DELETE RESTRICT,
    FOREIGN KEY (share_id) REFERENCES shared_ticket(id) ON DELETE RESTRICT
);
"""

# MISSING MESSAGES AND PURCHASE DETAILS


# for table_name, table_sql in tables.items():
#         cursor.execute(table_sql)
#         print(f"Created table: {table_name}")

# cursor.execute("ALTER TABLE shared_ticket_details RENAME TO shared_tickets")
# cursor.execute("ALTER TABLE shared_ticket RENAME TO shared_ticket_details")
# cursor.execute("ALTER TABLE shared_tickets RENAME TO shared_ticket")


# cursor.execute("ALTER TABLE dj ADD COLUMN phone VARCHAR(20)")



conn.commit()

cursor.close()
conn.close()
