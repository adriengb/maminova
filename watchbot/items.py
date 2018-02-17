import scrapy

class WatchPicture(scrapy.Item):
    image_name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    ref = scrapy.Field()
    movement = scrapy.Field()
    case_material = scrapy.Field()
    bracelet_material = scrapy.Field()
    gender = scrapy.Field()
    location = scrapy.Field()
    raw_text = scrapy.Field()
    image_urls = scrapy.Field()
    year = scrapy.Field()
    condition = scrapy.Field()
    price = scrapy.Field()