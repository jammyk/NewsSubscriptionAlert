import sqlite3


def get_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)


def get_all(conn):
    curs = conn.cursor()
    curs.execute('SELECT * FROM email_alerts WHERE enabled = true')
    return curs.fetchall()

# conn = get_connection(database)
# database = 'C:\\Users\\ehwo7\\Documents\\sqlite\\news_subscription_email.db'
# print(get_all(conn)[0])