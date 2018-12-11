import sqlite3

DATABASE = 'C:\\Users\\ryanj\\Documents\\git\\NewsSubscriptionAlert\\noonping.sqlite'
SELECT_SUBSCRIPTION = 'SELECT subscription FROM subscription'
SELECT_USER_WITH_SUBSCRIPTION = 'SELECT users.email, jxn.subscription FROM users_subscription as jxn ' \
                                'JOIN users ON jxn.email = users.email ' \
                                'WHERE jxn.subscription = ? AND users.enabled = 1'
INSERT_NEW_USER = "INSERT INTO users (email, enabled, time_inserted, time_updated) " \
                  "VALUES (?, 0, DATETIME('now'), DATETIME('now'));"
INSERT_NEW_SUBSCRIPTION = 'INSERT OR IGNORE INTO subscription (subscription) VALUES (?);'
INSERT_USERS_SUBSCRIPTION = 'INSERT INTO users_subscription (email, subscription) VALUES (?, ?)'


def get_connection(db_file=None):
    if db_file is None:
        db_file = DATABASE
    return sqlite3.connect(db_file)


def get_all_subscriptions(conn):
    curs = conn.cursor()
    curs.execute(SELECT_SUBSCRIPTION)
    return curs.fetchall()


def get_users_with_subscription(conn, subscription):
    curs = conn.cursor()
    curs.execute(SELECT_USER_WITH_SUBSCRIPTION, (subscription,))
    return curs.fetchall()


def insert_new_user(conn, user):
    curs = conn.cursor()
    curs.execute(INSERT_NEW_USER, (user,))


def insert_new_subscription(conn, user, subscription):
    curs = conn.cursor()
    curs.execute(INSERT_NEW_SUBSCRIPTION, (subscription,))
    curs.execute(INSERT_USERS_SUBSCRIPTION, (user, subscription))


def insert_sent_news(conn, hashed_articles):
    curs = conn.cursor()
    for hashed_articles in hashed_articles:
        curs.execute('INSERT INTO sent_articles VALUES (?)', hashed_articles)
    curs.commit()


def get_all_users_subscribed(conn):
    users_subscription = dict()
    for subscription in get_all_subscriptions(conn):
        users_subscription[subscription] = get_users_with_subscription(conn, subscription)
    return users_subscription


def parse_email_subscriptions(subscriptions):
    user_subscriptions = dict()
    for subscription in subscriptions:
        if subscription[0] not in user_subscriptions.keys():
            user_subscriptions[subscription[0]] = [subscription[1]]
        else:
            user_subscriptions[subscription[0]].append(subscription[1])
    return user_subscriptions


def check_for_entry(conn, value):
    curs = conn.cursor()
    curs.execute('SELECT COUNT(1) FROM hashed_articles WHERE hash = ?', (value,))
    return curs.fetch()


if __name__ == '__main__':
    with get_connection(DATABASE) as conn:
        for subscription in get_all_users_subscribed(conn):
            print(subscription + ' : ' + get_all_users_subscribed(conn).get(subscription))
        get_users_with_subscription(conn, 'terramera')
