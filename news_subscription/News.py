import requests
import hashlib

API_KEY = '09dab7bdd91948f5a48741f4a4b46135'


def get_news_by_keyword(word):
    url = ('https://newsapi.org/v2/everything?'
           'q={}&'
           'sortBy=popularity&'
           'apiKey={}'.format(word, API_KEY))
    response = requests.get(url)
    return response.json()


def parse_news(news_response):
    articles = []
    for article in news_response['articles']:
        articles.append((article['title'], article['description'], article['url']))
    return articles


def hash_articles(articles):
    hashed_articles = []
    for article in articles:
        md5_hash_article = hashlib.md5(article[0].encode('ascii', 'ignore').hexdigest())
        hashed_articles.append(md5_hash_article)
    return hashed_articles


if __name__ == '__main__':
    i = 0
    an = parse_news(get_news_by_keyword('simba'))
    for hashed_article in hash_articles(an):
        print('Article: ' + str(an[i][0]))
        print(hashed_article)
        i += 1
