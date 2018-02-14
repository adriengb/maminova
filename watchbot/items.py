import scrapy

class Watch(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    raw_text = scrapy.Field()
    image_urls = scrapy.Field()
