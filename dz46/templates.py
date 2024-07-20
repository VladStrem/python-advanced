from abc import ABC, abstractmethod


class ArticlesTemplate(ABC):
    @abstractmethod
    def render(self, articles):
        pass


class ArticleTemplate(ArticlesTemplate):
    def render(self, articles):
        if articles:
            article = articles[0]
            return f"ID: {article['id']}, Title: {article['title']}, Author: {article['author']}, Year: {article['year']}"
        else:
            return "No articles available"


class ArticlesTemplateTable(ArticlesTemplate):
    def render(self, articles):
        result = "\n&&&&&&&&&&&&&&&&&&&&&&&&&\n"
        for article in articles:
            result += f"ID: {article['id']}, Title: {article['title']}, Author: {article['author']}, Year: {article['year']}\n"
        result += "&&&&&&&&&&&&&&&&&&&&&&&&&\n"
        return result



class ArticlesTemplateSimple(ArticlesTemplate):
    def render(self, articles):
        result = " ".join([f"{article['title']} by {article['author']} ({article['year']})" for article in articles])
        return result
