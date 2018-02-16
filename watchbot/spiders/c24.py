import scrapy
from watchbot.items import WatchPicture


class C24pider(scrapy.Spider):
    name = "c24"
    start_urls = ['https://www.chrono24.fr/rolex/index.htm']
    #counter = 1

    def parse(self, response):
        # loop over all watches link elements that link off  and yield a request to grab the watch
        # data and images
        for div in response.xpath("//div[@class='article-item-container']"):
            yield scrapy.Request("https://www.chrono24.fr/{}".format(div.xpath("./a/@href").extract()[0]), self.parse_watch)
        #counter += 1
        #next = ['https://www.chrono24.fr/rolex/index-{}.htm'.format(counter)]
        #yield scrapy.Request(next, self.parse)

    def parse_watch(self, response):
        # grab the URL of the cover image
        #title = response.xpath("//h1[@class='h3 m-t-0']/text()").extract()[0].lower()
        #price = response.xpath("//tr[td[1]/strong/text()='Prix']/td[2]/text()").extract()
        print('PRICE')
        #print(price)
        yield WatchPicture(title=title, price=price)

