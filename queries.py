import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("SELECT * from pdfs")
connection.commit()

connection.close()
