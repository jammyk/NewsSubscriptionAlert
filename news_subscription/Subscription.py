import sqlite3

DATABASE = 'C:\\Users\\ehwo7\\Documents\\sqlite\\news_subscription_email.db'


def get_connection(db_file=None):
    if db_file is None:
        db_file = DATABASE
    return sqlite3.connect(db_file)


def get_all_enabled(conn):
    curs = conn.cursor()
    curs.execute('SELECT email, subscription FROM email_alerts WHERE enabled = 1')
    return curs.fetchall()


def get_same_enabled_user(conn):
    # TODO modify SQL to get all subscriptions from the same email
    # SELECT ea.id, ea.email, ea.subscription FROM email_alerts ea
    # 	INNER JOIN email_alerts ea2 ON ea.email = ea2.email AND ea.id <> ea2.id
    curs = conn.cursor()
    curs.execute('SELECT one.subscription FROM email_alerts as one'
                 'INNER JOIN email_alerts as two ON one.email = two.email WHERE enabled = 1')
    return curs.fetchall()


def parse_email_subscriptions(subscriptions):
    user_subscriptions = dict()
    for subscription in subscriptions:
        if subscription[0] not in user_subscriptions.keys():
            user_subscriptions[subscription[0]] = [subscription[1]]
        else:
            user_subscriptions[subscription[0]].append(subscription[1])
    return user_subscriptions


if __name__ == '__main__':
    with get_connection(DATABASE) as conn:
        user_subscriptions = get_all_enabled(conn)
        parse_email_subscriptions(user_subscriptions)
