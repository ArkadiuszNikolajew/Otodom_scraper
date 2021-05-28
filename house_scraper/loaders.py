from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class OtodomLoader(ItemLoader):

    default_output_processor = TakeFirst()