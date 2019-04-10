import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Generate and execute SQL statements to drop each table
for table in tables:
    cursor.execute("DROP TABLE IF EXISTS " + table[0] + ";")

# Commit changes and close the connection
conn.commit()
conn.close()
