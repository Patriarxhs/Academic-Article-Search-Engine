# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArxivCrawlerItem(scrapy.Item):
    title = scrapy.Field(); 
    abstract = scrapy.Field(); 
    authors = scrapy.Field(); 
    date = scrapy.Field(); 
    pass
