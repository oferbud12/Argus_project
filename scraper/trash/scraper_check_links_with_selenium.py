#scraper.py

"""
This script use selenium package in order to get information from github.
It searchs on github search field the world 'selenium' and check the validation
of the result's links. After that, it uses get request in order to retrive information
about each result. in the end, it will connect to github_scrape database and insert every
result as new line in selenium table. The scripts movve between 5 first pages of the search result.
"""

import time
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mysql.connector


# Chrome settings
option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument("--window-size=1920,1080");
option.add_argument("--disable-gpu");
option.add_argument("--disable-extensions");
option.add_argument("--proxy-server='direct://'");
option.add_argument("--proxy-bypass-list=*");
option.add_argument("--start-maximized");
option.add_argument("--headless")
option.add_argument('--no-sandbox')

driver = webdriver.Chrome(chrome_options=option)
#driver = webdriver.Chrome(executable_path=r'/Scraper/chromedriver', chrome_options=option)
driver.get('https://www.github.com')

############################### -db- #####################################
with open('host_ip.txt', 'r') as ip_file:      
	host = ip_file.read()
user = 'root'
passwd = '123'
database = 'github_scrape'
print('\n\n\n\n\n\n\n\n\n\nconnecting to github_scrape database')
db_connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database, charset='utf8mb4', use_unicode=True)
cursor = db_connection.cursor()
###########################################################################	

XPATHS = {
			'title': "//a[@class='v-align-middle']",
			'description': "//p[@class='col-12 col-md-9 d-inline-block text-gray mb-2 pr-4']",
			'tags': "//div[@class='topics-row-container col-12 col-md-9 d-inline-flex flex-wrap flex-items-center f6 my-1']",
			'time': "//p[@class='f6 text-gray mr-3 mb-0 mt-2']/relative-time",
			'language': "//div[@class='text-gray flex-auto min-width-0']",
			'rate': "//a[@class='muted-link']",
			'next_page': "//a[@class='next_page']"
}



def check_new_page_loaded(old_html):
	"""
		@Get- html body of old page
		@Description- Checks if html page has changed
		@Return- True if the page html body has changed, else returns False
	"""
	new_html = driver.find_element_by_tag_name('html').text
	if old_html == new_html:
		return False
	return True
	
	
def wait_for(old_html, timeout=60):
	"""
		@Get- html body of old page
		@Description- confirms that the page has changed using heck_new_page_loaded function
			if the page did not changed, waits 0.1 sec and try again.
		@Return- page load time
	"""
	start_time = time.time() 
	while time.time() < start_time + timeout: 
		if check_new_page_loaded(old_html): 
			return time.time() - start_time 
		else: 
			time.sleep(0.1) 
	raise Exception('WebPage Load Timeout')

	
def search(query):
	"""
		@Get- string to search in github
		@Description- confirms that the searched page has loaded using wait_for function
		@Return- page load time
	"""
	print('-> 	Seraching -> {}'.format(query))
	old_html = driver.find_element_by_tag_name('html').text
	s = driver.find_element_by_name('q')
	s.send_keys(query)
	s.send_keys(Keys.ENTER) 
	return wait_for(old_html)
	
	
def next_page():
	"""
		@Description- clicks on next-Page button and confirms that the next page has loaded using wait_for function
		@Return- page load time
	"""
	print('-> \nClicking next page')
	old_html = driver.find_element_by_tag_name('html').text
	link = driver.find_element_by_xpath(XPATHS['next_page']) 
	link.click()
	return wait_for(old_html)

	
def new_page(page_link):
	"""
		@Get- link of page to load
		@Description- confirms that the page has loaded using wait_for function
		@Return- page load time
	"""
	old_param = old_param = driver.find_element_by_tag_name('html').text
	driver.get(page_link)
	return wait_for(old_param)

	
def check_link_is_valid(page_link):
	"""
		@Get- link to a github page
		@Description- load the new page using new_page function.
			prints if the link is valid or not by checking the page title.
			
	"""
	new_page(page_link)
	if driver.title == 'Page not found · GitHub':
		print('-> 	{} is not valid'.format(page_link))
	else:
		print('-> 	{} is valid'.format(page_link))

		
def get_page_links(): 
	"""
		@Return- list of all the result links 
	"""  
	title = driver.find_elements_by_xpath(XPATHS['title'])
	links = [link.get_attribute('href') for link in title]
	return links
	
	
def check_page_links():
	"""
		@Description- check validation of all result links in the current page
	"""
	print("\nChecking page's link")
	return [check_link_is_valid(link) for link in get_page_links()]

	
