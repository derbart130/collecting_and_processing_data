import json
import datetime
import scrapy
from ..items import InstagramTagItem, InstagramPostItem
from .loaders import InstagramTagLoader, InstagramPostLoader


class InstagramParsingSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["www.instagram.com", "i.instagram.com"]
    start_urls = ["https://www.instagram.com/accounts/login/"]
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    _tags_path = "/explore/tags/"
    query_hash = 'ed2e3ff5ae8b96717476b62ef06ed8cc'
    api_url = '/graphql/query/'
    header_var = {'first': 10}

    def __init__(self, login, password, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self._login_url,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password},
                headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
            )
        except AttributeError:
            data = response.json()
            if data["authenticated"]:
                for tag in self.tags:
                    yield response.follow(f"{self._tags_path}{tag}/", callback=self.tag_page_parse)
            else:
                print("Authorization required")

    def tag_page_parse(self, response):
        js_data = self.js_data_extract(response)
        hashtag = js_data['entry_data']['TagPage'][0]['graphql']['hashtag']
        tag_item = InstagramTagItem()
        tag_loader = InstagramTagLoader(tag_item)
        tag_loader.add_value('date_parse', datetime.datetime.now())
        tag_loader.add_value('data', hashtag)
        yield tag_loader.load_item()

        for edge in hashtag['edge_hashtag_to_media']['edges']:
            yield from self.post_parse(edge)

        self.header_var.update({
            'tag_name': hashtag['name'],
            'after': hashtag["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        })

        yield response.follow(
            f"{self.api_url}?query_hash={self.query_hash}&variables={json.dumps(self.header_var)}",
            callback=self.pagination_parse)

    def pagination_parse(self, response):
        data = response.json()

        for edge in data['data']['hashtag']['edge_hashtag_to_media']['edges']:
            yield from self.post_parse(edge)

        self.header_var.update({
            'tag_name': data['data']['hashtag']['name'],
            'after': data['data']['hashtag']["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        })

        yield response.follow(
            f"{self.api_url}?query_hash={self.query_hash}&variables={json.dumps(self.header_var)}",
            callback=self.pagination_parse)

    def post_parse(self, data):
        post_item = InstagramPostItem()
        post_loader = InstagramPostLoader(post_item)
        post_loader.add_value('date_parse', datetime.datetime.now())
        post_loader.add_value('data', data)
        yield post_loader.load_item()

    def js_data_extract(self, response):
        script = response.xpath(
            "//script[contains(text(), 'window._sharedData =')]/text()"
        ).extract_first()
        return json.loads(script.replace("window._sharedData = ", "")[:-1])