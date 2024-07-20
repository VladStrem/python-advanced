class ArticleView:
    @staticmethod
    def input_article():
        title = input("Input article title:\n")
        author = input("Input article author:\n")
        year = input("Input article year:\n")
        return {"title": title, "author": author, "year": year}

    @staticmethod
    def show_articles(articles):
        for idx, article in enumerate(articles, start=1):
            print(f"{idx}. Title: {article['title']}, Author: {article['author']}, Year: {article['year']}")

    @staticmethod
    def show_menu():
        print("*************************")
        print("1 - Add article")
        print("2 - Show articles")
        print("3 - Update article")
        print("4 - Delete article")
        print("5 - Exit")
        result = int(input("Choose what to do:\n"))
        print("*************************")
        return result

    @staticmethod
    def input_article_id():
        return int(input("Input article ID:\n")) - 1
