from models import ArticleModel
from views import ArticleView

class ArticleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def action_add_article(self):
        article = self.view.input_article()
        self.model.add_article(article)

    def action_show_articles(self):
        articles = self.model.get_articles()
        self.view.show_articles(articles)

    def action_update_article(self):
        article_id = self.view.input_article_id()
        new_article = self.view.input_article()
        self.model.update_article(article_id, new_article)

    def action_delete_article(self):
        article_id = self.view.input_article_id()
        self.model.delete_article(article_id)

article_controller = ArticleController(ArticleModel(), ArticleView())