def check_description(descriptions, titles):
	"""
		@Get descriptions list and titles list
		@ Because not every result have a description, there ia a need to check the list and insert None where there is not description
		@Return- new description list
	"""
	parent = driver.find_elements_by_xpath("//div[@class='col-12 col-md-8 pr-md-3']")
	for i in range(len(titles)):
		val = parent[i].text.split('\n')[1]
		if not val == descriptions[i]:
			descriptions.insert(i,None)
	return descriptions
	
	
def change_tags_format(page_tags):
	"""
		@Get- result's tags list
		@Return- new tag list that instead of \n between every tag has ,
	"""
	return [tags.replace('\n', ', ') if not tags == None else None for tags in page_tags]
		
		
def check_tags(data):
	"""
		@Description- 	Some of the search results do not have tags, thus, they do not have specific div.
						in order to avoid off-by in the tag's data list, this function looks for
						results that have only one div, meta div, and do not have tag div.
		@Gets- tag elements data list
		@Return- sorted list of tags with None where search result do not have tags	
		
	"""	 
	#parent div contains tag div and meta_class div	
	parent = driver.find_elements_by_xpath("//div[@class='col-12 col-md-8 pr-md-3']/div") 
	tag_class = 'topics-row-container col-12 col-md-9 d-inline-flex flex-wrap flex-items-center f6 my-1'
	meta_class = 'd-flex flex-wrap'
	have_tag = []
	#if the first search result do not have tags
	if parent[0].get_attribute('class') == meta_class:			
		have_tag.append(False)
	for i in range(1,len(parent)):
		div_class = parent[i].get_attribute('class')
		if div_class == meta_class:
			if parent[i-1].get_attribute('class') == meta_class:
				have_tag.append(False)
			else:
				have_tag.append(True)
	new_tags_data = data			
	for i in range(len(have_tag)):
		if not have_tag[i]:
			new_tags_data.insert(i,None)
	return change_tags_format(new_tags_data)	
	
	
def get_element_by_attribure(attribute):
	"""
		@Get page attribute- one of ['title', 'description', 'tags', 'time', 'language', 'rate']
		@Return list of the attribute's data
	"""
	return driver.find_elements_by_xpath(XPATHS[attribute])
	
	
def get_attributes_data(attributes_to_scrape):
	"""
		@Get page arttibutes list ['title', 'description', 'tags', 'time', 'language', 'rate']
		@Return
	"""
	attributes_data = []
	for attribute in attributes_to_scrape:
		data = get_element_by_attribure(attribute)
		#time attribute's handling is different than the rest
		if attribute == 'time': 								
			data = [x.get_attribute('title') for x in data]
		else:
			data = [x.text for x in data]
			#tags attribute's handling is different than the rest
			if attribute == 'tags':								
				data = check_tags(data)
			#description attribute's handling is different than the rest
			elif attribute == 'description':
				data = check_description(data, attributes_data[0])
		attributes_data.append(data)
	return attributes_data	

	
def insert_page_to_db(page_data):
	"""
		@Get- list of all page's relevant data
		@Description- insert the data into MYSQL database- github_scrape to selenium table
	"""
	print('-> Insert page data to database')
	for i in range(len(page_data[0])):
		sql = """INSERT INTO selenium (title, description, tags, time, language, rate)
				VALUES (%s, %s, %s, %s, %s, %s)"""
		# values = (title[i], description[i], tags[i], time[i], language[i], rate[i])
		values = (page_data[0][i], page_data[1][i], page_data[2][i], page_data[3][i], page_data[4][i], page_data[5][i])
		cursor.execute(sql, values)
	db_connection.commit()


def main():	
	print('Start scraping github:')
	print('-> 		Search query took- {}Sec'.format(search('selenium')))
	#first five pages
	for i in range(5):				
		if not i == 0:
			#Clicking next page
			load_time = next_page()
			print('-> 	Page {} load took {}Sec'.format(i+1, load_time)) 
		#arttibutes to look for
		attributes_to_scrape = ['title', 'description', 'tags', 'time', 'language', 'rate']		
		page_attributes_data = get_attributes_data(attributes_to_scrape)
		insert_page_to_db(page_attributes_data)
		current_page = driver.current_url
		check_page_links()
		# check_page_links function changes the driver page	
		new_page(current_page) 											
	db_connection.close()
	print('---Finished scraping github---')
	
	
if __name__ == '__main__':
	main()

	
	