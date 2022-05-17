import sqlite3

# Define out connection + cursor
connection = sqlite3.connect('urls.db')
cursor = connection.cursor()

# Create table for URL entries
create_table = """CREATE TABLE IF NOT EXISTS entries(long_url TEXT PRIMARY KEY, short_url TEXT, timestamp TEXT)"""
cursor.execute(create_table)