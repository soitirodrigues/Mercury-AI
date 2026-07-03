from mercury_ai.news.news_provider import NewsProvider

provider = NewsProvider()

news = provider.get_news()

for item in news:
    print(item)