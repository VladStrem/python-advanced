from models import ArticleModel
from views import ArticleView, show_menu
from templates import ArticlesTemplateTable, ArticlesTemplateSimple, ArticleTemplate

if __name__ == '__main__':
    obj_model = ArticleModel()
    obj_view = ArticleView(obj_model)
    obj_table = ArticlesTemplateTable()
    obj_simple = ArticlesTemplateSimple()
    obj_simple_article = ArticleTemplate()

    while True:
        result = show_menu()

        match result:
            case 1:
                title = input("Enter article title: ")
                author = input("Enter article author: ")
                year = input("Enter article year: ")
                obj_model.add_article(title, author, year)
            case 2:
                print(obj_view.render(obj_table))
            case 3:
                print(obj_view.render(obj_simple))
            case 4:
                print(obj_view.render(obj_simple_article))
            case 5:
                article_id = int(input("Enter the ID of the article to delete: "))
                obj_model.delete_article(article_id)
            case 6:
                article_id = int(input("Enter the ID of the article to update: "))
                title = input("Enter new title: ")
                author = input("Enter new author: ")
                year = input("Enter new year: ")
                obj_model.update_article(article_id, title, author, year)
            case 7:
                print("Bye!")
                break
            case _:
                print("\nWrong choice. Try again!\n")
