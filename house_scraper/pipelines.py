# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import logging

from itemadapter import ItemAdapter


class HomescrapingPipeline:

    collection_name = 'scrapped'

    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb+srv://aniko:itcqLVRHjOgxL76KN5U1v3eO@cluster0.ybchr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client['homescrap']

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):

        def offer_exist():
            offer = self.db[self.collection_name].find_one({'offer_id': item['offer_id']})
            last_modified = self.db[self.collection_name].find_one({'last_modified': item['last_modified']})
            if not offer:
                self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
            elif offer == last_modified:
                pass
            else:
                offer = self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        offer_exist()
        return item
