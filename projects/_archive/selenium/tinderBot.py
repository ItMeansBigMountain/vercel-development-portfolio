from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

import time

try:
    howmany = int(input("Please enter how many likes you wanna full send, whore: "))

    profile = webdriver.FirefoxProfile()
    profile.set_preference("geo.wifi.uri", 'data:application/json,{"location": {"lat": 38.912650, "lng":-77.036185}, "accuracy": 20.0}')
    profile.set_preference("geo.prompt.testing", True)

    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options = options , firefox_profile=profile)
    driver.get("https://www.tinder.com/")
    time.sleep(2)

    # log in 
    loginButton = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/button')
    loginButton.click()
    time.sleep(2)
    print("Clicked login button")

    # phone
    phoneOption = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/div[3]/span/div[3]/button')
    phoneOption.click()
    time.sleep(2)
    print("chose phone option\n")


    # input phone number
    phoneNumberInput = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[2]/div/input')
    time.sleep(2)
    UserNumber = input("Please enter phone number: ")
    phoneNumberInput.send_keys(UserNumber)
    phoneNumberInput.send_keys(Keys.RETURN)
    time.sleep(2)
    print("\n entered phone number")


    # PHONE SECURITY
    phoneSecurity = input("Please enter security phone code: ")
    for x in range(len(phoneSecurity)):
        keyInput = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div[3]/input["+ str(x+1) + "]")
        keyInput.send_keys(phoneSecurity[x])
        print(phoneSecurity[x] + ' was entered')
    keyInput.send_keys(Keys.RETURN)
    print("Phone security code entered")

    # EMAIL SECURITY
    emailSecurity = input("Please enter security email code: ")
    for x in range(len(emailSecurity)):
        keyInput = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div[3]/input["+ str(x+1) + "]")
        keyInput.send_keys(emailSecurity[x])
        print(emailSecurity[x] + ' was entered')
    keyInput.send_keys(Keys.RETURN)
    print("Email security code entered")


    # accept cookies
    cookies = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/button')
    cookies.click()
    time.sleep(2)
    print("Cookies accepted")

    # accept location
    location = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/button[1]')
    location.click()
    time.sleep(2)
    print("Location accepted")


    time.sleep(2)


    # accept enable
    enable = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/button[1]')
    enable.click()
    time.sleep(3)
    print("IDK what i enabled.... notifications?")


    # LIKE BUTTON!!!
    superLikeBOOL = False
    for i in range(0 , howmany , 1):
        likeButton = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div[2]/div[4]/button')
        likeButton.click()
        time.sleep(5)

        if superLikeBOOL == False:
            superLike = driver.find_element_by_xpath('/html/body/div[2]/div/div/button[2]')
            superLike.click()
            superLikeBOOL = True
            time.sleep(5)

    # all done!
    driver.quit()


except Exception as e:
    print(e)
    driver.quit()