class ArticleModel:
    def __init__(self):
        self.articles = []
        self.next_id = 1

    def add_article(self, title, author, year):
        article = {
            "id": self.next_id,
            "title": title,
            "author": author,
            "year": year
        }
        self.articles.append(article)
        self.next_id += 1

    def get_articles(self):
        return self.articles

    def delete_article(self, article_id):
        self.articles = [article for article in self.articles if article["id"] != article_id]

    def update_article(self, article_id, title, author, year):
        for article in self.articles:
            if article["id"] == article_id:
                article["title"] = title
                article["author"] = author
                article["year"] = year
                break
