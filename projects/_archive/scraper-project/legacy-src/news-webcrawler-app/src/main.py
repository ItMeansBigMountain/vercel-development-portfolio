from crawler.index import WebCrawler
from newsletter.generator import NewsletterGenerator

def main():
    # Initialize the web crawler
    crawler = WebCrawler()
    
    # Fetch news articles from various sources
    articles = crawler.crawl()
    
    # Initialize the newsletter generator
    newsletter_generator = NewsletterGenerator()
    
    # Create the morning newsletter
    newsletter = newsletter_generator.create_newsletter(articles)
    
    # Print or send the newsletter
    print(newsletter)

if __name__ == "__main__":
    main()