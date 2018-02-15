# -*- coding: utf-8 -*-
import scrapy
import re
from watchbot.items import WatchPicture


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


    def parse_image_url(self, image):
        href = image.xpath('@src').extract()[0]
        if '.gif' in href:
            exit()
        elif 'http' in href:
            return href
        else:
            return "http://cda.chronomania.net/{}".format(href)

    def parse_watch(self, response):
        # grab the URL of the cover image
        banned_words = ['bracelet', 'boucle', 'boite', 'catalogue', 'nato', 'lot', 'livre', 'insert', 'écrin', 'lunette']
        title = response.xpath("//h2[@class='postingheadline']/text()").extract()[0].lower()
        date = response.xpath("//p[@class='author']/text()").extract()[1].split(',')[-2]
        if '[vends]' in title and not any(banned_word in title for banned_word in banned_words):
            text = " ".join(" ".join(response.xpath("//p[@class='posting']/text()").extract()).split())
            if text:
                price = re.search('(\d*)€', title).group(1)
                brand = re.search('MARQUE :(.*?)MODELE', text).group(1).lower()
                model = re.search('MODELE :(.*?)ANNEE', text).group(1).lower()
                year = re.search('ANNEE :(.*?)Etat', text).group(1).lower()
                condition = re.search('général : (\w+)', text).group(1).lower()
                images = response.xpath("//p[@class='posting']/img")
                image_urls = [self.parse_image_url(image) for image in images]
                for image in image_urls:
                    image_name = image.split('/')[-1]
                    yield WatchPicture(title=title, image_name=image_name, raw_text=text, image_urls=[image], brand=brand, model=model, year=year, condition=condition, price=price, date=date)

