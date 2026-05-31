from database import NewsDatabase

if __name__ == "__main__":
    news_db = NewsDatabase("database/news.db")
    while True:
        try:
            mode = input("Choose mode (add/view/del): ").strip().lower()
            if mode == "add":
                title = input("Title: ")
                date = input("Date: ")
                summary = input("Summary: ")
                content = input("Content: ")
                if not title or not date or not summary or not content:
                    print("All fields are required. Please try again.")
                    continue
                news_db.add_news(title, date, summary, content)
                print("News added successfully!\n")
            elif mode == "view":
                news_list = news_db.get_all_news()
                if not news_list:
                    print("No news found.\n")
                    continue
                for news in news_list:
                    print(f"ID: {news['id']}, Title: {news['title']}, Date: {news['date']}, Summary: {news['summary']}\n")
                print()
            elif mode == "del":
                news_id = input("Enter the ID of the news to delete: ")
                news_id = int(news_id)
                news_db.delete_news(news_id)
                print("News deleted successfully!\n")
        except KeyboardInterrupt:
            print("\nExiting...")
            break