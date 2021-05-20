from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Compose
from urllib.parse import urljoin


def get_url(itm):
    return urljoin("https://www.avito.ru", itm)


def get_price(itm):
    itm = itm.replace(" ", "")
    return int(itm)


def get_address(itm):
    itm = itm.replace("\n ", "")
    return itm


def get_parameters(parameters):
    params = [itm.replace(":", "") for itm in parameters if (itm != " ") and (itm != "\n  ")]
    params = [itm[:-1] if itm[-1] == " " else itm for itm in params]
    params_dict = dict(zip(params[::2], params[1::2]))
    return params_dict


def get_seller(itm):
    seller = "https://www.avito.ru" + itm
    return seller


class AvitoLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(get_price)
    price_out = TakeFirst()
    address_in = MapCompose(get_address)
    address_out = TakeFirst()
    parameters_out = Compose(get_parameters)
    author_in = MapCompose(get_seller)
    author_out = TakeFirst()