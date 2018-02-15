# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline

class MyPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super(MyPipeline, self).__init__(store_uri, settings=settings,
                                             download_func=download_func)
        self.file = open("data/raw_labels.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        return image_guid



    def close_spider(self, spider):
        super(ImagesPipeline, self).close_spider(spider)
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        super(ImagesPipeline, self).process_item(item, spider)
        self.exporter.export_item(item)
        return item
