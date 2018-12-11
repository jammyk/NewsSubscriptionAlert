import news_subscription.database as db
from news_subscription import news
import news_subscription.email_client as email_client

if __name__ == '__main__':
    with db.get_connection() as conn:
        articles = []
        sub_user_map = db.get_subscription_users(conn)
        for subscription in sub_user_map:
            articles = news.get_news_by_keyword(subscription, 3)
            unique_articles = news.remove_duplicates(articles)
            formatted_articles = email_client.create_body(unique_articles)
            formatted_email = email_client.create_email(formatted_articles)
            email_client.send_email(sub_user_map[subscription], formatted_email)
            db.insert_sent_news(conn, articles)




