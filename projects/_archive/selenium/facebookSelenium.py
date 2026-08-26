import time
import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


#TEMP CREDENTIALS uncomment lines below for user input
fb_email = ' '
password = ' '
fb_url = ' '



print('\n https://www.facebook.com/' + str(fb_url)+'\n')
time.sleep(3)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

def login(fb_email, password):
    driver.get("https://www.facebook.com/")

    #enter email
    email_phone = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[1]/input')
    email_phone.send_keys(fb_email)

    #enter password
    enter_password = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/table/tbody/tr[2]/td[2]/input')
    enter_password.send_keys(password)

    # submit
    enter_password.submit()

    pass

def profile(fb_url):
    driver.get("https://www.facebook.com/"+fb_url)

    # getting rid of initial notifications
    elem = driver.find_element_by_tag_name("body")
    time.sleep(3)#might not need in headless
    elem.click() #might not need in headless
    time.sleep(2)#might not need in headless

    #scroll down profile to load dynamic "lazy load" posts
    no_of_pagedowns = 5
    count=0
    while no_of_pagedowns>0:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        no_of_pagedowns-=1
        count+=1
        print(count, 'pages scrolled...')

    time.sleep(5)
    # class  of post = _5pbx userContent _3576
    # posts = driver.find_elements_by_class_name("_5pbx userContent _3576")
    posts = driver.find_elements_by_class_name("_5pcb _4b0l _2q8l")
    print(posts)


# CALLING FUNCTIONS
login(fb_email, password)
profile(fb_url)