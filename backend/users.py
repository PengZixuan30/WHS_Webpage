from database import NewsDatabase
import datetime

def add_news():
    title = input("请输入新闻标题: ")
    date = input("请输入新闻日期 (格式: YYYY-MM-DD): ")
    summary = input("请输入新闻摘要: ")
    content = input("请输入新闻内容: ")

    news_db = NewsDatabase("database/whs_news.db")

    if title and summary:
        if date:
            if content:
                news_db.add_news(title, date, summary, content)
                print(f"新闻已添加到数据库。信息:\n标题: {title}\n日期: {date}\n摘要: {summary}\n内容: {content}")
            else:
                news_db.add_news(title, date, summary, summary)
                print(f"新闻已添加到数据库。信息:\n标题: {title}\n日期: {date}\n摘要: {summary}\n内容: (无)")
        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            if content:
                news_db.add_news(title, date, summary, content)
                print(f"新闻已添加到数据库。信息:\n标题: {title}\n日期: {date}\n摘要: {summary}\n内容: {content}")
            else:
                news_db.add_news(title, date, summary, summary)
                print(f"新闻已添加到数据库。信息:\n标题: {title}\n日期: {date}\n摘要: {summary}\n内容: (无)")
    else:
        print("新闻标题和摘要不能为空。新闻未添加到数据库。")

def delete_news():
    news_id = input("请输入要删除的新闻ID: ")
    if news_id.isdigit():
        news_db = NewsDatabase("database/whs_news.db")
        news_db.delete_news(int(news_id))
        print(f"新闻ID {news_id} 已从数据库中删除。")
    else:
        print("无效的新闻ID。请输入一个数字。")

def read_news():
    news_db = NewsDatabase("database/whs_news.db")
    news_list = news_db.get_all_news()
    if news_list:
        print("当前新闻列表:\n")
        for news in news_list:
            print(f"ID: {news['id']}, \n标题: {news['title']}, \n日期: {news['date']}, \n摘要: {news['summary']}, \n内容: {news['content']}\n")

def main():
    while True:
        cont = input("请选择操作: [A]添加新闻, [D]删除新闻, [R]查看新闻, [Q]退出: ").strip().lower()
        if cont == 'q':
            break
        elif cont == 'a':
            add_news()
        elif cont == 'd':
            delete_news()
        elif cont == 'r':
            read_news()
        else:
            print("无效的选择。请重新输入。")

if __name__ == "__main__":
    main()
