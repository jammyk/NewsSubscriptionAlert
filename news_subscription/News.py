import requests



def get_news_by_keyword(word):
    url = ('https://newsapi.org/v2/everything?'
           'q={}&'
           'sortBy=popularity&'
           'apiKey=09dab7bdd91948f5a48741f4a4b46135'.format(word))
    response = requests.get(url)
    return response.json()


def parse_news(news_response):
    articles = []
    for article in news_response['articles']:
        articles.append((article['title'], article['description'],article['url']))
    return articles


for _article in parse_news(get_news_by_keyword('terramera')):
    print(_article)
