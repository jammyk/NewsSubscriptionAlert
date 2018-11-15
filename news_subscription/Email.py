import smtplib
import news_subscription.News as news

user = 'noonping.news@gmail.com'
password = 'home2worldforlurkers!'


def create_send_message():
    updated_news = news.parse_news(news.get_news_by_keyword('terramera'))
    body = ''
    for article in updated_news:
        body += 'Title: {} Description: {} Link: {}'.format(article[0], article[1], article[2])

    body = body.encode('ascii', 'ignore')

    to = ['ehwo78@gmail.com']
    email_text = 'Subject: {}\n\n{}'.format('Update from Noon Ping', body.decode('ascii'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, to, email_text, mail_options=['SMPTUTF8'])
        server.close()
    except Exception as ex:
        print(ex)
        print('Uh-oh something went wrong...')


create_send_message()



