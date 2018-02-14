# -*- coding: utf-8 -*-
import scrapy
import re
from watchbot.items import Watch


class CDASpider(scrapy.Spider):
    name = "cda"
    start_urls = ['http://cda.chronomania.net/']

    def parse(self, response):
        # loop over all watches link elements that link off  and yield a request to grab the watch
        # data and images
        for href in response.xpath("//ul[@class='thread']"):
            yield scrapy.Request("http://cda.chronomania.net/{}".format(href.xpath("./li/a/@href").extract()[0]), self.parse_watch)
        next = "http://cda.chronomania.net/{}".format(response.xpath("//div[@class='right']/a[img/@title = 'Page suivante']/@href").extract()[0])
        yield scrapy.Request(next, self.parse)

    def parse_watch(self, response):
        # grab the URL of the cover image
        title = response.xpath("//h2[@class='postingheadline']/text()").extract()[0]
        if '[VENDS]' in title:
            text = " ".join(" ".join(response.xpath("//p[@class='posting']/text()").extract()).split())
            if text:
                brand = re.search('MARQUE :(.*?)MODELE', text).group(1)
                model = re.search('MODELE :(.*?)ANNEE', text).group(1)
                images = response.xpath("//p[@class='posting']/img")
                image_urls = ["http://cda.chronomania.net/{}".format(image.xpath('@src').extract()[0]) for image in images]
                yield Watch(title=title, raw_text=text, image_urls=image_urls, brand=brand, model=model)

