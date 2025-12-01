import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ArxivCrawlerItem
import json

class MyCrawlSpider(CrawlSpider):
    name = "arx"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org"]

    rules = (
        Rule(LinkExtractor(allow='list/|/pastweek?skip=0&show=25'), follow=True),
        Rule(LinkExtractor(allow='abs'), callback='parse_item'),
    )

    def __init__(self, *a, **kw):
        super(MyCrawlSpider,self).__init__(*a, **kw)
        self.item_count = 0
        self.max_item_per_link = 25
        self.max_item_total = 2000
        self.output_file = 'papers.json'
        self.items_per_link = 0


    def parse_item(self, response):
        if self.item_count >= self.max_item_total:
            self.crawler.engine.close_spider(self, 'Reached maximum total items')
            return
        if self.items_per_link >= self.max_item_per_link:
            self.items_per_link = 0  # Reset counter for a new link
            return

        items = ArxivCrawlerItem()

        # Extract data from the response object
        title = response.css(".title::text").get()
        abstract = response.css(".abstract::text")[1].get().strip()
        authors = response.css(".authors a::text").extract()
        date = response.css(".dateline::text").get().strip()

        authors_str=', '.join(authors)
        date = date.strip('[]')
        date = date.replace("Submitted on" , "")

        items['title'] = title
        items['abstract'] = abstract
        items['authors'] = authors_str
        items['date'] = date

        self.item_count += 1

        

        yield items


