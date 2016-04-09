import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import TextResponse
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import urljoin
from selenium import webdriver
import time


class Product(scrapy.Item):
    title = scrapy.Field()
    review = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    

class FooSpider(CrawlSpider):
    name = 'foo'

    start_urls = ["https://play.google.com/store/apps/details?id=com.gaana&hl=en"]

    def __init__(self, *args, **kwargs):
        super(FooSpider, self).__init__(*args, **kwargs)
        self.download_delay = 0.25
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(60) # 

    def parse(self,response):
        self.browser.get(response.url)
        self.browser.implicitly_wait(30)
        for i in range(0, 200):
            items = []
            time.sleep(10)
            button = self.browser.find_element_by_xpath("/html \
                                        /body/div[5]/div[6] \
                                        /div/div/div[1]/div[2] \
                                      /div[2]/div[1]/div[4]/button[2]")

            button.click()
            
            sel = Selector(text=self.browser.page_source)
            
            item = Product()
            
            for z in range(1, 5):

                    item['title'] = sel.xpath('//div[contains(@class, "review-body with-review-wrapper")]/span/text()').extract()[z]
                    item['name'] = sel.xpath('//span[contains(@class, "author-name")]/a/text()').extract()[z]
                    item['review'] = sel.xpath('//div[contains(@class, "review-body with-review-wrapper")]/text()').extract()[z]
                    item['date'] = sel.xpath('//span[contains(@class, "review-date")]/text()').extract()[z]
                    yield item
              
            
