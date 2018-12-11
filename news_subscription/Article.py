import hashlib


class Article(object):
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url
        self.hash = 0

    def hash_article(self):
        self.hash = hashlib.md5(self.url.encode('ascii', 'ignore')).hexdigest()
