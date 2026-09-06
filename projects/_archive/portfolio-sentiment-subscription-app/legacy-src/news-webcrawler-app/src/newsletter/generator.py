class NewsletterGenerator:
    def __init__(self):
        self.articles = []

    def add_article(self, article):
        self.articles.append(article)

    def create_newsletter(self):
        newsletter_content = "Morning Newsletter\n\n"
        for article in self.articles:
            newsletter_content += f"Title: {article['title']}\n"
            newsletter_content += f"Link: {article['link']}\n"
            newsletter_content += f"Summary: {article['summary']}\n\n"
        return newsletter_content.strip()