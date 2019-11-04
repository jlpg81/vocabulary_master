import sqlite3
from install_data import data
import datetime

zero = datetime.date.today() - datetime.date.today()

def install_database():
    conn = sqlite3.connect("flashcards.db")

    c = conn.cursor()

    c.execute("""CREATE TABLE flashcards (
        id integer PRIMARY KEY,
        english text,
        vietnamese text,
        word_level integer,
        word_date text,
        days_left text
        )""")

    for i in data:
        c.execute("INSERT INTO flashcards VALUES (:id, :english, :vietnamese, :word_level, :word_date, :days_left)",
        {'id':i[0], 'english':i[1], 'vietnamese':i[2], 'word_level':0, 'word_date':"", 'days_left': 0})

    c.execute("SELECT * FROM flashcards")

    # print(c.fetchall())

    conn.commit()

    conn.close()