import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username = input('Enter Twitter Username: ')
howmany = input('Enter how many tweets user has: ')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://twitter.com/"+username)
time.sleep(1)

# focusing onto the body tag of the html
elem = driver.find_element_by_tag_name("body")

no_of_pagedowns = 10
# no_of_pagedowns = int(howmany)*.5

count=0
while no_of_pagedowns>0:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    no_of_pagedowns-=1
    count+=1
    print(count,'pages scrolled...')

# finding all text written in this div

# post_elems = driver.find_elements_by_class_name("css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

post_elems = driver.find_elements_by_class_name("TweetTextSize")
print(post_elems)

tweets = []
tweet_count = 0

with open('tweet_log.txt', 'a') as f:
    for x in post_elems:
        print (x.text , "\n")
        f.write(x.text)
        f.write("\n")
        tweet_count += 1
        tweets.append(x.text)

f.close()
driver.quit()
print(tweet_count)
print(tweets)