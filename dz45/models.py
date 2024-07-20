class ArticleModel:
    def __init__(self):
        self.articles = []

    def add_article(self, article):
        self.articles.append(article)

    def get_articles(self):
        return self.articles

    def update_article(self, article_id, new_article):
        if 0 <= article_id < len(self.articles):
            self.articles[article_id] = new_article

    def delete_article(self, article_id):
        if 0 <= article_id < len(self.articles):
            self.articles.pop(article_id)
