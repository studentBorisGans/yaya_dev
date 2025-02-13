import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Root1234'
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS yaya_dev;")
cursor.execute("USE yaya_dev;")


# Create tables
tables = {}

tables['user_data'] = """
CREATE TABLE user_data (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(100),
    language VARCHAR(50),
    gender ENUM('Male', 'Female', 'Other'),
    age TINYINT,
    spend_class ENUM('A', 'B', 'C', 'D', 'E'),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    notifications BOOLEAN DEFAULT FALSE,
    music_service BOOLEAN DEFAULT FALSE,
    established BOOLEAN DEFAULT FALSE
);
"""

tables['friendships'] = """
CREATE TABLE friendships (
    friendship_id INT AUTO_INCREMENT PRIMARY KEY,
    user_a_id INT NOT NULL,
    user_b_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_a_id, user_b_id),
    FOREIGN KEY (user_a_id) REFERENCES user_data(user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_b_id) REFERENCES user_data(user_id) ON DELETE CASCADE
);
"""

tables['user_chats'] = """
CREATE TABLE user_chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    friendship_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (friendship_id) REFERENCES friendships(friendship_id) ON DELETE CASCADE
);
"""

# How will sender_id work? I dont think I need it for frontend, but for analysis itll be helpful

tables['music_service'] = """
CREATE TABLE music_service (
    user_id INT NOT NULL,
    apple BOOLEAN DEFAULT FALSE,
    spotify BOOLEAN DEFAULT FALSE,
    sc BOOLEAN DEFAULT FALSE,
    access_token VARCHAR(255),
    refresh_token VARCHAR(255),
    expiration DATETIME,
    FOREIGN KEY (user_id) REFERENCES user_data(user_id) ON DELETE CASCADE
);
"""

# THIS IS REDUDANT. THESE VALUES CAN BE CALCULATED ON THE FLY
# tables['user_spend'] = """
# CREATE TABLE user_spend (
#     user_id INT PRIMARY KEY,
#     num_events INT DEFAULT 0,
#     total_spend FLOAT DEFAULT 0.0,
#     avg_spend FLOAT DEFAULT 0.0,
#     avg_ticket_num FLOAT DEFAULT 0.0,
#     FOREIGN KEY (user_id) REFERENCES user_data(user_id) ON DELETE CASCADE
# );
# """

tables['venues'] = """
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(255),
    venue_capacity MEDIUMINT,
    venue_address VARCHAR(255),
    venue_city VARCHAR(100),
    venue_state VARCHAR(100),
    venue_zip VARCHAR(20),
    venue_country VARCHAR(100)
);
"""

tables['organizer'] = """
CREATE TABLE organizer (
    organizer_id INT AUTO_INCREMENT PRIMARY KEY,
    org_name VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    country VARCHAR(100),
    website VARCHAR(255),
    notifications BOOLEAN DEFAULT FALSE
);
"""

tables['dj'] = """
CREATE TABLE dj (
    dj_id INT AUTO_INCREMENT PRIMARY KEY,
    dj_name VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    bio TEXT,
    location VARCHAR(100),
    interested_count INT DEFAULT 0,
    socials BOOLEAN DEFAULT FALSE,
    notifications BOOLEAN DEFAULT FALSE
);
"""

tables['event_data'] = """
CREATE TABLE event_data (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    organizer_id INT NOT NULL,
    venue_id INT NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    tagged BOOLEAN DEFAULT FALSE,
    event_name VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    budget FLOAT,
    pre_event_poster VARCHAR(2083) NULL,
    pre_bio TEXT NULL,
    FOREIGN KEY (organizer_id) REFERENCES organizer(organizer_id) ON DELETE RESTRICT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE RESTRICT
);
"""

tables['user_messages'] = """
CREATE TABLE user_messages (
    msg_id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    event_id INT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('sent', 'delivered', 'read') NOT NULL DEFAULT 'sent',
    FOREIGN KEY (chat_id) REFERENCES user_chats(chat_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES user_data(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE SET NULL
);
"""
# Organizers and venues will never delete??

tables['published_events'] = """
CREATE TABLE published_events (
    event_id INT NOT NULL,
    dj_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    sold_out BOOLEAN DEFAULT FALSE,
    event_poster VARCHAR(2083) NOT NULL,
    bio TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE RESTRICT,
    FOREIGN KEY (dj_id) REFERENCES dj(dj_id) ON DELETE RESTRICT
);
"""
# Changed event_poster and bio names in event_data to prevent confusion when joining

