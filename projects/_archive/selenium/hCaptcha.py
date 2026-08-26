'''
    Confirms H captcha cookies for skipping bot detection
'''



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

import time
import random

from fake_useragent import UserAgent

import json

import pickle

import pprint


'''
PROCEDURE
    # while view more in webpage, click button
    # after no more view mores, grab all project names

    go to repl of each project and store the code texts (all files )
    parse through the file texts and find API KEYS & PASSWORDS
'''


# VERIFIED EMAILED LINK
CATPCHA_EMAILED_LINK = ""





# functions
def saveCookies():
    time.sleep(30)
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

def loadCookies():
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)



def hCaptcha_Accessibility():
    global CATPCHA_EMAILED_LINK
    driver.get(CATPCHA_EMAILED_LINK)
    time.sleep(random.randint(3,10))
    button = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[3]/button').click()

def scroll_window(window):
    print('scrolling!')
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print(f'{last_height=}')
        # Scroll down to bottom
        driver.execute_script("arguments[0].scrollIntoView();", window )

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height




ua = UserAgent()
userAgent = ua.random
print(userAgent)


# selenium settings
options = Options()
options.add_argument(f'user-agent={userAgent}')
options.headless = False

profile = webdriver.FirefoxProfile('C:\\Users\\affan\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\zx5ijieg.default-release')

PROXY_HOST = "12.12.12.123"
PROXY_PORT = "1234"
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", PROXY_HOST)
profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX
driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired , options = options )








# captcha accesibility
try:
    hCaptcha_Accessibility()
    driver.close()
except:
    driver.close()

