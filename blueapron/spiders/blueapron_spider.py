from scrapy import Spider
from scrapy import Request
from blueapron.items import BlueapronItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BlueapronSpider(Spider):
	name = 'blueapron_spider'
	allowed_urls = ['https://www.blueapron.com']
	start_urls = ['https://www.blueapron.com/cookbook']

	def __init__(self):
		self.driver = webdriver.Chrome(r"C:\Users\amd-pc\Desktop\chromedriver.exe")

	def parse(self, response):
		self.driver.get("https://www.blueapron.com/cookbook")
		height = self.driver.execute_script("return document.body.scrollHeight")
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(1)
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == height:
			    break
			height = new_height
		
		# i = 1
		# while i < 2:
		# 	self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		# 	i = i + 1
		# 	time.sleep(1)

		urls = self.driver.find_elements_by_xpath('.//div[@class="recipe-thumb col-md-4"]/a')
		lst = []
		for url in urls:
			lst.append(url.get_attribute('href'))
		print(lst)
		print(len(lst))

		self.driver.close()
		
		for page in lst:
			yield Request(url = page, callback = self.parse_recipe_page)


	def parse_recipe_page(self, response):
		recipe_name = response.xpath('.//span[@itemtype="http://schema.org/Recipe"]/meta[@itemprop="name"]/@content').extract_first()
		recipe_date = response.xpath('.//span[@itemtype="http://schema.org/Recipe"]/meta[@itemprop="datePublished"]/@content').extract_first()
		rating = response.xpath('//span[@itemprop="aggregateRating"]/meta[@itemprop="ratingValue"]/@content').extract_first()
		num_ratings = response.xpath('//span[@itemprop="aggregateRating"]/meta[@itemprop="ratingCount"]/@content').extract_first()
		cuisine = response.xpath('.//span[@itemtype="http://schema.org/Recipe"]/meta[@itemprop="recipeCuisine"]/@content').extract_first()
		prep_time = response.xpath('.//span[@class="total-time"]/text()').extract_first()
		ingredients = list(filter(None, [i.replace("\n", "") for i in response.xpath('.//div[@class="non-story"]/text()').extract()]))
		vegetarian = 'Yes' if response.xpath('.//span[@class="ba-recipe__vegetarian"]/text()').extract_first() == "\n" else 'No'
		
		item = BlueapronItem()

		item['recipe_name'] = recipe_name
		item['recipe_date'] = recipe_date
		item['rating'] = rating
		item['num_ratings'] = num_ratings
		item['cuisine'] = cuisine
		item['prep_time'] = prep_time
		item['ingredients'] = ingredients
		item['vegetarian'] = vegetarian

		yield item


