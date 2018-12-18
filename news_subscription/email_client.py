import smtplib
import imaplib
import email
from email.parser import HeaderParser
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


def create_email(email_body=''):
    if not email_body:
        email_body = 'Sorry, there are no articles available!'
    subject_body = 'Subject: {}\n\n{}'.format('Updates from Noon Ping', email_body)
    return subject_body


def get_credentials():
    with open('email_login_credentials.txt', 'r') as credentials:
        user = credentials.readline().strip()
        password = credentials.readline().strip()
        return user, password


def send_email(to_list, content):
    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    user, password = get_credentials(server)
    server.login(user, password)
    server.sendmail(USER, to_list, content)
    server.close()


def gmail_login():
    gmail_imap = imaplib.IMAP4_SSL('imap.gmail.com')
    user, password = get_credentials()
    gmail_imap.login(user, password)
    return gmail_imap


def search_inbox(connection):
    emails = []
    connection.select('inbox')
    # retrieve the uuid of emails in inbox
    status, msg_ids = connection.search(None, 'UNSEEN')
    if status != 'OK':
        raise ValueError('The server response was {}'.format(status))

    for msg_id in msg_ids[0].split():
        # fetch the message data of the uuid
        _, msg_data = connection.fetch(msg_id, '(RFC822)')
        for raw_msg in msg_data:
            if isinstance(raw_msg, tuple):

                # feed to email.parser to parse
                email_parser = email.parser.BytesFeedParser()
                email_parser.feed(raw_msg[1])

                # return email.message.Message
                parsed_msg = email_parser.close()

                email_content = ''
                for body in parsed_msg.walk():
                    if body.get_content_type() == 'text/plain':
                        email_content = body.get_payload(decode=True).decode('utf-8')

                email_subject = parsed_msg['subject']
                email_from = parsed_msg['from']
                emails.append((email_from, email_subject, email_content))
    connection.close()
    connection.logout()
    return emails


def parse_new_subscriptions(emails):
    new_subscription = []
    for email in emails:
        str_subs = ''
        email_subject = email[1].lower()
        email_content = email[2].lower()
        if 'noonping' in email_subject:
            str_subs = email_subject.split('noonping', 1)[1]
        elif 'noonping' in email_content:
            str_subs = email_subject.split('nooping', 1)[1]

        if str_subs:
            subs = str_subs.split(',')
            new_subscription.append((email[0], subs))
    return new_subscription


if __name__ == '__main__':
    conn = gmail_login()
    emails = search_inbox(conn)
    new_subs = parse_new_subscriptions(emails)
    for subs in new_subs:
        for subscrip in subs[1]:
            print('{} just subscribed to {}'.format(subs[0], subscrip))
    # parsed_articles = news.parse_news(news.get_news_by_keyword('dogs'))
    # email_content = create_email(create_body(parsed_articles))
    # list_email = []
    # send_email(list_email, email_content)
    #print(create_body(parsed_articles))




