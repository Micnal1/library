from sqlite3 import connect

def select_authors():
    conn = connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM author;")
    result = cur.fetchall()
    return result