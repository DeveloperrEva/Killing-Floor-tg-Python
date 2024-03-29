import sqlite3
import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def join(chat_id, username, firstname, date):
    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?", [chat_id]
    )
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, firstname, date) VALUES (?,?,?,?)", (chat_id, username, firstname, date)
        )
        conn.commit()

def all_users():
    cursor.execute(
        'SELECT * FROM users'
        )
    row = cursor.fetchall()
    amount_user_all = 0
    amount_user_day = 0
    for i in row:
        amount_user_all += 1
        if datetime.datetime.now() - datetime.datetime.fromisoformat(i[3]) <=  datetime.timedelta(days=1):
            amount_user_day += 1

    return amount_user_all, amount_user_day

def all_users_send():
    cursor.execute(
        "SELECT * FROM users"
    )
    data = cursor.fetchall()
    conn.commit()

    return data