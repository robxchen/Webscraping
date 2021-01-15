# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BlueapronItem(scrapy.Item):

	recipe_name = scrapy.Field()
	recipe_date = scrapy.Field()
	rating = scrapy.Field()
	num_ratings = scrapy.Field()
	cuisine = scrapy.Field()
	prep_time = scrapy.Field()
	ingredients = scrapy.Field()
	vegetarian = scrapy.Field()

