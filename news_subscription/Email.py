import smtplib
from email.message import EmailMessage
import news_subscription.News as news

user = 'noonping.news@gmail.com'


def create_send_message():
    updated_news = news.parse_news(news.get_news_by_keyword('terramera'))
    body = ''
    for article in updated_news:
        body += 'Title: {} \n Description: {} \n Link: {} \n\n'.format(article[0], article[1], article[2])
    msg = EmailMessage()
    msg.set_content(body)
    to = ['ehwo78@gmail.com']
    email_text = 'Subject: {}\n\n{}'.format('Update from Noon Ping', msg)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, to, email_text)
        server.close()
    except Exception as ex:
        print(ex)
        print('Uh-oh something went wrong...')


create_send_message()



