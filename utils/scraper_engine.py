# scraper_engine.py
import scrapy
from scrapy.crawler import CrawlerProcess
import random
import logging

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

class TestSiteSpider(scrapy.Spider):
    name = "testsite"
    allowed_domains = ["sandbox.oxylabs.io"]
    start_urls = ['https://sandbox.oxylabs.io/products']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers={"User-Agent": random.choice(USER_AGENTS)},
                callback=self.parse
            )

    def parse(self, response):
        try:
            for product in response.css("div.product-card"):
                yield {
                    "name": product.css("h4::text").get(),
                    "price": product.css("span.price::text").get(),
                    "image": product.css("img::attr(src)").get()
                }
        except Exception as e:
            self.logger.error(f"Error parsing page: {e}")

def run():
    # Your implementation here
    pass