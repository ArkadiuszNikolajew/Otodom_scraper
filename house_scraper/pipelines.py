# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter


class DuplicatesPipeline:

    def __init__(self):
        self.seen = set()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        check_data = (adapter.get('id'), adapter.get('last_modified'))
        if check_data not in self.seen:
            self.seen.add(check_data)
            return item
