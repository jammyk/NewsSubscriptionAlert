import sqlite3

DATABASE = 'C:\\Users\\ryanj\\Documents\\git\\NewsSubscriptionAlert\\noonping.sqlite'
SELECT_SUBSCRIPTION = 'SELECT subscription FROM subscription'
SELECT_USER_WITH_SUBSCRIPTION = 'SELECT users.email FROM users_subscription as jxn ' \
                                'JOIN users ON jxn.email = users.email ' \
                                'WHERE jxn.subscription = ? AND users.enabled = 1'
INSERT_NEW_USER = "INSERT OR IGNORE INTO users (email, enabled, time_inserted, time_updated) " \
                  "VALUES (?, 0, DATETIME('now'), DATETIME('now'));"
INSERT_NEW_SUBSCRIPTION = 'INSERT OR IGNORE INTO subscription (subscription) VALUES (?);'
INSERT_USERS_SUBSCRIPTION = 'INSERT OR IGNORE INTO users_subscription (email, subscription, enabled) VALUES (?, ?, 1)'


def get_connection(db_file=None):
    if db_file is None:
        db_file = DATABASE
    return sqlite3.connect(db_file)


def insert_new_user(conn, user):
    curs = conn.cursor()
    curs.execute(INSERT_NEW_USER, (user,))


def enable_user(conn, user):
    curs = conn.cursor()
    curs.execute('UPDATE users SET enabled = 1, time_updated = DATETIME(\'now\') WHERE email = ?;', (user,))


def disable_user(conn, user):
    curs = conn.cursor()
    curs.execute('UPDATE users SET enabled = 0, time_updated = DATETIME(\'now\') WHERE email = ?;', (user,))


def convert_to_list(users):
    users_lst = []
    for user in users:
        users_lst.append(user[0])
    return users_lst


def _get_users_with_subscription(conn, subscription):
    curs = conn.cursor()
    curs.execute(SELECT_USER_WITH_SUBSCRIPTION, (subscription,))
    return curs.fetchall()


def _get_subscriptions(conn):
    curs = conn.cursor()
    curs.execute(SELECT_SUBSCRIPTION)
    return curs.fetchall()


def insert_new_subscription(conn, user, subscription):
    curs = conn.cursor()
    curs.execute(INSERT_NEW_SUBSCRIPTION, (subscription,))
    curs.execute(INSERT_USERS_SUBSCRIPTION, (user, subscription))


def get_subscription_users(conn):
    """
    Maps the subscription to the list of enabled users

    :param conn: sqlite.Connection
        The connection to the sqlite database
    :return: dict
        A dictionary with subscriptions mapped to an array of user e-mails represented by tuple
            {'keyword' : [(user_one,), (user_two,), ...]
    """
    sub_users_map = dict()
    for sub in _get_subscriptions(conn)[0]:
        sub_users_map[sub] = convert_to_list(_get_users_with_subscription(conn, sub))
    return sub_users_map


def insert_sent_news(conn, articles):
    curs = conn.cursor()
    for article in articles:
        article.hash_article()
        curs.execute('INSERT OR IGNORE INTO sent_articles (title, url, hash) VALUES (?, ?, ?)',
                    (article.title, article.url, article.hash))


def check_for_entry(conn, value):
    curs = conn.cursor()
    curs.execute('SELECT COUNT(1) FROM sent_articles WHERE hash = ?', [value])
    return curs.fetchall()[0][0]


if __name__ == '__main__':
    with get_connection(DATABASE) as connection:
        print(get_subscription_users(connection))
