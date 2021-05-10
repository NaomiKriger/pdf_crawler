import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create_table = "CREATE TABLE IF NOT EXISTS pdf (id INTEGER PRIMARY KEY, name text, phones text)"
# cursor.execute(create_table)

# cursor.execute("INSERT INTO pdf VALUES (1, 'my_pdf', '0523576254')")
# cursor.execute("DELETE * from pdf")
# connection.commit()
# select_query = "SELECT * FROM pdf"

cursor.execute("SELECT * from pdfs")
connection.commit()

# for row in cursor.execute(select_query):
#     print(row)
# cursor.execute("SELECT * FROM pdf")
# connection.commit()

connection.close()
