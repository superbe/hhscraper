from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hh import settings
from hh.spiders.hhspiser import HhSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider)
    process.start()
