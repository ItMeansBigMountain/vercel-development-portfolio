import constants
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class NewsApi:
    api_urls = [
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={constants.news_api}&category=business"
    ]

    webscrape_urls = [
        "https://www.foxnews.com/",
        "https://www.cnn.com/",
    ]


    def __init__(self, api=True, webscrape=True):
        self.api_urls = NewsApi.api_urls
        self.webscrape_urls = NewsApi.webscrape_urls
        
        self.api = api
        self.webscrape = webscrape
        
        self.api_articles = []
        self.webscrape_articles = []


    def fetch_api(self):
        if self.api == False:
            return
        articles = []
        for url in self.api_urls:
            top_news = requests.get(url).json()
            for a in top_news.get("articles"):
                # 'source','author','title','description','url','urlToImage','publishedAt','content'
                articles.append(a)
                self.api_articles.append(a)
        return articles





    def fetch_webscrape(self):
        if self.webscrape == False:
            return

        articles = []
        for x in self.webscrape_urls:
            # Check if the content is HTML
            data = requests.get(x)
            content_type = data.headers.get('Content-Type')
            if 'text/html' not in content_type:
                print(f"Skipping {x}, not an HTML page.")
                continue

            # INIT SOUP
            html = data.text
            soup = BeautifulSoup(html, 'html.parser')

            # Extract and store text from the HTML page
            text_data = """"""
            for string in soup.stripped_strings:
                text_data += f"\n{string}"

            self.webscrape_articles.append(text_data)
            articles.append(text_data)
        return articles

            # # collect links from webpage
            # for link in soup.find_all('a', href=True):
            #     url = link['href']
            #     full_url = urljoin(self.base_url, url)
            #     self.links.add(full_url)


    def clean_webpage(self, website_url):
        # CHECK IF WEBPAGE IS HTML
        data = requests.get(website_url)
        content_type = data.headers.get('Content-Type')
        if 'text/html' not in content_type:
            print(f"Skipping {website_url}, not an HTML page.")
            return None

        # INIT SOUP
        html = data.text
        soup = BeautifulSoup(html, 'html.parser')
        # Extract and store text from the HTML page
        text_data = """"""
        for string in list(set(soup.stripped_strings))[:-2]:
            text_data += f"\n\n{string}"
        return text_data












if __name__ == "__main__":
    news = NewsApi()
    
    # # API TEST
    # news_articles_API = news.fetch_api()
    # for article in news_articles_API:
    #     print( article )
    
    # WEBSCRAPE TEST
    news_articles_WEBSCRAPE = news.fetch_webscrape()
    for article in news_articles_WEBSCRAPE:
        print( article )