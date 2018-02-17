import scrapy
import re
from watchbot.items import WatchPicture


class C24pider(scrapy.Spider):
    name = "c24"
    start_urls = ['https://www.chrono24.com/rolex/index.htm']
    #counter = 1

    def parse(self, response):
        # loop over all watches link elements that link off  and yield a request to grab the watch
        # data and images
        for div in response.xpath("//div[@class='article-item-container']"):
            yield scrapy.Request("https://www.chrono24.com/{}".format(div.xpath("./a/@href").extract()[0]), self.parse_watch)
        #counter += 1
        #next = ['https://www.chrono24.fr/rolex/index-{}.htm'.format(counter)]
        #yield scrapy.Request(next, self.parse)

    def parse_watch(self, response):
        # grab the URL of the cover image
        title = response.xpath("//h1[@class='h3 m-t-0']/text()").extract()[0].lower()
        price = re.findall(r'\$(.*)', response.xpath("//tr[td[1]/strong/text()='Price']/td[2]/text()").extract()[0])[0]
        brand = response.xpath("//tr[td[1]/strong/text()='Brand']/td[2]/a/@title").extract()[Ø]
        model = response.xpath("//tr[td[1]/strong/text()='Model']/td[2]/text()").extract()[0]
        ref = response.xpath("//tr[td[1]/strong/text()='Ref.No']/td[2]/text()").extract()[0]
        movement = response.xpath("//tr[td[1]/strong/text()='Movement']/td[2]/text()").extract()[0]
        case_material = response.xpath("//tr[td[1]/strong/text()='Case material']/td[2]/text()").extract()[0]
        bracelet_material = response.xpath("//tr[td[1]/strong/text()='Bracelet material']/td[2]/text()").extract()[0]
        condition = response.xpath("//tr[td[1]/strong/text()='Condition']/td[2]/text()").extract()[0]
        gender = response.xpath("//tr[td[1]/strong/text()='Gender']/td[2]/text()").extract()[0]
        location = response.xpath("//tr[td[1]/strong/text()='Location']/td[2]/text()").extract()[0]
        yield WatchPicture(title=title, price=price, brand=brand, model=model, ref=ref, movement=movement, case_material=case_material,
                           bracelet_material=bracelet_material, condition=condition, gender=gender, location=location)

