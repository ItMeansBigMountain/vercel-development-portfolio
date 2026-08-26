from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time


'''
PROCEDURE
 - log into insta
 - enter hashtag you want to spam like
 - run bot!
'''


class InstagramBot:
	def __init__(self, username, password):
		options = Options()
		options.headless = False
		self.username = username
		self.password = password
		self.driver = webdriver.Firefox(options = options)
	
	def  closeBrowser(self):
		self.driver.close()

	def login(self):
		driver = self.driver
		driver.get("https://www.instagram.com/")
		time.sleep(3)

		# login_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[2]/p/a')
		# login_button.click()
		
		time.sleep(2)
		username_elm = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
		username_elm.clear()
		username_elm.send_keys(self.username)

		password_elm = driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
		password_elm.clear()
		password_elm.send_keys(self.password)
		
		password_elm.send_keys(Keys.RETURN)

		print('\nlogin complete\n')
		time.sleep(2)
	
	def like_photo(self, hashtag, scroll):
		driver = self.driver
		driver.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
		time.sleep(2)

		for i in range(0,int(scroll)):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(3)

		hrefs = driver.find_elements_by_tag_name('a')
		pic_hrefs= []
		for x in hrefs:
			if '/p/' in x.get_attribute('href'):
				pic_link = x.get_attribute('href')
				pic_hrefs.append(pic_link)

		for i in pic_hrefs:
			time.sleep(5)
			print(i)
			driver.get(str(i))
			like = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/section[1]/span[1]/button')
			like.click()
			print('** Like Button clicked **\n')
			# time.sleep(5)


# oyamaIG = InstagramBot('affan.fareed@gmail.com' , 'bug13ink')
# oyamaIG.login()
# oyamaIG.like_photo('martialarts' , 20)
# oyamaIG.closeBrowser()


email = input('\nEnter Your Account Email Here: \n')
email_password = input('\nEnter Your Account Password Here: \n')
search_hashtag = input('\nEnter A HashTag: \n')
Scrolling = input('\nEnter How Many Times You Want To Scroll (HIGHER MEANS MORE PICTURES AS AVAILABLE\n): ')


oyamaIG = InstagramBot(email , email_password)
oyamaIG.login()
oyamaIG.like_photo(search_hashtag , Scrolling)
oyamaIG.closeBrowser()

# YOU CAN LIKE ABOUT 45-50 PICTURES BEFORE INSTAGRAM DESTECTS BOTTING



