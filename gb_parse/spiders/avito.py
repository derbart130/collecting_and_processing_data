import scrapy
from gb_parse.loaders import AvitoLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry/prodam']

    _xpath_selectors = {
        "pagination": "//div[contains(@class, 'pagination-hidden')]//a[@class='pagination-page']/@href",
        "flat_url": "//div[contains(@class, 'iva-item-content')]//a[@itemprop='url']/@href",
    }

    _xpath_data_selectors = {
        "title": "//h1[@class='title-info-title']/span[@class='item-address__string']/text()",
        "price": "//div[@itemprop='offers']//span[@itemprop='price']/text()",
        "seller_url": "//div[@data-marker='seller-info/name']/a/@href",
        "address": "//div[@itemprop='address']/span/text()",
        "parameters": "//div[@class='item-params']//li//text()"
    }

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, self._xpath_selectors["pagination"], self.parse
        )
        yield from self._get_follow(
            response, self._xpath_selectors["flat_url"], self.flat_parse
        )

    def flat_parse(self, response):
        flat_loader = AvitoLoader(response=response)
        flat_loader.add_value("url", response.url)
        for key, xpath in self._xpath_data_selectors.items():
            flat_loader.add_xpath(key, xpath)
        yield flat_loader.load_item()
