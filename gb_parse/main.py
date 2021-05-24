import os

import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram.spiders.instagram_parsing import InstagramParsingSpider

if __name__ == "__main__":
    dotenv.load_dotenv('.env')
    crawler_settings = Settings()
    crawler_settings.setmodule('instagram.settings')
    crawler_process = CrawlerProcess(settings=crawler_settings)
    tags = ["data"]
    crawler_process.crawl(
        InstagramParsingSpider,
        login=os.getenv("INSTA_LOGIN"),
        password=os.getenv("INSTA_PASSWD"),
        tags=tags,
    )
    crawler_process.start()