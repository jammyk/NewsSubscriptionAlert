import smtplib
import news_subscription.news as news

USER = 'noonping.news@gmail.com'


def create_body(articles):
    """
    Structures articles in a reader-friendly fashion

    :param articles: lst
        The list article objects
    :return message: str
        The structured e-mail body
    """
    message = ''
    for article in articles:
        message += 'Title: {} new_line' \
                   'Description: {} new_line' \
                   'Link: {} new_line new_line'.format(article.title, article.description, article.url)
    message = message.encode('ascii', 'ignore')
    return message.decode('ascii').replace('new_line', '\n')


def create_email(email_body='Nothing to show here'):
    subject_body = 'Subject: {}\n\n{}'.format('Updates from Noon Ping', email_body)
    return subject_body


def login(server):
    """
    Login to the server by reading the user email and password from local file

    :param server: smptlib
        The server to login to
    """
    with open('email_login_credentials.txt', 'r') as credentials:
        user = credentials.readline().strip()
        password = credentials.readline().strip()
        server.login(user, password)


def send_email(to_list, content):
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    login(server)
    server.sendmail(USER, to_list, content)
    server.close()


if __name__ == '__main__':
    parsed_articles = news.parse_news(news.get_news_by_keyword('dogs'))
    email_content = create_email(create_body(parsed_articles))
    list_email = []
    send_email(list_email, email_content)
    #print(create_body(parsed_articles))




