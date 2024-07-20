from controllers import article_controller

if __name__ == '__main__':
    while True:
        result = article_controller.view.show_menu()

        match result:
            case 1:
                article_controller.action_add_article()
            case 2:
                article_controller.action_show_articles()
            case 3:
                article_controller.action_update_article()
            case 4:
                article_controller.action_delete_article()
            case 5:
                print("Bye!")
                break
            case _:
                print("\nWrong choice. Try again!\n")
