class ArticleView:
    def __init__(self, model):
        self.model = model
        
    def render(self, template):
        articles = self.model.get_articles()
        return template.render(articles)


def show_menu():
    print("*************************")
    print("1 - Add article")
    print("2 - Show articles in table style")
    print("3 - Show articles in simple style")
    print("4 - Show first article")
    print("5 - Delete article")
    print("6 - Update article")
    print("7 - Exit")
    result = int(input("Choose what to do:\n"))
    print("*************************")
    return result
