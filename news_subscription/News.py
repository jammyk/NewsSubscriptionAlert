import requests
from . import Article
from . import Subscription

API_KEY = '09dab7bdd91948f5a48741f4a4b46135'


def get_news_by_keyword(word):
    """
    Retrieves the news articles related to the word given

    :param word: str
        The keyword to search for
    :return: json
        The json response of news articles returned by News API
    """
    url = ('https://newsapi.org/v2/everything?'
           'q={}&'
           'sortBy=popularity&'
           'apiKey={}'.format(word, API_KEY))
    response = requests.get(url)
    return response.json()


def parse_news(news_response):
    """
    Structures the json response into a tuple of (Title, Description, URL)

    :param news_response: json
        The raw json response
    :return: lst
        The list of Article representing the news articles
    """
    articles = []
    for article in news_response['articles']:
        article_object = Article.Article(article['title'], article['description'], article['url'])
        article_object.hash_article()
        articles.append(article_object)
    return articles


def remove_duplicates(articles):
    with Subscription.get_connection() as conn:
        new_articles = [article for article in articles if not Subscription.check_for_entry(conn, article)]
    return new_articles


if __name__ == '__main__':
    pass
