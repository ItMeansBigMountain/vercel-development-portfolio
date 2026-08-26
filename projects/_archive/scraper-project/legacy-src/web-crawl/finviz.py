from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)



def fetch_articles(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}&ty=c&ta=1&p=d"

    try:
        # FETCH URL & INIT HTML PARSER
        driver.get(url)
        bs = BeautifulSoup(driver.page_source,"html.parser")
        
        # FETCH ALL LINKS
        all_links = bs.find_all("a")

        # FETCH ALL HEADLINES AND SOURCE OF NEWS
        news_headlines = bs.find_all('a', {'class': 'tab-link-news'})
        news_source = bs.find_all('div', {'class': 'news-link-right'})


        # CREATE OUTPUT JSON
        output = []
        for i in range(0,len(news_headlines),1):
            output.append({"headline" : news_headlines[i].text, "source"  :  news_source[i].text })

    except Exception as e:
        driver.quit()
        print(e)
        exit()


    # CLEANUP
    driver.quit()
    return output








# SEARCH FOR TICKER NEWS HERE
if __name__ == "__main__":
    import pprint
    output = fetch_articles("GOOGL")
    pprint.pprint(output)