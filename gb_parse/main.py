from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders import HHspyder

if __name__ == '__main__':
    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(HHspyder)
    crawl_proc.start()