tables['event_attendance'] = """
CREATE TABLE event_attendance (
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_data(user_id) ON DELETE CASCADE
);
"""

tables['tags'] = """
CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_type VARCHAR(50),
    tag_value VARCHAR(100) NOT NULL
);
"""

tables['user_tags'] = """
CREATE TABLE user_tags (
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (tag_id, user_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES user_data(user_id) ON DELETE CASCADE
);
"""

tables['event_tags'] = """
CREATE TABLE event_tags (
    tag_id INT NOT NULL,
    event_id INT NOT NULL,
    PRIMARY KEY (tag_id, event_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE RESTRICT,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE CASCADE
);
"""

tables['ticket_classes'] = """
CREATE TABLE ticket_classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50),
    num_left INT DEFAULT 0,
    price FLOAT NOT NULL
);
"""

tables['event_tickets'] = """
CREATE TABLE event_tickets (
    event_id INT NOT NULL,
    class_id INT NOT NULL,
    sold_out BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES ticket_classes(class_id) ON DELETE RESTRICT
);
"""

tables['purchase_details'] = """
CREATE TABLE purchase_details (
    purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    num_tickets INT NOT NULL,
    price FLOAT NOT NULL,
    table_booking BOOLEAN DEFAULT FALSE,
    shared BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES user_data(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE CASCADE
);
"""

tables['shared_ticket'] = """
CREATE TABLE shared_ticket (
    share_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255),
    resolved BOOLEAN DEFAULT FALSE,
);
"""

tables['ticket_sharing'] = """
CREATE TABLE ticket_sharing (
    purchase_id INT NOT NULL,
    share_id INT NOT NULL,
    PRIMARY KEY (purchase_id, share_id),
    FOREIGN KEY (purchase_id) REFERENCES purchase_details(purchase_id) ON DELETE CASCADE,
    FOREIGN KEY (share_id) REFERENCES shared_ticket(share_id) ON DELETE CASCADE
);
"""

tables['dj_socials'] = """
CREATE TABLE dj_socials (
    dj_id INT NOT NULL,
    website VARCHAR(2083) NULL,
    soundcloud VARCHAR(2083) NULL,
    spotify VARCHAR(2083) NULL,
    facebook VARCHAR(2083) NULL,
    instagram VARCHAR(2083) NULL,
    snapchat VARCHAR(2083) NULL,
    x VARCHAR(2083) NULL,
    FOREIGN KEY (dj_id) REFERENCES dj(dj_id) ON DELETE CASCADE
);
"""

tables['dj_tags'] = """
CREATE TABLE dj_tags (
    tag_id INT NOT NULL,
    dj_id INT NOT NULL,
    PRIMARY KEY (tag_id, dj_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE RESTRICT,
    FOREIGN KEY (dj_id) REFERENCES dj(dj_id) ON DELETE CASCADE
);
"""



tables['dj_org_chats'] = """
CREATE TABLE dj_org_chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    organizer_id INT NOT NULL,
    dj_id INT NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES organizer(organizer_id) ON DELETE RESTRICT,
    FOREIGN KEY (dj_id) REFERENCES dj(dj_id) ON DELETE RESTRICT
);
"""

tables['dj_org_messages'] = """
CREATE TABLE dj_org_messages (
    msg_id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    event_id INT NOT NULL,
    sender ENUM('dj', 'organizer') NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,
    status ENUM('sent', 'delivered', 'read') NOT NULL DEFAULT 'sent',
    FOREIGN KEY (chat_id) REFERENCES dj_org_chats(chat_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event_data(event_id) ON DELETE CASCADE
);
"""

tables['purchased_tickets'] = """
CREATE TABLE purchased_tickets (
    purchase_id INT NOT NULL,
    class_id INT NOT NULL,
    PRIMARY KEY (purchase_id, class_id),
    num_tickets INT NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchase_details(purchase_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES ticket_classes(class_id) ON DELETE RESTRICT
);
"""

# Execute table creation
# for table_name, table_sql in tables.items():
#     cursor.execute(table_sql)
#     print(f"Created table: {table_name}")

# cursor.execute(tables['purchased_tickets'])
# Close connection
cursor.close()
conn.close()
