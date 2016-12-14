import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains

#opens up a mechanized browser to the listed page
driver = webdriver.Firefox()
actions = ActionChains(driver)
driver.get('http://travel.usnews.com/New_York_NY/Things_To_Do/')

pghtml = driver.page_source

#creates a Beautiful Soup scraper
soup = BeautifulSoup(pghtml, "html.parser")

block_class = soup.find_all(class_ = 'attraction-name')

#appends the attractions to a list
attractions = []
for x in block_class:
	attraction = x.string
	attractions.append(attraction)

print(attractions)

driver.get('http://www.mapcoordinates.net/en')

coordinates = []

#iterates over the attractions to get their latitudes and longitudes
for attraction in attractions:

	time.sleep(3)
	inp = driver.find_element_by_id('pac-input')
	inp.clear()
	time.sleep(3)

	inp.send_keys(attraction)

	time.sleep(3)

	print('sending arrow')

	time.sleep(1)

	actions.send_keys(Keys.ARROW_DOWN).perform()

	time.sleep(3)

	print('sending enter')
	time.sleep(1)

	actions.send_keys(Keys.ENTER).perform()

	lat = driver.find_element_by_class_name('inputLat').get_attribute('value')
	lon = driver.find_element_by_class_name('inputLng').get_attribute('value')

	print(lat)
	print(lon)

	coordinates.append((attraction,lat,lon))

#write the data to a CSV
with open('attractions_data.csv','w') as outfile:
		for exchange in coordinates:
			out = (exchange[0]).encode('utf-8')+','+(exchange[1]).encode('utf-8')+','+(exchange[2]).encode('utf-8')
			outfile.write(out)
			outfile.write("\n")
		outfile.close()
