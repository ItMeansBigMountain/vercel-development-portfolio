class WebCrawler:
    def __init__(self, sources):
        self.sources = sources
        self.articles = []

    def crawl(self):
        for source in self.sources:
            if source == 'reddit':
                from services.reddit import fetch_reddit_news
                self.articles.extend(fetch_reddit_news())
            elif source == 'nextdoor':
                from services.nextdoor import fetch_nextdoor_news
                self.articles.extend(fetch_nextdoor_news())
            # Add more sources as needed

    def filter_articles(self, preferences):
        filtered_articles = []
        for article in self.articles:
            if self.matches_preferences(article, preferences):
                filtered_articles.append(article)
        return filtered_articles

    def matches_preferences(self, article, preferences):
        # Implement filtering logic based on user preferences
        return True  # Placeholder for actual filtering logic