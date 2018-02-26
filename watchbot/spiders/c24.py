import scrapy
from watchbot.items import WatchPicture

class C24pider(scrapy.Spider):
    name = "c24"
    brands = ['rolex', 'omega', 'jaeger', 'iwc', 'patek', 'panerai', 'seiko', 'cartier', 'hublot', 'breitling', 'zenith', 'tagheuer', 'tudor',
              'audemarspiguet', 'breguet', 'blancpain', 'chanel', 'alangesoehne']
    start_urls = ['https://www.chrono24.com/patekphilippe/index-1.htm?sortorder=5']
    count = 1

    def parse(self, response):
        # loop over all watches link elements that link off  and yield a request to grab the watch
        # data and images
        if len(response.xpath("//div[@class='article-list block']/div[@class='article-item-container']").extract())>0:
            for div in response.xpath("//div[@class='article-list block']/div[@class='article-item-container']"):
                yield scrapy.Request("https://www.chrono24.com/{}".format(div.xpath("./a/@href").extract()[0]), self.parse_watch)
            self.count += 1
            next = 'https://www.chrono24.com/patekphilippe/index-{}.htm?sortorder=5'.format(self.count)
            yield scrapy.Request(next, self.parse)

    def parse_watch(self, response):
        # grab the URL of the cover image
        title = response.xpath("//h1[@class='h3 m-t-0']/text()").extract()[0].lower().strip()
        brand = response.xpath("//tr[td[1]/strong/text()='Brand']/td[2]/a/@title").extract()[0].lower().strip()
        try:
            price = ''.join(response.xpath("//tr[td[1]/strong/text()='Price']/td[2]/text()").extract()).lower().strip()
        except:
            price = ''
        try:
            model = response.xpath("//tr[td[1]/strong/text()='Model']/td[2]/a/text()").extract()[0].lower().strip()
        except:
            model = ''
        try:
            ref = response.xpath("//tr[td[1]/strong/text()='Ref. No.']/td[2]/a/text()").extract()[0].lower().strip()
        except:
            ref = ''
        try:
            condition = response.xpath("//tr[td[1]/strong/text()='Condition']/td[2]/text()").extract()[0].lower().strip()
        except:
            condition = ''
        try:
            location = response.xpath("//tr[td[1]/strong/text()='Location']/td[2]/text()").extract()[0].lower().strip()
        except:
            location = ''
        try:
            year = response.xpath("//tr[td[1]/strong/text()='Year']/td[2]/text()").extract()[0].lower().strip()
        except:
            year = ''
        images = response.xpath("//div[@class='detail-images']//div/@data-original").extract()
        image_urls = [im.split('?')[0] for im in images]
        for image_url in image_urls:
            image_name = image_url.split('/')[-1]
            yield WatchPicture(title=title, price=price, brand=brand, model=model,
                               ref=ref, condition=condition, location=location,
                               image_name=image_name, image_urls=[image_url], year=year)

