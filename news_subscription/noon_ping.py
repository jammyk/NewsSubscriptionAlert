import news_subscription.Subscription as subs
import news_subscription.News as news
import news_subscription.Email as email

if __name__ == '__main__':
    with subs.get_connection() as conn:
        enabled_subscriptions = subs.get_all_enabled(conn)
        email_subscription = subs.parse_email_subscriptions(enabled_subscriptions)
        for user_subscription in email_subscription.keys():
            for subscription in email_subscription[user_subscription]:
                email.send_email(user_subscription, email.create_email(email.create_body(news.parse_news(news.get_news_by_keyword(subscription)))))




