import sqlite3
import datetime

def create_db():
    conn = sqlite3.connect('swimmers.db')

    c = conn.cursor()

    c.execute('''CREATE TABLE myroslav
                (id integer PRIMARY KEY, task text, date_added text, importance integer)''')

    c.execute('''CREATE TABLE danylo
                (id integer PRIMARY KEY, task text, date_added text, importance integer)''')

    c.execute('''CREATE TABLE messages
                (id integer PRIMARY KEY, email_id integer, sender text, receiver text, message text, date_added text)''')


    conn.commit()

    conn.close()
